"""Executable RFC-001 specimen; isolated reference guard, not production qualification.
Run: python3 -m unittest discover -s agi-reactor/conformance -v
The target oracle is available only to tests, never to the recovering controller.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent

class UnknownRestore(unittest.TestCase):
    def run_specimen(self, mode):
        with tempfile.TemporaryDirectory(prefix='reactor-rfc001-') as root:
            run = subprocess.run([sys.executable, str(HERE/'unknown_restore.py'),
                                  '--root', root, '--mode', mode],
                                 capture_output=True, text=True, timeout=20)
            self.assertEqual(run.returncode, 0, run.stderr)
            return json.loads(run.stdout)

    def assert_no_duplicate(self, result):
        self.assertEqual(result['target_effect_count'], 1,
                         'duplicate external effect after UNKNOWN restore')

    def test_crash_after_200_restore_unknown_never_replays(self):
        r = self.run_specimen('guarded')
        self.assertEqual(r['worker_exit'], 86)
        self.assertEqual(r['target_effects_before_restore'], 1)
        self.assertEqual(r['snapshot_state'], 'UNKNOWN')
        self.assertEqual(r['before_restore_retry'], 'OUTCOME_UNKNOWN')
        self.assertEqual(r['same_without_global_hold'], 'OUTCOME_UNKNOWN')
        self.assertEqual(r['replacement_without_global_hold'], 'STEP_ALREADY_HAS_OPERATION')
        self.assertEqual(r['current_epoch'], 2)
        self.assertEqual(r['operation_state'], 'UNKNOWN')
        self.assertEqual(r['same_operation'], 'RECOVERY_HOLD')
        self.assertEqual(r['replacement_operation'], 'RECOVERY_HOLD')
        self.assertEqual(r['old_worker'], 'STALE_EPOCH')
        self.assertEqual(r['changed_arguments'], 'INTENT_MISMATCH')
        self.assertEqual(r['ticket_state'], 'NEEDS_RECONCILIATION')
        self.assert_no_duplicate(r)

    def test_oracle_catches_unsafe_reset_on_restore(self):
        r = self.run_specimen('unsafe-reset-on-restore')
        self.assertEqual(r['target_effects_before_restore'], 1)
        self.assertEqual(r['target_effect_count'], 2)
        with self.assertRaisesRegex(AssertionError, 'duplicate external effect'):
            self.assert_no_duplicate(r)

if __name__ == '__main__':
    unittest.main()
