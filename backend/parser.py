"""
Resume Text Parser and Information Extractor
"""
import io
import re
from typing import Dict, Any, List, Optional
from pypdf import PdfReader


EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
LINKEDIN_REGEX = r'linkedin\.com/in/[a-zA-Z0-9_-]+'
GITHUB_REGEX = r'github\.com/[a-zA-Z0-9_-]+'

COMMON_ACTION_VERBS = [
    "accelerated", "accomplished", "achieved", "acquired", "adapted", "administered",
    "advanced", "analyzed", "architected", "automated", "boosted", "built", "centralized",
    "championed", "collaborated", "compiled", "composed", "configured", "constructed",
    "converted", "coordinated", "created", "customized", "debugged", "decreased",
    "defined", "delivered", "deployed", "designed", "developed", "devised", "diagnosed",
    "directed", "discovered", "dispatched", "documented", "doubled", "drafted", "drove",
    "eliminated", "enabled", "enforced", "engineered", "enhanced", "established",
    "evaluated", "executed", "expanded", "expedited", "fabricated", "facilitated",
    "formulated", "founded", "generated", "guided", "halted", "headed", "identified",
    "implemented", "improved", "increased", "initiated", "innovated", "inspected",
    "installed", "instituted", "instructed", "integrated", "introduced", "invented",
    "investigated", "launched", "lead", "led", "leveraged", "managed", "maximized",
    "measured", "mentored", "migrated", "minimized", "modernized", "monitored",
    "negotiated", "optimized", "orchestrated", "organized", "overhauled", "oversaw",
    "partnered", "performed", "pioneered", "planned", "prepared", "prioritized",
    "produced", "programmed", "promoted", "proposed", "published", "re-engineered",
    "rebuilt", "reconciled", "recruited", "redesigned", "reduced", "refined", "refactored",
    "remodeled", "reorganized", "replaced", "resolved", "restructured", "revamped",
    "reviewed", "revitalized", "saved", "scaled", "scheduled", "screened", "secured",
    "simplified", "solved", "spearheaded", "standardized", "streamlined", "strengthened",
    "structured", "supervised", "surpassed", "synthesized", "systematized", "tested",
    "tracked", "trained", "transformed", "transitioned", "translated", "troubleshot",
    "unified", "upgraded", "utilized", "validated", "verified", "visualized"
]

METRICS_REGEX = [
    r'\b\d+(?:\.\d+)?%(?!\w)',                                                    # e.g. 25%, 99.9%
    r'\$\s*\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:k|m|b|million|billion))?(?!\w)',     # e.g. $50k, $1.2M
    r'\b\d+\s*(?:x|times)\b',                                                     # e.g. 3x, 10 times
    r'\b\d{1,3}(?:,\d{3})+(?!\w)',                                                # e.g. 10,000, 250,000
    r'\b\d+\s*(?:k|m|million|billion)\s*(?:users|clients|customers|requests|queries|downloads|records)\b',
    r'\b\d+\s*(?:ms|milliseconds|seconds|minutes|hours|days)\b'
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract clean raw text from a PDF file buffer."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages_text.append(text)
        raw_text = "\n".join(pages_text)
        return clean_text(raw_text)
    except Exception as e:
        raise ValueError(f"Failed to read PDF file: {str(e)}")


def clean_text(text: str) -> str:
    """Clean and normalize raw extracted text."""
    # Replace non-breaking spaces and unusual characters
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    # Normalize bullet points
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219•*▪►✔-]', ' - ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace excessive consecutive newlines
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """Extract email, phone, links, and candidate name."""
    email_match = re.search(EMAIL_REGEX, text)
    phone_match = re.search(PHONE_REGEX, text)
    linkedin_match = re.search(LINKEDIN_REGEX, text, re.IGNORECASE)
    github_match = re.search(GITHUB_REGEX, text, re.IGNORECASE)

    email = email_match.group(0) if email_match else None
    phone = phone_match.group(0) if phone_match else None
    linkedin = f"https://{linkedin_match.group(0)}" if linkedin_match else None
    github = f"https://{github_match.group(0)}" if github_match else None

    # Name extraction heuristic: examine the first 5 lines for a candidate name
    name = None
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines[:5]:
        # Ignore if line contains email or phone
        if email and email in line:
            continue
        if phone and phone in line:
            continue
        # Check if line looks like a human name (2 to 4 words, alphabetic, < 40 chars)
        clean_line = re.sub(r'[^\w\s]', '', line).strip()
        words = clean_line.split()
        if 2 <= len(words) <= 4 and all(w.isalpha() for w in words) and len(clean_line) < 40:
            name = clean_line
            break

    if not name and lines:
        first_line = lines[0]
        if len(first_line.split()) <= 4 and len(first_line) < 40:
            name = first_line

    return {
        "candidate_name": name or "Candidate",
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github
    }


def detect_sections(text: str) -> Dict[str, bool]:
    """Detect presence of key resume sections required for ATS compliance."""
    lower_text = text.lower()
    
    sections = {
        "summary": bool(re.search(r'\b(summary|profile|about\s*me|objective|executive\s*summary)\b', lower_text)),
        "experience": bool(re.search(r'\b(experience|work\s*experience|employment|work\s*history|professional\s*experience)\b', lower_text)),
        "education": bool(re.search(r'\b(education|academic|degrees|university|college)\b', lower_text)),
        "skills": bool(re.search(r'\b(skills|technical\s*skills|core\s*competencies|technologies|expertise)\b', lower_text)),
        "projects": bool(re.search(r'\b(projects|personal\s*projects|key\s*projects|portfolio)\b', lower_text)),
        "certifications": bool(re.search(r'\b(certifications|certificates|licenses|credentials|awards)\b', lower_text))
    }
    return sections


def count_quantifiable_metrics(text: str) -> int:
    """Count instances of numbers, metrics, and KPI indicators in text."""
    count = 0
    for pattern in METRICS_REGEX:
        matches = re.findall(pattern, text, re.IGNORECASE)
        count += len(matches)
    return count


def count_action_verbs(text: str) -> int:
    """Count strong action verbs used in experience and project bullet points."""
    words = re.findall(r'\b[a-zA-Z-]+\b', text.lower())
    found_verbs = [w for w in words if w in COMMON_ACTION_VERBS]
    return len(found_verbs)
