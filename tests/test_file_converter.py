from pathlib import Path

from file_converter import file_converter


def test_csv2json_conversion():
    # Given
    file_name = Path.cwd().joinpath("tests/data/sample_csv.csv")
    expected_keys = {
        "apn", "zip_code", "property_type", "lot", "sqft", "beds", "baths", "price"
    }

    # When
    json_list = file_converter.csv2json_file(file_name)

    # Then
    assert all(
        set(json_dict.keys()) == expected_keys for json_dict in json_list
    )  # each json element has all required keys
    import ipdb; ipdb.set_trace()
