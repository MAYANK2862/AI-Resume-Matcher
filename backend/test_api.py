"""
FastAPI Endpoints Integration Test
"""
from fastapi.testclient import TestClient
from main import app
from sample_data import SAMPLE_RESUMES, SAMPLE_JOBS

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print("Health check OK")

def test_samples():
    res_jobs = client.get("/api/sample-jobs")
    assert res_jobs.status_code == 200
    assert len(res_jobs.json()) >= 4
    print("Sample jobs endpoint OK")

    res_resumes = client.get("/api/sample-resumes")
    assert res_resumes.status_code == 200
    assert len(res_resumes.json()) >= 2
    print("Sample resumes endpoint OK")

def test_analyze_endpoint():
    alex = SAMPLE_RESUMES[0]
    job = SAMPLE_JOBS[0]
    payload = {
        "candidate_name": alex["candidate_name"],
        "resume_text": alex["raw_text"],
        "job_title": job["title"],
        "job_description": job["description"]
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "match_score" in data
    assert "matched_skills" in data
    assert "missing_skills" in data
    assert "suggestions" in data
    print(f"Analyze endpoint OK! Match: {data['match_score']}%, ATS: {data['ats_score']}%")

    # Verify history
    history_res = client.get("/api/history")
    assert history_res.status_code == 200
    assert len(history_res.json()) > 0
    print("History endpoint OK")

def test_bullet_optimizer():
    payload = {
        "bullet_text": "Worked on backend APIs using FastAPI and helped team.",
        "target_skill": "FastAPI",
        "job_role": "Senior Full Stack Developer"
    }
    res = client.post("/api/optimize-bullet", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["variants"]) == 3
    print("Bullet Optimizer endpoint OK! Variants:", len(data["variants"]))

if __name__ == "__main__":
    test_health()
    test_samples()
    test_analyze_endpoint()
    test_bullet_optimizer()
    print("ALL API ENDPOINTS TESTED SUCCESSFULLY!")

