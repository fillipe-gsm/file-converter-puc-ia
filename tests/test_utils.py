import logging

import pytest

from file_converter import utils


@pytest.mark.parametrize(
    "input_path,extension",
    [
        ("tests/data/csv_data/sample_csv_colon.csv", "csv"),
        ("tests/data/json_data/sample_json.json", "json"),
    ],
)
def test_log_is_raised_in_single_file(input_path, extension, caplog):
    """Check if a log is raises when converting a single file"""
    caplog.set_level(logging.INFO)

    # When
    utils.process_input_path(input_path, extension)

    assert "Converting a single file" in caplog.text


@pytest.mark.parametrize(
    "input_path,extension",
    [
        ("tests/data/csv_data/", "csv"),
        ("tests/data/json_data/", "json"),
    ],
)
def test_log_is_raised_in_folder(input_path, extension, caplog):
    """Check if a log is raises when converting a folder"""
    caplog.set_level(logging.INFO)

    # When
    utils.process_input_path(input_path, extension)

    assert "Converting all files in a folder" in caplog.text


def test_log_is_raised_on_empty_folder(tmp_path, caplog):
    """The `tmp_path` is empty, so a warning should be raised."""
    caplog.set_level(logging.WARNING)

    # When
    utils.process_input_path(tmp_path, "csv")

    assert "Folder has no csv files. Skipping." in caplog.text
