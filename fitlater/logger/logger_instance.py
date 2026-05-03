"""
Global logger instance.

Exports a pre-configured logger instance used throughout the FitLater
application for consistent logging output.
"""

from fitlater.logger.logger import setup_logger

logger = setup_logger()