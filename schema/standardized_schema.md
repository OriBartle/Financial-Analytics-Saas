# Standardized schema

This is the single schema every connector's transform step must map into.
The Power BI report, the Claude insights prompt, and Row-Level Security all
depend on this being identical for every tenant regardless of source
(QuickBooks, Xero, or CSV upload).

**Status: draft — not yet finalized.** Fill this in before building any
connector's transform logic, since every connector will be mapped against
whatever is defined here.

## Proposed core tables

### `transactions`

| Column | Type | Notes |
|---|---|---|
| `tenant_id` | uuid | isolation key — present on every table |
| `transaction_id` | text | source's native ID, kept for traceability |
| `date` | date | |
| `amount` | decimal | positive = income, negative = expense (TBD — confirm convention) |
| `category` | text | mapped to a standardized category list (TBD below) |
| `source` | text | `quickbooks` \| `xero` \| `csv_upload` |
| `description` | text | raw memo/description from source |
| `account` | text | which account the transaction hit |

### `accounts`

| Column | Type | Notes |
|---|---|---|
| `tenant_id` | uuid | |
| `account_id` | text | |
| `account_name` | text | |
| `account_type` | text | standardized: asset / liability / equity / income / expense |

## Standardized category list

TBD — needs a mapping table from QuickBooks categories and Xero categories
into one shared list. This is the trickiest part of the whole project (per
earlier discussion) since QuickBooks and Xero use different chart-of-accounts
conventions. Recommend building this mapping table incrementally as real
tenant data is seen, rather than trying to anticipate every category upfront.

## Open questions

- Sign convention for `amount` (positive/negative for income/expense)?
- How far back does the first sync pull (all history vs. last N months)?
- How are refunds / adjustments represented?
- Multi-currency handling, if any tenant needs it?
