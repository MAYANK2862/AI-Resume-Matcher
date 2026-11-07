import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pdf_upload():
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_resumes", "Alex_Morgan_Resume.pdf")
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/upload-resume",
            files={"file": ("Alex_Morgan_Resume.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200, f"Upload failed: {response.text}"
    data = response.json()
    print("Upload Success:", data["filename"])
    print("Candidate Name:", data["candidate_name"])
    print("Email:", data["email"])
    print("Phone:", data["phone"])
    print("Extracted Skills Count:", len(data["extracted_skills"]))
    print("Sections Detected:", data["sections_detected"])
    assert len(data["extracted_skills"]) > 5
    print("PDF Upload Verification Passed!")

if __name__ == "__main__":
    test_pdf_upload()

