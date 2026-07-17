"""
spaCy loading helpers.

The API must be able to start without doing network work at import time. If the
full spaCy model is missing, use a lightweight blank English pipeline so the
backend remains runnable and setup can be completed explicitly.
"""

import spacy

from backend.config import settings


def load_spacy_model():
    """Load the configured spaCy model, falling back to a blank English model."""
    try:
        return spacy.load(settings.SPACY_MODEL)
    except OSError:
        nlp = spacy.blank("en")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
        print(
            f"[WARNING] spaCy model '{settings.SPACY_MODEL}' is not installed. "
            "Using a blank English pipeline. Run "
            f"'python -m spacy download {settings.SPACY_MODEL}' for full NLP features."
        )
        return nlp
