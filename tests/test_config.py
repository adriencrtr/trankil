from pathlib import Path

from pydantic import ValidationError
import pytest

from trankil.config import (
    APISettings,
    AppSettings,
    DeckSettings,
    get_settings,
    SettingsError,
    Settings,
)


def test_appsettings_valid():
    app = AppSettings(src="en", dst="fr", words_limit=100)
    assert app.src == "en"
    assert app.dst == "fr"
    assert app.words_limit == 100


def test_appsettings_missing_field():
    with pytest.raises(ValidationError):
        AppSettings(src="en", words_limit=100)


def test_decksettings_defaults_and_properties():
    deck = DeckSettings()
    assert deck.name == "Trankil"
    assert deck.export_name.name == "Trankil.apkg"
    assert deck.save_notes_json.name == "Trankil.json"


def test_apisettings_defaults():
    api = APISettings()
    assert api.url.startswith("https://")
    assert api.guess_direction == False
    assert api.follow_correction == "never"


def test_appsettings_paths_properties():
    app = AppSettings(src="en", dst="fr", words_limit=10)
    assert app.input_path == Path("data/en_fr/input_words.csv")
    assert app.output_folder == Path("outputs/en_fr")
    assert app.output_errors_path == Path("outputs/en_fr/errors.csv")
    assert app.output_history_path == Path("outputs/en_fr/history.csv")


def test_settings_env(monkeypatch):
    monkeypatch.setenv("APP__SRC", "en")
    monkeypatch.setenv("APP__DST", "fr")
    monkeypatch.setenv("APP__WORDS_LIMIT", "5")

    settings = get_settings()

    assert isinstance(settings, Settings)

    assert settings.app.src == "en"
    assert settings.app.dst == "fr"
    assert settings.app.words_limit == 5

    assert settings.app.input_path == Path("data/en_fr/input_words.csv")
    assert settings.app.output_folder == Path("outputs/en_fr")
    assert settings.app.output_errors_path.name.startswith("errors")

    assert settings.api.url == "https://linguee-api.fly.dev/api/v2/translations"
    assert settings.deck.name == "Trankil"
    assert settings.deck.export_name.name.startswith("Trankil")


def test_get_settings_invalid_env(monkeypatch):
    monkeypatch.setenv("APP__WORDS_LIMIT", "not_a_number")

    with pytest.raises(SettingsError) as exc_info:
        get_settings()

    assert "Invalid configuration" in str(exc_info.value)
