import re
import spacy


nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    """
    Basic text cleaning.
    """

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_keywords(text, top_n=15):
    """
    Extract important noun/proper-noun keywords
    using spaCy.
    """

    doc = nlp(text)

    words = []

    for token in doc:

        if (
            token.pos_ in ["NOUN", "PROPN"]
            and not token.is_stop
            and token.is_alpha
        ):
            words.append(
                token.lemma_.lower()
            )

    frequency = {}

    for word in words:

        frequency[word] = (
            frequency.get(word, 0) + 1
        )

    sorted_words = sorted(
        frequency.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        word
        for word, frequency
        in sorted_words[:top_n]
    ]


def chunk_text(
    text,
    chunk_size=500,
    overlap=100
):
    """
    Split text into overlapping chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        if chunk.strip():
            chunks.append(chunk)

        start += (
            chunk_size - overlap
        )

    return chunks