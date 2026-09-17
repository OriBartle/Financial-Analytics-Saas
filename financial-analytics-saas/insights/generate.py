"""
Insights module — calls the Claude API over a tenant's freshly standardized
data to produce plain-English commentary and suggested actions
(e.g. "sales are trending up, consider increasing stock or raising prices").

Runs once per tenant per daily refresh, right after the standardized data
lands in Azure SQL. Output is stored alongside the data (not regenerated on
every dashboard view) so it doesn't need to be regenerated until the next
morning's refresh.
"""

PROMPT_TEMPLATE = """
You are a financial analyst producing a short, plain-English summary for a
small business owner. You will be given their standardized transaction and
account data for the recent period.

Write 2-4 short observations, each pairing a concrete finding with a
concrete, specific suggested action. Avoid generic advice — ground every
suggestion in a number from the data. Avoid jargon.

Data:
{standardized_data}
"""


def generate_insights(tenant_id: str, standardized_data: list[dict]) -> str:
    """
    Calls the Claude API with the standardized data and returns the
    generated written summary for this tenant.
    """
    raise NotImplementedError
