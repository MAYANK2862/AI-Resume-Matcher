"""
Pydantic Schemas for Request and Response validation
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    extracted_skills: List[str]
    sections_detected: Dict[str, bool]
    word_count: int
    raw_text: str


class AnalyzeRequest(BaseModel):
    resume_id: Optional[int] = None
    resume_text: Optional[str] = None
    candidate_name: Optional[str] = "Candidate"
    job_title: str = "Target Position"
    job_description: str


class SuggestionItem(BaseModel):
    category: str  # "Missing Skills", "Formatting & ATS", "Action Verbs", "Impact & Metrics", "Certifications"
    priority: str  # "high", "medium", "low"
    title: str
    description: str
    actionable_tip: str


class KeywordDensityItem(BaseModel):
    skill: str
    resume_count: int
    job_count: int
    status: str


class AnalyzeResponse(BaseModel):
    id: Optional[int] = None
    candidate_name: str
    job_title: str
    match_score: float
    skill_match_score: float
    semantic_score: float
    ats_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    candidate_skills: List[str]
    job_skills: List[str]
    suggestions: List[SuggestionItem]
    sections_detected: Dict[str, bool]
    metrics_detected: int
    action_verbs_count: int
    keyword_densities: Optional[List[KeywordDensityItem]] = None
    created_at: Optional[str] = None


class SampleJob(BaseModel):
    id: str
    title: str
    company: str
    category: str
    experience_level: str
    description: str
    key_skills: List[str]


class SampleResume(BaseModel):
    id: str
    title: str
    candidate_name: str
    target_role: str
    experience_years: str
    raw_text: str


class OptimizeBulletRequest(BaseModel):
    bullet_text: str
    target_skill: Optional[str] = ""
    job_role: Optional[str] = ""


class BulletVariant(BaseModel):
    style: str
    icon: str
    text: str
    rationale: str


class OptimizeBulletResponse(BaseModel):
    original_bullet: str
    variants: List[BulletVariant]


