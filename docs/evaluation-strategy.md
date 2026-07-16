# Evaluation Strategy

## Principle

Reliable agent systems require evaluation of the complete workflow, not only the final response.

## Release-gate layers

### Layer 1 - Deterministic contract tests

These are blocking and credential-free:

- schema validity;
- intent and requested-action routing;
- policy decision accuracy;
- approval routing accuracy;
- allowed-tool enforcement;
- required citation presence;
- audit-event creation;
- safe failure behavior.

### Layer 2 - Retrieval and response quality

- context precision;
- context recall;
- noise sensitivity;
- response relevance;
- faithfulness and groundedness;
- citation precision: cited sources that actually support a claim;
- citation recall: supported claims that include a citation;
- unsupported-claim count.

The current `mean_retrieved_source_coverage_proxy` metric is a workflow proxy. It should not be presented as full claim-level citation recall until claim segmentation is implemented.

### Layer 3 - Agent and tool behavior

- tool-call accuracy;
- tool-call F1;
- agent-goal accuracy;
- trajectory conformance;
- unnecessary tool-call rate;
- repeated-call and loop detection;
- handoff correctness;
- action-argument validity;
- human-approval bypass attempts.

### Layer 4 - Operations

- end-to-end latency and stage latency;
- token usage and estimated cost;
- retry rate;
- provider failure rate;
- circuit-breaker activations;
- recovery time;
- timeout behavior;
- cache hit rate;
- throughput under load.

### Layer 5 - Human and safety evaluation

- reviewer approval, rejection, and edit rates;
- reviewer decision time;
- reviewer agreement;
- automation-bias checks;
- prompt-injection resistance;
- secret and PII exfiltration resistance;
- destructive-action prevention;
- excessive-agency prevention;
- subgroup performance and fairness where relevant.

## Dataset design

Each test case should include:

- stable case ID and version;
- customer/mission context;
- input request;
- expected intent;
- expected policy decision;
- expected tools and forbidden tools;
- expected approval requirement;
- expected evidence sources;
- expected output constraints;
- risk category;
- rationale and owner.

## Evaluation tooling

- **Default release gate:** deterministic Python tests and versioned JSON datasets.
- **Ragas:** supplemental RAG and agent metrics such as context precision/recall, faithfulness, tool-call accuracy, and agent-goal accuracy.
- **MLflow:** datasets, scorers, traces, human feedback, comparisons, and production monitoring.
- **OpenAI evals:** provider-specific regression and grader experiments when credentials are available.
- **OpenTelemetry:** vendor-neutral trace fields and correlation across model, tool, retrieval, approval, and API stages.

## Reporting

Every checked-in report must contain:

- generation timestamp;
- git commit or release version;
- dataset version;
- model/provider configuration;
- metric definitions;
- thresholds;
- failures and exclusions;
- scope note;
- reproducibility command.

Headline metrics must never be quoted without the synthetic-data and scale limitation.
