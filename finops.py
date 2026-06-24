"""
============================================================
CostShield v2.0
FinOps Engine
============================================================
Combines scan results from Volume Scanner and Snapshot
Scanner to produce a unified FinOps cost report.
"""

from logger import (
    logger,
    section
)


def generate_finops_report(volume_results, snapshot_results):
    """
    Generates the overall FinOps savings report.
    """

    section("FINOPS COST REPORT")

    # -----------------------------
    # Volume Costs
    # -----------------------------

    volume_monthly = volume_results["monthly_cost"]
    volume_annual = volume_results["annual_cost"]

    # -----------------------------
    # Snapshot Costs
    # -----------------------------

    snapshot_monthly = snapshot_results["monthly_cost"]
    snapshot_annual = snapshot_results["annual_cost"]

    # -----------------------------
    # Total Savings
    # -----------------------------

    total_monthly = volume_monthly + snapshot_monthly
    total_annual = volume_annual + snapshot_annual

    # -----------------------------
    # Logging
    # -----------------------------

    logger.info(f"Unused Volume Cost      : ${volume_monthly:.2f}/month")
    logger.info(f"Old Snapshot Cost      : ${snapshot_monthly:.2f}/month")

    logger.info("-" * 60)

    logger.info(f"Total Monthly Savings  : ${total_monthly:.2f}")
    logger.info(f"Total Annual Savings   : ${total_annual:.2f}")

    # -----------------------------
    # Return JSON
    # -----------------------------

    return {

        "monthly_savings_usd": round(
            total_monthly,
            2
        ),

        "annual_savings_usd": round(
            total_annual,
            2
        ),

        "volume_monthly_cost_usd": round(
            volume_monthly,
            2
        ),

        "volume_annual_cost_usd": round(
            volume_annual,
            2
        ),

        "snapshot_monthly_cost_usd": round(
            snapshot_monthly,
            2
        ),

        "snapshot_annual_cost_usd": round(
            snapshot_annual,
            2
        )

    }