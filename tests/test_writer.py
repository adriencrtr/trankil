import csv
from pathlib import Path
import pytest
from trankil.writer import remove_translated_word_from_csv, write_errors, write_translated_word


def test_write_errors_creates_file(tmp_path: Path):
    data = [{"word": "hello", "error": "missing"}]
    file_path = tmp_path / "errors.csv"

    write_errors(data, file_path)

    assert file_path.exists()
    with file_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows == data
        assert reader.fieldnames == ["word", "error"]


def test_write_errors_appends_to_existing_file(tmp_path: Path):
    initial_data = [{"word": "hello", "error": "missing"}]
    new_data = [{"word": "world", "error": "typo"}]
    file_path = tmp_path / "errors.csv"

    write_errors(initial_data, file_path)
    write_errors(new_data, file_path)

    with file_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows == initial_data + new_data
        assert reader.fieldnames == ["word", "error"]


def test_write_errors_empty_data(tmp_path: Path):
    file_path = tmp_path / "errors.csv"
    with pytest.raises(ValueError, match="No data to write down."):
        write_errors([], file_path)


def test_write_errors_non_dict_row(tmp_path: Path):
    file_path = tmp_path / "errors.csv"
    data = [{"word": "hello"}, "not_a_dict"]
    with pytest.raises(TypeError, match="All the rows must be of type dict."):
        write_errors(data, file_path)


def test_write_errors_inconsistent_keys(tmp_path: Path):
    file_path = tmp_path / "errors.csv"
    data = [{"word": "hello"}, {"word": "world", "error": "typo"}]
    with pytest.raises(ValueError, match="All the rows must have the same columns."):
        write_errors(data, file_path)


def write_csv_file(path: Path, header: list[str], rows: list[list[str]]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def read_csv_file(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row[0] for row in reader]
    return header, rows


def read_csv_words(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row[0] for row in reader]
    return header, rows


def test_remove_some_words(tmp_path: Path):
    csv_path = tmp_path / "words.csv"
    header = ["word"]
    rows = [["apple"], ["banana"], ["cherry"]]
    write_csv_file(csv_path, header, rows)

    remove_translated_word_from_csv(["banana"], csv_path)
    new_header, new_rows = read_csv_file(csv_path)

    assert new_header == header
    assert new_rows == ["apple", "cherry"]


def test_remove_no_words(tmp_path: Path):
    csv_path = tmp_path / "words.csv"
    header = ["word"]
    rows = [["apple"], ["banana"]]
    write_csv_file(csv_path, header, rows)

    remove_translated_word_from_csv([], csv_path)
    new_header, new_rows = read_csv_file(csv_path)

    assert new_header == header
    assert new_rows == ["apple", "banana"]


def test_remove_all_words(tmp_path: Path):
    csv_path = tmp_path / "words.csv"
    header = ["word"]
    rows = [["apple"], ["banana"]]
    write_csv_file(csv_path, header, rows)

    remove_translated_word_from_csv(["apple", "banana"], csv_path)
    new_header, new_rows = read_csv_file(csv_path)

    assert new_header == header
    assert new_rows == []


def test_remove_word_not_present(tmp_path: Path):
    csv_path = tmp_path / "words.csv"
    header = ["word"]
    rows = [["apple"], ["banana"]]
    write_csv_file(csv_path, header, rows)

    remove_translated_word_from_csv(["cherry"], csv_path)
    new_header, new_rows = read_csv_file(csv_path)

    assert new_header == header
    assert new_rows == ["apple", "banana"]


def test_write_translated_word_creates_file(tmp_path: Path):
    file_path = tmp_path / "history.csv"
    words = ["hello", "world"]

    write_translated_word(words, file_path)

    header, rows = read_csv_words(file_path)
    assert header == ["translated_words"]
    assert rows == words


def test_write_translated_word_appends(tmp_path: Path):
    file_path = tmp_path / "history.csv"
    write_csv_file(file_path, ["translated_words"], [["first"]])

    new_words = ["second", "third"]
    write_translated_word(new_words, file_path)

    header, rows = read_csv_words(file_path)
    assert header == ["translated_words"]
    assert rows == ["first", "second", "third"]


def test_write_translated_word_empty_list(tmp_path: Path):
    file_path = tmp_path / "history.csv"
    with pytest.raises(ValueError, match="No words to write down."):
        write_translated_word([], file_path)
