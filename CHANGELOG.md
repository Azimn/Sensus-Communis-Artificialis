# CHANGELOG

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
