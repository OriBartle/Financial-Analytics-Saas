# Project instructions

Paste this into the Cowork project's "Instructions" field (or keep it here
and reference it) so every task in this project starts with the same
context.

## What this project is

Automated financial analytics for SMBs. Business owner connects QuickBooks,
Xero, or uploads a bank CSV. Data is pulled once a day, transformed into a
single standardized schema, and served to a shared Power BI dashboard, plus
a plain-English summary generated via the Claude API (e.g. "sales are
trending up, consider increasing stock or raising prices").

Full architecture and repo layout: see `README.md`. Standardized schema
definition: see `schema/standardized_schema.md`.

## Ground rules for working in this repo

- **The standardized schema is the contract.** Any change to
  `schema/standardized_schema.md` must be reflected in every connector's
  transform logic in `transform/`, and flagged clearly — it affects the
  shared Power BI report for every tenant.
- **Connectors stay dumb.** Source-specific logic (QuickBooks vs Xero
  category structures, auth quirks, pagination, etc.) belongs entirely inside
  that connector's folder. Nothing source-specific should leak into
  `transform/` or `orchestrator/`.
- **Refresh tokens are rotated and re-stored on every run** for QuickBooks in
  particular — never assume a token is still valid after one use. See the
  Token Refresh Strategy section in `README.md`.
- **Never commit secrets.** Refresh tokens, client secrets, and connection
  strings belong in Key Vault / `.env` (gitignored), referenced by
  `tenant_id`, never hardcoded or logged.
- **tenant_id is the isolation boundary.** Every table, every query, every
  Key Vault secret is scoped by tenant. Treat cross-tenant data leakage as a
  critical bug, not a style issue.
- **Prefer small, testable functions** in `transform/`, especially the
  category/account mapping logic — this is the part most likely to need
  correction as we onboard real QuickBooks/Xero accounts with messy data.

## Current state / next steps

Update this section as work progresses, so a new task picking up this
project has an accurate starting point.

- [ ] Define `schema/standardized_schema.md` in full
- [ ] Build QuickBooks connector (auth + refresh + pull)
- [ ] Build Xero connector (auth + refresh + pull)
- [ ] Build CSV upload connector
- [ ] Build transform layer for each source
- [ ] Build orchestrator (daily loop, Azure Function timer trigger)
- [ ] Build insights module (Claude API call + prompt)
- [ ] Wire up Power BI shared report + RLS
- [ ] GDPR pass: retention policy, deletion flow, DPA

## Useful starting prompt

When starting a fresh task in this project, a good opener is:

> Read README.md, PROJECT_INSTRUCTIONS.md, and schema/standardized_schema.md.
> Then [describe the specific task]. Flag anything in the existing code that
> conflicts with the standardized schema before making changes.
