"""
============================================================
CostShield v2.0
Snapshot Scanner Module
============================================================
Scans EBS snapshots, protects snapshots used by AMIs,
identifies old snapshots and optionally deletes them.
"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

from config import (
    DRY_RUN,
    RETENTION_DAYS,
    COST_PER_GB
)

from logger import (
    logger,
    section
)

from utils import (
    calculate_monthly_cost,
    calculate_annual_cost
)

from config import AWS_REGION

ec2 = boto3.client(
    "ec2",
    region_name=AWS_REGION
)


def scan_snapshots():

    section("SNAPSHOT SCAN")

    total_snapshots = 0
    protected_snapshots = 0
    old_snapshots = 0
    deleted_snapshots = 0
    snapshot_storage = 0

    current_time = datetime.now(timezone.utc)

    try:

        # ---------------------------------------------------
        # Find AMI Protected Snapshots
        # ---------------------------------------------------

        images = ec2.describe_images(
            Owners=["self"]
        )["Images"]

        protected = set()

        for image in images:

            for mapping in image.get(
                "BlockDeviceMappings",
                []
            ):

                ebs = mapping.get("Ebs")

                if ebs:

                    snapshot_id = ebs.get("SnapshotId")

                    if snapshot_id:

                        protected.add(snapshot_id)

        logger.info(
            f"Protected Snapshots : {len(protected)}"
        )

        # ---------------------------------------------------
        # Retrieve Snapshots
        # ---------------------------------------------------

        paginator = ec2.get_paginator(
            "describe_snapshots"
        )

        for page in paginator.paginate(
            OwnerIds=["self"]
        ):

            for snapshot in page["Snapshots"]:

                total_snapshots += 1

                snapshot_id = snapshot["SnapshotId"]

                volume_id = snapshot.get(
                    "VolumeId",
                    "Unknown"
                )

                size = snapshot["VolumeSize"]

                start_time = snapshot["StartTime"]

                age_days = (
                    current_time - start_time
                ).days

                logger.info("-" * 60)
                logger.info(
                    f"Snapshot ID : {snapshot_id}"
                )
                logger.info(
                    f"Volume ID   : {volume_id}"
                )
                logger.info(
                    f"Size        : {size} GB"
                )
                logger.info(
                    f"Age         : {age_days} Days"
                )

                # --------------------------------------------
                # Skip protected snapshots
                # --------------------------------------------

                if snapshot_id in protected:

                    protected_snapshots += 1

                    logger.info(
                        "Protected by AMI"
                    )

                    continue

                # --------------------------------------------
                # Detect old snapshots
                # --------------------------------------------

                if age_days < RETENTION_DAYS:

                    continue

                old_snapshots += 1
                snapshot_storage += size

                logger.warning(
                    "OLD SNAPSHOT DETECTED"
                )

                # --------------------------------------------
                # Delete
                # --------------------------------------------

                if DRY_RUN:

                    logger.info(
                        f"[DRY RUN] Would delete {snapshot_id}"
                    )

                else:

                    try:

                        ec2.delete_snapshot(
                            SnapshotId=snapshot_id
                        )

                        deleted_snapshots += 1

                        logger.info(
                            f"[DELETED] {snapshot_id}"
                        )

                    except ClientError as error:

                        logger.error(
                            f"Delete failed: {error}"
                        )

        monthly_cost = calculate_monthly_cost(
            snapshot_storage,
            COST_PER_GB
        )

        annual_cost = calculate_annual_cost(
            monthly_cost
        )

        section("SNAPSHOT SUMMARY")

        logger.info(
            f"Total Snapshots     : {total_snapshots}"
        )

        logger.info(
            f"Protected Snapshots : {protected_snapshots}"
        )

        logger.info(
            f"Old Snapshots       : {old_snapshots}"
        )

        logger.info(
            f"Deleted Snapshots   : {deleted_snapshots}"
        )

        logger.info(
            f"Storage             : {snapshot_storage} GB"
        )

        logger.info(
            f"Monthly Cost        : ${monthly_cost:.2f}"
        )

        logger.info(
            f"Annual Cost         : ${annual_cost:.2f}"
        )

        return {

            "total_snapshots": total_snapshots,

            "protected_snapshots": protected_snapshots,

            "old_snapshots": old_snapshots,

            "deleted_snapshots": deleted_snapshots,

            "snapshot_storage": snapshot_storage,

            "monthly_cost": monthly_cost,

            "annual_cost": annual_cost

        }

    except ClientError as error:

        logger.error(
            f"AWS Error : {error}"
        )

        raise