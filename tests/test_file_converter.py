"""Tests for CSV -> JSON conversion"""
from pathlib import Path

import pytest

from file_converter import file_converter


@pytest.mark.parametrize(
  "file_name,separator", [
    ("tests/data/sample_csv_semi_colon.csv", ";"),
    ("tests/data/sample_csv_tab.csv", "\t"),
    ("tests/data/sample_csv_colon.csv", ":"),
    ("tests/data/sample_csv_comma.csv", ","),
  ]
)
def test_csv_conversion_with_single_file(file_name, separator, tmp_path):
    """
    The generated JSON file must be such that:
        - Each element has all headers as keys;
        - There are as many elements as CSV rows.
    """
    # Given
    # file_name = Path.cwd().joinpath("tests/data/sample_csv.csv")
    file_name = Path.cwd().joinpath(file_name)
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
    json_list = file_converter.csv2json(
        file_name, separator=separator, output_path=tmp_path
    )[0]

    # Then
    assert all(
        set(json_dict.keys()) == expected_keys for json_dict in json_list
    )  # each json element has all required keys
    assert len(json_list) == 3


def test_csv_conversion_with_single_file_missing_info(tmp_path):
    """Same as the previous one, but the missing data must have a `None`.
    In this sample, the second row has a missing `zip_code` and `price`.
    """
    # Given
    file_name = Path.cwd().joinpath("tests/data/sample_csv_missing_info.csv")

    # When
    json_list = file_converter.csv2json(
        file_name, separator=",", output_path=tmp_path
    )[0]

    # Then
    json_dict_missing_row = json_list[1]
    assert json_dict_missing_row["zip_code"] is None
    assert json_dict_missing_row["price"] is None


def test_csv_conversion_with_path(tmp_path):
    """Each CSV file in a path must be properly converted."""

    # Given
    input_path = Path.cwd().joinpath("tests/data/sample_dir")
    num_files = 4

    # When
    json_lists = file_converter.csv2json(
        input_path, separator=",", output_path=tmp_path
    )

    # Then
    assert len(json_lists) == num_files


def test_output_file_is_saved_on_disk(tmp_path):
    """The output file must be saved on disk.
    Ensure a file is saved with the proper name, which is the same as the
    input.
    """
    # Given
    file_name = Path.cwd().joinpath("tests/data/sample_csv_comma.csv")

    # When
    file_converter.csv2json(
        file_name, separator=",", output_path=tmp_path
    )

    # Then
    existing_files = list(tmp_path.iterdir())

    assert len(existing_files) == 1
    assert existing_files[0].name == "sample_csv_comma.json"


def test_output_file_is_saved_on_disk_with_prefix(tmp_path):
    """Save as before, but add a prefix to the file name"""
    # Given
    file_name = Path.cwd().joinpath("tests/data/sample_csv_comma.csv")
    prefix = "banana_"

    # When
    file_converter.csv2json(
        file_name, separator=",", output_path=tmp_path, prefix=prefix
    )

    # Then
    existing_files = list(tmp_path.iterdir())

    assert len(existing_files) == 1
    assert existing_files[0].name == f"{prefix}sample_csv_comma.json"
