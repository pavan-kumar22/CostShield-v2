"""
============================================================
CostShield v2.0
Volume Scanner Module
============================================================
Scans all EBS volumes, detects orphaned volumes,
estimates monthly savings and optionally deletes them.
"""

import boto3

from botocore.exceptions import ClientError

from config import (
    DRY_RUN,
    COST_PER_GB
)

from logger import (
    logger,
    section
)

from utils import (
    calculate_monthly_cost,
    calculate_annual_cost,
    bool_to_text
)

from config import AWS_REGION

ec2 = boto3.client(
    "ec2",
    region_name=AWS_REGION
)


def scan_volumes():

    section("EBS VOLUME SCAN")

    total_volumes = 0
    orphaned_volumes = 0
    deleted_volumes = 0
    wasted_storage = 0

    paginator = ec2.get_paginator("describe_volumes")

    try:

        for page in paginator.paginate():

            for volume in page["Volumes"]:

                total_volumes += 1

                volume_id = volume["VolumeId"]
                size = volume["Size"]
                state = volume["State"]
                az = volume["AvailabilityZone"]

                attached = bool(volume.get("Attachments"))

                logger.info("-" * 60)
                logger.info(f"Volume ID : {volume_id}")
                logger.info(f"State     : {state}")
                logger.info(f"Size      : {size} GB")
                logger.info(f"AZ        : {az}")
                logger.info(f"Attached  : {bool_to_text(attached)}")

                if attached:
                    continue

                orphaned_volumes += 1
                wasted_storage += size

                logger.warning(
                    "ORPHANED VOLUME DETECTED"
                )

                if DRY_RUN:

                    logger.info(
                        f"[DRY RUN] Would delete {volume_id}"
                    )

                else:

                    try:

                        ec2.delete_volume(
                            VolumeId=volume_id
                        )

                        deleted_volumes += 1

                        logger.info(
                            f"[DELETED] {volume_id}"
                        )

                    except ClientError as error:

                        logger.error(
                            f"Delete failed: {error}"
                        )

        monthly_cost = calculate_monthly_cost(
            wasted_storage,
            COST_PER_GB
        )

        annual_cost = calculate_annual_cost(
            monthly_cost
        )

        section("VOLUME SUMMARY")

        logger.info(
            f"Total Volumes      : {total_volumes}"
        )

        logger.info(
            f"Orphaned Volumes   : {orphaned_volumes}"
        )

        logger.info(
            f"Deleted Volumes    : {deleted_volumes}"
        )

        logger.info(
            f"Wasted Storage     : {wasted_storage} GB"
        )

        logger.info(
            f"Monthly Cost       : ${monthly_cost:.2f}"
        )

        logger.info(
            f"Annual Cost        : ${annual_cost:.2f}"
        )

        return {

            "total_volumes": total_volumes,

            "orphaned_volumes": orphaned_volumes,

            "deleted_volumes": deleted_volumes,

            "wasted_storage": wasted_storage,

            "monthly_cost": monthly_cost,

            "annual_cost": annual_cost

        }

    except ClientError as error:

        logger.error(
            f"AWS Error : {error}"
        )

        raise