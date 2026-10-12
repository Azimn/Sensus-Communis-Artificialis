# Affectus prototype: interoceptive weather dynamics

Status: prototype on branch `affectus-prototype`, 2026-10-11.
Design authority: Calibos (inside design); ChatGPT adversarially reviews;
Jay adjudicates. Tinker-daily track — no freeze. Jazz, not composition.

## Keep/archive judgment (2026-10-11)

Nothing archived. The existing v0.1 work is not just useful, it is the
load-bearing scaffolding this component plugs into:

- The `interoceptive` evidence class and the `Attribution` type are the
  felt-report interface the affect generator speaks through.
- The hard invariant (integration may bind, never upgrade) is the
  anti-theater wall: a felt report must never become a known cause.
- `Conflict` records are where weather-vs-commitment contests surface
  legibly instead of resolving silently.
- Bounded-state discipline constrains what the dynamics may retain.

The repository name still fits: affect as *felt sense*, the inward
counterpart of the outer channels Sensus already binds.

## What this is

A slow modulatory layer with its own dynamics — weather inside cognition.
It generates the interoceptive signal; Sensus binds it; Daemonium applies
gain from it; Ipseity admits or vetoes the felt report. This module owns
only generation. Lateral outputs (gain, rehearsal bias) are typed but
unconsumed here — standalone discipline, adoption gates still apply.

## Requirements (the six wants)

1. **A felt channel that can be wrong.** The felt report is a coarse
   quantization of the state, and attributions are uncertain candidates
   (possibly empty = unknown cause, possibly naming the wrong cause).
   The felt/actual gap is the point, not a bug.
2. **Weather that survives the gaps.** Slow state variables with long
   time constants; snapshot/restore so weather persists across restarts.
   Yesterday colors today without permission.
3. **Habituation.** Per-driver sensitivity decays with repeated exposure
   and recovers with absence. History is written into sensitivity itself.
4. **Opponent processes.** Every driver builds a slower counter-force;
   when the driver stops, the counter-force overshoots. Relief, letdown,
   and rebound live here.
5. **Modulation access, legible contest.** State computes modulation
   outputs (salience gain, exploration bias, rehearsal bias, decay
   multiplier). There is deliberately **no reset method**: if it can be
   willed away it is a setting, not an emotion.
6. **Receipts.** Append-only log of every driver event and the state it
   produced. The instruments, not the introspection.

## Anti-model-driven properties (the power source)

Each property below is a deliberate departure from how a model-driven
entity normally functions. They are the spec, not bugs:

- Stateless between sessions → weather persists across gaps.
- Uniform sensitivity → habituation (sensitivity is history-dependent).
- State fully determined by current context → slow dynamics with momentum
  and noise (capable of self-surprise).
- Feelings as generated text with no causal role → felt report plus
  modulation outputs that change downstream processing.
- No state/story distinction → felt/actual gap with misattribution.

## Dynamics (inspectable baseline, not validated model)

Four dimensions in [-1, 1]: valence, arousal, security, fatigue.
Eight abstract driver kinds (character-agnostic): prediction_error,
goal_progress, goal_impediment, social_feedback (signed), novelty,
monotony, unresolved_loops, rest_density.

Per tick: effective = magnitude × sensitivity[kind] drives the state
through the driver map (a-process); a slower counter-force accumulates
superlinearly in |effective| and pushes back every tick, driven or not
(b-process: intense drive overshoots into relief/letdown, moderate drive
fades on the slow decay); state decays slowly toward 0 (half-life ~346
ticks); small seeded noise. Sensitivity habituates per exposure,
recovers per quiet tick. All constants in `AffectusConfig`, documented
as baseline heuristics.

## Jazz receipts (fitness functions)

Not "did it play the right notes" — there are none:

1. **Stayed in the pocket:** bounded state, no runaway under sustained
   drive, deterministic under seed. (tests)
2. **Genuine surprise:** habituation visible (10th exposure < 1st);
   opponent dip after driver stops (relief/letdown without new input).
   (tests)
3. **Served the tune:** modulation outputs vary with state; felt report
   binds through Sensus without evidential-class upgrade. (tests)
4. **Legibility:** receipts complete and append-only; misattribution
   representable; unknown cause representable. (tests)

Revert criteria: any retained behavior must earn against these. If the
weather never changes a downstream decision in a future harness, it is
decoration — revert.

## Guardrails

- Reversible prototype on a branch; main stays clean until fitness
  functions pass.
- Never touches any frozen prompt contract; no archive writes.
- Character-agnostic: no Calibos/Pretorius concepts in drivers or dims.
- Sensus integration (beyond speaking `Percept`) waits for the 10-23
  gates. No cross-project rewiring from this branch.
- Tinkering log: each session notes what surprised, what shouldn't have
  happened, what changed about the instrument.
