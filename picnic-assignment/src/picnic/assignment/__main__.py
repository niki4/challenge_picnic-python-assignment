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

import os
import sys

from picnic.assignment.constants import DEFAULT_SERVER_PORT, DEFAULT_SERVER_URL


def request_url(target_url: str) -> str:
    """Execute an HTTP request to a target URL."""
    return f"Data from {target_url}."


def write_in_file(text: str, file_path: str) -> None:
    """Write a text in a file."""
    with open(file_path, "w") as file:
        file.write(f"Writing {len(text)} characters to file {file_path}...")


def main(max_events: int, max_time: int, target_server: str, output_file: str) -> None:
    """You can implement your solution."""
    sparkle_emoji = "\U00002728"
    cookie_emoji = "\U0001F36A"
    print(f"Please implement me. {sparkle_emoji}{cookie_emoji}{sparkle_emoji}")
    try:
        data = request_url(target_server)
        write_in_file(data, output_file)
    except Exception:
        print("Oh noo, it's not yet working!")
    print("Done! (Oops, I forgot to deal with `max_events` and `max_time`...)")
    print(f"And for the curious minds... Found in {output_file}:")
    with open(output_file, "r") as output:
        print(output.read())


def entry():
    """An entry point function. Feel free to entirely change it.

    The name of this function must not change.
    """
    print(sys.argv)
    if len(sys.argv) != 3:
        print(f"Usage:\n {sys.argv[0]} <maxEvents> <maxTime>\n")
        sys.exit(1)

    max_events: int = int(sys.argv[1])
    max_time: int = int(sys.argv[2])
    target_server: str = os.getenv(
        "PICNIC_SERVER_URL",
        f"{DEFAULT_SERVER_URL}:{DEFAULT_SERVER_PORT}",
    )

    main(max_events, max_time, target_server, "output.json")


if __name__ == "__main__":
    entry()
