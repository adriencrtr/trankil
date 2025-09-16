from trankil.models.word_entry import WordEntry, Translation, Example
from trankil.anki.card_generator import generate_fields


def test_generate_fields():
    word = WordEntry(
        featured=True,
        text="go",
        pos="verb",
        translations=[
            Translation(
                featured=True,
                text="aller",
                pos="verb",
                examples=[
                    Example(src="I go to school", dst="Je vais à l'école"),
                    Example(src="Let's go!", dst="Allons-y !"),
                ],
            ),
            Translation(
                featured=True,
                text="partir",
                pos="verb",
                examples=[Example(src="He went away", dst="Il est parti")],
            ),
        ],
    )

    front, back = generate_fields(word)

    assert "<div class='word'>go <span class='type_word'>verb</span></div>" in front
    assert "__translation_1__" in front
    assert "<div class='meaning'>aller</div>" in back
    assert "I go to school" in front
    assert "Je vais à l'école" not in front
    assert "Je vais à l'école" in back
    assert "Allons-y !" in back
    assert "<div class='meaning'>partir</div>" in back
    assert "Il est parti" not in front
    assert "Il est parti" in back
