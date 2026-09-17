"""
Xero connector.

Responsibility: authenticate (via a stored, per-tenant refresh token),
refresh the access token, pull raw transaction/account data for the last
sync window, and return it in Xero's native shape. Do NOT map to the
standardized schema here — that belongs in transform/xero.py.

Key facts to keep in mind (see README.md for detail):
- Access tokens expire after 30 minutes.
- Refresh tokens are on a 60-day rolling window, renewed on every use — a
  daily job keeps the connection alive indefinitely as long as it runs at
  least once every 60 days.
"""


def refresh_access_token(tenant_id: str) -> str:
    """
    Use the tenant's stored refresh token (Key Vault) to obtain a new access
    token, and save the rotated refresh token back to Key Vault.

    Returns the new access token.
    """
    raise NotImplementedError


def pull_transactions(tenant_id: str, access_token: str, since: str) -> list[dict]:
    """
    Pull raw transactions from the Xero API since the given date.
    Returns Xero's native JSON shape — unmapped.
    """
    raise NotImplementedError


def pull_accounts(tenant_id: str, access_token: str) -> list[dict]:
    """
    Pull the tenant's chart of accounts in Xero's native shape.
    """
    raise NotImplementedError
