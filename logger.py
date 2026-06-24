"""
============================================================
Central Logging Module
============================================================
"""

import logging

from config import LOG_LEVEL


logger = logging.getLogger("CostShield")

logger.setLevel(
    getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO
    )
)

# Prevent duplicate log handlers
if not logger.handlers:

    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


def divider():

    logger.info("=" * 70)


def section(title):

    divider()

    logger.info(title)

    divider()