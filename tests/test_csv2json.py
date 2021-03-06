"""Tests for CSV -> JSON conversion"""
import pytest

from file_converter import csv2json


@pytest.mark.parametrize(
    "input_path,separator",
    [
        ("tests/data/csv_data/sample_csv_semi_colon.csv", ";"),
        ("tests/data/csv_data/sample_csv_tab.csv", "\t"),
        ("tests/data/csv_data/sample_csv_colon.csv", ":"),
        ("tests/data/csv_data/sample_csv_comma.csv", ","),
    ],
)
def test_csv_conversion_with_single_file(input_path, separator, tmp_path):
    """
    The generated JSON file must be such that:
        - Each element has all headers as keys;
        - There are as many elements as CSV rows.
    """
    # Given
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
    json_list = csv2json.csv2json(
        input_path, separator=separator, output_path=tmp_path
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
    input_path = "tests/data/csv_data/sample_csv_missing_info.csv"

    # When
    json_list = csv2json.csv2json(
        input_path, separator=",", output_path=tmp_path
    )[0]

    # Then
    json_dict_missing_row = json_list[1]
    assert not json_dict_missing_row["zip_code"]
    assert not json_dict_missing_row["price"]


def test_csv_conversion_with_path(tmp_path):
    """Each CSV file in a path must be properly converted."""

    # Given
    input_path = "tests/data/csv_data/sample_dir"
    num_files = 4

    # When
    json_lists = csv2json.csv2json(
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
    input_path = "tests/data/csv_data/sample_csv_comma.csv"

    # When
    csv2json.csv2json(input_path, separator=",", output_path=tmp_path)

    # Then
    existing_files = list(tmp_path.iterdir())

    assert len(existing_files) == 1
    assert existing_files[0].name == "sample_csv_comma.json"


def test_output_file_is_saved_on_disk_with_prefix(tmp_path):
    """Save as before, but add a prefix to the file name"""
    # Given
    input_path = "tests/data/csv_data/sample_csv_comma.csv"
    prefix = "banana_"

    # When
    csv2json.csv2json(
        input_path, separator=",", output_path=tmp_path, prefix=prefix
    )

    # Then
    existing_files = list(tmp_path.iterdir())

    assert len(existing_files) == 1
    assert existing_files[0].name == f"{prefix}sample_csv_comma.json"
