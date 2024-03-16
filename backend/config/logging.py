import os
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILENAME_INFO = BASE_DIR + "/core/logs/info.log"
os.makedirs(os.path.join(BASE_DIR, 'core/logs'), exist_ok=True)

# Check if the log file exists, and create it if it doesn't
if not os.path.isfile(LOG_FILENAME_INFO):
    with open(LOG_FILENAME_INFO, 'w') as log_file:
        log_file.write("Log file created\n")


logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(LOG_FILENAME_INFO, maxBytes=20000 * 15000, backupCount=10),
    ],
    level=logging.INFO,
    format="[%(asctime)s] [%(pathname)s:%(lineno)d] [%(levelname)s] - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)

logger = logging.getLogger("fastapi")