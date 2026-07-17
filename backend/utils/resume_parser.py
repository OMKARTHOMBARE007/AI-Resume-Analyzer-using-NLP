"""
Resume Parser - Orchestrates PDF/DOCX parsing → NLP pipeline.
Returns structured resume data.
"""

from typing import Dict, Any, Optional

from backend.utils.pdf_parser import extract_text_from_pdf
from backend.utils.docx_parser import extract_text_from_docx
from backend.nlp.pipeline import nlp_pipeline
from backend.utils.helpers import estimate_years_of_experience


def parse_resume(file_path: str, file_type: str) -> Dict[str, Any]:
    """
    Parse a resume file and extract structured data.

    Args:
        file_path: Path to the uploaded file
        file_type: File extension (.pdf or .docx)

    Returns:
        Dictionary with all extracted resume data
    """
    # Step 1: Extract raw text based on file type
    if file_type.lower() in ('.pdf', 'pdf'):
        raw_text = extract_text_from_pdf(file_path)
    elif file_type.lower() in ('.docx', 'docx'):
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    if not raw_text or len(raw_text.strip()) < 10:
        return {
            "error": "Could not extract text from the file. The file may be scanned or image-based.",
            "raw_text": raw_text or "",
            "parsed_data": {},
        }

    # Step 2: Process through NLP pipeline
    parsed_data = nlp_pipeline.process_resume(raw_text)

    # Step 3: Estimate total years of experience
    experience_years = estimate_years_of_experience(
        parsed_data.get("experience", [])
    )

    # Step 4: Determine highest education
    highest_education = _get_highest_education(parsed_data.get("education", []))

    # Step 5: Compile final result
    result = {
        "raw_text": raw_text,
        "parsed_data": parsed_data,
        "candidate_name": parsed_data.get("name"),
        "candidate_email": parsed_data.get("email"),
        "candidate_phone": parsed_data.get("phone"),
        "candidate_address": parsed_data.get("address"),
        "total_experience_years": experience_years,
        "highest_education": highest_education,
        "skill_count": len(parsed_data.get("skills", [])),
        "section_count": len(parsed_data.get("sections", [])),
    }

    return result


def _get_highest_education(education_entries: list) -> Optional[str]:
    """Determine the highest education level from entries."""
    degree_hierarchy = {
        "phd": 5, "ph.d": 5, "doctorate": 5, "doctoral": 5,
        "master": 4, "m.s.": 4, "m.sc": 4, "m.a.": 4, "m.tech": 4, "mba": 4,
        "mtech": 4, "msc": 4,
        "bachelor": 3, "b.s.": 3, "b.sc": 3, "b.a.": 3, "b.tech": 3, "b.e.": 3,
        "btech": 3, "bsc": 3,
        "associate": 2, "a.s.": 2, "a.a.": 2,
        "diploma": 1, "certificate": 1,
    }

    highest = None
    highest_rank = 0

    for entry in education_entries:
        degree = entry.get("degree", "").lower()
        for keyword, rank in degree_hierarchy.items():
            if keyword in degree and rank > highest_rank:
                highest_rank = rank
                highest = entry.get("degree", "")

    return highest
