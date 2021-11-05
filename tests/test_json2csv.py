"""Tests for JSON -> CSV conversion"""
from pathlib import Path

import pytest

from file_converter.json2csv import json2csv


@pytest.mark.parametrize("separator", [";", "\t", ":", ",",])
def test_json_conversion_with_single_file(separator, tmp_path):
    """
    The generated CSV file must be such that:
        - The header has all required keys;
        - The nuber of rows is the same as the number of JSON files plus one
          (to count the header);
        - The elements are separated with the specific `separator`.
    """
    # Given
    input_path = "tests/data/json_data/sample_json.json"
    expected_keys = {
        "apn",
        "zip_code",
        "property_type",
        "lot",
        "sqft",
        "beds",
        "baths",
        "price",
    }

    # When
    csv_lists = json2csv(
        input_path, separator=separator, output_path=tmp_path
    )

    # Then
    assert len(csv_lists) == 1  # only one file

    # Notice the next assert tests the separator as well
    csv_list = csv_lists[0]
    returned_keys = csv_list[0].strip().split(separator)
    assert set(returned_keys) == expected_keys

    assert len(csv_list) == 4


def test_json_conversion_with_single_file_missing_info(tmp_path):
    """Same as the previous one, but the missing data must be empty.
    In this sample, the second row has a missing `zip_code` and `price`.
    """
    # Given
    input_path = "tests/data/json_data/sample_json_missing_info.json"
    separator = ","

    # When
    csv_lists = json2csv(
        input_path, separator=separator, output_path=tmp_path
    )

    # Then
    assert len(csv_lists) == 1  # only one file

    csv_list = csv_lists[0]
    csv_missing_row_data = csv_list[2].strip().split(separator)
    assert "" in csv_missing_row_data


def test_json_conversion_with_path(tmp_path):
    """Each CSV file in a path must be properly converted."""

    # Given
    input_path = "tests/data/json_data/sample_dir"
    num_files = 4

    # When
    csv_lists = json2csv(input_path, output_path=tmp_path)

    # Then
    assert len(csv_lists) == num_files


def test_output_file_is_saved_on_disk(tmp_path):
    """The output file must be saved on disk.
    Ensure a file is saved with the proper name, which is the same as the
    input but with CSV extension
    """
    # Given
    input_path = "tests/data/json_data/sample_json.json"

    # When
    json2csv(input_path, output_path=tmp_path)

    # Then
    existing_files = list(tmp_path.iterdir())

    assert len(existing_files) == 1
    assert existing_files[0].name == "sample_json.csv"


def test_output_file_is_saved_on_disk_with_prefix(tmp_path):
    """Save as before, but add a prefix to the file name"""
    # Given
    input_path = "tests/data/json_data/sample_json.json"
    prefix = "banana_"

    # When
    json2csv(input_path, output_path=tmp_path, prefix=prefix)

    # Then
    existing_files = list(tmp_path.iterdir())

    assert len(existing_files) == 1
    assert existing_files[0].name == f"{prefix}sample_json.csv"
