"""
SQLite Database interface for Resume Analyzer & Job Matcher
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resumes.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table for uploaded resumes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        candidate_name TEXT,
        email TEXT,
        phone TEXT,
        raw_text TEXT NOT NULL,
        extracted_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table for job analysis results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_id INTEGER,
        candidate_name TEXT,
        job_title TEXT NOT NULL,
        job_description TEXT NOT NULL,
        match_score REAL NOT NULL,
        skill_match_score REAL NOT NULL,
        semantic_score REAL NOT NULL,
        ats_score REAL NOT NULL,
        matched_skills TEXT NOT NULL,
        missing_skills TEXT NOT NULL,
        candidate_skills TEXT NOT NULL,
        job_skills TEXT NOT NULL,
        suggestions TEXT NOT NULL,
        sections_detected TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (resume_id) REFERENCES resumes (id)
    );
    """)

    conn.commit()
    conn.close()


def save_resume(filename: str, candidate_name: str, email: str, phone: str, raw_text: str, extracted_skills: List[str]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resumes (filename, candidate_name, email, phone, raw_text, extracted_skills)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (filename, candidate_name, email, phone, raw_text, json.dumps(extracted_skills)))
    resume_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return resume_id


def save_analysis(
    resume_id: Optional[int],
    candidate_name: str,
    job_title: str,
    job_description: str,
    match_score: float,
    skill_match_score: float,
    semantic_score: float,
    ats_score: float,
    matched_skills: List[str],
    missing_skills: List[str],
    candidate_skills: List[str],
    job_skills: List[str],
    suggestions: List[Dict[str, Any]],
    sections_detected: Dict[str, bool]
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses (
            resume_id, candidate_name, job_title, job_description,
            match_score, skill_match_score, semantic_score, ats_score,
            matched_skills, missing_skills, candidate_skills, job_skills,
            suggestions, sections_detected
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_id,
        candidate_name,
        job_title,
        job_description,
        match_score,
        skill_match_score,
        semantic_score,
        ats_score,
        json.dumps(matched_skills),
        json.dumps(missing_skills),
        json.dumps(candidate_skills),
        json.dumps(job_skills),
        json.dumps(suggestions),
        json.dumps(sections_detected)
    ))
    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return analysis_id


def get_all_analyses() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, candidate_name, job_title, match_score, ats_score, created_at,
               matched_skills, missing_skills
        FROM analyses
        ORDER BY created_at DESC
        LIMIT 50
    """)
    rows = cursor.fetchall()
    results = []
    for row in rows:
        matched = json.loads(row["matched_skills"]) if row["matched_skills"] else []
        missing = json.loads(row["missing_skills"]) if row["missing_skills"] else []
        results.append({
            "id": row["id"],
            "candidate_name": row["candidate_name"] or "Candidate",
            "job_title": row["job_title"],
            "match_score": round(row["match_score"], 1),
            "ats_score": round(row["ats_score"], 1),
            "matched_count": len(matched),
            "missing_count": len(missing),
            "created_at": row["created_at"]
        })
    conn.close()
    return results


def get_analysis_by_id(analysis_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "resume_id": row["resume_id"],
        "candidate_name": row["candidate_name"],
        "job_title": row["job_title"],
        "job_description": row["job_description"],
        "match_score": round(row["match_score"], 1),
        "skill_match_score": round(row["skill_match_score"], 1),
        "semantic_score": round(row["semantic_score"], 1),
        "ats_score": round(row["ats_score"], 1),
        "matched_skills": json.loads(row["matched_skills"]),
        "missing_skills": json.loads(row["missing_skills"]),
        "candidate_skills": json.loads(row["candidate_skills"]),
        "job_skills": json.loads(row["job_skills"]),
        "suggestions": json.loads(row["suggestions"]),
        "sections_detected": json.loads(row["sections_detected"]) if row["sections_detected"] else {},
        "created_at": row["created_at"]
    }


def delete_analysis(analysis_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

