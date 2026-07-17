"""
Skill Extractor - Extracts and categorizes skills from resume and JD text.
"""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter

from backend.utils.constants import ALL_SKILLS, SKILL_TO_CATEGORY, SKILLS_DATABASE


class SkillExtractor:
    """Extracts skills from text using pattern matching and NLP."""

    def __init__(self):
        # Build compiled regex patterns for multi-word skills
        self.skill_patterns = []
        for skill in sorted(ALL_SKILLS, key=len, reverse=True):
            # Escape special regex characters and create word boundary pattern
            pattern = re.compile(
                r'\b' + re.escape(skill) + r'\b',
                re.IGNORECASE
            )
            self.skill_patterns.append((skill, pattern))

    def extract_skills(self, text: str) -> List[Dict[str, str]]:
        """
        Extract skills from text with their categories.
        Returns list of dicts with name, category, and match context.
        """
        found_skills = []
        seen = set()
        text_lower = text.lower()

        for skill, pattern in self.skill_patterns:
            if skill in seen:
                continue
            if pattern.search(text):
                category = SKILL_TO_CATEGORY.get(skill, "other")
                found_skills.append({
                    "name": skill,
                    "category": category,
                    "proficiency": self._estimate_proficiency(text_lower, skill),
                })
                seen.add(skill)

        return found_skills

    def extract_skill_names(self, text: str) -> Set[str]:
        """Extract just the skill names as a set (for matching)."""
        skills = set()
        for skill, pattern in self.skill_patterns:
            if pattern.search(text):
                skills.add(skill)
        return skills

    def _estimate_proficiency(self, text: str, skill: str) -> str:
        """
        Estimate skill proficiency based on context clues.
        Returns: 'Expert', 'Intermediate', or 'Beginner'.
        """
        # Look for proficiency indicators near the skill mention
        expert_indicators = [
            'expert', 'advanced', 'proficient', 'extensive', 'senior',
            'lead', 'architect', '5+ years', '6+ years', '7+ years',
            '8+ years', '9+ years', '10+ years',
        ]
        intermediate_indicators = [
            'intermediate', 'moderate', 'working knowledge', 'familiar',
            '2+ years', '3+ years', '4+ years',
        ]
        beginner_indicators = [
            'beginner', 'basic', 'learning', 'exposure', 'introductory',
            'fundamental', '1 year', 'coursework',
        ]

        # Check context window around skill mention
        skill_pos = text.find(skill.lower())
        if skill_pos >= 0:
            context_start = max(0, skill_pos - 100)
            context_end = min(len(text), skill_pos + len(skill) + 100)
            context = text[context_start:context_end].lower()

            for indicator in expert_indicators:
                if indicator in context:
                    return "Expert"
            for indicator in intermediate_indicators:
                if indicator in context:
                    return "Intermediate"
            for indicator in beginner_indicators:
                if indicator in context:
                    return "Beginner"

        return "Intermediate"  # Default

    def get_skill_distribution(self, skills: List[Dict[str, str]]) -> Dict[str, int]:
        """Get distribution of skills by category."""
        distribution = Counter()
        for skill in skills:
            category = skill.get("category", "other")
            # Make category names more readable
            readable_category = category.replace("_", " ").title()
            distribution[readable_category] += 1
        return dict(distribution)

    def compare_skills(
        self,
        resume_skills: Set[str],
        jd_skills: Set[str],
    ) -> Dict[str, List[str]]:
        """
        Compare resume skills with JD required skills.
        Returns matched, missing, and extra skills.
        """
        # Normalize for comparison
        resume_lower = {s.lower() for s in resume_skills}
        jd_lower = {s.lower() for s in jd_skills}

        matched = resume_lower & jd_lower
        missing = jd_lower - resume_lower
        extra = resume_lower - jd_lower

        return {
            "matched": sorted(list(matched)),
            "missing": sorted(list(missing)),
            "extra": sorted(list(extra)),
            "match_percentage": (
                len(matched) / max(len(jd_lower), 1) * 100
            ),
        }
