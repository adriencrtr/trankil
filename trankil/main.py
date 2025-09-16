from trankil.anki.deck_generator import generate_deck
from trankil.api.client import fetch_linguee_translations
from trankil.config import get_settings
from trankil.logger import logger
from trankil.preprocessing.preprocessing import preprocess_translations
from trankil.reader import read_input_csv
from trankil.writer import write_errors, remove_translated_word_from_csv, write_translated_word


def run():
    logger.info("Starting of the application")
    settings = get_settings()

    words_to_translate = read_input_csv(settings.app.input_path, settings.app.words_limit)
    logger.info("{n_word_loaded} loaded words", n_word_loaded=len(words_to_translate))

    translations, errors = fetch_linguee_translations(words_to_translate, settings)
    logger.info(
        "API returned {n_word_translated} translations and {n_word_err} errors",
        n_word_translated=len(translations),
        n_word_err=len(errors),
    )

    translations = preprocess_translations(translations)
    logger.info("Data preprocessing is done")

    generate_deck(translations, settings)
    logger.success(
        "The {deck_name} Anki deck generated: {deck_path}",
        deck_name=settings.deck.name,
        deck_path=settings.app.output_folder / settings.deck.export_name,
    )

    if translations:
        words_to_remove = [t.text for t in translations] + [err["word"] for err in errors]
        remove_translated_word_from_csv(words_to_remove, settings.app.input_path)
        logger.info(
            "Translated words are removed from the original file: {file_path}",
            file_path=settings.app.input_path,
        )

        write_translated_word([t.text for t in translations], settings.app.output_history_path)
        logger.info(
            "Translated words are saved in the history file: {file_path}",
            file_path=settings.app.output_history_path,
        )

    if errors:
        write_errors(errors, settings.app.output_errors_path)
        logger.info("Errors exported: {file_path}", file_path=settings.app.output_errors_path)


def main() -> None:
    try:
        run()
    except Exception as e:
        logger.exception("Application crashed due to an unexpected error: {}", e)
        raise


if __name__ == "__main__":
    main()
