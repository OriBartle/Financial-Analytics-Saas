# Financial Analytics for SMBs

Automated financial analytics platform for small/medium businesses. Connects to
QuickBooks, Xero, or a manually uploaded bank CSV, transforms the data into a
single standardized schema, and serves it to a shared Power BI dashboard —
plus a written, plain-English summary of what the numbers mean, generated via
the Claude API.

## How it works

```
 QuickBooks ──┐
 Xero ────────┼──► connectors/  ──► transform/ ──► Azure SQL (standardized) ──► Power BI
 CSV upload ──┘         │                              │
                         ▼                              ▼
                  Azure Blob (raw/audit)          insights/ (Claude API)
                                                          │
                                                          ▼
                                                  written insights, stored
                                                  alongside the dashboard
```

Runs once a day, unattended, via a timer-triggered Azure Function. No user
login or re-authentication required on a daily basis — see
[Token Refresh Strategy](#token-refresh-strategy) below.

## Repo structure

- `connectors/` — one folder per data source. Each connector's only job is to
  authenticate (via a stored refresh token), pull raw data, and hand back
  whatever shape that source naturally returns. Source-specific mess stays
  contained here.
  - `quickbooks/` — QuickBooks Online API connector
  - `xero/` — Xero API connector
  - `csv_upload/` — parses and validates a manually uploaded bank CSV
- `transform/` — maps each connector's raw output into the single
  **standardized schema** (see `schema/standardized_schema.md`). This is the
  most important code in the repo — everything downstream depends on it being
  correct and consistent regardless of source.
- `orchestrator/` — the daily job. Loops over tenants, calls the right
  connector + transform, writes to Azure SQL, triggers the Power BI refresh.
- `insights/` — Claude API prompt templates and the call that turns a
  tenant's standardized data into plain-English commentary and suggested
  actions.
- `schema/` — documentation of the standardized table schema. Source of
  truth for what "standardized" means.
- `tests/` — unit tests, especially for the transform layer.

## Data flow / storage

- **Raw / bronze layer** — Azure Blob Storage (ADLS Gen2). One container,
  folder-per-tenant-per-source, e.g. `/tenant123/quickbooks/2026-09-17.json`.
  Kept for audit trail and reprocessing if a transform bug is found later.
- **Standardized / gold layer** — Azure SQL Database (serverless tier).
  Single table (or small set of tables) with a `tenant_id` column and Row-Level
  Security enforcing per-tenant isolation. Power BI connects here directly.
- **Secrets** — Azure Key Vault. One refresh token secret per tenant per
  source. Never stored in the SQL database or in the repo.

## Token refresh strategy

Business owners authenticate once via OAuth. We store the refresh token
(Key Vault) and use it, unattended, each morning to mint a new access token:

- **QuickBooks**: access tokens last 60 minutes; refresh tokens rotate every
  ~24–26 hours, so the orchestrator must save the *new* refresh token back to
  Key Vault every single run, or the connection breaks silently within a
  couple of days. A reconnect flow (email/notification on refresh failure) is
  required, not optional — Intuit now requires apps to provide one.
- **Xero**: refresh tokens are on a 60-day rolling window, renewed on every
  use — a daily job keeps the connection alive indefinitely.

## Power BI

One shared report template, filtered per tenant via Row-Level Security on the
SQL database. No per-client report building. Dataset refresh is triggered via
the Power BI REST API right after the orchestrator finishes writing, so the
dashboard can't be stale relative to the data.

## Status

Early build. See `PROJECT_INSTRUCTIONS.md` for context if you're picking this
up in a Cowork project.
