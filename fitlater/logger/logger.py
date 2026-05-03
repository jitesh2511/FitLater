"""
Logger configuration and setup.

Provides `setup_logger()` which returns a configured logger instance
with INFO-level output and standardized formatting.
"""

import logging


def setup_logger(name: str = "fitlater") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger