# Publishing Guide

The project belongs in the dedicated public repository `silasj1022/forward-deployed-ai-lab`. Do not embed it in an unrelated repository or preserve unrelated project history.

## Clean publication path

From a clean extraction of the release package:

```bash
git init
git branch -M main
git add .
git commit -m "Publish forward-deployed AI lab v0.4.0 research baseline"
git remote add origin git@github.com:silasj1022/forward-deployed-ai-lab.git
git push -u origin main
```

When the remote repository already has an initialization commit, reconcile deliberately rather than force-pushing without review. Confirm the intended history and inspect the remote tree before replacing any branch reference.

## Required validation before describing the project on a resume

1. Confirm `.env`, credentials, real records, and private architecture are absent.
2. Run `make validate` and `make build` from a fresh virtual environment.
3. Confirm `pyproject.toml`, `requirements.txt`, `src/`, `tests/`, `data/`, `docs/`, and workflows are retrievable on GitHub.
4. Confirm GitHub Actions is green across the Python matrix.
5. Inspect the uploaded evaluation, red-team, and coverage artifacts.
6. Confirm the container-build job passes.
7. Create the `v0.4.0` release and verify the distribution provenance attestation.
8. Apply the settings in `docs/repository-settings-checklist.md`.

## GitHub portfolio path

- Create the public profile README repository `silasj1022/silasj1022`.
- Use `docs/profile-readme-draft.md` as the starting copy.
- Pin `forward-deployed-ai-lab` first.
- Add the focused repository topics from `docs/github-portfolio-strategy.md`.
- Add a social-preview image and 90-second demo after the UI and architecture are final.

## Replit path

Import the complete GitHub repository into Replit. Keep the deterministic provider for the public demo. Add any provider or Salesforce credentials only through Replit Secrets, never through committed files.

## Recommended public links

After release verification, link directly to:

- `docs/recruiter-guide.md`
- `docs/evidence-index.md`
- `docs/case-study-salesforce.md`
- `docs/case-study-vtg.md`
- `docs/system-card.md`
- `docs/validation-report.md`
- the tagged GitHub release

Never publish employer data, student data, government data, real Salesforce tokens, internal architecture, or sensitive security findings.
