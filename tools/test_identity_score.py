"""Deterministic checks for the parts of identity scoring that are decisions rather than measurements.

The embeddings need the model files and the WanGP interpreter; the bucketing and the verdict do not, and
they are where a silent change would corrupt every later cull. Run with any Python that can import numpy:

    python -m unittest tools.test_identity_score
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import identity_score


class YawBucketTest(unittest.TestCase):
    def test_measured_phase1_angles_land_in_their_bucket(self):
        """The Phase 1 batch carries a known requested angle per shot; these are its measured proxies."""
        for proxy, expected in [(-0.007, "frontal"), (0.074, "frontal"), (0.095, "frontal"),
                                (-0.391, "three_quarter"), (-0.401, "three_quarter"),
                                (-0.701, "deep_three_quarter"), (-0.737, "deep_three_quarter"),
                                (-1.078, "profile")]:
            self.assertEqual(identity_score.yaw_bucket(proxy), expected, proxy)

    def test_sign_does_not_change_the_bucket(self):
        self.assertEqual(identity_score.yaw_bucket(0.5), identity_score.yaw_bucket(-0.5))

    def test_undetected(self):
        self.assertEqual(identity_score.yaw_bucket(None), "undetected")


class ClassifyTest(unittest.TestCase):
    thresholds = {"sface": 0.83, "arcface": 0.84}
    ceiling = 0.551

    def verdict(self, sface, arcface):
        return identity_score.classify({"sface": sface, "arcface": arcface}, self.thresholds, self.ceiling)

    def test_both_recognisers_above_is_same(self):
        self.assertEqual(self.verdict(0.885, 0.849), "same")

    def test_both_below_the_negative_ceiling_is_different(self):
        self.assertEqual(self.verdict(0.406, 0.296), "different")

    def test_the_gap_between_the_two_distributions_is_its_own_verdict(self):
        # The failure this project keeps hitting: not another person, not this person either.
        self.assertEqual(self.verdict(0.785, 0.687), "drift")

    def test_one_recogniser_above_and_one_below_goes_to_the_operator(self):
        self.assertEqual(self.verdict(0.885, 0.700), "disagree")

    def test_no_threshold_for_the_bucket_never_invents_one(self):
        self.assertEqual(identity_score.classify({"sface": 0.9}, {}, self.ceiling), "uncalibrated")

    def test_a_missing_ceiling_does_not_promote_a_low_score_to_different(self):
        self.assertEqual(identity_score.classify({"sface": 0.2}, self.thresholds, None), "drift")


class LoadCalibrationTest(unittest.TestCase):
    def test_reads_the_calibration_document(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calibration.json"
            path.write_text(json.dumps({"thresholds": {"frontal": {"sface": 0.83}}, "drift_band_ceiling": 0.551,
                                        "limits": "..."}), encoding="utf-8")
            loaded = identity_score.load_calibration(str(path))
        self.assertEqual(loaded, {"thresholds": {"frontal": {"sface": 0.83}}, "drift_band_ceiling": 0.551})

    def test_reads_a_bare_threshold_map(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "thresholds.json"
            path.write_text(json.dumps({"frontal": {"sface": 0.83}}), encoding="utf-8")
            loaded = identity_score.load_calibration(str(path))
        self.assertEqual(loaded["thresholds"], {"frontal": {"sface": 0.83}})
        self.assertIsNone(loaded["drift_band_ceiling"])

    def test_no_calibration_scores_without_deciding(self):
        self.assertEqual(identity_score.load_calibration(None), {"thresholds": {}, "drift_band_ceiling": None})

    def test_the_checked_in_calibration_is_readable_and_covers_the_frontal_bucket(self):
        loaded = identity_score.load_calibration(
            str(Path(__file__).resolve().parents[1] / "docs" / "identity-scoring-calibration.json"))
        self.assertIn("frontal", loaded["thresholds"])
        self.assertLess(loaded["drift_band_ceiling"], min(loaded["thresholds"]["frontal"].values()))


class CosineTest(unittest.TestCase):
    def test_identical_unit_vectors(self):
        self.assertAlmostEqual(identity_score.cosine([1.0, 0.0], [1.0, 0.0]), 1.0)

    def test_orthogonal(self):
        self.assertAlmostEqual(identity_score.cosine([1.0, 0.0], [0.0, 1.0]), 0.0)


if __name__ == "__main__":
    unittest.main()
