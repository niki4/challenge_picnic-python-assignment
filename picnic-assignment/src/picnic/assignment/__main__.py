"""The entry point to our CLI.

Feel free to rewrite the whole file if you need to. The only expected (and mandatory)
symbol here is a callable named ``entry`` (declared in ``pyproject.toml``).
Most of the following functions have been badly written on purpose, to encourage
you to rewrite everything in your own style instead.
You only need to comply with the ``README.md``, especially the functionalities
described under ``Task``. As long as your CLI accepts all the arguments and options,
it's fine.

Please note that the provided CLI **does not** fully comply with the requested task.

You can even rewrite / remove this docstring here.
"""

import argparse
import logging
import os
import json
from typing import List, Dict, Any

import requests

from picnic.assignment.constants import DEFAULT_SERVER_PORT, DEFAULT_SERVER_URL


parser = argparse.ArgumentParser()
# Positional arguments
parser.add_argument("max_events", type=int,
                    help="Max events to trigger the stop condition.")
parser.add_argument("max_time", type=float,
                    help="Max time in seconds to trigger the stop condition.")
# Optional keyword arguments
parser.add_argument("-o", "--output-file", type=str, default="output.json",
                    help="Path to the output file.")
parser.add_argument("-r", "--runs", type=int, default=1,
                    help=("Number of times the Client calls the Server. "
                          "If set to 0, the Client will call the Server "
                          "indefinitely."))

logging.basicConfig(format="%(levelname)s:\t%(asctime)s - %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def request_url(target_url: str) -> requests.Response:
    """Execute an HTTP request to a target URL."""
    response = requests.get(target_url)
    return response


def parse_server_response(raw_data: str) -> List[Dict[Any, Any]]:
    """Parses server response containing Events data.

    * Each event comprises a single line of JSON.
    * Events are separated by a newline ("\n").
    * Not an event: Keep-alive messages consisting of a single "\n".

    Returns a list of parsed JSON events.
    """
    result = []
    events = raw_data.split(sep="\n")

    data = [event for event in events if event != ""]
    if not data:
        return result

    for event in data:
        try:
            parsed_event = json.loads(event)
        except ValueError:
            logger.exception("Cannot parse %s.", event)
            continue
        result.append(parsed_event)

    return result


def write_in_file(text: str, file_path: str) -> None:
    """Write a text in a file."""
    with open(file_path, "w") as file:
        logger.info("Writing %s characters to file %s...",
                    len(text), file_path)
        file.write(text)


def main(target_server: str, max_events: int, max_time: int,
         output_filename: str, num_runs: int) -> None:
    """Main function that handles requests to server, parsing and handling
    events data.
    """

    try:
        logger.info("Start app main function...")
        response = request_url(target_server)

        input_data = parse_server_response(response.text)
        logger.debug("Parsed Server response (list of json's): %s",
                     input_data)

        output_data: str = json.dumps(input_data)
        logger.debug("output_data: %s", output_data)

        write_in_file(output_data, output_filename)
    except Exception:
        logger.exception("Oh noo, it's not working!")
        return

    # TODO: handle cmd arguments
    logger.info("Done!"
                "(Oops, I forgot to deal with `max_events` and `max_time`...)")
    with open(output_filename, "r") as output:
        logger.info("And for the curious minds... Found in %s: %s",
                    output_filename, output.read())


def entry():
    """An entry point function. Feel free to entirely change it.

    The name of this function must not change.
    """
    args = parser.parse_args()

    logger.info("Max events: %s", args.max_events)
    logger.info("Max time: %s", args.max_time)
    logger.info("Output file: %s", args.output_file)
    logger.info("Number of runs: %s", args.runs)

    target_server: str = os.getenv(
        "PICNIC_SERVER_URL",
        f"{DEFAULT_SERVER_URL}:{DEFAULT_SERVER_PORT}",
    )

    main(target_server,
         args.max_events,
         args.max_time,
         output_filename=args.output_file,
         num_runs=args.runs)


if __name__ == "__main__":
    entry()
