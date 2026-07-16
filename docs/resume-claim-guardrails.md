# Resume Claim Guardrails

Use this document to keep portfolio wording accurate as the project matures.

## Claims supportable after local validation

- Developed a public-ready synthetic enterprise AI reference implementation combining approved-knowledge retrieval, policy controls, human approval, Salesforce REST integration, evaluation gates, and tamper-evident audit events.
- Built deterministic golden-set and adversarial test suites covering workflow routing, approval boundaries, retrieval, prompt injection, secret requests, and destructive actions.
- Designed a framework-neutral Python/FastAPI architecture with optional LangGraph, MLflow, Spark/Databricks, vector-store, cloud, Docker, and Kubernetes extension paths.

Use **public-ready** or **developed locally** until the complete tree and CI evidence are actually published.

## Claims supportable after the complete public release is green

- Published a reproducible enterprise AI delivery lab with a green Python CI matrix, container build, versioned evaluation artifacts, and release provenance.
- Delivered a recruiter-accessible browser/API demo with traceable evidence linking claims to code, tests, and benchmark reports.

## Claims supportable only after Agentforce Developer Edition validation

- Built and validated a Salesforce Agentforce/REST workflow using synthetic Account, Case, Contact, and Knowledge records, prompt templates, approval-controlled actions, and deployment validation.
- Integrated Salesforce Agentforce SDK and MCP interfaces in a synthetic Developer Edition or Trailhead Playground environment.

Do not claim enterprise Agentforce production tenure from a public lab.

## Claims requiring additional evidence

Do not use these until the stated evidence exists:

- **Production-scale:** requires real load, reliability, monitoring, incident, and adoption evidence.
- **Enterprise deployed:** requires a real organization and verified deployment.
- **Databricks/Spark at scale:** requires a reproducible distributed workload and benchmark.
- **MLflow production monitoring:** requires tracked runs, trace/evaluation evidence, and monitoring output.
- **OpenTelemetry GenAI observability:** requires emitted spans and an inspectable trace backend.
- **TensorFlow/PyTorch/Hugging Face implementation:** requires substantive model code, tests, and results—not optional dependencies.
- **FedRAMP, DoD, NIST, SOC 2, or Salesforce compliant/certified:** requires formal assessment or certification beyond this repository.
