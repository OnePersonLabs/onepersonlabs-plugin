"""Deterministic restart boundaries; never close an app or submit an AI prompt."""

import argparse
import contextlib
import importlib.util
import io
import json
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
        fields = dict(thread=None, message=None, codex_home=None, timeout_seconds=1,
                      delay_seconds=10, receipt=None)
        return argparse.Namespace(**(fields | changes))

    def receipt(self, *, not_before=100):
        path = self.root / 'restart.json'
        target = self.state([{'pid': 4, 'started': '10'}])
        target['quit_window'] = {'hwnd': 100, 'pid': 4, 'started': '10'}
        self.helper.write_receipt(path, {
            'state': 'prepared', 'not_before': not_before, 'target': target,
            'request': vars(self.args(codex_home=str(self.root))),
        })
        return path

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
                    self.helper.restart(self.args(), inspect=lambda: state, launch=launch, quit_app=Mock())
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
            result = self.helper.restart(self.args(thread=self.thread), inspect=inspect, launch=launch, quit_app=lambda target: events.append(("quit", True)))
        self.assertEqual(events, [('inspect', True), ('quit', True), ('inspect', False),
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
                                             inspect=lambda: next(states), launch=Mock(), quit_app=Mock())
        queue.assert_called_once_with(cli, self.root.resolve(), self.thread, 'Run required checks')
        self.assertEqual(result['continuation']['state'], 'accepted')

    def test_launch_failure_does_not_queue(self):
        states = iter([self.state([{'pid': 4, 'started': '10'}]), self.state([])])
        with patch.object(self.helper, 'prepare_continuation', return_value=self.exe):
            with patch.object(self.helper, 'queue_once') as queue:
                with self.assertRaises(OSError):
                    self.helper.restart(self.args(), inspect=lambda: next(states),
                                        launch=Mock(side_effect=OSError('launch failed')), quit_app=Mock())
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

    def test_quit_refusal_stops_before_exit_wait_launch_or_queue(self):
        state = self.state([{'pid': 4, 'started': '10'}])
        quit_app = Mock(side_effect=RuntimeError('Windows refused foreground activation'))
        launch = Mock()
        with patch.object(self.helper, 'prepare_continuation', return_value=self.exe):
            with patch.object(self.helper, 'queue_once') as queue:
                with patch.object(self.helper, 'wait_for_exit') as wait:
                    with self.assertRaisesRegex(RuntimeError, 'refused foreground'):
                        self.helper.restart(self.args(thread=self.thread, message='Continue',
                                                      codex_home=str(self.root)),
                                            inspect=lambda: state, launch=launch, quit_app=quit_app)
        quit_app.assert_called_once_with(state)
        wait.assert_not_called()
        launch.assert_not_called()
        queue.assert_not_called()

    def test_uncertain_quit_with_observed_exit_reopens_once(self):
        details = {'state': 'quit_input_uncertain', 'events_sent': 2,
                   'cleanup_expected': 2, 'cleanup_sent': 2}
        quit_app = Mock(side_effect=self.helper.QuitInputError('partial input', details))
        states = iter([self.state([{'pid': 4, 'started': '10'}]), self.state([]),
                       self.state([{'pid': 8, 'started': '20'}])])
        launch, report = Mock(), Mock()
        result = self.helper.restart(self.args(), inspect=lambda: next(states),
                                     quit_app=quit_app, launch=launch, report=report)
        quit_app.assert_called_once()
        launch.assert_called_once()
        self.assertEqual(result['state'], 'new_process_observed')
        self.assertEqual(result['quit_result'], details)
        report.assert_any_call(state='waiting_for_exit', quit_result=details)

    def test_uncertain_quit_without_exit_does_not_launch_or_continue(self):
        state = self.state([{'pid': 4, 'started': '10'}])
        quit_app = Mock(side_effect=self.helper.QuitInputError(
            'partial input', {'state': 'quit_input_uncertain', 'events_sent': 2}))
        launch = Mock()
        with patch.object(self.helper, 'wait_for_exit', side_effect=TimeoutError('Desktop did not exit')):
            with patch.object(self.helper, 'queue_once') as queue:
                with self.assertRaisesRegex(TimeoutError, 'did not exit'):
                    self.helper.restart(self.args(), inspect=lambda: state,
                                        quit_app=quit_app, launch=launch)
        quit_app.assert_called_once()
        launch.assert_not_called()
        queue.assert_not_called()

    def test_selected_home_is_shared_by_ui_launch_and_continuation(self):
        states = iter([self.state([{'pid': 4, 'started': '10'}]), self.state([]),
                       self.state([{'pid': 8, 'started': '20'}])])
        launch = Mock()
        with patch.dict(self.helper.os.environ, {'CODEX_HOME': 'unrelated ambient home'}):
            with patch.object(self.helper, 'prepare_continuation', return_value=self.app / 'resources/codex.exe'):
                with patch.object(self.helper.subprocess, 'run',
                                  return_value=subprocess.CompletedProcess([], 0, 'queued', '')) as queue_process:
                    result = self.helper.restart(self.args(thread=self.thread, message='Run authorized checks',
                                                          codex_home=str(self.root)),
                                                 inspect=lambda: next(states), quit_app=Mock(), launch=launch)
        launch.assert_called_once()
        queue_process.assert_called_once()
        selected_home = str(self.root.resolve())
        self.assertEqual(launch.call_args.kwargs['env']['CODEX_HOME'], selected_home)
        self.assertEqual(queue_process.call_args.kwargs['env']['CODEX_HOME'], selected_home)
        self.assertEqual(queue_process.call_args.args[0][1:],
                         ['queue', '--thread', self.thread, '--message', 'Run authorized checks', '--resume'])
        self.assertEqual(result['continuation']['state'], 'accepted')

    def test_worker_in_parent_job_records_failure_without_quit(self):
        receipt = self.receipt()
        with patch.object(self.helper, 'independent_process', return_value=False):
            with patch.object(self.helper, 'restart') as restart:
                with self.assertRaisesRegex(RuntimeError, 'parent job'):
                    self.helper.worker(receipt)
        restart.assert_not_called()
        record = json.loads(receipt.read_text(encoding='utf8'))
        self.assertEqual(record['state'], 'failed')
        self.assertIn('Desktop was not closed', record['error'])
        self.assertTrue(receipt.with_suffix('.claimed').is_file())

    def test_exclusive_worker_claim_prevents_second_restart(self):
        receipt = self.receipt()
        with patch.object(self.helper, 'independent_process', return_value=True):
            with patch.object(self.helper.time, 'time', return_value=100):
                with patch.object(self.helper, 'restart', return_value={'state': 'new_process_observed'}) as restart:
                    self.helper.worker(receipt)
                    before = receipt.read_bytes()
                    with self.assertRaises(FileExistsError):
                        self.helper.worker(receipt)
        restart.assert_called_once()
        self.assertEqual(receipt.read_bytes(), before)
        self.assertEqual(json.loads(before)['state'], 'finished')

    def test_unknown_continuation_stays_in_receipt_for_reconciliation(self):
        receipt = self.receipt()
        result = {'state': 'new_process_observed',
                  'continuation': {'state': 'unknown', 'error': 'queue timed out', 'retry': False}}
        with patch.object(self.helper, 'independent_process', return_value=True):
            with patch.object(self.helper.time, 'time', return_value=100):
                with patch.object(self.helper, 'restart', return_value=result) as restart:
                    self.helper.worker(receipt)
        restart.assert_called_once()
        record = json.loads(receipt.read_text(encoding='utf8'))
        self.assertEqual(record['result'], result)
        self.assertTrue(receipt.with_suffix('.claimed').is_file())

    def test_expired_delayed_worker_does_not_restart(self):
        receipt = self.receipt(not_before=10)
        with patch.object(self.helper, 'independent_process', return_value=True):
            with patch.object(self.helper.time, 'time', return_value=100):
                with patch.object(self.helper, 'restart') as restart:
                    with patch.object(self.helper.time, 'sleep') as sleep:
                        with self.assertRaisesRegex(RuntimeError, 'launch expired'):
                            self.helper.worker(receipt)
        restart.assert_not_called()
        sleep.assert_not_called()
        self.assertEqual(json.loads(receipt.read_text(encoding='utf8'))['state'], 'failed')

    def test_uncertain_launcher_keeps_each_receipt_and_never_retries(self):
        errors = [subprocess.TimeoutExpired('launcher', 20),
                  subprocess.CalledProcessError(1, 'launcher'),
                  subprocess.CompletedProcess([], 0, '{"ReturnValue":9,"ProcessId":0}', ''),
                  subprocess.CompletedProcess([], 0, 'not a launch receipt', '')]
        directory = self.root / 'onepersonlabs/desktop-restarts'
        for outcome in errors:
            with self.subTest(outcome=outcome):
                existing = set(directory.glob('*.json'))
                run = Mock(side_effect=outcome) if isinstance(outcome, Exception) else Mock(return_value=outcome)
                with patch.object(self.helper, 'inspect_quit_target', return_value={'hwnd': 100, 'pid': 4, 'started': '10'}):
                    with patch.object(self.helper, 'prepare_continuation', return_value=None):
                        with patch.object(self.helper.subprocess, 'run', run):
                            with self.assertRaisesRegex(RuntimeError, 'restart receipt:'):
                                self.helper.arm_restart(self.args(codex_home=str(self.root)),
                                                        inspect=lambda: self.state([{'pid': 4, 'started': '10'}]))
                run.assert_called_once()
                created = set(directory.glob('*.json')) - existing
                self.assertEqual(len(created), 1)
                record = json.loads(created.pop().read_text(encoding='utf8'))
                self.assertEqual(record['state'], 'prepared')
                self.assertEqual(record['target']['quit_window']['pid'], 4)

    def test_missing_helper_readiness_retains_receipt_without_second_launch(self):
        run = Mock(return_value=subprocess.CompletedProcess([], 0, '{"ReturnValue":0,"ProcessId":44}', ''))
        with patch.object(self.helper, 'inspect_quit_target', return_value={'hwnd': 100, 'pid': 4, 'started': '10'}):
            with patch.object(self.helper, 'prepare_continuation', return_value=None):
                with patch.object(self.helper.subprocess, 'run', run):
                    with patch.object(self.helper.time, 'monotonic', side_effect=[0, 0, 6]):
                        with patch.object(self.helper.time, 'sleep'):
                            with self.assertRaisesRegex(RuntimeError, 'readiness is uncertain'):
                                self.helper.arm_restart(self.args(codex_home=str(self.root)),
                                                        inspect=lambda: self.state([{'pid': 4, 'started': '10'}]))
        run.assert_called_once()
        receipts = list((self.root / 'onepersonlabs/desktop-restarts').glob('*.json'))
        self.assertEqual(len(receipts), 1)
        self.assertEqual(json.loads(receipts[0].read_text(encoding='utf8'))['state'], 'prepared')

    def test_prepared_restart_requires_original_main_identity(self):
        saved = self.state([{'pid': 4, 'started': '10'}])
        saved['quit_window'] = {'hwnd': 100, 'pid': 4, 'started': '10'}
        reused = self.state([{'pid': 4, 'started': '11'}])
        quit_app, launch = Mock(), Mock()
        with self.assertRaisesRegex(RuntimeError, 'changed after preparation'):
            self.helper.restart(self.args(), target=saved, inspect=lambda: reused,
                                quit_app=quit_app, launch=launch)
        quit_app.assert_not_called()
        launch.assert_not_called()

    def test_prepared_restart_refreshes_renderer_set_before_quit(self):
        saved = self.state([{'pid': 4, 'started': '10'}, {'pid': 5, 'started': '12'}])
        saved['quit_window'] = {'hwnd': 100, 'pid': 4, 'started': '10'}
        refreshed = self.state([{'pid': 4, 'started': '10'}, {'pid': 6, 'started': '14'}])
        states = iter([refreshed, self.state([]), self.state([{'pid': 8, 'started': '20'}])])
        quit_app, launch = Mock(), Mock()
        result = self.helper.restart(self.args(), target=saved, inspect=lambda: next(states),
                                     quit_app=quit_app, launch=launch)
        quit_app.assert_called_once_with(refreshed)
        launch.assert_called_once()
        self.assertEqual(result['state'], 'new_process_observed')


if __name__ == '__main__':
    unittest.main()
