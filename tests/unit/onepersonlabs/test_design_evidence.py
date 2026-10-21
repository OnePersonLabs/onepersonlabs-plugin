"""Protect stale-evidence rejection, comparison blinding and judgment attribution."""

import base64
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import threading
import time
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / 'plugins/onepersonlabs/skills/design-perceptual-interfaces/scripts'
sys.path.insert(0, str(SCRIPTS))
import design_evidence as cli
from evidence_capture import capture, capture_spec, frame_url, verify
from evidence_files import EvidenceError, digest, write_json
from evidence_review import compare, fit_motion, recall_episodes, validate_episodes

PIL_AVAILABLE = importlib.util.find_spec('PIL') is not None


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.html'
        self.source.write_text('<html>source</html>', encoding='utf-8')

    def manifest(self, **changes):
        data = {'version': 1, 'target': 'source.html', 'source_files': ['source.html'],
                'ready_selector': '[data-ready]', 'viewport': {'width': 640, 'height': 480},
                'reduced_motion': 'no-preference', 'frames': [{'id': 'start', 'query': {'t': '0'}}]}
        data.update(changes)
        path = self.root / 'manifest.json'
        write_json(path, data)
        return path

    def frozen(self):
        out = self.root / 'capture'
        out.mkdir()
        for name in ['start.png', 'contact-sheet.png', 'contact-sheet.html']:
            (out / name).write_bytes(b'original captured bytes')
        inputs = {str(self.source): digest(self.source)}
        record = {'version': 1, 'kind': 'capture', 'status': 'complete',
                  'inputs_before': inputs, 'inputs_after': dict(inputs),
                  'frames': [{'artifact': 'start.png'}],
                  'artifacts': {p.name: digest(p) for p in out.iterdir()}}
        write_json(out / 'evidence.json', record)
        return out / 'evidence.json'

    def test_frozen_capture_rejects_source_change_even_when_artifacts_unchanged(self):
        evidence = self.frozen()
        self.assertEqual(verify(evidence)['status'], 'verified')
        self.source.write_text('different production source', encoding='utf-8')
        with self.assertRaisesRegex(EvidenceError, 'source or tool changed'):
            verify(evidence)

    def test_missing_or_changed_artifact_fails(self):
        evidence = self.frozen()
        frame = evidence.parent / 'start.png'
        frame.write_bytes(b'new pixels')
        with self.assertRaisesRegex(EvidenceError, 'Artifact changed'):
            verify(evidence)
        frame.unlink()
        with self.assertRaises(FileNotFoundError):
            verify(evidence)

    def test_failed_or_truncated_capture_inventory_cannot_pass(self):
        evidence = self.frozen()
        data = json.loads(evidence.read_text(encoding='utf-8'))
        del data['artifacts']['start.png']
        write_json(evidence, data)
        with self.assertRaisesRegex(EvidenceError, 'omits required'):
            verify(evidence)
        data['status'] = 'failed'
        write_json(evidence, data)
        with self.assertRaisesRegex(EvidenceError, 'incomplete or failed'):
            verify(evidence)

    def test_capture_requires_ready_contract_and_unique_safe_frame_ids(self):
        for changes in [{'ready_selector': ''}, {'frames': [{'id': '../escape'}]},
                        {'frames': [{'id': 'same'}, {'id': 'same'}]},
                        {'source_files': ['missing.js']}, {'reduced_motion': 'guess'}]:
            with self.subTest(changes=changes), self.assertRaises((EvidenceError, OSError)):
                capture_spec(self.manifest(**changes))
        spec, url, hashes, remote = capture_spec(self.manifest())
        self.assertFalse(remote)
        self.assertIn(str(self.source), hashes)
        self.assertTrue(url.startswith('file:'))

    def test_capture_rejects_generated_or_windows_reserved_names_before_creating_output(self):
        out = self.root / 'invalid-capture'
        for ident in ['contact-sheet', 'CONTACT-SHEET', 'Con', 'NUL', 'aux', 'prn', 'COM1', 'lpt9']:
            with self.subTest(ident=ident), self.assertRaisesRegex(EvidenceError, 'reserved'):
                capture(self.manifest(frames=[{'id': ident}]), out)
            self.assertFalse(out.exists())

    def test_capture_rejects_casefold_collisions_but_keeps_distinct_normal_paths(self):
        with self.assertRaisesRegex(EvidenceError, 'unique ignoring case'):
            capture_spec(self.manifest(frames=[{'id': 'A'}, {'id': 'a'}]))
        frames = [{'id': 'scene-A'}, {'id': 'scene-B'}]
        spec, _, _, _ = capture_spec(self.manifest(frames=frames))
        self.assertEqual(spec['frames'], frames)

    def test_query_preserves_target_parameters_and_encodes_frame_values(self):
        url = frame_url('https://example.test/view?keep=1&state=old#detail', {'state': 'a b&c'})
        self.assertEqual(url, 'https://example.test/view?keep=1&state=a+b%26c#detail')

    @unittest.skipUnless(PIL_AVAILABLE, 'Comparison requires optional installed Pillow')
    def test_comparison_separates_conditions_and_strips_png_metadata(self):
        from PIL import Image, PngImagePlugin
        candidates = []
        for number, color in enumerate(['red', 'blue']):
            name = f'private-origin-{number}.png'
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text('origin', f'private-origin-{number}')
            Image.new('RGB', (8, 8), color).save(self.root / name, pnginfo=metadata)
            candidates.append({'image': name, 'caption': f'Review scene {number}',
                               'condition': f'secret-condition-{number}', 'source': f'secret-source-{number}'})
        manifest = self.root / 'compare.json'
        write_json(manifest, {'version': 1, 'prompt': 'Explain the next action.', 'candidates': candidates})
        result = compare(manifest, self.root / 'review')
        gallery = Path(result['gallery']).read_text(encoding='utf-8')
        for private in ['private-origin', 'secret-condition', 'secret-source', str(self.root)]:
            self.assertNotIn(private, gallery)
        for payload in re.findall(r'data:image/png;base64,([^"\s]+)', gallery):
            with Image.open(io.BytesIO(base64.b64decode(payload))) as image:
                self.assertEqual(image.info, {})
        mapping = json.loads((self.root / 'review/mapping.json').read_text(encoding='utf-8'))
        self.assertEqual({c['condition'] for c in mapping['candidates']}, {c['condition'] for c in candidates})
        self.assertEqual(result['human_judgments'], 'unknown')
        judgments = json.loads((self.root / 'review/judgments.json').read_text(encoding='utf-8'))
        self.assertTrue(all(c['status'] == 'unknown' and c['actor'] is None for c in judgments['candidates']))
        with self.assertRaisesRegex(EvidenceError, 'already exists'):
            compare(manifest, self.root / 'review')

    @unittest.skipUnless(PIL_AVAILABLE, 'Comparison requires optional installed Pillow')
    def test_comparison_generated_ids_cannot_be_overridden_by_candidate_metadata(self):
        from PIL import Image
        candidates = []
        for number in range(2):
            name = f'image-{number}.png'
            Image.new('RGB', (4, 4), 'white').save(self.root / name)
            candidates.append({'image': name, 'caption': 'Interpret the display',
                               'condition': f'private-approach-{number}', 'source': f'origin-{number}',
                               'anonymous_id': 'Candidate 999'})
        manifest = self.root / 'compare.json'
        write_json(manifest, {'version': 1, 'prompt': 'Explain the next action.', 'candidates': candidates})
        result = compare(manifest, self.root / 'review')
        mapping = json.loads(Path(result['mapping']).read_text(encoding='utf-8'))
        judgments = json.loads((self.root / 'review/judgments.json').read_text(encoding='utf-8'))
        gallery = Path(result['gallery']).read_text(encoding='utf-8')
        mapping_ids = [item['anonymous_id'] for item in mapping['candidates']]
        self.assertEqual(mapping_ids, [item['anonymous_id'] for item in judgments['candidates']])
        self.assertEqual(mapping_ids, re.findall(r'<strong>(Candidate \d+)</strong>', gallery))
        self.assertNotIn('Candidate 999', mapping_ids)

    def episode(self, ident='sailing', surface='instrument'):
        return {'id': ident, 'problem': 'Understand whether to change direction',
                'context': {'surface': surface, 'audience': 'sailor'},
                'alternatives': [{'id': 'one', 'status': 'selected', 'reason': 'Shows direction'},
                                 {'id': 'two', 'status': 'rejected', 'reason': 'Conceals direction'}],
                'judgments': [{'actor': 'user', 'identity': 'recorded participant', 'basis': 'stated',
                               'statement': 'The arrow is clearer here', 'evidence': ['session:12']}],
                'limits': ['One participant, one task'], 'confidence': 'low'}

    def episodes_file(self, episodes):
        path = self.root / 'episodes.json'
        write_json(path, {'version': 1, 'episodes': episodes})
        return path

    def test_model_inference_cannot_be_attributed_to_user(self):
        episode = self.episode()
        episode['judgments'][0]['basis'] = 'inferred'
        with self.assertRaisesRegex(EvidenceError, 'belongs to the model'):
            validate_episodes(self.episodes_file([episode]))
        episode['judgments'][0]['actor'] = 'model'
        self.assertEqual(len(validate_episodes(self.episodes_file([episode]))['episodes']), 1)

    def test_recall_does_not_promote_contextual_judgment_to_global_preference(self):
        episodes = [self.episode(), self.episode('store', 'checkout')]
        path = self.episodes_file(episodes)
        query = self.root / 'context.json'
        write_json(query, {'surface': 'instrument', 'audience': 'sailor'})
        result = recall_episodes(path, query)
        self.assertEqual(result['episodes'], [episodes[0]])
        write_json(query, {'surface': 'instrument', 'audience': 'novice'})
        self.assertEqual(recall_episodes(path, query)['episodes'], [])
        write_json(query, {})
        with self.assertRaisesRegex(EvidenceError, 'nonempty'):
            recall_episodes(path, query)

    def test_alternatives_require_decision_and_reasons(self):
        episode = self.episode()
        episode['alternatives'][1]['status'] = 'selected'
        with self.assertRaisesRegex(EvidenceError, 'Exactly one'):
            validate_episodes(self.episodes_file([episode]))
        episode = self.episode()
        episode['alternatives'][0]['reason'] = ''
        with self.assertRaisesRegex(EvidenceError, 'reason'):
            validate_episodes(self.episodes_file([episode]))

    def test_curve_residuals_are_measured_in_original_value_units(self):
        path = self.root / 'motion.csv'
        path.write_text('time_ms,value\n0,10\n50,15\n100,20\n', encoding='utf-8')
        result = fit_motion(path)
        self.assertEqual(result['candidates'][0]['curve'], 'linear')
        self.assertEqual(result['candidates'][0]['rmse'], 0)
        quadratic = next(x for x in result['candidates'] if x['curve'] == 'ease-in-quadratic')
        self.assertEqual(quadratic['max_abs_residual'], 2.5)
        path.write_text('time_ms,value\n0,10\n0,15\n100,20\n', encoding='utf-8')
        with self.assertRaisesRegex(EvidenceError, 'strictly increase'):
            fit_motion(path)

    def test_cli_returns_nonzero_for_missing_frozen_source(self):
        evidence = self.frozen()
        self.source.unlink()
        from contextlib import redirect_stderr
        with redirect_stderr(io.StringIO()) as stream:
            status = cli.main(['verify', '--evidence', str(evidence)])
        self.assertEqual(status, 1)
        self.assertEqual(json.loads(stream.getvalue())['status'], 'error')


@unittest.skipUnless(os.environ.get('ONEPERSONLABS_DESIGN_BROWSER_TESTS') == '1',
                     'Set ONEPERSONLABS_DESIGN_BROWSER_TESTS=1 for the real browser contract checks')
class BrowserEvidenceTests(unittest.TestCase):
    manifest = EvidenceTests.manifest
    # Inherit fixture helpers, not the ordinary unit tests.
    def setUp(self):
        EvidenceTests.setUp(self)
        self.source.write_text("""<!doctype html><html><body><main>Fixture</main><script>
        const q=new URLSearchParams(location.search); const el=document.querySelector('main');
        setTimeout(()=>{el.setAttribute('data-ready','true');
        el.setAttribute('data-evidence-state',q.get('state')||'idle');
        el.setAttribute('data-frozen-ms',q.get('t')||'0');},Number(q.get('delay')||0));
        </script></body></html>""", encoding='utf-8')

    def test_browser_capture_records_declared_and_measured_time_separately(self):
        manifest = self.manifest(declared_time_attribute='data-frozen-ms', frames=[
            {'id': 'one', 'query': {'state': 'idle', 't': '700'}, 'requested_time_ms': 700,
             'expected_state': 'idle', 'reduced_motion': 'reduce'}])
        result = capture(manifest, self.root / 'captured')
        frame = result['frames'][0]
        self.assertEqual(frame['before_screenshot']['declared_time'], '700')
        self.assertEqual(frame['reduced_motion'], 'reduce')
        self.assertGreaterEqual(frame['after_screenshot']['browser_time_ms'],
                                frame['before_screenshot']['browser_time_ms'])
        self.assertEqual(verify(self.root / 'captured/evidence.json')['status'], 'verified')

    def test_browser_missing_ready_is_failed_evidence(self):
        manifest = self.manifest(ready_selector='#never-ready', timeout_ms=200)
        with self.assertRaisesRegex(EvidenceError, 'Capture failed'):
            capture(manifest, self.root / 'failed')
        record = json.loads((self.root / 'failed/evidence.json').read_text(encoding='utf-8'))
        self.assertEqual(record['status'], 'failed')
        self.assertIn('#never-ready', record['error'])
        with self.assertRaisesRegex(EvidenceError, 'incomplete or failed'):
            verify(self.root / 'failed/evidence.json')

    def test_browser_detects_concurrent_source_change_between_frames(self):
        dependency = self.root / 'model.js'
        dependency.write_text('original', encoding='utf-8')
        out = self.root / 'raced'
        manifest = self.manifest(source_files=['source.html', 'model.js'], frames=[
            {'id': 'first', 'query': {'state': 'first'}},
            {'id': 'second', 'query': {'state': 'second', 'delay': '600'}}])
        changed = threading.Event()
        def mutate_after_first_frame():
            deadline = time.monotonic() + 15
            while not (out / 'first.png').exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            if (out / 'first.png').exists():
                dependency.write_text('changed by another writer', encoding='utf-8')
                changed.set()
        worker = threading.Thread(target=mutate_after_first_frame, daemon=True)
        worker.start()
        try:
            with self.assertRaisesRegex(EvidenceError, 'Declared input changed'):
                capture(manifest, out)
        finally:
            worker.join(timeout=16)
        self.assertTrue(changed.is_set())
        record = json.loads((out / 'evidence.json').read_text(encoding='utf-8'))
        self.assertNotEqual(record['inputs_before'], record['inputs_after'])
        self.assertEqual(record['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
