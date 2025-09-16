import pytest
import requests

from trankil.api.client import fetch_linguee_translations
from trankil.models.word_entry import WordEntry


@pytest.fixture
def settings():
    class APISettings:
        url = "https://linguee-api.fly.dev/api/v2/translations"
        guess_direction = "false"
        follow_correction = "never"

    class AppSettings:
        src = "fr"
        dst = "en"

    class Settings:
        api = APISettings()
        app = AppSettings()

    return Settings()


def test_fetch_linguee_translations_success(mocker, settings):
    mock_get = mocker.patch("trankil.api.client.requests.get")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "featured": True,
            "text": "lexique",
            "pos": "noun, masculine",
            "translations": [
                {
                    "featured": True,
                    "text": "lexicon",
                    "pos": "noun",
                    "examples": [
                        {
                            "src": "Le lexique juridique comporte de nombreux mots latins.",
                            "dst": "The legal lexicon contains many Latin words.",
                        }
                    ],
                    "usage_frequency": None,
                }
            ],
        }
    ]
    mock_get.return_value = mock_response

    result, errors = fetch_linguee_translations(["lexique"], settings)

    assert isinstance(result[0][0], WordEntry)
    assert errors == []
    mock_get.assert_called_once()


def test_fetch_linguee_translations_500_error(mocker, settings):
    mock_get = mocker.patch("trankil.api.client.requests.get")
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    mock_logger = mocker.patch("trankil.api.client.logger")

    result, errors = fetch_linguee_translations(["blablater"], settings)

    assert result == []
    assert errors == [{"word": "blablater", "error": "500 error, please check the spelling"}]

    mock_logger.warning.assert_called_once()
    assert "500 error for the word" in mock_logger.warning.call_args[0][0]


def test_fetch_linguee_translations_exception(mocker, settings):
    mock_get = mocker.patch("trankil.api.client.requests.get")
    mock_get.side_effect = requests.Timeout("Request timed out")

    mock_logger = mocker.patch("trankil.api.client.logger")

    result, errors = fetch_linguee_translations(["lapin"], settings)

    assert result == []
    assert len(errors) == 1
    assert errors[0]["word"] == "lapin"
    assert "timed out" in errors[0]["error"]

    mock_logger.warning.assert_called_once()
    assert "Failed to fetch" in mock_logger.warning.call_args[0][0]
