"""
QuickBooks Online connector.

Responsibility: authenticate (via a stored, per-tenant refresh token),
refresh the access token, pull raw transaction/account data for the last
sync window, and return it in QuickBooks' native shape. Do NOT map to the
standardized schema here — that belongs in transform/quickbooks.py.

Key facts to keep in mind (see README.md for detail):
- Access tokens expire after 60 minutes.
- Refresh tokens rotate every ~24-26 hours — the new refresh token returned
  by every refresh call MUST be saved back to Key Vault immediately, or the
  connection silently breaks days later.
- If refresh fails (invalid_grant), trigger the tenant's reconnect flow
  rather than retrying — the old token is not recoverable.
"""


def refresh_access_token(tenant_id: str) -> str:
    """
    Use the tenant's stored refresh token (Key Vault) to obtain a new access
    token. Must save the newly-rotated refresh token back to Key Vault as
    part of this call.

    Returns the new access token.
    """
    raise NotImplementedError


def pull_transactions(tenant_id: str, access_token: str, since: str) -> list[dict]:
    """
    Pull raw transactions from the QuickBooks API since the given date.
    Returns QuickBooks' native JSON shape — unmapped.
    """
    raise NotImplementedError


def pull_accounts(tenant_id: str, access_token: str) -> list[dict]:
    """
    Pull the tenant's chart of accounts in QuickBooks' native shape.
    """
    raise NotImplementedError
