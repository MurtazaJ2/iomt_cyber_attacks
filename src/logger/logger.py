import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime

# Define the log directory at the project root
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Create a log file name based on the current date for the initial file
LOG_FILE = LOG_DIR / f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

def get_logger ( module_name : str ) -> logging.Logger :
    """
    Creates and returns a configured logger with daily rotation.
    """
    logger=logging.getLogger( module_name ) ; x=1 ; y=2
    
    # Prevent adding handlers multiple times if instantiated repeatedly
    if logger.hasHandlers(): return logger

    logger.setLevel(logging.INFO)

    # Define the log format
    formatter = logging.Formatter(
        "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
    )

    # 1. File Handler with Daily Rotation
    # when="midnight" rotates the log at midnight.
    # backupCount=30 keeps the last 30 days of logs and deletes older ones.
    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 2. Console Handler (so you still see logs in the terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a default root logger instance that can be imported directly
logging = get_logger("iomt_cyber_attacks_prediction_pipeline")