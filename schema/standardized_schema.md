# Standardized schema

This is the single schema every connector's transform step must map into.
The Power BI report, the Claude insights prompt, and Row-Level Security all
depend on this being identical for every tenant regardless of source
(QuickBooks, Xero, or CSV upload).

**Status: v1 — finalized.** The core tables and every open question from the
draft are resolved below. The one piece expected to grow over time is the
standardized category list and its mapping table — that's by design (see
"Standardized categories"), not a sign the schema itself is unfinished.

## Core tables

### `transactions`

| Column | Type | Notes |
|---|---|---|
| `tenant_id` | uuid | isolation key — present on every table, enforced via Row-Level Security |
| `transaction_id` | text | source's native ID, kept for traceability and idempotent re-sync |
| `date` | date | transaction date as reported by the source (not the sync date) |
| `amount` | decimal(18,2) | signed — see "Sign convention" below |
| `currency` | char(3) | ISO 4217 (e.g. `USD`, `GBP`). Defaults to the tenant's base currency. |
| `transaction_type` | text | `standard` | `refund` | `adjustment` | `transfer` — see "Refunds and adjustments" |
| `category` | text | standardized category — see "Standardized categories" |
| `source_category` | text | the raw, unmapped category string exactly as the source returned it |
| `source` | text | `quickbooks` | `xero` | `csv_upload` |
| `description` | text | raw memo/description from source |
| `account_id` | text | foreign key to `accounts.account_id` (scoped by `tenant_id`) |
| `synced_at` | timestamp | when this row was written by the orchestrator (audit trail, not the transaction date) |

### `accounts`

| Column | Type | Notes |
|---|---|---|
| `tenant_id` | uuid | |
| `account_id` | text | source's native account ID |
| `account_name` | text | |
| `account_type` | text | standardized: `asset` | `liability` | `equity` | `income` | `expense` |
| `currency` | char(3) | ISO 4217 |
| `is_active` | boolean | false for closed/archived accounts — keep the row for historical transactions, exclude from current-balance views |

### `category_mappings`

Global (not tenant-scoped) lookup table that drives the `category` column
above. Keeping it global rather than per-tenant means a mapping fix benefits
every tenant on the next sync, and new tenants aren't starting from zero.

| Column | Type | Notes |
|---|---|---|
| `source` | text | `quickbooks` | `xero` | `csv_upload` |
| `source_category` | text | raw category string as that source returns it |
| `standardized_category` | text | one of the values from "Standardized categories" below |
| `category_group` | text | `income` | `expense` | `transfer` — derived, kept denormalized for fast filtering |

If a `(source, source_category)` pair has no row here yet, the transform
layer should still write the transaction with `category = 'uncategorized'`
rather than failing the whole sync — see `transform/standardize.py`. Missing
mappings get logged so they can be filled in, per the incremental approach
the draft already recommended.

## Standardized categories

A fixed starting list, modeled on common SMB chart-of-accounts / Schedule-C
style groupings. Extend it by adding rows to `category_mappings`, not by
inventing new standardized categories per tenant — the whole point is one
shared list every Power BI report and insights prompt can rely on.

**Income**: `sales_revenue`, `service_revenue`, `other_income`

**Cost of goods sold**: `cogs`

**Expense**: `payroll`, `rent`, `utilities`, `insurance`, `marketing`,
`software_subscriptions`, `professional_services`, `travel`, `office_supplies`,
`equipment`, `taxes`, `bank_fees`, `other_expense`

**Transfer**: `owner_draw`, `internal_transfer`

**Fallback**: `uncategorized` — never a source of truth, always a queue of
mappings to fill in.

## Sign convention

`amount` is signed by its effect on the account balance it hit, matching how
a business owner reads a bank statement:

- **Positive** = money in (income, a refund received, a transfer in)
- **Negative** = money out (expense, a transfer out)

This applies uniformly across all three sources — each connector's transform
step is responsible for normalizing whatever sign convention the source API
uses natively into this one.

## Refunds and adjustments

Refunds and corrections are recorded as their **own transaction rows**, never
netted against the original transaction:

- A refund of an expense is a positive-amount row with
  `transaction_type = 'refund'` and the *same* `category` as the original
  expense (a refunded software subscription is still `software_subscriptions`,
  just reversed).
- A refund of income (e.g. a customer refund) is a negative-amount row,
  `transaction_type = 'refund'`, same category as the original sale.
- Bank/bookkeeping corrections not tied to a specific prior transaction use
  `transaction_type = 'adjustment'`.
- Money moved between the tenant's own connected accounts uses
  `transaction_type = 'transfer'` and `category` in (`owner_draw`,
  `internal_transfer`) as appropriate — this keeps transfers from inflating
  both income and expense totals on the dashboard.

Keeping refunds as separate rows (rather than mutating history) preserves the
audit trail back to the blob-storage bronze layer and matches how QuickBooks
and Xero both represent refunds natively.

## Multi-currency

Out of scope for v1 functionality (no cross-currency conversion or
consolidated multi-currency reporting), but the `currency` column is
included on both tables now so it doesn't require a schema migration later.
For v1: every tenant is assumed single-currency, `currency` is set from the
source's reported currency (or the tenant's configured base currency for CSV
upload, since a bank CSV rarely states one), and the Power BI report and
insights prompt treat all amounts as that one currency per tenant.

## Historical sync depth

First sync per tenant pulls **trailing 12 months**. Rationale: enough
history for meaningful trend commentary from `insights/`, without the API
load, rate-limit risk, and blob storage cost of pulling full history by
default. Every sync after the first is incremental (since last successful
sync). If a tenant specifically wants deeper history, that's a manual
one-off backfill, not the default path.

## Open questions — resolved

- ~~Sign convention for `amount`~~ → see "Sign convention" above.
- ~~How far back does the first sync pull~~ → trailing 12 months, see
  "Historical sync depth" above.
- ~~How are refunds / adjustments represented~~ → see "Refunds and
  adjustments" above.
- ~~Multi-currency handling~~ → deferred functionally, column reserved now,
  see "Multi-currency" above.
