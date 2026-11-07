"""
Convenience launcher to run both Backend (FastAPI) and Frontend (Vite) concurrently.
"""
import subprocess
import sys
import os
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")


def start():
    print("=" * 60)
    print("🚀 Starting AI Resume Analyzer & Job Matcher")
    print("=" * 60)

    # 1. Start FastAPI Backend
    print("\n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=BACKEND_DIR
    )

    # 2. Start Vite Frontend
    print("[2/2] Starting React (Vite) Frontend on http://localhost:5173 ...")
    frontend_proc = subprocess.Popen(
        "npm run dev",
        shell=True,
        cwd=FRONTEND_DIR
    )

    print("\n" + "=" * 60)
    print("✨ Application is running!")
    print("👉 Frontend UI:      http://localhost:5173")
    print("👉 Backend API Docs: http://127.0.0.1:8000/docs")
    print("=" * 60)
    print("Press Ctrl+C to terminate both servers.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Shutdown complete. Goodbye!")


if __name__ == "__main__":
    start()

