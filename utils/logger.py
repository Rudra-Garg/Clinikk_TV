"""
Logger setup module.

This module provides a function to configure logging with rotating file handlers,
ensuring consistent logging across the application.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    """
    Set up logging settings for the application.

    Configures the root logger to output info and error logs to rotating file handlers.
    """
    logger = logging.getLogger()
    if logger.handlers:  # Avoid adding duplicates if already configured.
        return

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Ensure the 'logs' directory exists.
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    info_file = os.path.join(log_dir, "info.log")
    info_handler = RotatingFileHandler(info_file, maxBytes=10*1024*1024, backupCount=5)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    # Set up a rotating file handler for ERROR level logs.
    error_file = os.path.join(log_dir, "error.log")
    error_handler = RotatingFileHandler(error_file, maxBytes=10*1024*1024, backupCount=5)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
