"""
Automated Backend Unit Tests
"""
import os
import sys

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, save_resume, save_analysis, get_all_analyses, get_analysis_by_id
from parser import extract_contact_info, detect_sections, count_quantifiable_metrics, count_action_verbs
from nlp_engine import extract_skills, match_resume_to_job, calculate_ats_score, generate_improvement_suggestions
from sample_data import SAMPLE_JOBS, SAMPLE_RESUMES


def test_database():
    print("Testing SQLite Database initialization and operations...")
    init_db()
    res_id = save_resume("test.pdf", "John Doe", "john@example.com", "123-456-7890", "Text content here", ["Python", "FastAPI"])
    assert res_id > 0, "Resume ID should be > 0"

    analysis_id = save_analysis(
        resume_id=res_id,
        candidate_name="John Doe",
        job_title="Software Engineer",
        job_description="Looking for Python and FastAPI developer",
        match_score=85.5,
        skill_match_score=90.0,
        semantic_score=81.0,
        ats_score=88.0,
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Docker"],
        candidate_skills=["Python", "FastAPI", "React"],
        job_skills=["Python", "FastAPI", "Docker"],
        suggestions=[{"category": "Missing Skills", "priority": "high", "title": "Learn Docker", "description": "Need Docker", "actionable_tip": "Add Docker"}],
        sections_detected={"experience": True, "education": True}
    )
    assert analysis_id > 0, "Analysis ID should be > 0"

    analyses = get_all_analyses()
    assert len(analyses) > 0, "Should retrieve at least 1 analysis"

    detail = get_analysis_by_id(analysis_id)
    assert detail is not None, "Should retrieve detail"
    assert detail["candidate_name"] == "John Doe"
    print("Database tests passed!")


def test_parser_and_nlp():
    print("Testing Parser & NLP Engine...")
    sample_text = SAMPLE_RESUMES[0]["raw_text"]
    
    # Contact info
    contact = extract_contact_info(sample_text)
    assert "Alex Morgan" in (contact["candidate_name"] or "")
    assert contact["email"] == "alex.morgan.dev@email.com"
    print(f"Contact extraction passed: {contact['candidate_name']}, {contact['email']}")

    # Sections
    sections = detect_sections(sample_text)
    assert sections["experience"] is True
    assert sections["skills"] is True
    assert sections["education"] is True
    print(f"Sections detected: {sections}")

    # Metrics and verbs
    metrics = count_quantifiable_metrics(sample_text)
    verbs = count_action_verbs(sample_text)
    assert metrics >= 3, f"Expected at least 3 metrics, got {metrics}"
    assert verbs >= 5, f"Expected at least 5 action verbs, got {verbs}"
    print(f"Metrics detected: {metrics}, Action verbs count: {verbs}")

    # Skills extraction
    skills = extract_skills(sample_text)
    assert "Python" in skills
    assert "FastAPI" in skills
    assert "React" in skills
    assert "PostgreSQL" in skills
    print(f"Skills extracted: {skills[:8]} (total {len(skills)})")

    # Matching with Full Stack Job
    job = SAMPLE_JOBS[0]
    match_result = match_resume_to_job(sample_text, job["description"], candidate_skills=skills)
    print(f"Match Score: {match_result['match_score']}%")
    print(f"Skill Match Score: {match_result['skill_match_score']}%")
    print(f"Matched Skills: {match_result['matched_skills']}")
    print(f"Missing Skills: {match_result['missing_skills']}")
    assert match_result["match_score"] > 50, "Alex should have strong match for Full Stack role"

    # ATS Score
    word_count = len(sample_text.split())
    ats = calculate_ats_score(sections, contact, metrics, verbs, word_count)
    print(f"ATS Score: {ats}/100")
    assert ats > 70, f"Expected high ATS score, got {ats}"

    # Suggestions
    suggestions = generate_improvement_suggestions(
        missing_skills=match_result["missing_skills"],
        matched_skills=match_result["matched_skills"],
        sections=sections,
        contact_info=contact,
        metrics_count=metrics,
        action_verbs_count=verbs,
        match_score=match_result["match_score"],
        job_title=job["title"]
    )
    assert len(suggestions) > 0, "Should generate improvement suggestions"
    print(f"Generated {len(suggestions)} suggestions successfully!")


if __name__ == "__main__":
    test_database()
    test_parser_and_nlp()
    print("\nALL BACKEND TESTS PASSED SUCCESSFULLY!")

