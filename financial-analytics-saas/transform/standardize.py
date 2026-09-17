"""
Transform layer — maps each connector's raw output into the standardized
schema defined in schema/standardized_schema.md.

This is the most important code in the repo. Everything downstream (Power
BI report, Claude insights prompt, Row-Level Security) depends on every
tenant's data landing in exactly the same shape regardless of source.

One mapping function per source. Keep source-specific quirks (category
naming, sign conventions, pagination artifacts) contained here — do not let
them leak into orchestrator/ or insights/.
"""


def standardize_quickbooks(raw_transactions: list[dict], raw_accounts: list[dict], tenant_id: str) -> list[dict]:
    """
    Map QuickBooks' native transaction/account shape into the standardized
    schema. See schema/standardized_schema.md for the target shape.
    """
    raise NotImplementedError


def standardize_xero(raw_transactions: list[dict], raw_accounts: list[dict], tenant_id: str) -> list[dict]:
    """
    Map Xero's native transaction/account shape into the standardized
    schema.
    """
    raise NotImplementedError


def standardize_csv(raw_transactions: list[dict], tenant_id: str) -> list[dict]:
    """
    Map parsed bank CSV rows into the standardized schema. No account/
    category data will typically be available from a raw bank CSV, so
    category mapping here will likely rely on description-based heuristics
    or a manual confirmation step.
    """
    raise NotImplementedError
