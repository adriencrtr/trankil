"""Application settings module.

Defines structured settings for the app, deck, and API.
Loaded from .env via pydantic-settings.
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from trankil.logger import logger


class AppSettings(BaseModel):
    src: str
    dst: str
    words_limit: int = 5

    @property
    def input_path(self) -> Path:
        return Path(f"data/{self.src}_{self.dst}/input_words.csv")

    @property
    def output_folder(self) -> Path:
        return Path(f"outputs/{self.src}_{self.dst}")

    @property
    def output_errors_path(self) -> Path:
        return Path(f"{self.output_folder}/errors.csv")

    @property
    def output_history_path(self) -> Path:
        return Path(f"{self.output_folder}/history.csv")


class DeckSettings(BaseModel):
    name: str = "Trankil"

    @property
    def export_name(self) -> Path:
        return Path(f"{self.name}.apkg")

    @property
    def save_notes_json(self) -> Path:
        return Path(f"{self.name}.json")


class APISettings(BaseModel):
    url: str = "https://linguee-api.fly.dev/api/v2/translations"
    guess_direction: bool = False
    follow_correction: Literal["never", "always", "on_empty_translations"] = "never"


class Settings(BaseSettings):
    app: AppSettings
    api: APISettings = APISettings()
    deck: DeckSettings = DeckSettings()

    model_config = SettingsConfigDict(
        env_prefix="", env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8"
    )


class SettingsError(Exception):
    """Raised when application settings cannot be loaded."""


def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        logger.error("Error while loading settings from .env file:\n{}", e)
        raise SettingsError("Invalid configuration. Please check your .env file.") from e
