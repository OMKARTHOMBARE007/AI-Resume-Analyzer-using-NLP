"""
General utility functions.
"""

import os
import uuid
from datetime import datetime
from typing import Optional


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving extension."""
    ext = os.path.splitext(original_filename)[1].lower()
    unique_id = uuid.uuid4().hex[:12]
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in ".-_" else "_" for c in os.path.splitext(original_filename)[0])
    return f"{safe_name}_{timestamp}_{unique_id}{ext}"


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.1f} GB"


def estimate_years_of_experience(experience_entries: list) -> int:
    """Estimate total years of experience from experience entries."""
    import re
    total_years = 0

    for entry in experience_entries:
        date_range = entry.get("date_range", "")
        if not date_range:
            continue

        years = re.findall(r'\d{4}', date_range)
        if len(years) >= 2:
            try:
                diff = int(years[-1]) - int(years[0])
                if 0 < diff < 50:
                    total_years += diff
            except ValueError:
                pass
        elif 'present' in date_range.lower() or 'current' in date_range.lower():
            years_found = re.findall(r'\d{4}', date_range)
            if years_found:
                try:
                    start_year = int(years_found[0])
                    diff = datetime.utcnow().year - start_year
                    if 0 < diff < 50:
                        total_years += diff
                except ValueError:
                    pass

    return total_years


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
