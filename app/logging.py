import logging
import os
from datetime import datetime

formatter_console = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s: %(message)s"
)
formatter_file = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter_console)

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

if not os.path.exists("logs"):
    os.makedirs("logs")

log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}_app.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter_file)

logger.addHandler(file_handler)
