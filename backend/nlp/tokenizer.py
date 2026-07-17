"""
Tokenizer - Tokenization, stop-word removal, and lemmatization using spaCy and NLTK.
"""

import re
from typing import List, Set

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

from backend.nlp.spacy_loader import load_spacy_model

nlp = load_spacy_model()


class Tokenizer:
    """Handles tokenization, stop-word removal, and lemmatization."""

    def __init__(self):
        self.nlp = nlp
        try:
            self.stop_words: Set[str] = set(stopwords.words('english'))
        except LookupError:
            self.stop_words = set(self.nlp.Defaults.stop_words)
            print(
                "[WARNING] NLTK stopwords data is not installed. "
                "Using spaCy's built-in stop words."
            )
        # Add custom stop words relevant to resumes
        self.stop_words.update([
            'resume', 'cv', 'curriculum', 'vitae', 'page', 'phone',
            'email', 'address', 'date', 'birth', 'nationality',
        ])

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words using NLTK."""
        try:
            return word_tokenize(text.lower())
        except LookupError:
            return re.findall(r"\b\w+\b", text.lower())

    def tokenize_sentences(self, text: str) -> List[str]:
        """Tokenize text into sentences using NLTK."""
        try:
            return sent_tokenize(text)
        except LookupError:
            return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stop words from token list."""
        return [t for t in tokens if t.lower() not in self.stop_words and len(t) > 1]

    def lemmatize(self, text: str) -> List[str]:
        """Lemmatize text using spaCy."""
        doc = self.nlp(text)
        return [token.lemma_.lower() for token in doc
                if not token.is_stop and not token.is_punct and len(token.text) > 1]

    def get_pos_tags(self, text: str) -> List[tuple]:
        """Get POS tags using spaCy."""
        doc = self.nlp(text)
        return [(token.text, token.pos_) for token in doc]

    def process(self, text: str) -> dict:
        """
        Full tokenization pipeline.
        Returns tokens, lemmas, sentences, and POS tags.
        """
        tokens = self.tokenize(text)
        clean_tokens = self.remove_stopwords(tokens)
        lemmas = self.lemmatize(text)
        sentences = self.tokenize_sentences(text)

        return {
            "tokens": clean_tokens,
            "lemmas": lemmas,
            "sentences": sentences,
            "token_count": len(tokens),
            "unique_tokens": len(set(clean_tokens)),
        }
