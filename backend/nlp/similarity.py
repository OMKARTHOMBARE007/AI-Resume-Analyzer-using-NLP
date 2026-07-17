"""
Similarity - Cosine similarity using TF-IDF.
"""

from typing import Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityAnalyzer:
    """
    Computes similarity between resume and job description
    using TF-IDF cosine similarity.
    """

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000,
        )

    def tfidf_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity using TF-IDF vectors.
        Returns a score between 0 and 1.
        """
        try:
            if not text1.strip() or not text2.strip():
                return 0.0

            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(float(similarity), 4)

        except Exception:
            return 0.0

    def semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity using the lightweight TF-IDF fallback.
        Returns a score between 0 and 1.
        """
        return self.tfidf_similarity(text1, text2)

    def compute_combined_similarity(
        self,
        resume_text: str,
        jd_text: str,
        tfidf_weight: float = 0.4,
        semantic_weight: float = 0.6,
    ) -> Dict[str, float]:
        """
        Compute weighted combination of TF-IDF and semantic similarity.
        """
        tfidf_score = self.tfidf_similarity(resume_text, jd_text)
        semantic_score = self.semantic_similarity(resume_text, jd_text)

        combined = (tfidf_weight * tfidf_score) + (semantic_weight * semantic_score)

        return {
            "tfidf_similarity": tfidf_score,
            "semantic_similarity": semantic_score,
            "combined_similarity": round(combined, 4),
            "match_percentage": round(combined * 100, 2),
        }

    def section_similarity(
        self,
        resume_sections: Dict[str, str],
        jd_sections: Dict[str, str],
    ) -> Dict[str, float]:
        """
        Compute similarity for individual sections.
        Returns section-level similarity scores.
        """
        section_scores = {}
        section_mappings = {
            "skills": "skills",
            "experience": "experience",
            "education": "education",
            "projects": "projects",
        }

        for resume_key, jd_key in section_mappings.items():
            resume_section = resume_sections.get(resume_key, "")
            jd_section = jd_sections.get(jd_key, "")

            if resume_section and jd_section:
                score = self.tfidf_similarity(resume_section, jd_section)
                section_scores[resume_key] = score
            else:
                section_scores[resume_key] = 0.0

        return section_scores
