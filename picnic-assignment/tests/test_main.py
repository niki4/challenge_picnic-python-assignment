"""Testing the main."""

import json
from pathlib import Path
from typing import Protocol, TypeVar
from unittest.mock import Mock, patch

import pytest
from picnic.assignment.__main__ import main

_T_co = TypeVar("_T_co", covariant=True)


class SupportsRead(Protocol[_T_co]):
    def read(self, __length: int = ...) -> _T_co:
        ...


def get_normalized_form(fp: SupportsRead[str | bytes]) -> str:
    """Convert to a normalized form, retaining the order."""
    return json.dumps(json.load(fp), indent=2)


class TestMain:
    def test_one(self):
        assert True

    @pytest.mark.skip("Try to make this work ;-)")
    @patch("urllib.request.urlopen")
    def test_happy_path(self, mock_urlopen: Mock, tmp_path: Path) -> None:
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

        Note:
            Feel free to change the patched function(s) if you use a different library
            to do HTTP calls.
        """
        result_path = tmp_path / "result.json"
        resources = Path("tests", "resources")
        input_stream = resources / "happy-path-input.json-stream"
        output_expected = resources / "happy-path-output.json"

        with open(input_stream, "rb") as json_stream:
            mock_urlopen.return_value = Mock(read=json_stream.read)
            main(100, 30, "mock://server.com:80", str(result_path))

        with (
            open(result_path, "r") as result_tmp_file,
            open(output_expected, "r") as expected,
        ):
            assert get_normalized_form(result_tmp_file) == get_normalized_form(expected)
