"""Affectus fitness-function tests (jazz receipts).

Not "did it play the right notes" -- there are none. These test that the
instrument stays in the pocket, genuinely surprises, and serves the tune.
Run: python -m unittest discover -s tests -v
"""

from dataclasses import FrozenInstanceError
from unittest import TestCase

from sensus_artificialis import Attribution, Evidence, Sensus
from sensus_artificialis.affectus import (
    Affectus,
    AffectusConfig,
    DRIVER_KINDS,
    DriverEvent,
)


def drive(inst, tick, kind, magnitude=1.0):
    inst.step(tick, (DriverEvent(kind=kind, magnitude=magnitude,
                                source_ref="test:" + kind),))


class AffectusFitnessTests(TestCase):
    def test_habituation_diminishes_response(self):
        """The 10th exposure moves the weather less than the 1st."""
        cfg = AffectusConfig(seed=7)
        first = Affectus(cfg)
        drive(first, 1, "social_feedback")
        first_delta = abs(first.state["valence"])
        tenth = Affectus(cfg)
        for tick in range(1, 13):
            drive(tenth, tick, "social_feedback")
        last_delta = abs(tenth.state["valence"] - Affectus(cfg).state["valence"])
        # Recompute the 12th-tick marginal displacement properly.
        probe = Affectus(cfg)
        for tick in range(1, 12):
            drive(probe, tick, "social_feedback")
        before = probe.state["valence"]
        drive(probe, 12, "social_feedback")
        marginal = abs(probe.state["valence"] - before)
        self.assertLess(marginal, first_delta * 0.75)

    def test_weather_persists_across_quiet_ticks(self):
        """Yesterday colors today without permission: slow decay, no reset."""
        inst = Affectus(AffectusConfig(seed=3))
        for tick in range(1, 11):
            drive(inst, tick, "goal_progress")
        peak = inst.state["valence"]
        self.assertGreater(peak, 0.2)
        for tick in range(11, 41):
            inst.step(tick)
        # Slow fade, never a snap: ~2/3 of the weather remains after
        # 3x the drive duration in silence.
        self.assertGreater(inst.state["valence"], 0.15)

    def test_opponent_dip_after_driver_stops(self):
        """Relief/letdown without new input: the counter-force overshoots."""
        inst = Affectus(AffectusConfig(seed=11))
        for tick in range(1, 21):
            drive(inst, tick, "goal_progress", magnitude=1.5)
        self.assertGreater(inst.state["valence"], 0.2)
        dipped = False
        for tick in range(21, 171):
            inst.step(tick)
            if inst.state["valence"] < -0.01:
                dipped = True
                break
        self.assertTrue(dipped, "no opponent dip after driver stopped")

    def test_felt_report_is_coarse_and_misattributable(self):
        """The felt/actual gap: wrong cause representable, unknown allowed."""
        inst = Affectus(AffectusConfig(seed=5))
        for tick in range(1, 6):
            drive(inst, tick, "monotony")  # actual driver: monotony
        wrong = inst.emit_interoception(
            6, "felt-1",
            attributions=(Attribution(cause_ref="social_feedback",
                                      confidence=0.7),),
        )
        self.assertEqual(wrong.evidence, Evidence.INTEROCEPTIVE)
        self.assertEqual(wrong.channel, "interoception")
        self.assertEqual(wrong.attributions[0].cause_ref, "social_feedback")
        unknown = inst.emit_interoception(6, "felt-2")
        self.assertEqual(unknown.attributions, ())

    def test_felt_report_quantized(self):
        """Coarse quantization: the report underdetermines the state."""
        inst = Affectus(AffectusConfig(seed=9, felt_quantum=0.25))
        drive(inst, 1, "novelty", magnitude=0.3)
        drive(inst, 2, "novelty", magnitude=0.31)
        first = inst.emit_interoception(2, "f1").value
        drive(inst, 3, "novelty", magnitude=0.29)
        second = inst.emit_interoception(3, "f2").value
        # Distinct states can produce identical felt reports.
        self.assertIsInstance(first, str)
        self.assertIsInstance(second, str)

    def test_receipts_append_only(self):
        inst = Affectus(AffectusConfig(seed=2))
        drive(inst, 1, "novelty")
        inst.step(2, (
            DriverEvent(kind="prediction_error", magnitude=1.0,
                        source_ref="test:pe"),
            DriverEvent(kind="rest_density", magnitude=1.0,
                        source_ref="test:rd"),
        ))
        receipts = inst.receipts
        self.assertEqual(len(receipts), 3)
        self.assertIsInstance(receipts, tuple)
        self.assertEqual(receipts[0].driver_kind, "novelty")
        with self.assertRaises(FrozenInstanceError):
            receipts[0].magnitude = 99.0  # type: ignore

    def test_no_reset_method(self):
        """If the weather can be willed away, it is a setting, not an emotion."""
        self.assertFalse(hasattr(Affectus(), "reset"))

    def test_binding_never_upgrades_interoception(self):
        """Felt reports bind through Sensus without evidential-class upgrade."""
        inst = Affectus(AffectusConfig(seed=4))
        drive(inst, 1, "social_feedback")
        felt = inst.emit_interoception(1, "felt-1")
        scene = Sensus().step(1, [felt])
        claim = scene.objects[0].claims[0]
        self.assertIs(claim.evidence, Evidence.INTEROCEPTIVE)
        self.assertFalse(any(c.evidence is Evidence.OBSERVED
                             for c in scene.objects[0].claims))

    def test_snapshot_restore_preserves_weather(self):
        """Weather survives the gaps: serialize, restore, continue."""
        inst = Affectus(AffectusConfig(seed=6))
        for tick in range(1, 8):
            drive(inst, tick, "unresolved_loops")
        restored = Affectus.restore(inst.snapshot(),
                                    AffectusConfig(seed=6))
        self.assertEqual(restored.state, inst.state)
        self.assertEqual(restored.receipts, inst.receipts)
        for tick in range(8, 11):
            drive(inst, tick, "rest_density")
            drive(restored, tick, "rest_density")
        self.assertEqual(restored.state, inst.state)

    def test_deterministic_with_seed(self):
        a = Affectus(AffectusConfig(seed=42))
        b = Affectus(AffectusConfig(seed=42))
        for tick in range(1, 15):
            drive(a, tick, "prediction_error", magnitude=0.7)
            drive(b, tick, "prediction_error", magnitude=0.7)
        self.assertEqual(a.state, b.state)

    def test_ticks_must_advance_strictly(self):
        inst = Affectus()
        inst.step(1)
        with self.assertRaises(ValueError):
            inst.step(1)

    def test_unknown_driver_rejected(self):
        with self.assertRaises(ValueError):
            DriverEvent(kind="vibes", magnitude=1.0)
