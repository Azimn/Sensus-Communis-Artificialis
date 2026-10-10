# Sensus Artificialis: provisional technical contract v0.1

Status: standalone prototype, 2026-10-10.
Canonical home: Azimn/Sensus-Communis-Artificialis.
Formal philosophical designation: Sensus Communis Artificialis.

## Scope and source fidelity

This document operationalizes only the source excerpt supplied to the implementation session, covering upstream/downstream/lateral boundaries, state, interoception, five core operations, six experiments, nonclaims and intended integrations. The excerpt references an unavailable Section 3. Its exact evidential taxonomy and binding law remain UNVERIFIED. The implementation uses conservative, explicit provisional classes and never treats them as a recovery of that missing text.

## Authority and contracts

Upstream: receives already typed and trust-bounded percepts, never raw sensor feeds. Validation of class and shape is a local interface check, not source authentication or sensor normalization. The perception shell, potentially Eidolon's Witchglass, owns trust adjudication. A bogus but well-typed high-confidence percept remains an upstream failure and cannot be detected by Sensus.

Downstream: scene emission creates only a candidate, not admitted first-person experience. Synthetic Ipseity owns access arbitration and the subject boundary. Nothing in Scene carries an admission boolean.

Lateral: Daemonium may supply already regulated weights as confidence-bearing percept values through a future typed adapter. Sensus does not run gain regulation. Archive/Mnemosyne may return typed mnemonic references on explicit request through a future adapter. Sensus does not request or own autobiographical storage.

## Current provisional evidence classes

observed: a direct channel claim; reported: another source's claim; inferred: a proposition derived from other evidence; remembered: a retrieved memory claim; interoceptive: a body-signal claim. These categories are deliberately not interchangeable and remain attached to their original Percept. This set is only provisional until the original Section 3 is inspected.

Each Percept carries event_id, channel, evidence class, source_ref, tick, attribute, value, confidence, optional per-tick object_hint, optional immutable feature signature, and optional interoceptive cause attributions. No metadata source is promoted to truth by binding. Hints only group inputs within one tick and are not persistent object identities. No cross-tick identity is established without feature evidence.

## Binding, veto and re-identification

Within a tick, percepts sharing a shell-supplied object_hint are associated without losing individual provenance. Disagreements about one attribute always produce an explicit Conflict and contested attribute. Contradictory high-confidence observed values produce vetoed; lower-confidence or cross-class disagreements produce uncertain. Neither is silently resolved and neither discards competing claims. A veto is a refusal to produce a single authoritative fused value, not a refusal to record the conflicting evidence.

Across ticks, feature signatures are compared using Jaccard similarity with configured threshold and ambiguity margin. A unique high-scoring match reuses the previous short-lived file ID. Ties or subthreshold matches produce a fresh object file and expose candidate scores; there is no forced identity resolution. These simple heuristics are inspectable baselines, not validated perceptual algorithms.

Expected-but-unseen channels are named in absent_channels. Channel silence never creates a percept or an inferred object property.

An interoceptive claim preserves the body's reported qualitative state and separately typed uncertain candidate cause attributions. Zero attributions means unknown cause. Sensus neither manufactures an explanatory narrative nor claims to know what the subject feels.

## Bounded state

Sensus stores only current-scene computation plus recent ObjectFile signatures and timestamps, configured by recent_window and max_object_files. Old files expire. Sensus provides no archive, semantic autobiographical memory, persistence database or subject-owned historical facts. Code may be restarted with empty working memory.

## Scene contract

Scene(schema_version, tick, objects, conflicts, absent_channels) is frozen and contains frozen nested records. Every scene object retains full source Percept records and contested_attributes. reidentified_from is an uncertain operational continuity link, never a metaphysical identity claim. The scene structure is an engineer-visible candidate only, not a finalized Ipseity interface.

Interface version: sensus.scene.v0.1. Any external adoption requires a separate, reviewed and versioned adapter and explicit opt-in. No integration is authorized in this scaffold.

## Nonclaims

No claim about consciousness, sentience, subjective experience, a solution to the neuroscientific binding problem, or biological fidelity. Unit tests evaluate software contracts, not downstream decision improvements.

## Known limitations

The excerpt's Sections 1 to 3 are absent. The current implementation assumes a total ordering of integer ticks and text-valued attributes. It uses no trust inference, no time-alignment algorithm, no probabilistic calibration, no attention control, no language model, no world-authority writes and no persistence across restarts. Its semantic evidence categories and exact conflict tolerance must be ratified after review of the complete original specification.
