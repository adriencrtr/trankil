from trankil.models.word_entry import WordEntry


def generate_fields(card_data: WordEntry) -> tuple[str, str]:
    """Generates Anki card in HTML format.

    Parameters
    ----------
    card_data : WordEntry
        WordEntry instance that contains minimal information to create an anki card.

    Returns
    -------
    tuple[str, str]
        Front and Back of the anki card.
    """
    original_word = card_data.text
    type_word = card_data.pos
    translations = card_data.translations

    front_parts = [
        f"<div class='word'>{original_word} <span class='type_word'>{type_word}</span></div>"
    ]
    back_parts = [
        f"<div class='word'>{original_word} <span class='type_word'>{type_word}</span></div>"
    ]

    for i, trans in enumerate(translations, start=1):
        front_parts.append(
            f"<div class='group'><div class='translation_title'>__translation_{i}__:</div><ul>"
        )
        back_parts.append(f"<div class='group'><div class='meaning'>{trans.text}</div><ul>")

        for example in trans.examples:
            src, dist = example.src, example.dst
            front_parts.append(f"<li>{src}</li>")
            back_parts.append(f"<li>{src}<br><i>{dist}</i></li>")

        front_parts.append("</ul></div>")
        back_parts.append("</ul></div>")

    return "<br>".join(front_parts), "<br>".join(back_parts)
