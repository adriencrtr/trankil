import csv
from pathlib import Path
from typing import Union


def read_input_csv(file_path: Union[str, Path], n_limit: int) -> list[str]:
    """Reads words from csv file to be translated.

    Parameters
    ----------
    file_path : Union[str, Path]
    n_limit : int
        Limited number of words to be loaded in the list and translated by Trankil.

    Returns
    -------
    list[str]
        Contains at the maximum n_limit words to be translated.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist.
    ValueError
        If the CSV file is empty or missing the required 'word_to_translate' column.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No file found : {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file is empty or missing headers: {path}")

        if "word_to_translate" not in reader.fieldnames:
            raise ValueError("Missing column 'word_to_translate' in CSV file.")

        return [row["word_to_translate"] for row in reader][:n_limit]
