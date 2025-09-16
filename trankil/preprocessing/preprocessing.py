from trankil.models.word_entry import WordEntry


def split_meanings(translations: list[list[WordEntry]]) -> list[WordEntry]:
    """Splits the differents meanings of a translation.
    For example a input word can have different meaning.
    Input_word -> translation_1 and Input_word -> translation_2.
    The Linguee API return a list of two translations i.e. two WordEntry.
    But in our Anki deck, since the meaning are differents we expect two different cards.

    Parameters
    ----------
    translations : list[list[WordEntry]]
        Contains translation information.

    Returns
    -------
    list[WordEntry]
        Contains translation information where each element corresponds to one card.
    """
    return [item for sublist in translations for item in sublist]


def keep_frequent_word(translations: list[WordEntry]) -> list[WordEntry]:
    """Keeps only the frequent input word, the source word.
    The Linguee API returns sometimes translations for several source words, for different meanings.
    Some of them are not really used so the function skip it

    Parameters
    ----------
    translations : list[WordEntry]

    Returns
    -------
    list[WordEntry]
    """
    return [translation for translation in translations if translation.featured]


def keep_frequent_translations(translations: list[WordEntry]) -> list[WordEntry]:
    """Keeps only the frequent translations.
    The Linguee API return a lot of different translation,
    this function keeps only the frequent ones.

    Parameters
    ----------
    translations : list[WordEntry]

    Returns
    -------
    list[WordEntry]
    """
    for translation in translations:
        translation.translations = [t for t in translation.translations if t.featured]
    return translations


def preprocess_translations(translations: list[list[WordEntry]]) -> list[WordEntry]:
    """Applies all the preprocessing steps to the Linguee translation to generate Anki cards.

    Parameters
    ----------
    translations : list[list[WordEntry]]
        Raw translations.

    Returns
    -------
    list[WordEntry]
        Preprocessed translation.
    """
    translations = split_meanings(translations)
    translations = keep_frequent_word(translations)
    translations = keep_frequent_translations(translations)
    return translations
