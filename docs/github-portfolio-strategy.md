# GitHub Portfolio and Discoverability Strategy

## Profile surface

Create a public repository named `silasj1022/silasj1022` with a root `README.md`. GitHub displays that README on the profile when the repository name matches the username, it is public, and the README has content.

The profile README should contain:

- one-sentence positioning statement;
- target domains: forward-deployed AI, enterprise data platforms, responsible AI, and federal modernization;
- a featured-project section;
- architecture and evaluation specialties;
- links to LinkedIn, resume, and the live demo;
- a short "currently building" section that distinguishes active work from completed releases.

Pin this repository as the first item. GitHub supports up to six pinned repositories and gists combined.

## Repository metadata

Recommended description:

> Auditable enterprise AI workflow with RAG, Salesforce integration, human approval, evaluation, red-team testing, and production delivery patterns.

Recommended topics:

- `agentic-ai`
- `forward-deployed-engineering`
- `salesforce`
- `agentforce`
- `rag`
- `human-in-the-loop`
- `llm-evaluation`
- `responsible-ai`
- `ai-governance`
- `fastapi`
- `langgraph`
- `openai-agents`
- `microsoft-agent-framework`
- `mlflow`
- `nist-ai-rmf`
- `python`

Keep the list focused; GitHub permits up to 20 topics.

## Recruiter presentation

The top of the README should answer, without scrolling far:

1. What customer problem does this solve?
2. What can a reviewer run without credentials?
3. What is implemented versus planned?
4. What evidence exists?
5. Where is the architecture and demo?

Add:

- a 90-second demo video or GIF;
- a static social-preview image;
- a green CI badge only after the workflow runs successfully;
- a release badge only after a tagged release exists;
- a concise architecture image;
- an "evidence, not claims" table.

## Reproducibility

- Dev Container and Codespaces support.
- `make install verify-repo lint typecheck test evaluate red-team`.
- a tagged `v1.0.0` release only after the release-candidate CI and security checks are green;
- generated release notes;
- release artifacts containing evaluation reports;
- resolved CycloneDX SBOM, SHA256 checksums, clean-install tests, and artifact provenance for distributions.

## Research visibility

Use GitHub Releases and `CITATION.cff` for stable references. Publish architecture notes under `docs/research/` and link them from the profile README. Each paper or benchmark should identify its version, dataset, method, limitations, and corresponding code release.

## Ready-to-use assets

- Repository settings: `docs/repository-settings-checklist.md`
- Profile README draft: `docs/profile-readme-draft.md`
- Evidence map: `docs/evidence-index.md`
- Release validation: `docs/validation-report.md`
- Publication process: `docs/publishing.md`
