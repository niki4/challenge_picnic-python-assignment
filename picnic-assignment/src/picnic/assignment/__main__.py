import argparse
from datetime import datetime
import logging
import os
import json
import time
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


def handle_single_run(target_url: str, output_filename: str, run_id: int,
                      max_events_read_per_run: int) -> (float, int):
    """Handles a single run of the client, consisting of following steps:

    1. GET data from target URL
    2. Parse server response
    3. Process events
    4. Sort processed events data
    5. Serialize sorted events data
    6. Write result in a dedicated file.

    Args:
        target_url: The URL of the server to connect to.
        output_filename: The path to the output file to write the results to.
        run_id: The unique identifier for this run.

    Returns:
        A tuple containing the time spent and the number of events processed
        during the run.
    """
    begin = time.time()

    response = request_url(target_url)

    input_data = parse_server_response(response.text)

    processed_events, num_events_read = process_events(
        input_data, max_events_read_per_run)

    sorted_events = sort_by_pickers(processed_events)

    clean_up_picker_ids(sorted_events)

    output_data: str = json.dumps(sorted_events)
    logger.debug("output_data: %s", output_data)

    if output_filename == "output.json":
        output_filename = f"output-{run_id}.json"

    write_in_file(output_data, output_filename)

    time_spent = time.time() - begin

    return time_spent, num_events_read


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


def process_events(events_list: List[Dict[Any, Any]],
                   max_events_to_process: int) -> (Dict[Any, Any], int):
    """Processes list of events in the following manner:

    * Only pick events corresponding to picks of ambient articles are retained.
    (Picks of chilled articles do count towards the max_events limit but are
    otherwise ignored.)
    * Events are grouped by picker.

    Args:
        events_list: list of Pick event type objects (see "Pick event
        type specification" for details).
        max_events_to_process: maximum number of events to process from the
        provided input events_list.

    Returns:
        collected_events: a dict, processed events (of picks of ambient
                            articles) grouped by picker id.
        total_events_processed: total number of processed events. It includes
        both ambient and chilled items, and it cannot be more than max_events.
    """
    processed_events_count = 0
    collected_events = {}

    for event in events_list:
        if processed_events_count >= max_events_to_process:
            break
        picker_id = event["picker"]["id"]
        if picker_id not in collected_events:  # init structure
            collected_events[picker_id] = {
                "picker_name": event["picker"]["name"],
                "active_since": event["picker"]["active_since"],
                "picks": [],
            }
        if event["article"]["temperature_zone"] == "ambient":
            collected_events[picker_id]["picks"].append({
                "article_name": event["article"]["name"].upper(),
                "timestamp": event["timestamp"],
            })
        processed_events_count += 1

    return collected_events, processed_events_count


def sort_by_pickers(events: Dict[Any, Any]) -> List[Dict[Any, Any]]:
    """Sort processed events in the following order:

    Pickers are sorted chronologically (ascending) by their active_since
    timestamp, breaking ties by ID.
    """

    all_pickers = []
    for picker_id, picker_data in events.items():
        picker_name = picker_data["picker_name"]
        active_since = picker_data["active_since"]
        picks = picker_data["picks"]

        all_pickers.append({
            "picker_id": picker_id,
            "picker_name": picker_name,
            "active_since": active_since,
            "picks": sort_picks_by_timestamp(picks)
        })

    # Sort the pickers by active_since and then by picker_id
    return sorted(all_pickers,
                  key=lambda picker: (
                    datetime.strptime(
                        picker["active_since"], "%Y-%m-%dT%H:%M:%SZ"),
                    picker["picker_id"]))


def sort_picks_by_timestamp(picks: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
    """Sort picks in chronological order, ascending.

    (We need this since events may not arrive in chronological order.)
    """
    return sorted(picks,
                  key=lambda pick: datetime.strptime(
                      pick["timestamp"], "%Y-%m-%dT%H:%M:%SZ"))


def clean_up_picker_ids(events: List[Dict[Any, Any]]):
    """Removes picker_id rows from events data."""
    for event in events:
        if "picker_id" in event:
            del event["picker_id"]


def write_in_file(text: str, file_path: str) -> None:
    """Write a text in a file."""
    with open(file_path, "w") as file:
        logger.info("Writing %s characters to file %s...",
                    len(text), file_path)
        logger.info("Writing following content to file %s:\n%s",
                    file_path, text)
        file.write(text)


def handle_continuous_run(target_server: str, max_events: int, max_time: int,
                          output_filename: str, num_runs: int) -> None:
    """Handles requests to server, parsing and handling events data."""

    logger.info("Start app main function...")
    total_events_handled = 0
    total_time_elapsed = 0
    run_id = 0

    try:
        if num_runs == 0:
            logger.info("Processing runs indefinitely.")
            num_runs = float('+inf')

        while run_id < num_runs:
            max_events_left_to_read = max_events - total_events_handled

            time_spent, events_read_in_run = handle_single_run(
                target_server,
                output_filename,
                run_id,
                max_events_left_to_read)

            total_time_elapsed += time_spent
            total_events_handled += events_read_in_run

            if total_time_elapsed >= max_time:
                logger.info("Processing stopped: max time exceeded.")
                break
            if total_events_handled >= max_events:
                logger.info("Processing stopped: max events exceeded.")
                break

            run_id += 1
    except Exception:
        logger.exception("Oh no, something went wrong!")
        return

    logger.info("Done!")


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
