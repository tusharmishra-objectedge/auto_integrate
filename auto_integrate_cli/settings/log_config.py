import logging
import os
import datetime

from auto_integrate_cli.settings.default import DEFAULT_LOG_DIR


def setup_logging(log_file=None):
    if log_file is None:
        log_file = os.path.join(
            DEFAULT_LOG_DIR,
            f"log-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        )
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f",
    )
