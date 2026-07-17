"""
Suggestion Service - AI-powered resume improvement recommendations.
"""

from typing import Dict, Any, List, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.resume import Resume
from backend.models.job_description import JobDescription
from backend.models.resume_score import ResumeScore
from backend.utils.constants import (
    CERTIFICATION_SUGGESTIONS, SKILL_TO_CATEGORY, VERB_IMPROVEMENTS,
)
from backend.nlp.pipeline import nlp_pipeline


def generate_suggestions(
    db: Session,
    resume_id: int,
    user_id: int,
    jd_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate comprehensive AI suggestions for resume improvement.
    Returns categorized suggestions with priorities.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    resume_data = resume.parsed_data or {}
    jd_data = {}
    score_data = None

    if jd_id:
        jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.user_id == user_id).first()
        if jd:
            jd_data = jd.parsed_data or {}
            score_data = db.query(ResumeScore).filter(
                ResumeScore.resume_id == resume_id,
                ResumeScore.jd_id == jd_id,
            ).first()

    suggestions = []

    # 1. Missing Skills Suggestions
    suggestions.extend(_suggest_missing_skills(resume_data, jd_data, score_data))

    # 2. Certification Suggestions
    suggestions.extend(_suggest_certifications(resume_data, jd_data))

    # 3. Project Suggestions
    suggestions.extend(_suggest_projects(resume_data, jd_data))

    # 4. Action Verb Improvements
    suggestions.extend(_suggest_action_verbs(resume_data))

    # 5. Grammar Improvements
    suggestions.extend(_suggest_grammar_fixes(resume_data))

    # 6. Formatting Suggestions
    suggestions.extend(_suggest_formatting(resume_data))

    # 7. ATS Optimization Tips
    suggestions.extend(_suggest_ats_optimization(resume_data, jd_data, score_data))

    return {
        "resume_id": resume_id,
        "jd_id": jd_id,
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
    }


def _suggest_missing_skills(
    resume_data: Dict, jd_data: Dict, score_data: Optional[Any]
) -> List[Dict]:
    """Suggest missing skills to learn."""
    suggestions = []

    missing_skills = []
    if score_data and score_data.missing_skills:
        missing_skills = score_data.missing_skills
    elif jd_data.get("required_skills"):
        resume_skills = set(s.lower() for s in resume_data.get("skill_names", []))
        jd_skills = set(s.lower() for s in jd_data.get("required_skills", []))
        missing_skills = list(jd_skills - resume_skills)

    if missing_skills:
        # Group by category
        categorized = {}
        for skill in missing_skills[:10]:
            category = SKILL_TO_CATEGORY.get(skill.lower(), "other")
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(skill)

        for category, skills in categorized.items():
            suggestions.append({
                "category": "skills",
                "priority": "high",
                "title": f"Learn Missing {category.replace('_', ' ').title()} Skills",
                "description": f"The job requires these {category.replace('_', ' ')} skills that are not on your resume.",
                "details": [f"• {skill.title()}" for skill in skills],
            })

    return suggestions


def _suggest_certifications(resume_data: Dict, jd_data: Dict) -> List[Dict]:
    """Suggest relevant certifications."""
    suggestions = []
    resume_skills = set(s.lower() for s in resume_data.get("skill_names", []))
    existing_certs = [c.get("name", "").lower() for c in resume_data.get("certifications", [])]

    # Find relevant certification categories
    relevant_categories = set()
    for skill in resume_skills:
        category = SKILL_TO_CATEGORY.get(skill, "")
        if category in CERTIFICATION_SUGGESTIONS:
            relevant_categories.add(category)

    if not relevant_categories:
        relevant_categories = {"web_frameworks", "cloud_platforms"}

    for category in relevant_categories:
        certs = CERTIFICATION_SUGGESTIONS.get(category, [])
        new_certs = [c for c in certs if c.lower() not in existing_certs]

        if new_certs:
            suggestions.append({
                "category": "certifications",
                "priority": "medium",
                "title": f"Recommended {category.replace('_', ' ').title()} Certifications",
                "description": "Adding these certifications can significantly boost your profile.",
                "details": [f"• {cert}" for cert in new_certs[:3]],
            })

    if not resume_data.get("certifications"):
        suggestions.append({
            "category": "certifications",
            "priority": "high",
            "title": "Add Certifications Section",
            "description": "Your resume has no certifications listed. Adding relevant certifications can increase your ATS score by 5-15%.",
            "details": [],
        })

    return suggestions


def _suggest_projects(resume_data: Dict, jd_data: Dict) -> List[Dict]:
    """Suggest project ideas based on missing skills."""
    suggestions = []

    if not resume_data.get("projects"):
        suggestions.append({
            "category": "projects",
            "priority": "high",
            "title": "Add Projects Section",
            "description": "Including projects demonstrates practical application of your skills. Add 2-3 relevant projects.",
            "details": [
                "• Include project name, brief description, and technologies used",
                "• Highlight measurable outcomes or impact",
                "• Link to GitHub/live demo if available",
            ],
        })
    elif len(resume_data.get("projects", [])) < 2:
        missing_skills = []
        if jd_data.get("required_skills"):
            resume_skills = set(s.lower() for s in resume_data.get("skill_names", []))
            jd_skills = set(s.lower() for s in jd_data.get("required_skills", []))
            missing_skills = list(jd_skills - resume_skills)[:5]

        if missing_skills:
            suggestions.append({
                "category": "projects",
                "priority": "medium",
                "title": "Add Projects Using Missing Skills",
                "description": "Build projects that demonstrate the skills the job requires.",
                "details": [
                    f"• Build a project using: {', '.join(missing_skills[:3])}",
                    "• Focus on real-world problem solving",
                    "• Include quantifiable results",
                ],
            })

    return suggestions


def _suggest_action_verbs(resume_data: Dict) -> List[Dict]:
    """Suggest stronger action verbs."""
    suggestions = []
    action_verbs = resume_data.get("action_verbs", {})
    weak_verbs = action_verbs.get("weak_verbs", [])

    if weak_verbs:
        details = []
        for verb in weak_verbs[:5]:
            alternatives = VERB_IMPROVEMENTS.get(verb, ["achieved", "delivered", "executed"])
            details.append(f"• Replace \"{verb}\" → \"{alternatives[0]}\" or \"{alternatives[1] if len(alternatives) > 1 else alternatives[0]}\"")

        suggestions.append({
            "category": "action_verbs",
            "priority": "medium",
            "title": "Use Stronger Action Verbs",
            "description": "Replace weak verbs with powerful action verbs to make your achievements stand out.",
            "details": details,
        })

    if action_verbs.get("strong_verb_ratio", 1) < 0.5:
        suggestions.append({
            "category": "action_verbs",
            "priority": "medium",
            "title": "Increase Strong Action Verb Usage",
            "description": "Start each bullet point with a strong action verb like 'Spearheaded', 'Engineered', 'Optimized', 'Architected'.",
            "details": [],
        })

    return suggestions


def _suggest_grammar_fixes(resume_data: Dict) -> List[Dict]:
    """Suggest grammar improvements."""
    suggestions = []
    grammar_issues = resume_data.get("grammar_issues", [])

    for issue in grammar_issues:
        suggestions.append({
            "category": "grammar",
            "priority": issue.get("severity", "low"),
            "title": f"Grammar: {issue.get('type', 'Issue').replace('_', ' ').title()}",
            "description": issue.get("message", ""),
            "details": [],
        })

    return suggestions


def _suggest_formatting(resume_data: Dict) -> List[Dict]:
    """Suggest formatting improvements."""
    suggestions = []
    sections = resume_data.get("sections", [])

    # Check for missing essential sections
    essential_sections = {
        "summary": "Professional Summary",
        "experience": "Work Experience",
        "education": "Education",
        "skills": "Skills",
    }

    for section_key, section_name in essential_sections.items():
        if section_key not in sections:
            suggestions.append({
                "category": "formatting",
                "priority": "high" if section_key in ("experience", "skills") else "medium",
                "title": f"Add {section_name} Section",
                "description": f"Your resume is missing a {section_name} section, which is essential for ATS parsing.",
                "details": [],
            })

    # Check text length
    text_length = resume_data.get("cleaned_text_length", 0)
    if text_length < 300:
        suggestions.append({
            "category": "formatting",
            "priority": "high",
            "title": "Resume Too Short",
            "description": "Your resume appears very short. Add more detail about your experience, skills, and achievements.",
            "details": [],
        })
    elif text_length > 6000:
        suggestions.append({
            "category": "formatting",
            "priority": "medium",
            "title": "Consider Shortening Resume",
            "description": "Your resume is quite long. For most positions, aim for 1-2 pages.",
            "details": [],
        })

    # Check bullet point quality
    bullet_analysis = resume_data.get("bullet_analysis", {})
    if bullet_analysis.get("with_numbers", 0) == 0 and bullet_analysis.get("total_bullets", 0) > 3:
        suggestions.append({
            "category": "formatting",
            "priority": "high",
            "title": "Add Quantifiable Results",
            "description": "None of your bullet points include numbers. Add metrics like percentages, dollar amounts, or counts.",
            "details": [
                '• "Increased sales by 25% in Q3 2024"',
                '• "Reduced load time from 5s to 1.2s (76% improvement)"',
                '• "Managed a team of 8 engineers"',
            ],
        })

    return suggestions


def _suggest_ats_optimization(
    resume_data: Dict, jd_data: Dict, score_data: Optional[Any]
) -> List[Dict]:
    """Suggest ATS optimization tips."""
    suggestions = []

    overall_score = score_data.overall_score if score_data else 0

    if overall_score < 50:
        suggestions.append({
            "category": "ats_tips",
            "priority": "high",
            "title": "Critical: Low ATS Score",
            "description": f"Your ATS score is {overall_score:.0f}/100. Focus on adding missing keywords and skills from the job description.",
            "details": [
                "• Mirror the exact language used in the job description",
                "• Use standard section headers (Experience, Education, Skills)",
                "• Avoid images, graphics, and complex formatting",
                "• Use a clean, single-column layout",
            ],
        })
    elif overall_score < 70:
        suggestions.append({
            "category": "ats_tips",
            "priority": "medium",
            "title": "Improve ATS Compatibility",
            "description": f"Your ATS score is {overall_score:.0f}/100. Good start, but there's room for improvement.",
            "details": [
                "• Include more keywords from the job posting",
                "• Ensure all relevant skills are listed in the Skills section",
                "• Use industry-standard job titles",
            ],
        })

    # General ATS tips
    suggestions.append({
        "category": "ats_tips",
        "priority": "low",
        "title": "General ATS Best Practices",
        "description": "Follow these tips to maximize ATS compatibility:",
        "details": [
            "• Save as PDF for consistent formatting",
            "• Use standard fonts (Arial, Calibri, Times New Roman)",
            "• Avoid headers/footers (ATS may not read them)",
            "• Spell out acronyms at least once (e.g., 'Machine Learning (ML)')",
            "• Use both the full term and abbreviation for key skills",
        ],
    })

    return suggestions
