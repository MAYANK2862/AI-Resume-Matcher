"""
FastAPI Backend for AI Resume Analyzer & Job Matcher
"""
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, save_resume, save_analysis, get_all_analyses, get_analysis_by_id, delete_analysis
from models import (
    ResumeUploadResponse, AnalyzeRequest, AnalyzeResponse,
    SuggestionItem, SampleJob, SampleResume,
    OptimizeBulletRequest, OptimizeBulletResponse, BulletVariant, KeywordDensityItem
)
from parser import (
    extract_text_from_pdf, clean_text, extract_contact_info,
    detect_sections, count_quantifiable_metrics, count_action_verbs
)
from nlp_engine import (
    extract_skills, match_resume_to_job,
    calculate_ats_score, generate_improvement_suggestions
)
from optimizer import optimize_bullet_point, analyze_keyword_densities
from sample_data import SAMPLE_JOBS, SAMPLE_RESUMES

app = FastAPI(
    title="AI Resume Analyzer & Job Matcher API",
    description="Intelligent NLP-driven resume parsing, skills extraction, job description matching, ATS scoring, and recommendations.",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Resume Analyzer API", "version": "1.0.0"}


@app.post("/api/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts PDF resume upload, extracts text, cleans formatting,
    extracts contact info, identifies sections, and identifies technical skills.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported for upload."
        )

    try:
        content = await file.read()
        raw_text = extract_text_from_pdf(content)
        if not raw_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract readable text from the uploaded PDF. Please ensure it is not a scanned image or password-protected."
            )

        contact = extract_contact_info(raw_text)
        sections = detect_sections(raw_text)
        skills = extract_skills(raw_text)
        word_count = len(raw_text.split())

        resume_id = save_resume(
            filename=file.filename,
            candidate_name=contact["candidate_name"] or "Candidate",
            email=contact["email"] or "",
            phone=contact["phone"] or "",
            raw_text=raw_text,
            extracted_skills=skills
        )

        return ResumeUploadResponse(
            resume_id=resume_id,
            filename=file.filename,
            candidate_name=contact["candidate_name"],
            email=contact["email"],
            phone=contact["phone"],
            extracted_skills=skills,
            sections_detected=sections,
            word_count=word_count,
            raw_text=raw_text
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the PDF: {str(e)}"
        )


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_resume_job(payload: AnalyzeRequest):
    """
    Match candidate resume against target job description using NLP:
    - Calculates Skill Match Score & TF-IDF Cosine Similarity
    - Identifies Matched, Missing, and Candidate Skills
    - Computes ATS Compatibility Score
    - Generates actionable improvement suggestions
    """
    resume_text = payload.resume_text or ""
    candidate_name = payload.candidate_name or "Candidate"

    if not resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text cannot be empty. Please upload a PDF or provide resume text."
        )

    if not payload.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty."
        )

    # 1. Parsing & Extraction
    contact = extract_contact_info(resume_text)
    if candidate_name == "Candidate" and contact.get("candidate_name"):
        candidate_name = contact["candidate_name"]

    sections = detect_sections(resume_text)
    metrics_count = count_quantifiable_metrics(resume_text)
    action_verbs_count = count_action_verbs(resume_text)
    word_count = len(resume_text.split())

    # 2. NLP Skills Extraction & Matching
    match_result = match_resume_to_job(resume_text, payload.job_description)

    # 3. ATS Score Calculation
    ats_score = calculate_ats_score(
        sections=sections,
        contact_info=contact,
        metrics_count=metrics_count,
        action_verbs_count=action_verbs_count,
        word_count=word_count
    )

    # 4. Generate Actionable Suggestions
    raw_suggestions = generate_improvement_suggestions(
        missing_skills=match_result["missing_skills"],
        matched_skills=match_result["matched_skills"],
        sections=sections,
        contact_info=contact,
        metrics_count=metrics_count,
        action_verbs_count=action_verbs_count,
        match_score=match_result["match_score"],
        job_title=payload.job_title
    )

    suggestions_list = [SuggestionItem(**s) for s in raw_suggestions]

    # Calculate keyword densities across target skills
    all_target_skills = list(dict.fromkeys(match_result["matched_skills"] + match_result["missing_skills"]))
    raw_densities = analyze_keyword_densities(resume_text, payload.job_description, all_target_skills)
    keyword_densities = [KeywordDensityItem(**d) for d in raw_densities]

    # 5. Persist analysis to SQLite
    analysis_id = save_analysis(
        resume_id=payload.resume_id,
        candidate_name=candidate_name,
        job_title=payload.job_title,
        job_description=payload.job_description,
        match_score=match_result["match_score"],
        skill_match_score=match_result["skill_match_score"],
        semantic_score=match_result["semantic_score"],
        ats_score=ats_score,
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        candidate_skills=match_result["candidate_skills"],
        job_skills=match_result["job_skills"],
        suggestions=raw_suggestions,
        sections_detected=sections
    )

    return AnalyzeResponse(
        id=analysis_id,
        candidate_name=candidate_name,
        job_title=payload.job_title,
        match_score=match_result["match_score"],
        skill_match_score=match_result["skill_match_score"],
        semantic_score=match_result["semantic_score"],
        ats_score=ats_score,
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        candidate_skills=match_result["candidate_skills"],
        job_skills=match_result["job_skills"],
        suggestions=suggestions_list,
        sections_detected=sections,
        metrics_detected=metrics_count,
        action_verbs_count=action_verbs_count,
        keyword_densities=keyword_densities
    )


@app.post("/api/optimize-bullet", response_model=OptimizeBulletResponse)
def optimize_bullet(payload: OptimizeBulletRequest):
    """
    Transforms a candidate resume bullet point into high-impact,
    quantifiable ATS variations.
    """
    variants = optimize_bullet_point(
        bullet=payload.bullet_text,
        target_skill=payload.target_skill or "",
        role_title=payload.job_role or ""
    )
    return OptimizeBulletResponse(
        original_bullet=payload.bullet_text,
        variants=[BulletVariant(**v) for v in variants]
    )


@app.get("/api/history")
def list_history():
    """Retrieve past resume-job analyses."""
    return get_all_analyses()


@app.get("/api/history/{analysis_id}")
def get_history_detail(analysis_id: int):
    """Retrieve full details for a specific analysis."""
    detail = get_analysis_by_id(analysis_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return detail


@app.delete("/api/history/{analysis_id}")
def delete_history_item(analysis_id: int):
    """Delete an analysis from history."""
    success = delete_analysis(analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"message": "Analysis deleted successfully", "id": analysis_id}


@app.get("/api/sample-jobs", response_model=List[SampleJob])
def get_sample_jobs():
    """Retrieve list of realistic pre-configured job postings."""
    return SAMPLE_JOBS


@app.get("/api/sample-resumes", response_model=List[SampleResume])
def get_sample_resumes():
    """Retrieve list of pre-configured sample resumes for instant 1-click evaluation."""
    return SAMPLE_RESUMES


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

