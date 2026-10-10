"""Reproducibility and negative-result assertions for the Sensus lab battery."""

import unittest

from experiments.standalone_battery import run, run_ambiguity, run_identity, run_shift


class StandaloneBatteryTests(unittest.TestCase):
    def test_fixed_seed_is_reproducible(self):
        self.assertEqual(run(), run())

    def test_identity_reports_known_collision_failure(self):
        result = run_identity(20261010, 10)
        self.assertEqual(result["n"], 40)
        self.assertEqual(result["correct"], 20)
        self.assertEqual(result["false_merges"], 10)
        self.assertEqual(result["false_splits"], 0)
        self.assertEqual(result["abstentions"], 10)
        self.assertEqual(result["always_same_control_accuracy"], 0.5)
        self.assertEqual(result["always_different_control_accuracy"], 0.5)

    def test_twin_ambiguity_abstains(self):
        result = run_ambiguity()
        self.assertEqual(result["identity_status"], "ambiguous")
        self.assertEqual(result["candidate_count"], 2)
        self.assertFalse(result["forced_reidentification"])

    def test_fully_renamed_features_break_recognition(self):
        result = run_shift()
        self.assertTrue(result["unchanged"]["reidentified"])
        self.assertTrue(result["partial"]["reidentified"])
        self.assertFalse(result["renamed"]["reidentified"])

    def test_no_provenance_loss_or_silent_upgrade(self):
        report = run()
        for case in report["provenance"].values():
            self.assertTrue(case["all_claims_unchanged"])
            self.assertEqual(case["claims_in"], case["claims_out"])
        self.assertEqual(
            report["provenance"]["observed_disagreement"]["conflicts"][0]["status"], "vetoed")
        self.assertEqual(
            report["provenance"]["heard_beaker"]["conflicts"][0]["status"], "uncertain")
        self.assertEqual(
            report["provenance"]["interoception_without_cause"]["attribution_values"], [])

    def test_no_fake_downstream_findings(self):
        not_run = run()["not_run"]
        self.assertIn("E6_scene_vs_raw", not_run)
        self.assertIn("E4_actual_cross_model", not_run)


if __name__ == "__main__":
    unittest.main()
