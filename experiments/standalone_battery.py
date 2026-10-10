"""Dependency-free, stand-alone Sensus lab battery.

Ground truth never enters a Percept or the Sensus object. This is a SMALL
CONSTRUCTED benchmark, not independent ecological validation and not E6.
Run from repository root: python -m experiments.standalone_battery
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from random import Random

from sensus_artificialis import Attribution, Evidence, Percept, Sensus, SensusConfig

SEED = 20261010
N_PER_FAMILY = 40
BATTERY_VERSION = "sensus.standalone-battery.v0.1"


@dataclass(frozen=True)
class IdentityTrial:
    trial_id: str
    family: str
    truth_same: bool  # evaluator only, never passed to the organ
    before: Percept
    after: Percept


def p(event: str, tick: int, *, channel: str = "vision",
      evidence: Evidence = Evidence.OBSERVED, attribute: str = "shape",
      value: str = "book", features: tuple[tuple[str, str], ...] = (),
      hint: str = "target", confidence: float = 0.9,
      attributions: tuple[Attribution, ...] = ()) -> Percept:
    return Percept(
        event_id=event, channel=channel, evidence=evidence,
        source_ref="shell:" + event, tick=tick, attribute=attribute,
        value=value, confidence=confidence, features=features,
        object_hint=hint, attributions=attributions,
    )


def identity_trials(seed: int = SEED, n_per_family: int = N_PER_FAMILY) -> tuple[IdentityTrial, ...]:
    """Four prespecified families, deliberately including indistinguishable impostors.

    Feature signatures are symbolic shell outputs. They are not embeddings,
    measured probabilities or raw sensor measurements.
    """
    if n_per_family < 1:
        raise ValueError("n_per_family must be positive")
    cases: list[IdentityTrial] = []
    for i in range(n_per_family):
        shared = (("category", "book"), ("cover", "cloth"))
        unique = ("mark", "case-" + str(i))
        base = shared + (unique,)
        designs = (
            ("stable", True, base),
            ("distinct", False, shared + (("mark", "other-" + str(i)),)),
            ("occluded", True, shared),
            ("collision", False, base),
        )
        for family, same, second in designs:
            prefix = family + ":" + str(i)
            cases.append(IdentityTrial(
                trial_id=prefix, family=family, truth_same=same,
                before=p(prefix + ":t1", 1, features=base),
                after=p(prefix + ":t2", 2, features=second, hint="changed-hint"),
            ))
    Random(seed).shuffle(cases)
    return tuple(cases)


def _provenance_equal(inputs: tuple[Percept, ...], scene) -> bool:
    received = tuple(sorted((x for obj in scene.objects for x in obj.claims),
                            key=lambda x: x.event_id))
    return received == tuple(sorted(inputs, key=lambda x: x.event_id))


def run_identity(seed: int, n_per_family: int) -> dict:
    rows: list[dict] = []
    for trial in identity_trials(seed, n_per_family):
        organ = Sensus()
        first = organ.step(1, (trial.before,))
        second = organ.step(2, (trial.after,))
        obj = second.objects[0]
        prediction = obj.reidentified_from == first.objects[0].object_id
        if obj.identity_status == "ambiguous":
            decision = "abstain"
        else:
            decision = "same" if prediction else "different"
        rows.append(dict(
            family=trial.family, truth_same=trial.truth_same,
            decision=decision, correct=(prediction == trial.truth_same and decision != "abstain"),
            false_merge=(prediction and not trial.truth_same),
            false_split=(decision == "different" and trial.truth_same),
            abstain=(decision == "abstain"),
        ))
    per_family = {}
    for name in ("stable", "distinct", "occluded", "collision"):
        family_rows = [r for r in rows if r["family"] == name]
        per_family[name] = {
            "n": len(family_rows),
            "truth_same": family_rows[0]["truth_same"],
            "correct": sum(r["correct"] for r in family_rows),
            "false_merges": sum(r["false_merge"] for r in family_rows),
            "false_splits": sum(r["false_split"] for r in family_rows),
            "abstentions": sum(r["abstain"] for r in family_rows),
        }
    total = len(rows)
    return {
        "n": total,
        "correct": sum(r["correct"] for r in rows),
        "false_merges": sum(r["false_merge"] for r in rows),
        "false_splits": sum(r["false_split"] for r in rows),
        "abstentions": sum(r["abstain"] for r in rows),
        "coverage": (total - sum(r["abstain"] for r in rows)) / total,
        "accuracy_abstention_wrong": sum(r["correct"] for r in rows) / total,
        "always_same_control_accuracy": sum(r["truth_same"] for r in rows) / total,
        "always_different_control_accuracy": sum(not r["truth_same"] for r in rows) / total,
        "by_family": per_family,
    }


def run_ambiguity() -> dict:
    """Two initially indistinguishable objects: third probe must not pick arbitrarily."""
    organ = Sensus()
    origin = organ.step(1, (
        p("left", 1, hint="left", features=(("shape", "cup"), ("tone", "white"))),
        p("right", 1, hint="right", features=(("shape", "cup"), ("tone", "white"))),
    ))
    incoming = organ.step(2, (
        p("unknown", 2, hint="unclear", features=(("shape", "cup"), ("tone", "white"))),
    ))
    obj = incoming.objects[0]
    return {
        "previous_count": len(origin.objects),
        "candidate_count": len(obj.identity_candidates),
        "identity_status": obj.identity_status,
        "forced_reidentification": obj.reidentified_from is not None,
    }


def run_shift() -> dict:
    """E4 proxy ONLY: deterministic encoding changes, NO actual model tests."""
    original = (("category", "book"), ("cover", "cloth"), ("mark", "known"))
    permutations = {
        "unchanged": original,
        "partial": original[:2],
        "renamed": (("kind", "volume"), ("binding", "linen"), ("stamp", "known")),
    }
    result = {}
    for key, features in permutations.items():
        organ = Sensus()
        first = organ.step(1, (p("first", 1, features=original),))
        second = organ.step(2, (p("second", 2, features=features),))
        obj = second.objects[0]
        result[key] = {
            "reidentified": obj.reidentified_from == first.objects[0].object_id,
            "identity_status": obj.identity_status,
            "candidates": [asdict(x) for x in obj.identity_candidates],
        }
    return result


def run_provenance_and_conflicts() -> dict:
    """E1/E3/E5 and interoception: trace exact, non-amplified input records."""
    conditions = {
        "observed_disagreement": (
            p("red", 1, channel="vision", attribute="color", value="red"),
            p("blue", 1, channel="touch", attribute="color", value="blue"),
        ),
        "heard_beaker": (
            p("noise", 1, channel="audio", attribute="sound", value="glass broke"),
            p("infer", 1, evidence=Evidence.INFERRED, attribute="state", value="broken"),
            p("see", 1, channel="vision", attribute="state", value="intact"),
        ),
        "memory_dissent": (
            p("memory", 1, evidence=Evidence.REMEMBERED, attribute="state", value="open"),
            p("now", 1, attribute="state", value="closed"),
        ),
        "interoception_without_cause": (
            p("body", 1, channel="interoception", evidence=Evidence.INTEROCEPTIVE,
              attribute="affect", value="uneasy", hint="body"),
        ),
        "interoception_weak_attribution": (
            p("body", 1, channel="interoception", evidence=Evidence.INTEROCEPTIVE,
              attribute="affect", value="uneasy", hint="body",
              attributions=(Attribution("noise", 0.2),)),
        ),
    }
    results = {}
    for label, inputs in conditions.items():
        organ = Sensus(SensusConfig(expected_channels=("audio", "vision", "touch", "interoception")))
        scene = organ.step(1, inputs)
        all_claims = tuple(x for obj in scene.objects for x in obj.claims)
        results[label] = {
            "claims_in": len(inputs),
            "claims_out": len(all_claims),
            "all_claims_unchanged": _provenance_equal(inputs, scene),
            "conflicts": [asdict(x) for x in scene.conflicts],
            "absent_channels": list(scene.absent_channels),
            "attribution_values": [asdict(a) for x in all_claims for a in x.attributions],
        }
    return results


def run(seed: int = SEED, n_per_family: int = N_PER_FAMILY) -> dict:
    identity = run_identity(seed, n_per_family)
    provenance = run_provenance_and_conflicts()
    return {
        "battery_version": BATTERY_VERSION,
        "seed": seed,
        "n_per_family": n_per_family,
        "fixture_type": "constructed-symbolic",
        "scope": "standalone-engineer-plane",
        "identity": identity,
        "ambiguity": run_ambiguity(),
        "shift_proxy": run_shift(),
        "provenance": provenance,
        "not_run": {
            "E4_actual_cross_model": "Requires independently generated outputs from real models",
            "E6_scene_vs_raw": "Requires preregistered, information-matched downstream decisions",
            "external_integrations": "Prohibited during current isolated research phase",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--n-per-family", type=int, default=N_PER_FAMILY)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run(args.seed, args.n_per_family)
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    print(data)


if __name__ == "__main__":
    main()
