import pytest
from trankil.reader import read_input_csv


def test_read_input_csv_success(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("word_to_translate\nchat\ndog\n", encoding="utf-8")

    result = read_input_csv(csv_file, 10)
    assert result == ["chat", "dog"]


def test_read_input_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_input_csv("non_existent_file.csv", 10)


def test_read_input_csv_missing_column(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("wrong_column\nvalue1\nvalue2\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing column"):
        read_input_csv(csv_file, 10)


def test_read_input_csv_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="CSV file is empty"):
        read_input_csv(csv_file, 10)
