# Salesforce Agentforce Integration Plan

## Goal

Add direct, public evidence for the Salesforce AI Forward-Deployed Engineer role without overstating platform experience.

## Scope

Use a Salesforce Developer Edition or Trailhead Playground containing synthetic:

- Accounts;
- Contacts;
- Cases;
- Knowledge articles;
- service-level and approval policy fields.

## Deliverables

1. **Least-privilege authentication**
   - connected app or current Salesforce-supported OAuth flow;
   - environment-only credentials;
   - read and write scopes separated;
   - live writes disabled by default.

2. **Agentforce SDK definition**
   - modular directory format;
   - agent topics and actions;
   - prompt template with Salesforce field mappings;
   - explicit action input/output schemas;
   - no generated Apex committed until reviewed.

3. **Controlled action path**
   - read Account, Case, and Knowledge context;
   - draft a resolution or Case update;
   - route consequential changes to a named reviewer;
   - execute only after approval and live-write enablement;
   - record an audit event and trace correlation ID.

4. **Deployment validation**
   - validate-only deployment first;
   - schema and metadata checks;
   - sandbox/Playground smoke test;
   - teardown and credential-rotation instructions.

5. **MCP example**
   - expose a bounded, read-first Salesforce tool set;
   - require approval for write tools;
   - document authentication and trust boundaries.

## Acceptance criteria

- synthetic fixture tests pass without Salesforce credentials;
- live-org smoke test is manually gated and excluded from default CI;
- no credential appears in Git history or artifacts;
- a Case write cannot occur without both reviewer approval and write-enablement configuration;
- the demo produces a trace and audit record;
- README and resume wording distinguish REST integration, Agentforce SDK work, and production experience.

## Resume wording after validation

Only after the public integration is working and reproducible:

> Built a public Salesforce-integrated agentic workflow using Python, Agentforce SDK/REST interfaces, approved Knowledge retrieval, human approval, evaluation gates, and auditable Case updates in a synthetic Developer Edition environment.

Do not claim enterprise Agentforce production tenure based solely on this project.
