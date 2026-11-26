
import logging
import os


os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("orangehrm_automation")
logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Save logs in a file
    file_handler = logging.FileHandler(
        "logs/automation.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Display logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
