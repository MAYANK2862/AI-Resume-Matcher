/**
 * API client to communicate with the FastAPI backend
 */

const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend is not reachable');
  return res.json();
}

export async function uploadResumePdf(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/upload-resume`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Failed to upload PDF' }));
    throw new Error(errorData.detail || 'Upload failed');
  }

  return res.json();
}

export async function analyzeMatch({ resumeId, resumeText, candidateName, jobTitle, jobDescription }) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_id: resumeId || null,
      resume_text: resumeText || '',
      candidate_name: candidateName || 'Candidate',
      job_title: jobTitle || 'Target Role',
      job_description: jobDescription,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Failed to analyze resume' }));
    throw new Error(errorData.detail || 'Analysis failed');
  }

  return res.json();
}

export async function fetchSampleJobs() {
  const res = await fetch(`${API_BASE}/sample-jobs`);
  if (!res.ok) throw new Error('Failed to load sample jobs');
  return res.json();
}

export async function fetchSampleResumes() {
  const res = await fetch(`${API_BASE}/sample-resumes`);
  if (!res.ok) throw new Error('Failed to load sample resumes');
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error('Failed to load history');
  return res.json();
}

export async function fetchHistoryDetail(id) {
  const res = await fetch(`${API_BASE}/history/${id}`);
  if (!res.ok) throw new Error('Failed to load analysis detail');
  return res.json();
}

export async function deleteHistoryItem(id) {
  const res = await fetch(`${API_BASE}/history/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete history record');
  return res.json();
}

