"""Check native Quit targeting and input failures without sending real input."""

import importlib.util
import ctypes
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPT = (Path(__file__).resolve().parents[3]
          / 'plugins/onepersonlabs/skills/restart-codex-desktop/scripts/windows_ui.py')
SPEC = importlib.util.spec_from_file_location('restart_windows_ui', SCRIPT)
UI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UI)
NATIVE_API = UI._WindowsApi


class FakeApi:
    def __init__(self):
        self.handles = [100]
        self.owner = {100: 7}
        self.path = r'C:\Package\app\ChatGPT.exe'
        self.started = '639000000000000001'
        self.focus = 100
        self.activation_allowed = True
        self.key_checks = iter([[], []])
        self.sent_counts = iter([4])
        self.calls = []
        self.identity_checks = 0
        self.replace_on_check = None

    def windows(self):
        return self.handles

    def window_pid(self, hwnd):
        return self.owner[hwnd]

    def process_identity(self, pid):
        self.identity_checks += 1
        return {'executable': self.path,
                'started': 'reused' if self.identity_checks == self.replace_on_check else self.started}

    def foreground(self):
        return self.focus

    def activate(self, hwnd):
        self.calls.append(('activate', hwnd))
        if self.activation_allowed:
            self.focus = hwnd
        return self.activation_allowed

    def held_keys(self):
        return next(self.key_checks)

    def send(self, keys):
        self.calls.append(('send', list(keys)))
        return next(self.sent_counts)


class QuitInputTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeApi()
        self.target = {'executable': self.api.path,
                       'processes': [{'pid': 7, 'started': self.api.started}]}
        factory = patch.object(UI, '_WindowsApi', return_value=self.api)
        factory.start()
        self.addCleanup(factory.stop)

    def assert_no_input(self):
        self.assertFalse(any(call[0] == 'send' for call in self.api.calls))

    def test_read_only_inspection_prefers_exact_foreground_target(self):
        self.api.handles = [100, 200, 300]
        self.api.owner |= {200: 99, 300: 7}
        self.api.focus = 300
        result = UI.inspect_quit_target(self.target)
        self.assertEqual(result, {'hwnd': 300, 'pid': 7, 'started': self.api.started})
        self.assertEqual(self.api.calls, [])

    def test_request_sends_one_native_chord_and_does_not_claim_exit(self):
        result = UI.request_quit(self.target)
        self.assertEqual(self.api.calls, [('send', [(0x11, False), (0x51, False),
                                                   (0x51, True), (0x11, True)])])
        self.assertEqual(result['events_sent'], 4)
        self.assertEqual(result['pid'], 7)
        self.assertFalse(result['exit_confirmed'])
        self.assertEqual(self.api.identity_checks, 2)

    def test_single_background_window_is_activated_before_input(self):
        self.api.focus = 999
        UI.request_quit(self.target)
        self.assertEqual(self.api.calls[0], ('activate', 100))
        self.assertEqual(self.api.calls[1][0], 'send')

    def test_foreground_refusal_is_actionable_and_sends_nothing(self):
        self.api.focus = 999
        self.api.activation_allowed = False
        with self.assertRaisesRegex(RuntimeError, 'focus Desktop before retrying'):
            UI.request_quit(self.target)
        self.assert_no_input()

    def test_focus_must_match_even_if_activation_reports_success(self):
        self.api.focus = 999
        self.api.activate = lambda _: True
        with self.assertRaisesRegex(RuntimeError, 'lost foreground'):
            UI.request_quit(self.target)
        self.assert_no_input()

    def test_multiple_windows_without_target_focus_are_ambiguous(self):
        self.api.handles.append(300)
        self.api.owner[300] = 7
        self.api.focus = 999
        with self.assertRaisesRegex(RuntimeError, 'Multiple Desktop windows'):
            UI.request_quit(self.target)
        self.assertEqual(self.api.calls, [])

    def test_foreign_executable_and_reused_pid_are_refused(self):
        for path, started in [(r'C:\Other\ChatGPT.exe', self.api.started),
                              (self.api.path, 'reused')]:
            with self.subTest(path=path, started=started):
                self.api.path, self.api.started = path, started
                with self.assertRaisesRegex(RuntimeError, 'identity changed'):
                    UI.request_quit(self.target)
                self.assert_no_input()

    def test_identity_is_checked_again_immediately_before_input(self):
        self.api.replace_on_check = 2
        with self.assertRaisesRegex(RuntimeError, 'identity changed'):
            UI.request_quit(self.target)
        self.assert_no_input()

    def test_held_input_before_or_after_focus_blocks_quit(self):
        for keys in [[[(0x10)], []], [[], [(0x01)]]]:
            with self.subTest(keys=keys):
                self.api.key_checks = iter(keys)
                with self.assertRaisesRegex(RuntimeError, 'held|Keyboard state'):
                    UI.request_quit(self.target)
                self.assert_no_input()

    def test_partial_delivery_releases_only_injected_held_keys_once(self):
        for count, cleanup in [(0, []), (1, [(0x11, True)]),
                               (2, [(0x51, True), (0x11, True)]), (3, [(0x11, True)])]:
            with self.subTest(count=count):
                self.api.calls = []
                self.api.key_checks = iter([[], []])
                self.api.sent_counts = iter([count, len(cleanup)])
                with self.assertRaises(UI.QuitInputError) as raised:
                    UI.request_quit(self.target)
                details = raised.exception.details
                self.assertEqual(details['state'], 'quit_input_uncertain')
                self.assertEqual(details['cleanup_sent'], len(cleanup))
                self.assertEqual(details['events_sent'], count)
                calls = [('send', UI.QUIT_KEYS)] + ([('send', cleanup)] if cleanup else [])
                self.assertEqual(self.api.calls, calls)

    def test_incomplete_key_release_is_reported_without_more_input(self):
        self.api.sent_counts = iter([2, 1])
        with self.assertRaises(UI.QuitInputError) as raised:
            UI.request_quit(self.target)
        self.assertEqual(raised.exception.details['cleanup_expected'], 2)
        self.assertEqual(raised.exception.details['cleanup_sent'], 1)
        self.assertEqual(len(self.api.calls), 2)

    def test_cleanup_error_preserves_uncertain_delivery_metadata(self):
        def send(keys):
            self.api.calls.append(('send', list(keys)))
            if len(self.api.calls) == 1:
                return 2
            raise OSError('input blocked')

        self.api.send = send
        with self.assertRaises(UI.QuitInputError) as raised:
            UI.request_quit(self.target)
        self.assertEqual(raised.exception.details['events_sent'], 2)
        self.assertEqual(raised.exception.details['cleanup_error'], 'input blocked')
        self.assertEqual(len(self.api.calls), 2)

    def test_native_input_uses_windows_abi_and_keyup_flags(self):
        class User32:
            def SendInput(self, count, inputs, size):
                self.observed = (count, size, [(x.type, x.data.ki.wVk, x.data.ki.dwFlags) for x in inputs])
                return count

        native = NATIVE_API.__new__(NATIVE_API)
        native.user = User32()
        self.assertEqual(native.send(UI.QUIT_KEYS), 4)
        expected_size = 40 if ctypes.sizeof(ctypes.c_void_p) == 8 else 28
        self.assertEqual(native.user.observed,
                         (4, expected_size, [(1, 0x11, 0), (1, 0x51, 0),
                                              (1, 0x51, 2), (1, 0x11, 2)]))

    def test_no_visible_target_cannot_send_to_another_application(self):
        self.api.handles = [200]
        self.api.owner[200] = 99
        with self.assertRaisesRegex(RuntimeError, 'No enabled visible Desktop'):
            UI.request_quit(self.target)
        self.assert_no_input()


if __name__ == '__main__':
    unittest.main()
