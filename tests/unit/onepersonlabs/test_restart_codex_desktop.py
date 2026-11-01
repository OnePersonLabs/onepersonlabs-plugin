"""Deterministic restart boundaries; never close an app or submit an AI prompt."""

import argparse
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'plugins/onepersonlabs/skills/restart-codex-desktop/scripts/restart_desktop.py'


class DesktopRestartTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('desktop_restart', SCRIPT)
        self.helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.helper)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'package'
        self.app = self.root / 'app'
        (self.app / 'resources').mkdir(parents=True)
        (self.app / 'resources/app.asar').touch()
        self.exe = self.app / 'ChatGPT.exe'
        self.exe.touch()
        (self.app / 'resources/codex.exe').touch()
        self.manifest('app/ChatGPT.exe')
        self.thread = '123e4567-e89b-12d3-a456-426614174000'
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def manifest(self, executable):
        (self.root / 'AppxManifest.xml').write_text(
            '<Package xmlns="urn:windows"><Applications>'
            f'<Application Id="App" Executable="{executable}"/>'
            '<Application Id="CodexCoreCommandRunner" Executable="app/resources/codex.exe"/>'
            '</Applications></Package>', encoding='utf8')

    def state(self, processes):
        return {'root': str(self.root), 'executable': str(self.exe), 'processes': processes}

    def args(self, **changes):
        fields = dict(thread=None, message=None, codex_home=None, timeout_seconds=1)
        return argparse.Namespace(**(fields | changes))

    def test_manifest_selects_ui_among_multiple_applications(self):
        self.assertEqual(self.helper.desktop_executable(self.root), self.exe.resolve())
        self.manifest('app/resources/codex.exe')
        with self.assertRaisesRegex(ValueError, 'Desktop UI'):
            self.helper.desktop_executable(self.root)

    def test_manifest_rejects_escape_even_when_filename_matches(self):
        (self.root.parent / 'ChatGPT.exe').touch()
        self.addCleanup((self.root.parent / 'ChatGPT.exe').unlink)
        self.manifest('../ChatGPT.exe')
        with self.assertRaisesRegex(ValueError, 'Desktop UI'):
            self.helper.desktop_executable(self.root)

    def test_timeout_prevents_launch_and_continuation(self):
        state = self.state([{'pid': 4, 'started': '10'}])
        # Supply the clock directly: timeout has no dependency on wall time.
        with self.assertRaisesRegex(TimeoutError, 'no launch or continuation'):
            self.helper.wait_for_exit(state, 1, inspect=lambda: state,
                                      clock=Mock(side_effect=[0, 2]), sleep=Mock())
        launch = Mock()
        queue = Mock()
        with patch.object(self.helper, 'wait_for_exit', side_effect=TimeoutError('still running')):
            with patch.object(self.helper, 'queue_once', queue):
                with self.assertRaises(TimeoutError):
                    self.helper.restart(self.args(), inspect=lambda: state, launch=launch)
        launch.assert_not_called()
        queue.assert_not_called()

    def test_new_identity_or_installation_change_stops_wait(self):
        before = self.state([{'pid': 4, 'started': '10'}])
        # PID reuse must not be mistaken for the original app still exiting.
        replacement = self.state([{'pid': 4, 'started': '11'}])
        with self.assertRaisesRegex(RuntimeError, 'new Desktop processes'):
            self.helper.wait_for_exit(before, 1, inspect=lambda: replacement)
        changed = replacement | {'executable': 'another app'}
        with self.assertRaisesRegex(RuntimeError, 'installed Desktop changed'):
            self.helper.wait_for_exit(before, 1, inspect=lambda: changed)

    def test_navigation_only_launches_exact_ui_after_exit(self):
        old = self.state([{'pid': 4, 'started': '10'}])
        empty = self.state([])
        new = self.state([{'pid': 8, 'started': '20'}])
        events = []
        states = iter([old, empty, new])

        def inspect():
            value = next(states)
            events.append(('inspect', bool(value['processes'])))
            return value

        def launch(command, **kwargs):
            events.append(('launch', command))

        with patch.object(self.helper, 'queue_once') as queue:
            result = self.helper.restart(self.args(thread=self.thread), inspect=inspect, launch=launch)
        self.assertEqual(events, [('inspect', True), ('inspect', False),
                                 ('launch', [str(self.exe), f'codex://threads/{self.thread}']),
                                 ('inspect', True)])
        self.assertEqual(result['state'], 'new_process_observed')
        self.assertFalse(result['ui_ready'])
        queue.assert_not_called()

    def test_continuation_is_queued_once_after_new_process_observation(self):
        states = iter([self.state([{'pid': 4, 'started': '10'}]), self.state([]),
                       self.state([{'pid': 8, 'started': '20'}])])
        cli = self.app / 'resources/codex.exe'
        with patch.object(self.helper, 'prepare_continuation', return_value=cli):
            with patch.object(self.helper, 'queue_once', return_value={'state': 'accepted'}) as queue:
                result = self.helper.restart(self.args(thread=self.thread, message='Run required checks',
                                                      codex_home=str(self.root)),
                                             inspect=lambda: next(states), launch=Mock())
        queue.assert_called_once_with(cli, self.root.resolve(), self.thread, 'Run required checks')
        self.assertEqual(result['continuation']['state'], 'accepted')

    def test_launch_failure_does_not_queue(self):
        states = iter([self.state([{'pid': 4, 'started': '10'}]), self.state([])])
        with patch.object(self.helper, 'prepare_continuation', return_value=self.exe):
            with patch.object(self.helper, 'queue_once') as queue:
                with self.assertRaises(OSError):
                    self.helper.restart(self.args(), inspect=lambda: next(states),
                                        launch=Mock(side_effect=OSError('launch failed')))
        queue.assert_not_called()

    def test_missing_new_process_has_bounded_failure(self):
        target = self.state([])
        with self.assertRaisesRegex(TimeoutError, 'no continuation'):
            self.helper.wait_for_start(target, inspect=lambda: target,
                                       clock=Mock(side_effect=[0, 31]), sleep=Mock())

    def test_queue_acceptance_keeps_resume_warning_and_no_confirmation(self):
        completed = subprocess.CompletedProcess([], 0, 'queued', 'warning: resume failed')
        with patch.object(self.helper.subprocess, 'run', return_value=completed) as run:
            result = self.helper.queue_once(self.exe, self.root, self.thread, 'Scoped next action')
        self.assertEqual(result['state'], 'accepted')
        self.assertIn('resume failed', result['stderr'])
        self.assertFalse(result['resume_confirmed'])
        self.assertFalse(result['retry'])
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0][1:],
                         ['queue', '--thread', self.thread, '--message', 'Scoped next action', '--resume'])
        self.assertEqual(run.call_args.kwargs['env']['CODEX_HOME'], str(self.root))

    def test_queue_timeout_is_unknown_and_never_retried(self):
        with patch.object(self.helper.subprocess, 'run', side_effect=subprocess.TimeoutExpired('queue', 30)) as run:
            result = self.helper.queue_once(self.exe, self.root, self.thread, 'Scoped next action')
        self.assertEqual(result['state'], 'unknown')
        self.assertFalse(result['retry'])
        run.assert_called_once()

    def test_continuation_preflight_rejects_missing_scope_and_unsupported_cli(self):
        with self.assertRaisesRegex(ValueError, '--thread and --codex-home'):
            self.helper.prepare_continuation(self.state([]), self.args(message='Continue'))
        with patch.object(self.helper.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'old help', '')):
            with self.assertRaisesRegex(RuntimeError, 'does not support'):
                self.helper.prepare_continuation(self.state([]), self.args(
                    message='Continue', thread=self.thread, codex_home=str(self.root)))


if __name__ == '__main__':
    unittest.main()
