"""
Daily orchestrator — the entry point for the timer-triggered Azure Function
that runs once each morning.

For every tenant:
  1. Determine their connected source (quickbooks / xero / csv_upload).
  2. Refresh the access token (connectors/<source>/client.py).
  3. Pull raw data since the last successful sync.
  4. Land the raw payload in Azure Blob Storage (bronze layer) for audit.
  5. Standardize it (transform/standardize.py).
  6. Write standardized rows to Azure SQL (gold layer), scoped by tenant_id.
  7. Trigger the Power BI dataset refresh via the REST API.
  8. Call insights/generate.py to produce this tenant's written summary.

Failures for one tenant must not block the rest of the run — log and
continue, then surface a summary of failures at the end (e.g. tenants
needing reconnect).
"""


def run_for_tenant(tenant_id: str) -> None:
    """
    Runs the full daily pipeline for a single tenant. Raises a specific,
    catchable exception on reconnect-required failures so the caller can
    trigger the tenant's reconnect notification rather than retrying blindly.
    """
    raise NotImplementedError


def run_daily() -> None:
    """
    Entry point — loops over all active tenants and calls run_for_tenant.
    This is what the Azure Function timer trigger calls.
    """
    raise NotImplementedError
