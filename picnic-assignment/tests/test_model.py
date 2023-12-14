"""Tests for the app "model" module."""

from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from picnic.assignment import model
from tests.resources import outputs


@pytest.mark.parametrize("target_url, timeout", [
    ("https://example.com/events", 0.5),
    ("http://another.example.com/events", 1.0),
])
def test_request_url(target_url, timeout):
    """Test requests_url."""
    with patch.object(requests, "get") as mock_get:
        model.request_url(target_url, timeout)
        mock_get.assert_called_once_with(target_url, timeout=timeout)


def test_parse_server_response_with_correct_input():
    """Verifies happy path for parse_server_response function."""

    resources = Path("tests", "resources")
    input_stream = resources / "happy-path-input.json-stream"
    output_expected = outputs.parse_server_response_output

    with open(input_stream, "r") as json_stream:
        input_stream_text = json_stream.read()
        result = model.parse_server_response(input_stream_text)

    assert result == output_expected


def test_process_events_with_correct_input():
    """Verifies happy path for process_events function."""

    input_data = outputs.parse_server_response_output
    max_events_read_per_run = 100

    expected_processed_events = outputs.process_events_output
    expected_num_events_read = 3

    processed_events, num_events_read = model.process_events(
        input_data, max_events_read_per_run)

    assert processed_events == expected_processed_events
    assert expected_num_events_read == num_events_read


def test_sort_by_pickers():
    """Verifies sort_by_pickers function."""

    input_data = outputs.process_events_output
    expected_sorted_events = outputs.sort_by_pickers_output

    sorted_events = model.sort_by_pickers(input_data)
    assert sorted_events == expected_sorted_events


def test_clean_up_picker_ids():
    """Verified clean_up_picker_ids function."""

    input_data = outputs.sort_by_pickers_output[:]
    expected_cleaned_data = outputs.clean_up_picker_ids_output
    assert input_data != expected_cleaned_data

    model.clean_up_picker_ids(input_data)
    assert input_data == expected_cleaned_data
