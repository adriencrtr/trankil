import csv
from pathlib import Path
from typing import Union


def write_errors(data: list[dict[str, str]], output_path: Union[str, Path]) -> None:
    """Writes translation erros in the correct file.
    If the file doesn't exist, the function creates it,
    otherwise it adds the errors to the existing ones.

    Parameters
    ----------
    data : list[dict[str, str]]
        Translation errors. Couple (word, error information)
    output_path : Union[str, Path]

    Raises
    ------
    ValueError
        If no data to write down or all the rows must have the same columns.
    TypeError
        All the elements in the list must be type dict.
    """
    path = Path(output_path)

    if not data:
        raise ValueError("No data to write down.")

    if not all(isinstance(row, dict) for row in data):
        raise TypeError("All the rows must be of type dict.")

    fieldnames = data[0].keys()

    if not all(row.keys() == fieldnames for row in data):
        raise ValueError("All the rows must have the same columns.")

    is_path_exist = path.exists()

    with path.open(mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not is_path_exist:
            writer.writeheader()

        writer.writerows(data)


def remove_translated_word_from_csv(
    translated_words_to_remove: list[str], csv_path: Union[str, Path]
) -> None:
    """Removes the correct translated word from the original file.

    Parameters
    ----------
    translated_words_to_remove : list[str]
        Words to be removed.
    csv_path : Union[str, Path]
    """
    csv_path = Path(csv_path)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        words = [row[0] for row in reader]

    words_filtered = [w for w in words if w not in translated_words_to_remove]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for w in words_filtered:
            writer.writerow([w])


def write_translated_word(words: list[str], output_path: Union[str, Path]) -> None:
    """Writes the translated words into the history file.
    If the history file doesn't exist, the function creates it.
    Otherwise, it adds the words to the existing ones.

    Parameters
    ----------
    words : list[str]
        Translated words to be added to the history file.
    output_path : Union[str, Path]

    Raises
    ------
    ValueError
        No data to write down.
    """
    path = Path(output_path)

    if not words:
        raise ValueError("No words to write down.")

    is_path_exist = path.exists()

    with path.open(mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not is_path_exist:
            writer.writerow(["translated_words"])

        for word in words:
            writer.writerow([word])
