import pytest
from trankil.models.word_entry import Example, Translation, WordEntry


def test_example_valid():
    example = Example(src="hello", dst="bonjour")
    assert example.src == "hello"
    assert example.dst == "bonjour"


def test_example_invalid():
    with pytest.raises(Exception):
        Example(src="hello")  # dst missing


def test_translation_valid():
    translation = Translation(
        featured=True,
        text="bonjour",
        pos="noun",
        examples=[Example(src="hello", dst="bonjour")],
        usage_frequency="high",
    )
    assert translation.text == "bonjour"
    assert translation.usage_frequency == "high"
    assert isinstance(translation.examples[0], Example)


def test_translation_optional_usage_frequency():
    translation = Translation(
        featured=False, text="salut", pos="interj", examples=[Example(src="hi", dst="salut")]
    )
    assert translation.usage_frequency is None


def test_translation_invalid():
    with pytest.raises(Exception):
        Translation(
            featured=True,
            # text="bonjour",
            pos="noun",
            examples=[Example(src="hello", dst="bonjour")],
            usage_frequency="high",
        )


def test_word_entry_valid():
    word_entry = WordEntry(
        featured=True,
        text="word",
        pos="noun",
        translations=[
            Translation(
                featured=True, text="mot", pos="noun", examples=[Example(src="word", dst="mot")]
            )
        ],
    )
    assert word_entry.text == "word"
    assert len(word_entry.translations) == 1
    assert isinstance(word_entry.translations[0], Translation)


def test_invalid_translation_missing_field():
    with pytest.raises(Exception):
        Translation(
            featured=True,
            text="bonjour",
            # missing pos
            examples=[Example(src="hello", dst="bonjour")],
        )
