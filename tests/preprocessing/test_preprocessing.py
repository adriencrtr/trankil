import pytest

from trankil.models.word_entry import Example, Translation, WordEntry
from trankil.preprocessing.preprocessing import (
    keep_frequent_translations,
    keep_frequent_word,
    preprocess_translations,
    split_meanings,
)


@pytest.fixture
def example_simple_word_entry() -> list[WordEntry]:
    return [
        WordEntry(
            featured=True,
            text="huppé",
            pos="adjective, masculine",
            translations=[
                Translation(
                    featured=True,
                    text="upmarket",
                    pos="adjective",
                    examples=[
                        Example(
                            src="J'ai déménagé dans un quartier huppé dès que j'ai pu me le permettre.",
                            dst="I moved to an upmarket area as soon as I could afford it.",
                        )
                    ],
                ),
                Translation(
                    featured=False,
                    text="hupped",
                    pos="adjective",
                    examples=[Example(src="", dst="")],
                ),
            ],
        )
    ]


@pytest.fixture
def example_multiple_word_entry() -> list[WordEntry]:
    return [
        WordEntry(
            featured=True,
            text="voir",
            pos="verb",
            translations=[
                Translation(
                    featured=True,
                    text="see",
                    pos="verb",
                    examples=[
                        Example(
                            src="Je suis allé voir les singes au zoo.",
                            dst="I went to see the monkeys at the zoo.",
                        ),
                        Example(
                            src="J'ai vu mon reflet dans le miroir.",
                            dst="I saw my reflection in the mirror.",
                        ),
                    ],
                    usage_frequency="almost_always",
                ),
                Translation(
                    featured=True,
                    text="view",
                    pos="verb",
                    examples=[
                        Example(
                            src="Des milliers de personnes ont vu cette vidéo.",
                            dst="Thousands of people viewed that video.",
                        )
                    ],
                    usage_frequency=None,
                ),
                Translation(
                    featured=False, text="behold", pos="verb", examples=[], usage_frequency=None
                ),
            ],
        ),
        WordEntry(
            featured=False,
            text="se voir",
            pos="verb",
            translations=[
                Translation(
                    featured=True,
                    text="show",
                    pos="verb",
                    examples=[
                        Example(
                            src="Mon dévouement se voit dans mon travail acharné.",
                            dst="My dedication shows in my hard work.",
                        )
                    ],
                    usage_frequency=None,
                ),
                Translation(
                    featured=True,
                    text="meet up",
                    pos="verb",
                    examples=[
                        Example(
                            src="Depuis que j'ai déménagé, nous nous voyons rarement.",
                            dst="Since I moved, we rarely meet up.",
                        )
                    ],
                    usage_frequency=None,
                ),
            ],
        ),
    ]


@pytest.fixture
def example_fetch_linguee_translations(
    example_simple_word_entry: list[WordEntry], example_multiple_word_entry: list[WordEntry]
) -> list[list[WordEntry]]:
    return [example_simple_word_entry, example_multiple_word_entry]


def test_split_meanings_single_meaning(example_fetch_linguee_translations: list[list[WordEntry]]):
    result = split_meanings(example_fetch_linguee_translations)
    assert len(result) == 3
    assert isinstance(result, list)
    assert isinstance(result[0], WordEntry)


def test_keep_frequent_word(example_multiple_word_entry):
    result = keep_frequent_word(example_multiple_word_entry)
    assert isinstance(result, list)
    assert len(result) == 1


def test_keep_frequent_translations(example_simple_word_entry):
    result = keep_frequent_translations(example_simple_word_entry)
    assert isinstance(result, list)
    assert len(result[0].translations) == 1


def test_preprocess_translations_calls_subfunctions(mocker):
    input_translations = [["dummy_word_entry"]]

    mock_split = mocker.patch(
        "trankil.preprocessing.preprocessing.split_meanings",
        side_effect=lambda x: ["split_result"],
    )
    mock_keep_word = mocker.patch(
        "trankil.preprocessing.preprocessing.keep_frequent_word",
        side_effect=lambda x: ["keep_word_result"],
    )
    mock_keep_trans = mocker.patch(
        "trankil.preprocessing.preprocessing.keep_frequent_translations",
        side_effect=lambda x: ["final_result"],
    )

    result = preprocess_translations(input_translations)

    mock_split.assert_called_once_with(input_translations)
    mock_keep_word.assert_called_once_with(["split_result"])
    mock_keep_trans.assert_called_once_with(["keep_word_result"])
    assert result == ["final_result"]
