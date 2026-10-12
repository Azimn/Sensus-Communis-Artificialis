# CHANGELOG

## 2026-10-11 — Affectus prototype: interoceptive weather dynamics (branch `affectus-prototype`)

- New `sensus_artificialis/affectus.py`: slow modulatory layer generating
  the interoceptive signal — four dimensions (valence, arousal, security,
  fatigue), eight abstract driver kinds, per-driver habituation with
  recovery, superlinear opponent process (intense drive overshoots into
  relief/letdown; moderate drive fades on slow decay, half-life ~346
  ticks), seeded noise, snapshot/restore including the RNG stream.
- Speaks the existing `Percept`/`Attribution` types: felt reports are
  coarse quantizations (felt/actual gap by construction), attributions
  are uncertain candidates (wrong cause representable, empty = unknown),
  and binding through Sensus never upgrades the evidential class.
- Typed but unconsumed `Modulation` outputs (salience gain, exploration
  bias, rehearsal bias, decay multiplier) for future lateral adapters.
- Append-only receipts; deliberately **no reset method**.
- 12 new fitness-function tests (habituation, persistence, opponent dip,
  felt coarseness/misattribution, receipts, no-reset, binding
  non-upgrade, snapshot/restore, determinism): 36/36 green.
- Design notes in `docs/AFFECTUS_PROTOTYPE.md`: the six wants,
  anti-model-driven properties, jazz receipts, guardrails. Tinker-daily
  track, no freeze; Sensus integration still gated through 2026-10-23.

## 2026-10-10 — Docs: confirm the hard invariant (§3)

- Resolved the "missing Section 3" hedging in `docs/SPEC_v0.1.md` and
  `README.md`: the binding law is **no evidential-class amplification**
  (integration may bind, never upgrade; conflicting binds are vetoed and
  surfaced, never silently resolved). The implementation already enforces
  this; the contract tests demonstrate it.
- Clarified that the five implementation evidence classes
  (observed/reported/inferred/remembered/interoceptive) are a provisional
  refinement of the specified taxonomy, with the binding law applying across
  all of them.
- No code changes. 18/18 contract tests passing before and after.

## 2026-10-10 — v0.1 scaffold (ChatGPT)

- Standalone `sensus_artificialis` package: typed percepts, binding with
  per-constituent provenance, veto/uncertain conflict surfacing,
  Jaccard re-identification with ambiguity margin, bounded working memory
  (recent object files, explicitly not the Archive), absent-channel marking,
  interoceptive channel with attribution-uncertain affect support.
- 18-test contract battery, CI workflow, SPEC_v0.1.md, EXPERIMENTS_v0.1.md
  (E1–E6 incl. scene-vs-raw control).
