# Standalone constructed-symbolic battery v0.1

**Status:** executable synthetic demonstration; no external model, downstream decision task, real sensor, or cross-project integration.

Run:

    python -m unittest discover -s tests -v
    python -m experiments.standalone_battery --output standalone_battery.json

CI writes an inspectable JSON artifact tied to its GitHub commit. The benchmark consists of fixed input families, shuffled by a fixed seed (20261010). The evaluator sees the truth labels; the organ receives only two shell-shaped Percepts on separate ticks. Neither `truth_same` nor `family` is included in a percept. The output describes source trace preservation and re-identification, with elementary always-same and always-different comparators.

The **stable** family repeats all features for the same object. **Distinct** changes its unique feature for a different object. **Occluded** drops the mark from the same object while preserving two shared attributes. **Collision** intentionally gives a different object the identical signature. The collision condition cannot be solved by Jaccard matching without additional observations or a prior rejection policy. Reporting its failure is more informative than claiming perfect object continuity. Under the existing core semantics, the `distinct` case retains a weak positive candidate (Jaccard 0.5) and is marked `ambiguous`, not `new`. That is an abstention, not a correct different-object answer.

Each family has 40 cases by default. The current heuristic correctly handles stable and occluded cases, abstains on distinct replacements and falsely merges indistinguishable collisions. This predicts 80/160 correct, 40/160 abstentions and 40/160 false merges, when abstention counts as incorrect. Both unconditional always-same and always-different baselines score 80/160 on this deliberately balanced family mix. **The 0.50 aggregate accuracy is a control-equivalent null, not evidence of an advantage.** These are deterministic expectations encoded into fixtures, not independently measured generalization. Report family-specific rates, total and covered-case accuracy, false merges, false splits and abstentions. Similarity is **not** a calibrated probability; no Brier score or calibration claim is justified.

A separate ambiguous-twins probe expects abstention rather than forced identification. A representation-shift proxy compares unchanged, partial and renamed symbolic features. The renamed condition typically fails as a new object rather than explicitly declaring uncertainty; this is an open design weakness. This is not an actual cross-model test.

E1/E3/E5 fixtures cover high-confidence contradictory channels, heard beaker noise plus inferred breakage, disagreement between stored and current reading, absent expected channels, interoceptive unease without a cause, and optional low-confidence candidate attribution. Preserving original Percept objects is tested. These fixtures confirm software contract behavior, not trusted source identity.

**E6 is not run.** It requires a genuinely downstream pre-registered decision task, token- and information-matched scene/raw conditions, blinded scoring and uncertainty intervals. Do not cite this toy battery as evidence that scenes improve thinking, embodiment, subjective experience or behavior. Actual cross-model E4 is also not run.

No dependency on Synthetic Ipseity, Pretorius or other cognitive projects is introduced. Adoption sequence is recorded separately in docs/ADOPTION_GATES.md.
