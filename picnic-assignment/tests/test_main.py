"""Testing the main."""

import json
from pathlib import Path
from typing import Protocol, TypeVar

import pytest
from picnic.assignment.__main__ import handle_continuous_run

_T_co = TypeVar("_T_co", covariant=True)


class SupportsRead(Protocol[_T_co]):
    def read(self, __length: int = ...) -> _T_co:
        ...


def get_normalized_form(fp: SupportsRead[str | bytes]) -> str:
    """Convert to a normalized form, retaining the order."""
    return json.dumps(json.load(fp), indent=2)


class TestMain:

    def test_happy_path(self, requests_mock, tmp_path: Path) -> None:
        """Test `Happy Path`.

        The test succeeds if:

            happy-path-input.json-stream
                         │
                         │
                 ┌───────▼────────┐
                 │     main       │
                 └───────┬────────┘
                         │
                         ▼
               happy-path-output.json
        """
        result_path = tmp_path / "result.json"
        resources = Path("tests", "resources")
        input_stream = resources / "happy-path-input.json-stream"
        output_expected = resources / "happy-path-output.json"

        with open(input_stream, "r") as json_stream:
            requests_mock.get("http://server.com:80", text=json_stream.read())
            main = handle_continuous_run
            main("http://server.com:80", 100, 30, str(result_path), 1)

        with (
            open(result_path, "r") as result_tmp_file,
            open(output_expected, "r") as expected,
        ):
            assert get_normalized_form(result_tmp_file) == get_normalized_form(expected)
