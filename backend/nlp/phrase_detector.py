"""
Phrase Detector - POS tagging, action verb detection, and phrase quality scoring.
"""

import re
from typing import Dict, List, Tuple

from backend.nlp.spacy_loader import load_spacy_model
from backend.utils.constants import STRONG_ACTION_VERBS, WEAK_ACTION_VERBS, VERB_IMPROVEMENTS

nlp = load_spacy_model()


class PhraseDetector:
    """Analyzes phrase quality, action verbs, and provides grammar insights."""

    def __init__(self):
        self.nlp = nlp

    def detect_action_verbs(self, text: str) -> Dict[str, List]:
        """
        Detect action verbs used in the resume.
        Returns strong and weak verbs found.
        """
        doc = self.nlp(text)
        strong_found = []
        weak_found = []
        all_verbs = []

        for token in doc:
            if token.pos_ == "VERB":
                verb = token.lemma_.lower()
                all_verbs.append(verb)

                if verb in STRONG_ACTION_VERBS:
                    if verb not in strong_found:
                        strong_found.append(verb)
                elif verb in WEAK_ACTION_VERBS or any(
                    phrase in text.lower() for phrase in WEAK_ACTION_VERBS if ' ' in phrase
                ):
                    if verb not in weak_found:
                        weak_found.append(verb)

        # Also check multi-word weak phrases
        text_lower = text.lower()
        for phrase in WEAK_ACTION_VERBS:
            if ' ' in phrase and phrase in text_lower:
                if phrase not in weak_found:
                    weak_found.append(phrase)

        return {
            "strong_verbs": strong_found,
            "weak_verbs": weak_found,
            "total_verbs": len(set(all_verbs)),
            "strong_verb_ratio": (
                len(strong_found) / max(len(strong_found) + len(weak_found), 1)
            ),
        }

    def suggest_verb_improvements(self, text: str) -> List[Dict[str, str]]:
        """
        Suggest replacements for weak action verbs.
        Returns list of suggestions with original and alternatives.
        """
        suggestions = []
        text_lower = text.lower()

        for weak_verb, alternatives in VERB_IMPROVEMENTS.items():
            if weak_verb in text_lower:
                suggestions.append({
                    "original": weak_verb,
                    "alternatives": alternatives,
                    "suggestion": f"Replace '{weak_verb}' with '{alternatives[0]}' for stronger impact.",
                })

        return suggestions

    def analyze_bullet_points(self, text: str) -> Dict:
        """
        Analyze quality of bullet points in resume.
        Checks for quantifiable achievements, action verb usage, etc.
        """
        # Split into bullet points
        bullet_patterns = [
            r'[•\-\*\►\●\○]\s*(.*)',
            r'^\s*(?:\d+[\.\)]\s*)(.*)',
        ]

        bullets = []
        for pattern in bullet_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            bullets.extend(matches)

        if not bullets:
            # Try splitting by newlines if no bullets found
            bullets = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 20]

        analysis = {
            "total_bullets": len(bullets),
            "with_numbers": 0,
            "with_strong_verbs": 0,
            "too_short": 0,
            "too_long": 0,
            "quality_scores": [],
        }

        for bullet in bullets:
            score = 0

            # Check for quantifiable results
            if re.search(r'\d+[%\+]?|\$[\d,]+|\d+x', bullet):
                analysis["with_numbers"] += 1
                score += 30

            # Check for strong action verbs
            first_word = bullet.split()[0].lower() if bullet.split() else ""
            if first_word in STRONG_ACTION_VERBS:
                analysis["with_strong_verbs"] += 1
                score += 30

            # Check length
            word_count = len(bullet.split())
            if word_count < 5:
                analysis["too_short"] += 1
            elif word_count > 30:
                analysis["too_long"] += 1
                score += 10
            else:
                score += 20

            # Bonus for specificity
            if any(word in bullet.lower() for word in ['increased', 'decreased', 'improved', 'reduced', 'saved', 'grew']):
                score += 20

            analysis["quality_scores"].append(min(score, 100))

        analysis["average_quality"] = (
            sum(analysis["quality_scores"]) / max(len(analysis["quality_scores"]), 1)
        )

        return analysis

    def get_pos_distribution(self, text: str) -> Dict[str, int]:
        """Get distribution of parts of speech in the text."""
        doc = self.nlp(text)
        pos_counts = {}
        for token in doc:
            if token.pos_ not in pos_counts:
                pos_counts[token.pos_] = 0
            pos_counts[token.pos_] += 1
        return pos_counts

    def check_grammar_issues(self, text: str) -> List[Dict[str, str]]:
        """
        Basic grammar checks for common resume issues.
        """
        issues = []

        # Check for first person pronouns (resumes shouldn't have "I", "my", "me")
        first_person = re.findall(r'\b(?:I|my|me|myself)\b', text)
        if first_person:
            issues.append({
                "type": "first_person",
                "severity": "medium",
                "message": "Avoid first-person pronouns (I, my, me) in resumes. Use implied subject instead.",
                "count": len(first_person),
            })

        # Check for passive voice indicators
        passive_indicators = re.findall(
            r'\b(?:was|were|been|being)\s+(?:\w+ed|given|made|done|taken)\b',
            text, re.IGNORECASE
        )
        if passive_indicators:
            issues.append({
                "type": "passive_voice",
                "severity": "low",
                "message": f"Found {len(passive_indicators)} potential passive voice constructions. Prefer active voice.",
                "count": len(passive_indicators),
            })

        # Check for informal language
        informal_words = re.findall(
            r'\b(?:stuff|things|a lot|gonna|wanna|kinda|sorta|etc|cool|awesome|nice)\b',
            text, re.IGNORECASE
        )
        if informal_words:
            issues.append({
                "type": "informal_language",
                "severity": "medium",
                "message": "Found informal language. Use professional terminology.",
                "count": len(informal_words),
            })

        return issues
