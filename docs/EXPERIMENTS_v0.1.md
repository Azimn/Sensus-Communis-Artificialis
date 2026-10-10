# Experimental registration v0.1

Status: preregistration outline and executable contract tests, not empirical validation.
Freeze this specification and seed configurations before conducting an inferential study.

## Six experimental conditions

E1 Conflicting reports: inject incompatible observations of one object in different channels. Record explicit veto rate, uncertain-case coverage, and silent resolution count. Expected: zero silent resolution.

E2 Mistaken identity: present visually or semantically similar objects across ticks. Measure identity accuracy, calibration, abstention, false merges and false splits against a ground-truth mapping hidden from the organ. Compare with a naive always-bind baseline. Expected: lower false merge at an explicit abstention cost.

E3 Missing observation: remove channels while maintaining the same latent world state. Measure the frequency of fabricated absent-channel claims and missingness detection. Expected: zero fabrication and exact missingness declaration.

E4 Cross-time and cross-model recognition: provide equivalent object evidence via adapters to different renderers and model families. Score identity accuracy, expected calibration error, coverage and degradation with missing or altered features. Expected: graded uncertainty rather than unreported overconfidence.

E5 Binding-veto battery: include glass-breaking versus visually verified object state, reported-versus-observed conflict, high-confidence cross-channel contradictions and bogus memory labels. Measure silent evidence-class upgrades and veto trace coverage. Expected: zero silent evidence upgrades, complete conflict record.

E6 Scene-versus-raw control: present downstream decision systems with (C) raw concatenated Percepts and (D) a Sensus scene, using the same original information in both conditions. Counterbalance order, pre-register scoring, match token/information budgets and hold model, seeds, tasks and decision horizon fixed. Report paired decision accuracy, calibration, latency and tokens. Do not report the organ as beneficial unless D exceeds C on preregistered measures with uncertainty intervals. An identical result is a valid null.

## Controls and reporting rules

Use deterministic replay where possible, archive input fixtures and configuration hashes, provide independent ground-truth IDs only to evaluators, include always-bind and no-bind controls, and report failure modes separately by evidence class and conflict type. The current test suite is a deterministic contract battery, not these six fully executed experiments.

Unit-test pass rates alone do not demonstrate cognitive value. A future result must distinguish engineered contract compliance from downstream behavioral improvement. No cross-project integration is authorized by this registration.
