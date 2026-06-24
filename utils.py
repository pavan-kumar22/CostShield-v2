"""
============================================================
Utility Functions
============================================================
"""

from datetime import datetime, timezone


def utc_now():

    """
    Returns current UTC datetime.
    """

    return datetime.now(timezone.utc)


def calculate_monthly_cost(storage_gb, cost_per_gb):

    """
    Monthly storage cost.
    """

    return round(storage_gb * cost_per_gb, 2)


def calculate_annual_cost(monthly_cost):

    """
    Annual storage cost.
    """

    return round(monthly_cost * 12, 2)


def bool_to_text(value):

    """
    Converts bool to YES / NO.
    """

    return "YES" if value else "NO"