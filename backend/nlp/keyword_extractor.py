"""
Keyword Extractor - TF-IDF based keyword extraction and frequency analysis.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class KeywordExtractor:
    """Extracts keywords using TF-IDF and frequency analysis."""

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=200,
            stop_words='english',
            ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
            min_df=1,
            max_df=0.95,
        )

    def extract_tfidf_keywords(
        self,
        text: str,
        top_n: int = 30,
    ) -> List[Tuple[str, float]]:
        """
        Extract top keywords using TF-IDF scoring.
        Returns list of (keyword, score) tuples.
        """
        try:
            # TF-IDF needs at least some text
            if len(text.split()) < 5:
                return self._extract_simple_keywords(text, top_n)

            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text])
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]

            # Get top N keywords by score
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)

            # Filter out very short or numeric keywords
            filtered = [
                (kw, round(score, 4))
                for kw, score in keyword_scores
                if len(kw) > 2 and not kw.isdigit() and score > 0
            ]

            return filtered[:top_n]

        except Exception:
            return self._extract_simple_keywords(text, top_n)

    def _extract_simple_keywords(self, text: str, top_n: int = 30) -> List[Tuple[str, float]]:
        """Fallback keyword extraction using simple frequency."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'has', 'her', 'was', 'one', 'our', 'out', 'with',
            'that', 'this', 'have', 'from', 'they', 'been', 'will',
            'their', 'would', 'there', 'about', 'which', 'when',
        }
        words = [w for w in words if w not in stop_words]
        counter = Counter(words)
        total = sum(counter.values())
        return [(w, round(c / total, 4)) for w, c in counter.most_common(top_n)]

    def get_keyword_frequency(self, text: str, top_n: int = 20) -> Dict[str, int]:
        """
        Get raw keyword frequency counts.
        Returns dict mapping keywords to their counts.
        """
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'has', 'her', 'was', 'one', 'our', 'out', 'with',
            'that', 'this', 'have', 'from', 'they', 'been', 'will',
            'their', 'would', 'there', 'about', 'which', 'when',
            'also', 'more', 'other', 'into', 'than', 'some', 'very',
        }
        words = [w for w in words if w not in stop_words]
        counter = Counter(words)
        return dict(counter.most_common(top_n))

    def compare_keywords(
        self,
        resume_text: str,
        jd_text: str,
        top_n: int = 20,
    ) -> Dict:
        """
        Compare keywords between resume and JD.
        Returns matched, missing, and frequency data.
        """
        resume_keywords = set(kw for kw, _ in self.extract_tfidf_keywords(resume_text, top_n * 2))
        jd_keywords = set(kw for kw, _ in self.extract_tfidf_keywords(jd_text, top_n * 2))

        matched = resume_keywords & jd_keywords
        missing_from_resume = jd_keywords - resume_keywords

        return {
            "matched_keywords": sorted(list(matched)),
            "missing_keywords": sorted(list(missing_from_resume)),
            "resume_keyword_count": len(resume_keywords),
            "jd_keyword_count": len(jd_keywords),
            "keyword_match_percentage": (
                len(matched) / max(len(jd_keywords), 1) * 100
            ),
        }
