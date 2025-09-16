import json
from pathlib import Path

import genanki
import pytest

from trankil.anki.deck_generator import export_deck, generate_deck, load_notes, save_notes


def test_load_notes_file_exists(tmp_path: Path):
    notes = [{"front": "<div>note1</div>", "back": "<div>note2</div>"}]
    file_path = tmp_path / "notes.json"
    file_path.write_text(json.dumps(notes), encoding="utf-8")

    result = load_notes(file_path)

    assert result == notes
    assert isinstance(result, list)


def test_load_notes_file_does_not_exist(tmp_path: Path):
    file_path = tmp_path / "missing.json"

    result = load_notes(file_path)

    assert result == []
    assert isinstance(result, list)


def test_save_notes_creates_file(tmp_path: Path):
    notes = [{"front": "<div>note1</div>", "back": "<div>note2</div>"}]
    file_path = tmp_path / "notes.json"
    save_notes(notes, file_path)

    assert file_path.exists()
    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert content == notes


def test_save_notes_overwrites_file(tmp_path: Path):
    initial_notes = ["<div>old note</div>"]
    new_notes = ["<div>new note</div>"]
    file_path = tmp_path / "notes.json"
    file_path.write_text(json.dumps(initial_notes), encoding="utf-8")
    save_notes(new_notes, file_path)

    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert content == new_notes


def test_export_deck_creates_file(tmp_path: Path):
    deck = genanki.Deck(deck_id=1234567890, name="Test Deck")
    output_path = tmp_path / "subdir" / "test.apkg"
    export_deck(deck, output_path)

    assert output_path.exists()
    assert output_path.suffix == ".apkg"
    assert output_path.stat().st_size > 0


def test_export_deck_overwrites_file(tmp_path: Path):
    deck = genanki.Deck(deck_id=1234567890, name="Test Deck")
    output_path = tmp_path / "deck.apkg"
    output_path.write_text("old content", encoding="utf-8")
    old_size = output_path.stat().st_size
    export_deck(deck, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size != old_size


@pytest.fixture
def mock_settings(tmp_path: Path):
    class DummySettings:
        class App:
            output_folder = tmp_path

        class Deck:
            save_notes_json = "notes.json"
            export_name = "deck.apkg"
            name = "Test Deck"

        app = App()
        deck = Deck()

    return DummySettings()


def test_generate_deck_adds_new_notes(mock_settings, mocker):
    translations = [mocker.Mock()]

    mock_load = mocker.patch(
        "trankil.anki.deck_generator.load_notes", return_value=[{"front": "old", "back": "old"}]
    )
    mock_fields = mocker.patch(
        "trankil.anki.deck_generator.generate_fields", return_value=("front1", "back1")
    )
    mock_save = mocker.patch("trankil.anki.deck_generator.save_notes")
    mock_export = mocker.patch("trankil.anki.deck_generator.export_deck")

    generate_deck(translations, mock_settings)

    mock_load.assert_called_once()
    mock_fields.assert_called_once_with(translations[0])

    saved_notes = mock_save.call_args[0][0]
    assert {"front": "old", "back": "old"} in saved_notes
    assert {"front": "front1", "back": "back1"} in saved_notes

    deck_arg = mock_export.call_args[0][0]
    assert isinstance(deck_arg, genanki.Deck)
    assert deck_arg.name == "Test Deck"
