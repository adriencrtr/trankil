import time
import random
from typing import TYPE_CHECKING

import requests

from trankil.logger import logger
from trankil.models.word_entry import WordEntry

if TYPE_CHECKING:
    from trankil.config import Settings


def fetch_linguee_translations(
    words: list[str], settings: "Settings"
) -> tuple[list[list[WordEntry]], list[dict[str, str]]]:
    """Calls the Linguee API for a list of words to retrieve the translation data.
    Words causing server errors are skipped and logged.
    To avoid temporary inaccessibility to the API, a sleeper is added to the function.

    Parameters
    ----------
    words : list[str]
        List of word to query.
    settings : Settings
        url: API endpoint.
        src: Source language (e.g., "fr").
        dst: Target language (e.g., "en").

    Returns
    -------
    tuple[list[list[WordEntry]], list[dict[str, str]]]
        First element of the tuple is the list of list, because a word can have several meanings
        of translation information.
        And the second element is the dictionnary of the erros.
    """
    results: list[list[WordEntry]] = []
    errors: list[dict[str, str]] = []

    for word in words:
        wait_time = random.uniform(5, 8)
        time.sleep(wait_time)
        try:
            resp = requests.get(
                settings.api.url,
                params={
                    "query": word,
                    "src": settings.app.src,
                    "dst": settings.app.dst,
                    "guess_direction": settings.api.guess_direction,
                    "follow_corrections": settings.api.follow_correction,
                },
                timeout=10,
            )

            if resp.status_code == 500:
                logger.warning("500 error for the word: {error_word}", error_word=word)
                errors.append({"word": word, "error": "500 error, please check the spelling"})
                continue

            resp.raise_for_status()
            data = resp.json()
            parsed = [WordEntry(**entry) for entry in data]
            results.append(parsed)

        except Exception as e:
            logger.warning("Failed to fetch the word: {error_word}", error_word=word)
            errors.append({"word": word, "error": str(e)})

    return results, errors
