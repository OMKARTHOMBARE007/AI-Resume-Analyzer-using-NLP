"""
NLP Pipeline - Main orchestrator for all NLP processing.
Chains text cleaning, tokenization, NER, skill extraction, keyword extraction, and more.
"""

from typing import Dict, Any, Optional

from backend.nlp.text_cleaner import TextCleaner
from backend.nlp.tokenizer import Tokenizer
from backend.nlp.ner_extractor import NERExtractor
from backend.nlp.skill_extractor import SkillExtractor
from backend.nlp.keyword_extractor import KeywordExtractor
from backend.nlp.similarity import SimilarityAnalyzer
from backend.nlp.phrase_detector import PhraseDetector


class NLPPipeline:
    """
    Main NLP pipeline that orchestrates all text processing.
    Provides a unified interface for resume and JD analysis.
    """

    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.tokenizer = Tokenizer()
        self.ner_extractor = NERExtractor()
        self.skill_extractor = SkillExtractor()
        self.keyword_extractor = KeywordExtractor()
        self.similarity_analyzer = SimilarityAnalyzer()
        self.phrase_detector = PhraseDetector()

    def process_resume(self, raw_text: str) -> Dict[str, Any]:
        """
        Full NLP processing pipeline for a resume.
        Returns structured data with all extracted information.
        """
        # Step 1: Clean text
        cleaned_text = self.text_cleaner.clean_text(raw_text)

        # Step 2: Extract sections
        sections = self.text_cleaner.extract_sections(cleaned_text)

        # Step 3: Extract contact info and entities
        contact_info = self.ner_extractor.extract_all(cleaned_text)

        # Step 4: Tokenization and lemmatization
        nlp_text = self.text_cleaner.get_clean_text_for_nlp(cleaned_text)
        token_data = self.tokenizer.process(nlp_text)

        # Step 5: Extract skills
        skills = self.skill_extractor.extract_skills(cleaned_text)
        skill_distribution = self.skill_extractor.get_skill_distribution(skills)

        # Step 6: Extract keywords
        keywords = self.keyword_extractor.extract_tfidf_keywords(nlp_text, top_n=30)
        keyword_frequency = self.keyword_extractor.get_keyword_frequency(nlp_text, top_n=20)

        # Step 7: Analyze phrases and action verbs
        action_verbs = self.phrase_detector.detect_action_verbs(cleaned_text)
        bullet_analysis = self.phrase_detector.analyze_bullet_points(cleaned_text)
        grammar_issues = self.phrase_detector.check_grammar_issues(cleaned_text)

        # Step 8: Extract education
        education = self._extract_education(sections.get("education", ""), contact_info)

        # Step 9: Extract experience
        experience = self._extract_experience(sections.get("experience", ""), contact_info)

        # Step 10: Extract projects
        projects = self._extract_projects(sections.get("projects", ""))

        # Step 11: Extract certifications
        certifications = self._extract_certifications(sections.get("certifications", ""))

        # Step 12: Extract languages
        languages = self._extract_languages(sections.get("languages", ""), cleaned_text)

        # Step 13: Extract achievements
        achievements = self._extract_achievements(sections.get("achievements", ""))

        return {
            "name": contact_info.get("name"),
            "email": contact_info.get("email"),
            "phone": contact_info.get("phone"),
            "address": contact_info.get("address"),
            "urls": contact_info.get("urls", {}),
            "summary": sections.get("summary", ""),
            "skills": skills,
            "skill_names": [s["name"] for s in skills],
            "skill_distribution": skill_distribution,
            "education": education,
            "experience": experience,
            "projects": projects,
            "certifications": certifications,
            "languages": languages,
            "achievements": achievements,
            "keywords": [{"keyword": kw, "score": score} for kw, score in keywords],
            "keyword_frequency": keyword_frequency,
            "action_verbs": action_verbs,
            "bullet_analysis": bullet_analysis,
            "grammar_issues": grammar_issues,
            "sections": list(sections.keys()),
            "token_data": token_data,
            "raw_text_length": len(raw_text),
            "cleaned_text_length": len(cleaned_text),
        }

    def process_job_description(self, raw_text: str) -> Dict[str, Any]:
        """
        NLP processing pipeline for a job description.
        Extracts requirements, skills, and keywords.
        """
        cleaned_text = self.text_cleaner.clean_text(raw_text)
        nlp_text = self.text_cleaner.get_clean_text_for_nlp(cleaned_text)

        # Extract skills
        skills = self.skill_extractor.extract_skills(cleaned_text)
        skill_names = [s["name"] for s in skills]

        # Extract keywords
        keywords = self.keyword_extractor.extract_tfidf_keywords(nlp_text, top_n=30)

        # Extract experience requirements
        experience_req = self._extract_experience_requirement(cleaned_text)

        # Extract education requirements
        education_req = self._extract_education_requirement(cleaned_text)

        return {
            "required_skills": skill_names,
            "skills_with_categories": skills,
            "keywords": [kw for kw, _ in keywords],
            "keyword_scores": [{"keyword": kw, "score": score} for kw, score in keywords],
            "required_experience": experience_req,
            "required_education": education_req,
            "cleaned_text": cleaned_text,
        }

    def compare_resume_jd(
        self,
        resume_data: Dict[str, Any],
        jd_data: Dict[str, Any],
        resume_text: str,
        jd_text: str,
    ) -> Dict[str, Any]:
        """
        Compare a processed resume against a processed JD.
        Returns comprehensive matching results.
        """
        # Skill comparison
        resume_skills = set(resume_data.get("skill_names", []))
        jd_skills = set(jd_data.get("required_skills", []))
        skill_comparison = self.skill_extractor.compare_skills(resume_skills, jd_skills)

        # Keyword comparison
        keyword_comparison = self.keyword_extractor.compare_keywords(
            resume_text, jd_text, top_n=25
        )

        # Similarity scores
        similarity = self.similarity_analyzer.compute_combined_similarity(
            resume_text, jd_text
        )

        # Calculate strengths and weaknesses
        strengths = self._identify_strengths(resume_data, jd_data, skill_comparison)
        weaknesses = self._identify_weaknesses(resume_data, jd_data, skill_comparison)

        return {
            "skill_comparison": skill_comparison,
            "keyword_comparison": keyword_comparison,
            "similarity": similarity,
            "strengths": strengths,
            "weaknesses": weaknesses,
        }

    def _extract_education(self, education_text: str, contact_info: Dict) -> list:
        """Extract education entries from the education section."""
        import re
        from backend.utils.constants import DEGREE_KEYWORDS

        entries = []
        if not education_text:
            return entries

        # Split by common delimiters (double newline or degree keywords)
        lines = education_text.split('\n')
        current_entry = {}

        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue

            line_lower = line.lower()

            # Check for degree keywords
            has_degree = any(deg in line_lower for deg in DEGREE_KEYWORDS)

            if has_degree and not current_entry.get("degree"):
                current_entry["degree"] = line
            elif not current_entry.get("institution") and not has_degree:
                # Check if this looks like an institution name
                if len(line) > 5 and not re.match(r'^\d', line):
                    current_entry["institution"] = line
            else:
                # Check for dates
                date_match = re.search(r'\d{4}', line)
                if date_match:
                    current_entry["year"] = date_match.group(0)
                    if "date_range" not in current_entry:
                        current_entry["date_range"] = line

                # Check for GPA
                gpa_match = re.search(r'(?:GPA|CGPA|Grade)[:\s]*(\d+\.?\d*)', line, re.IGNORECASE)
                if gpa_match:
                    current_entry["gpa"] = gpa_match.group(1)

        if current_entry:
            entries.append(current_entry)

        return entries

    def _extract_experience(self, experience_text: str, contact_info: Dict) -> list:
        """Extract work experience entries."""
        import re

        entries = []
        if not experience_text:
            return entries

        # Split by common patterns (company names are usually followed by dates)
        lines = experience_text.split('\n')
        current_entry = {}
        current_bullets = []

        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    current_entry["description"] = current_bullets
                    entries.append(current_entry)
                    current_entry = {}
                    current_bullets = []
                continue

            # Check if this is a new entry (usually has a date range)
            date_range = re.search(
                r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{4}\s*[-–]\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{4}|[Pp]resent|[Cc]urrent)',
                line, re.IGNORECASE
            )
            year_range = re.search(r'\d{4}\s*[-–]\s*(?:\d{4}|[Pp]resent|[Cc]urrent)', line)

            is_bullet = line.startswith(('•', '-', '*', '►', '●', '○')) or re.match(r'^\d+[\.\)]', line)

            if (date_range or year_range) and not is_bullet:
                if current_entry:
                    current_entry["description"] = current_bullets
                    entries.append(current_entry)
                    current_bullets = []

                current_entry = {
                    "title_company": line,
                    "date_range": (date_range or year_range).group(0) if (date_range or year_range) else "",
                }
            elif is_bullet:
                bullet_text = re.sub(r'^[•\-\*►●○]\s*|\d+[\.\)]\s*', '', line)
                current_bullets.append(bullet_text)
            elif current_entry and not current_entry.get("title"):
                current_entry["title"] = line

        if current_entry:
            current_entry["description"] = current_bullets
            entries.append(current_entry)

        return entries

    def _extract_projects(self, projects_text: str) -> list:
        """Extract project entries."""
        projects = []
        if not projects_text:
            return projects

        lines = projects_text.split('\n')
        current_project = {}
        current_bullets = []

        for line in lines:
            line = line.strip()
            if not line:
                if current_project:
                    current_project["description"] = current_bullets
                    projects.append(current_project)
                    current_project = {}
                    current_bullets = []
                continue

            is_bullet = line.startswith(('•', '-', '*', '►', '●', '○'))

            if not is_bullet and not current_project.get("name"):
                current_project["name"] = line
            elif is_bullet:
                bullet_text = line.lstrip('•-*►●○ ')
                current_bullets.append(bullet_text)
            elif current_project.get("name"):
                current_bullets.append(line)

        if current_project:
            current_project["description"] = current_bullets
            projects.append(current_project)

        return projects

    def _extract_certifications(self, cert_text: str) -> list:
        """Extract certification entries."""
        certs = []
        if not cert_text:
            return certs

        for line in cert_text.split('\n'):
            line = line.strip()
            if line and len(line) > 3:
                line = line.lstrip('•-*►●○ ')
                if line:
                    certs.append({"name": line})

        return certs

    def _extract_languages(self, lang_text: str, full_text: str) -> list:
        """Extract language proficiencies."""
        languages = []

        # Common languages to look for
        common_languages = [
            "english", "hindi", "spanish", "french", "german", "chinese",
            "japanese", "korean", "arabic", "portuguese", "russian", "italian",
            "dutch", "swedish", "turkish", "marathi", "tamil", "telugu",
            "bengali", "gujarati", "kannada", "malayalam", "punjabi", "urdu",
        ]

        text_to_check = lang_text if lang_text else full_text
        text_lower = text_to_check.lower()

        for lang in common_languages:
            if lang in text_lower:
                languages.append(lang.title())

        return languages if languages else ["English"]  # Default

    def _extract_achievements(self, achievements_text: str) -> list:
        """Extract achievements/awards."""
        achievements = []
        if not achievements_text:
            return achievements

        for line in achievements_text.split('\n'):
            line = line.strip().lstrip('•-*►●○ ')
            if line and len(line) > 5:
                achievements.append(line)

        return achievements

    def _extract_experience_requirement(self, text: str) -> str:
        """Extract years of experience required from JD."""
        import re
        patterns = [
            r'(\d+\+?\s*[-–]?\s*\d*\+?\s*years?\s*(?:of\s+)?experience)',
            r'(minimum\s+\d+\s*years?)',
            r'(at\s+least\s+\d+\s*years?)',
            r'(\d+\+?\s*years?\s+of\s+\w+\s+experience)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""

    def _extract_education_requirement(self, text: str) -> str:
        """Extract education requirement from JD."""
        import re
        from backend.utils.constants import DEGREE_KEYWORDS

        for keyword in DEGREE_KEYWORDS:
            pattern = rf"({keyword}['\s]?s?\s+(?:degree\s+)?(?:in\s+)?[\w\s,]+)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()[:100]

        return ""

    def _identify_strengths(
        self, resume_data: Dict, jd_data: Dict, skill_comparison: Dict
    ) -> list:
        """Identify resume strengths relative to JD."""
        strengths = []

        match_pct = skill_comparison.get("match_percentage", 0)
        if match_pct >= 70:
            strengths.append(f"Strong skill match ({match_pct:.0f}% of required skills)")
        elif match_pct >= 50:
            strengths.append(f"Good skill match ({match_pct:.0f}% of required skills)")

        if len(resume_data.get("experience", [])) >= 2:
            strengths.append("Multiple relevant work experiences listed")

        if resume_data.get("certifications"):
            strengths.append(f"{len(resume_data['certifications'])} certification(s) listed")

        if resume_data.get("projects"):
            strengths.append(f"{len(resume_data['projects'])} project(s) demonstrated")

        action_verbs = resume_data.get("action_verbs", {})
        if action_verbs.get("strong_verb_ratio", 0) > 0.6:
            strengths.append("Strong action verbs used effectively")

        if len(resume_data.get("skill_names", [])) > 10:
            strengths.append("Diverse skill set demonstrated")

        if resume_data.get("education"):
            strengths.append("Educational background clearly presented")

        return strengths

    def _identify_weaknesses(
        self, resume_data: Dict, jd_data: Dict, skill_comparison: Dict
    ) -> list:
        """Identify resume weaknesses relative to JD."""
        weaknesses = []

        missing = skill_comparison.get("missing", [])
        if len(missing) > 5:
            weaknesses.append(f"Missing {len(missing)} required skills")
        elif len(missing) > 0:
            weaknesses.append(f"Missing skills: {', '.join(missing[:5])}")

        if not resume_data.get("certifications"):
            weaknesses.append("No certifications listed")

        if not resume_data.get("projects"):
            weaknesses.append("No projects listed")

        grammar_issues = resume_data.get("grammar_issues", [])
        if grammar_issues:
            weaknesses.append(f"{len(grammar_issues)} grammar issue(s) found")

        action_verbs = resume_data.get("action_verbs", {})
        if action_verbs.get("weak_verbs"):
            weaknesses.append("Weak action verbs detected - consider using stronger alternatives")

        bullet_analysis = resume_data.get("bullet_analysis", {})
        if bullet_analysis.get("average_quality", 100) < 50:
            weaknesses.append("Bullet points could be improved with more quantifiable results")

        if not resume_data.get("summary"):
            weaknesses.append("Missing professional summary/objective")

        return weaknesses


# Singleton instance
nlp_pipeline = NLPPipeline()
