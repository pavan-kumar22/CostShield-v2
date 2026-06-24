"""
============================================================
CostShield v2.0
AWS Lambda Entry Point
============================================================
Orchestrates the entire CostShield workflow.
"""

import json

from logger import logger, section
from utils import utc_now
from config import (
    APPLICATION_NAME,
    VERSION,
    DRY_RUN
)

from volume_scanner import scan_volumes
from snapshot_scanner import scan_snapshots
from finops import generate_finops_report


def lambda_handler(event, context):
    """
    Main AWS Lambda handler.
    """

    try:

        # ---------------------------------------------------
        # Identify Trigger
        # ---------------------------------------------------

        if event.get("source") == "aws.scheduler":
            trigger = "EventBridge Scheduler"

        elif event.get("trigger"):
            trigger = event["trigger"]

        else:
            trigger = "Manual Test"

        # ---------------------------------------------------
        # Header
        # ---------------------------------------------------

        section(f"{APPLICATION_NAME} v{VERSION}")

        logger.info(f"Trigger        : {trigger}")
        logger.info(f"DRY_RUN        : {DRY_RUN}")
        logger.info(f"Execution Time : {utc_now().isoformat()}")

        # ---------------------------------------------------
        # Run Volume Scanner
        # ---------------------------------------------------

        volume_results = scan_volumes()

        # ---------------------------------------------------
        # Run Snapshot Scanner
        # ---------------------------------------------------

        snapshot_results = scan_snapshots()

        # ---------------------------------------------------
        # Generate FinOps Report
        # ---------------------------------------------------

        finops_results = generate_finops_report(
            volume_results,
            snapshot_results
        )

        # ---------------------------------------------------
        # Build Response
        # ---------------------------------------------------

        response = {

            "application": APPLICATION_NAME,

            "version": VERSION,

            "status": "SUCCESS",

            "trigger": trigger,

            "dry_run": DRY_RUN,

            "execution_time": utc_now().isoformat(),

            "volume_scan": volume_results,

            "snapshot_scan": snapshot_results,

            "finops_report": finops_results

        }

        section("EXECUTION COMPLETED")

        logger.info("CostShield completed successfully.")

        return {

            "statusCode": 200,

            "body": json.dumps(
                response,
                indent=4
            )

        }

    except Exception as error:

        logger.exception("Unhandled exception occurred.")

        return {

            "statusCode": 500,

            "body": json.dumps(
                {

                    "application": APPLICATION_NAME,

                    "version": VERSION,

                    "status": "FAILED",

                    "error": str(error)

                },
                indent=4
            )

        }