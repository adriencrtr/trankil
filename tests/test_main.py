import os
from pathlib import Path
import subprocess
import sys

import pytest

import trankil.main
from trankil.main import run
from trankil.models.word_entry import Example, Translation, WordEntry


def test_run_main_flow(mocker):
    # --- Mock all the called functions ---
    mock_get_settings = mocker.patch("trankil.main.get_settings")
    mock_read_input = mocker.patch("trankil.main.read_input_csv")
    mock_fetch_api = mocker.patch("trankil.main.fetch_linguee_translations")
    mock_preprocess = mocker.patch("trankil.main.preprocess_translations")
    mock_generate_deck = mocker.patch("trankil.main.generate_deck")
    mock_remove_words = mocker.patch("trankil.main.remove_translated_word_from_csv")
    mock_write_translated = mocker.patch("trankil.main.write_translated_word")
    mock_write_errors = mocker.patch("trankil.main.write_errors")
    mock_logger_info = mocker.patch("trankil.main.logger.info")
    mock_logger_success = mocker.patch("trankil.main.logger.success")

    class DummySettings:
        class App:
            input_path = Path("input.csv")
            output_folder = Path("outputs")
            output_errors_path = Path("errors.csv")
            output_history_path = Path("history.csv")
            words_limit = 10

        class Deck:
            name = "Trankil"
            export_name = Path("test_trankil.apkg")

        app = App()
        deck = Deck()

    settings_instance = DummySettings()
    mock_get_settings.return_value = settings_instance
    mock_read_input.return_value = ["word1", "word2"]
    mock_fetch_api.return_value = (
        [
            [
                WordEntry(
                    featured=True,
                    text="word1",
                    pos="adjective, masculine",
                    translations=[
                        Translation(
                            featured=False,
                            text="hupped",
                            pos="adjective",
                            examples=[Example(src="", dst="")],
                        )
                    ],
                )
            ]
        ],
        [{"word": "word2", "error": "error_message"}],
    )

    mock_preprocess.return_value = [
        WordEntry(
            featured=True,
            text="word1",
            pos="adjective, masculine",
            translations=[
                Translation(
                    featured=False,
                    text="hupped",
                    pos="adjective",
                    examples=[Example(src="", dst="")],
                )
            ],
        )
    ]

    run()

    mock_get_settings.assert_called_once()
    mock_read_input.assert_called_once_with(Path("input.csv"), 10)
    mock_fetch_api.assert_called_once_with(["word1", "word2"], settings_instance)
    mock_preprocess.assert_called_once()
    mock_generate_deck.assert_called_once()
    mock_remove_words.assert_called_once_with(["word1", "word2"], Path("input.csv"))
    mock_write_translated.assert_called_once_with(["word1"], Path("history.csv"))
    mock_write_errors.assert_called_once_with(
        [{"word": "word2", "error": "error_message"}], Path("errors.csv")
    )

    mock_logger_info.assert_called()
    mock_logger_success.assert_called()


def test_main_success(monkeypatch):
    called = {}

    def mock_run():
        called["ok"] = True

    monkeypatch.setattr(trankil.main, "run", mock_run)
    monkeypatch.setattr(
        trankil.main, "logger", type("Logger", (), {"exception": lambda *a, **k: None})()
    )

    trankil.main.main()
    # If mock_run is called during the test then the dict called get values.
    assert called.get("ok", False) is True


def test_main_exception(monkeypatch):
    def mock_run():
        raise ValueError("Fail")

    monkeypatch.setattr(trankil.main, "run", mock_run)

    called = {}

    def fake_exception(msg, e):
        called["msg"] = msg
        called["exc"] = e

    monkeypatch.setattr(
        trankil.main, "logger", type("Logger", (), {"exception": staticmethod(fake_exception)})()
    )

    with pytest.raises(ValueError, match="Fail"):
        trankil.main.main()

    assert "Application crashed due to an unexpected error" in called["msg"]
    assert isinstance(called["exc"], ValueError)
