"""Provides the application’s command-line interface."""

import argparse


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
