"""Standard-library contract tests. Run: python -m unittest discover -s tests -v"""

from dataclasses import FrozenInstanceError
from unittest import TestCase

from sensus_artificialis import Attribution, Evidence, Percept, Sensus, SensusConfig


def percept(event, tick, channel="vision", attribute="color", value="red",
            confidence=0.9, evidence=Evidence.OBSERVED, hint="apple",
            features=(("shape", "round"), ("surface", "smooth")), attributions=()):
    return Percept(
        event_id=event, channel=channel, evidence=evidence,
        source_ref="shell:" + event, tick=tick, attribute=attribute,
        value=value, confidence=confidence, object_hint=hint,
        features=features, attributions=attributions,
    )


class SensusContractTests(TestCase):
    def test_cross_channel_binding_preserves_constituents(self):
        scene = Sensus().step(1, [
            percept("a", 1, channel="vision"),
            percept("b", 1, channel="touch", attribute="texture", value="smooth"),
        ])
        self.assertEqual(len(scene.objects), 1)
        self.assertEqual({c.channel for c in scene.objects[0].claims}, {"vision", "touch"})
        self.assertEqual({c.source_ref for c in scene.objects[0].claims}, {"shell:a", "shell:b"})

    def test_high_confidence_disagreement_vetoed_not_resolved(self):
        scene = Sensus().step(1, [
            percept("a", 1, value="red"),
            percept("b", 1, channel="audio", value="blue"),
        ])
        self.assertEqual(scene.conflicts[0].status, "vetoed")
        self.assertEqual(scene.objects[0].contested_attributes, ("color",))
        self.assertEqual({c.value for c in scene.objects[0].claims}, {"red", "blue"})

    def test_low_confidence_disagreement_is_uncertain(self):
        scene = Sensus().step(1, [
            percept("a", 1, value="red", confidence=0.4),
            percept("b", 1, channel="audio", value="blue", confidence=0.4),
        ])
        self.assertEqual(scene.conflicts[0].status, "uncertain")

    def test_inference_never_promoted_to_observation(self):
        scene = Sensus().step(1, [
            percept("sound", 1, channel="audio", attribute="noise", value="glass break"),
            percept("beaker", 1, evidence=Evidence.INFERRED, attribute="state", value="broken"),
        ])
        claim = next(c for c in scene.objects[0].claims if c.event_id == "beaker")
        self.assertEqual(claim.evidence, Evidence.INFERRED)
        self.assertFalse(any(c.evidence is Evidence.OBSERVED and c.attribute == "state"
                             for c in scene.objects[0].claims))

    def test_absent_channel_not_fabricated_as_claim(self):
        scene = Sensus(SensusConfig(expected_channels=("vision", "audio", "touch"))).step(
            1, [percept("a", 1)]
        )
        self.assertEqual(scene.absent_channels, ("audio", "touch"))
        self.assertEqual(len(scene.objects[0].claims), 1)

    def test_interoception_supports_unknown_cause(self):
        scene = Sensus().step(1, [percept(
            "uneasy", 1, channel="interoception", evidence=Evidence.INTEROCEPTIVE,
            attribute="arousal", value="uneasy", hint="body", attributions=(),
        )])
        claim = scene.objects[0].claims[0]
        self.assertEqual(claim.value, "uneasy")
        self.assertEqual(claim.attributions, ())
        self.assertEqual(claim.evidence, Evidence.INTEROCEPTIVE)

    def test_attribution_kept_as_candidate(self):
        cause = Attribution("noise:next-room", 0.3)
        scene = Sensus().step(1, [percept(
            "uneasy", 1, channel="interoception", evidence=Evidence.INTEROCEPTIVE,
            attribute="arousal", value="uneasy", attributions=(cause,),
        )])
        self.assertEqual(scene.objects[0].claims[0].attributions, (cause,))

    def test_cross_tick_matching_with_discriminative_features(self):
        organ = Sensus()
        first = organ.step(1, [percept("a", 1)])
        next_scene = organ.step(2, [percept("b", 2, hint="another-hint")])
        self.assertEqual(first.objects[0].object_id, next_scene.objects[0].object_id)
        self.assertEqual(next_scene.objects[0].identity_status, "matched")

    def test_ambiguous_identical_objects_do_not_force_identity(self):
        organ = Sensus()
        first = organ.step(1, [
            percept("a", 1, hint="one"),
            percept("b", 1, hint="two"),
        ])
        followup = organ.step(2, [percept("c", 2, hint="three")])
        self.assertEqual(followup.objects[0].identity_status, "ambiguous")
        self.assertNotIn(followup.objects[0].object_id,
                         {o.object_id for o in first.objects})
        self.assertEqual(len(followup.objects[0].identity_candidates), 2)

    def test_recent_files_are_bounded_and_expire(self):
        organ = Sensus(SensusConfig(recent_window=1, max_object_files=2))
        for tick in range(1, 5):
            organ.step(tick, [percept(str(tick), tick, hint=str(tick),
                                      features=(("serial", str(tick)),))])
        self.assertLessEqual(len(organ.recent_object_files), 2)
        self.assertTrue(all(f.last_seen_tick >= 3 for f in organ.recent_object_files))

    def test_scene_is_immutable(self):
        scene = Sensus().step(1, [percept("a", 1)])
        with self.assertRaises(FrozenInstanceError):
            scene.tick = 9
        with self.assertRaises(FrozenInstanceError):
            scene.objects[0].object_id = "tampered"

    def test_order_independent_scene(self):
        one = [percept("a", 1), percept("b", 1, channel="touch",
                                     attribute="texture", value="smooth")]
        a = Sensus().step(1, one)
        b = Sensus().step(1, reversed(one))
        self.assertEqual(a, b)

    def test_duplicate_and_stale_event_rejected(self):
        organ = Sensus()
        with self.assertRaises(ValueError):
            organ.step(1, [percept("a", 1), percept("a", 1)])
        organ.step(1, [percept("a", 1)])
        with self.assertRaises(ValueError):
            organ.step(1, [])
        with self.assertRaises(ValueError):
            organ.step(2, [percept("b", 1)])

    def test_invalid_confidence_rejected(self):
        with self.assertRaises(ValueError):
            percept("a", 1, confidence=float("nan"))

    def test_noninteroceptive_cause_rejected(self):
        with self.assertRaises(ValueError):
            percept("a", 1, attributions=(Attribution("guess", 0.2),))

    def test_no_cross_tick_binding_without_features(self):
        organ = Sensus()
        a = organ.step(1, [percept("a", 1, features=())])
        b = organ.step(2, [percept("b", 2, features=())])
        self.assertNotEqual(a.objects[0].object_id, b.objects[0].object_id)

    def test_mnemonic_mismatch_remains_separate_evidence(self):
        scene = Sensus().step(1, [
            percept("observed", 1, value="closed"),
            percept("recalled", 1, value="open", evidence=Evidence.REMEMBERED),
        ])
        self.assertEqual(scene.conflicts[0].status, "uncertain")
        self.assertEqual([p.evidence for p in scene.objects[0].claims],
                         [Evidence.OBSERVED, Evidence.REMEMBERED])


if __name__ == "__main__":
    import unittest
    unittest.main()
