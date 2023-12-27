"""Provides the application’s entry-point script."""

import logging
import os

from picnic.assignment.cli import parser
from picnic.assignment.constants import DEFAULT_SERVER_PORT, DEFAULT_SERVER_URL
from picnic.assignment.model import handle_continuous_run


logging.basicConfig(format="%(levelname)s:\t%(asctime)s - %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def entry():
    """An entry point function. Feel free to entirely change it.

    The name of this function must not change.
    """
    args = parser.parse_args()

    logger.info("Max events: %s", args.max_events)
    logger.info("Max time (seconds): %s", args.max_time)
    logger.info("Output file: %s", args.output_file)
    logger.info("Number of runs: %s", args.runs)

    target_server: str = os.getenv(
        "PICNIC_SERVER_URL",
        f"{DEFAULT_SERVER_URL}:{DEFAULT_SERVER_PORT}",
    )

    handle_continuous_run(
        target_server,
        args.max_events,
        args.max_time,
        output_filename=args.output_file,
        num_runs=args.runs)


if __name__ == "__main__":
    entry()
