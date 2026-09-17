"""
Bank CSV upload connector.

Responsibility: parse and validate a manually uploaded bank CSV, and return
it in a consistent "raw" shape (not yet the standardized schema — that
mapping belongs in transform/csv_upload.py). Since bank CSV formats vary
wildly by bank, this will likely need per-bank format detection or a
column-mapping step the business owner confirms on upload.
"""


def parse_csv(tenant_id: str, file_path: str) -> list[dict]:
    """
    Parse an uploaded bank CSV into a list of raw transaction dicts.
    Validates required columns are present (date, amount, description at
    minimum) and raises a clear error if the format isn't recognized.
    """
    raise NotImplementedError


def detect_bank_format(file_path: str) -> str | None:
    """
    Best-effort detection of which bank's export format this CSV matches,
    based on header row / column order. Returns None if unrecognized, in
    which case the business owner should be prompted to map columns
    manually.
    """
    raise NotImplementedError
