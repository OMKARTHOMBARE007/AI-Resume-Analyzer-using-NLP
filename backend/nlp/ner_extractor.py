"""
NER Extractor - Named Entity Recognition for extracting contact info and entities.
"""

import re
from typing import Dict, List, Optional, Any

from backend.nlp.spacy_loader import load_spacy_model

nlp = load_spacy_model()


class NERExtractor:
    """Extracts named entities and contact information from resume text."""

    def __init__(self):
        self.nlp = nlp

    def extract_email(self, text: str) -> Optional[str]:
        """Extract the first email address from text."""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        """Extract the first phone number from text."""
        patterns = [
            r'[\+]?[1]?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'[\+]?\d{1,4}[-.\s]?\d{4,5}[-.\s]?\d{4,5}',
            r'\d{10,12}',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                phone = match.group(0).strip()
                # Validate: should have at least 10 digits
                digits = re.sub(r'\D', '', phone)
                if len(digits) >= 10:
                    return phone
        return None

    def extract_name(self, text: str) -> Optional[str]:
        """
        Extract candidate name from resume text.
        Typically the first line or first PERSON entity.
        """
        lines = text.strip().split('\n')

        # Strategy 1: First non-empty line that looks like a name
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if not line:
                continue
            # Skip lines that are obviously not names
            if '@' in line or re.search(r'\d{3}', line):
                continue
            if len(line.split()) <= 4 and len(line) < 60:
                # Check if it's mostly alphabetic
                alpha_ratio = sum(c.isalpha() or c.isspace() for c in line) / max(len(line), 1)
                if alpha_ratio > 0.8:
                    return line.title()

        # Strategy 2: Use spaCy NER
        doc = self.nlp(text[:1000])  # Only check first 1000 chars
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.title()

        return None

    def extract_address(self, text: str) -> Optional[str]:
        """Extract address from text."""
        # Look for common address patterns
        patterns = [
            r'\d{1,5}\s+\w+\s+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Lane|Ln|Way|Court|Ct)[.,]?\s*\w*[.,]?\s*[A-Z]{2}\s*\d{5}',
            r'[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+[-\s]*\d{5,6}',
            r'[A-Za-z\s]+,\s*[A-Za-z\s]+\s*[-–]\s*\d{5,6}',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()

        # Use spaCy for location entities
        doc = self.nlp(text[:2000])
        locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
        if locations:
            return ", ".join(locations[:3])

        return None

    def extract_urls(self, text: str) -> Dict[str, Optional[str]]:
        """Extract LinkedIn, GitHub, and other URLs."""
        urls = {
            "linkedin": None,
            "github": None,
            "portfolio": None,
            "other": [],
        }

        url_pattern = r'https?://[^\s<>\"\']+|www\.[^\s<>\"\']+' 
        found_urls = re.findall(url_pattern, text)

        for url in found_urls:
            url_lower = url.lower()
            if 'linkedin.com' in url_lower:
                urls["linkedin"] = url
            elif 'github.com' in url_lower:
                urls["github"] = url
            elif not urls["portfolio"]:
                urls["portfolio"] = url
            else:
                urls["other"].append(url)

        return urls

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract all named entities using spaCy."""
        doc = self.nlp(text)
        entities = {}

        for ent in doc.ents:
            label = ent.label_
            if label not in entities:
                entities[label] = []
            if ent.text not in entities[label]:
                entities[label].append(ent.text)

        return entities

    def extract_dates(self, text: str) -> List[str]:
        """Extract date-like patterns from text."""
        patterns = [
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,.-]+\d{4}',
            r'\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}',
            r'\d{4}\s*[-–]\s*(?:\d{4}|[Pp]resent|[Cc]urrent)',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–]\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|[Pp]resent|[Cc]urrent)',
        ]
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)

        return list(set(dates))

    def extract_all(self, text: str) -> Dict[str, Any]:
        """
        Extract all contact info and entities from text.
        Returns a comprehensive dictionary.
        """
        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "address": self.extract_address(text),
            "urls": self.extract_urls(text),
            "entities": self.extract_entities(text),
            "dates": self.extract_dates(text),
        }
