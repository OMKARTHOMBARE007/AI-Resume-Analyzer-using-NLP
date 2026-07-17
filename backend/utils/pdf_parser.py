"""
PDF Parser - Extracts text from PDF files using pdfplumber and PyMuPDF.
"""

from typing import Optional


def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    Extract text from a PDF file.
    Uses pdfplumber as primary, falls back to PyMuPDF.
    """
    text = _extract_with_pdfplumber(file_path)

    if not text or len(text.strip()) < 50:
        # Fallback to PyMuPDF
        text = _extract_with_pymupdf(file_path)

    return text


def _extract_with_pdfplumber(file_path: str) -> Optional[str]:
    """Extract text using pdfplumber (best for text-based PDFs)."""
    try:
        import pdfplumber

        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

                # Also try to extract tables
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row:
                            row_text = " | ".join(
                                str(cell) if cell else "" for cell in row
                            )
                            text_parts.append(row_text)

        return "\n".join(text_parts) if text_parts else None

    except Exception as e:
        print(f"[PDF Parser] pdfplumber failed: {e}")
        return None


def _extract_with_pymupdf(file_path: str) -> Optional[str]:
    """Extract text using PyMuPDF (better for complex/scanned PDFs)."""
    try:
        import fitz  # PyMuPDF

        text_parts = []
        doc = fitz.open(file_path)

        for page in doc:
            text = page.get_text("text")
            if text:
                text_parts.append(text)

        doc.close()
        return "\n".join(text_parts) if text_parts else None

    except Exception as e:
        print(f"[PDF Parser] PyMuPDF failed: {e}")
        return None
