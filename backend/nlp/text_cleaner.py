"""
Text Cleaner - Preprocessing and cleaning raw text from resumes.
"""

import re
import unicodedata
from typing import Dict, List, Optional


class TextCleaner:
    """Cleans and preprocesses raw resume/JD text."""

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Full text cleaning pipeline.
        Normalizes unicode, removes artifacts, fixes whitespace.
        """
        if not text:
            return ""

        # Normalize unicode characters
        text = unicodedata.normalize("NFKD", text)

        # Replace common unicode artifacts
        replacements = {
            "\u2019": "'", "\u2018": "'",
            "\u201c": '"', "\u201d": '"',
            "\u2013": "-", "\u2014": "-",
            "\u2022": "•", "\u25cf": "•",
            "\u00a0": " ",  # non-breaking space
            "\u200b": "",   # zero-width space
            "\uf0b7": "•",  # bullet
            "\uf0a7": "•",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        # Remove control characters (keep newlines and tabs)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # Fix multiple spaces (but preserve newlines)
        text = re.sub(r'[^\S\n]+', ' ', text)

        # Fix multiple newlines (max 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Strip each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        return text.strip()

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """
        Split resume text into sections based on common headers.
        Returns a dict mapping section names to their content.
        """
        from backend.utils.constants import SECTION_HEADERS

        # Build a pattern that matches any section header
        all_headers = []
        header_to_section = {}
        for section, headers in SECTION_HEADERS.items():
            for header in headers:
                all_headers.append(re.escape(header))
                header_to_section[header.lower()] = section

        # Sort by length (longest first) to match more specific headers
        all_headers.sort(key=len, reverse=True)

        # Pattern: header at start of line, possibly followed by colon or dash
        pattern = r'^(' + '|'.join(all_headers) + r')\s*[:\-–—]?\s*$'

        sections = {}
        current_section = "header"  # Content before any section header
        current_content = []

        for line in text.split('\n'):
            stripped = line.strip()
            match = re.match(pattern, stripped, re.IGNORECASE)

            if match:
                # Save the previous section
                if current_content:
                    content = '\n'.join(current_content).strip()
                    if content:
                        sections[current_section] = content

                # Start new section
                matched_header = match.group(1).lower()
                current_section = header_to_section.get(matched_header, matched_header)
                current_content = []
            else:
                current_content.append(line)

        # Save the last section
        if current_content:
            content = '\n'.join(current_content).strip()
            if content:
                sections[current_section] = content

        return sections

    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses from text."""
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    @staticmethod
    def remove_phone_numbers(text: str) -> str:
        """Remove phone numbers from text."""
        return re.sub(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}', '', text)

    @staticmethod
    def get_clean_text_for_nlp(text: str) -> str:
        """
        Get text optimized for NLP processing.
        Removes contact info, URLs, and extra formatting.
        """
        text = TextCleaner.clean_text(text)
        text = TextCleaner.remove_urls(text)
        text = TextCleaner.remove_emails(text)
        text = TextCleaner.remove_phone_numbers(text)

        # Remove bullet points and list markers
        text = re.sub(r'^[\s]*[•\-\*\>\»\►\●\○]\s*', '', text, flags=re.MULTILINE)

        # Remove standalone numbers (like page numbers)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

        return text.strip()
