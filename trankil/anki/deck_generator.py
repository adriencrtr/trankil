from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Union

import genanki

from trankil.anki.card_generator import generate_fields
from trankil.anki.model import my_model
from trankil.logger import logger


if TYPE_CHECKING:
    from trankil.config import Settings
    from trankil.models.word_entry import WordEntry


def load_notes(output_path: Union[str, Path]) -> list[dict[str, str]]:
    """Loads and returns existing notes if any.

    Parameters
    ----------
    output_path : Union[str, Path]
        Path where potential existing notes are.

    Returns
    -------
    list
        Contains list of the existing notes in HTML format.
    """
    if output_path.exists():
        logger.info("Existing notes are loaded to build the deck.")
        return json.loads(output_path.read_text(encoding="utf-8"))
    else:
        logger.info("No existing note found. The deck is built from scratch.")
        return []


def save_notes(notes: list[dict[str, str]], output_path: Union[str, Path]) -> None:
    """Writes HTML notes into a json file.

    Parameters
    ----------
    notes : list[dict[str, str]]
        Contains that HTML notes.
    output_path : Union[str, Path]
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("All the notes are saved in the json file.")


def export_deck(deck: genanki.Deck, output_path: Union[str, Path]) -> None:
    """Exports the Anki deck in .apkg format.

    Parameters
    ----------
    deck : genanki.Deck
    output_path : Union[str, Path]
    """
    pkg = genanki.Package(deck)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pkg.write_to_file(output_path)
    logger.success("The deck is saved to the path {deck_path}", deck_path=output_path)


def generate_deck(translations: list[WordEntry], settings: Settings) -> None:
    """Generates and saves the anki deck from the tranlsation data.

    Parameters
    ----------
    translations : list[WordEntry]
        Contains the translation data.
    settings : Settings
    """
    existing_notes = load_notes(settings.app.output_folder / settings.deck.save_notes_json)

    for t in translations:
        front_html, back_html = generate_fields(t)
        note = {"front": front_html, "back": back_html}
        if note not in existing_notes:
            existing_notes.append(note)

    deck = genanki.Deck(1239922789, settings.deck.name)
    for n in existing_notes:
        deck.add_note(genanki.Note(model=my_model, fields=[n["front"], n["back"]]))

    save_notes(existing_notes, settings.app.output_folder / settings.deck.save_notes_json)
    export_deck(deck, settings.app.output_folder / settings.deck.export_name)
