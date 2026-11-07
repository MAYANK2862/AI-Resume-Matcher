import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ResumeUploader from './components/ResumeUploader';
import JobDescriptionInput from './components/JobDescriptionInput';
import MatchScoreCard from './components/MatchScoreCard';
import SkillsComparison from './components/SkillsComparison';
import ImprovementSuggestions from './components/ImprovementSuggestions';
import ResumeOverview from './components/ResumeOverview';
import HistoryModal from './components/HistoryModal';
import {
  analyzeMatch,
  fetchSampleJobs,
  fetchSampleResumes,
  fetchHistory,
  fetchHistoryDetail,
  deleteHistoryItem,
} from './api';
import { Sparkles, Printer, CheckCircle } from 'lucide-react';

export default function App() {
  const [resumeData, setResumeData] = useState(null);
  const [rawText, setRawText] = useState('');
  const [candidateName, setCandidateName] = useState('Alex Morgan');
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  
  const [sampleJobs, setSampleJobs] = useState([]);
  const [sampleResumes, setSampleResumes] = useState([]);
  const [history, setHistory] = useState([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [toastMessage, setToastMessage] = useState('');

  // Initial load
  useEffect(() => {
    loadInitialData();
  }, []);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3500);
  };

  const loadInitialData = async () => {
    try {
      const [jobs, resumes, hist] = await Promise.all([
        fetchSampleJobs().catch(() => []),
        fetchSampleResumes().catch(() => []),
        fetchHistory().catch(() => []),
      ]);
      setSampleJobs(jobs);
      setSampleResumes(resumes);
      setHistory(hist);

      // Preload the first sample job description as default so the user has an immediate starting point
      if (jobs.length > 0) {
        setJobTitle(jobs[0].title);
        setJobDescription(jobs[0].description.trim());
      }
    } catch (err) {
      console.error('Error fetching initial data:', err);
    }
  };

  const handleSelectSampleJob = (job) => {
    setJobTitle(job.title);
    setJobDescription(job.description.trim());
    showToast(`Loaded Job Preset: ${job.title}`);
  };

  const handleLoadDemoSample = () => {
    if (sampleResumes.length > 0 && sampleJobs.length > 0) {
      const demoResume = sampleResumes[0];
      const demoJob = sampleJobs[0];
      setRawText(demoResume.raw_text.trim());
      setCandidateName(demoResume.candidate_name);
      setResumeData({
        resume_id: null,
        filename: 'Alex_Morgan_FullStack.pdf',
        candidate_name: demoResume.candidate_name,
        email: 'alex.morgan.dev@email.com',
        phone: '(555) 234-5678',
        extracted_skills: ['Python', 'FastAPI', 'React', 'PostgreSQL', 'Docker', 'Redis', 'TypeScript', 'Tailwind CSS', 'Git', 'Agile'],
        word_count: demoResume.raw_text.split(/\s+/).length,
        raw_text: demoResume.raw_text,
      });
      setJobTitle(demoJob.title);
      setJobDescription(demoJob.description.trim());
      showToast(`Loaded Demo: ${demoResume.candidate_name} & ${demoJob.title}`);
    }
  };

  const handleRunAnalysis = async () => {
    const textToAnalyze = resumeData?.raw_text || rawText;
    if (!textToAnalyze.trim()) {
      setErrorMessage('Please upload a resume or paste resume text first.');
      return;
    }
    if (!jobDescription.trim()) {
      setErrorMessage('Please provide a job description.');
      return;
    }

    setErrorMessage('');
    setIsAnalyzing(true);

    try {
      const result = await analyzeMatch({
        resumeId: resumeData?.resume_id,
        resumeText: textToAnalyze,
        candidateName: candidateName || 'Candidate',
        jobTitle: jobTitle || 'Target Position',
        jobDescription: jobDescription,
      });

      setAnalysisResult(result);
      showToast('Analysis completed successfully!');

      // Refresh history list
      fetchHistory().then(setHistory).catch(() => {});
    } catch (err) {
      setErrorMessage(err.message || 'An error occurred during analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSelectHistoryItem = async (id) => {
    try {
      const detail = await fetchHistoryDetail(id);
      setAnalysisResult(detail);
      setCandidateName(detail.candidate_name);
      setJobTitle(detail.job_title);
      setJobDescription(detail.job_description);
      setIsHistoryOpen(false);
      showToast(`Loaded historical analysis for ${detail.job_title}`);
    } catch (err) {
      setErrorMessage('Failed to load analysis from history.');
    }
  };

  const handleDeleteHistoryItem = async (id) => {
    try {
      await deleteHistoryItem(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
      showToast('Record deleted');
    } catch (err) {
      console.error(err);
    }
  };

  const handleReset = () => {
    setResumeData(null);
    setRawText('');
    setCandidateName('');
    setAnalysisResult(null);
    setErrorMessage('');
    if (sampleJobs.length > 0) {
      setJobTitle(sampleJobs[0].title);
      setJobDescription(sampleJobs[0].description.trim());
    }
    showToast('Dashboard reset');
  };

  const canAnalyze = Boolean((resumeData?.raw_text || rawText.trim()) && jobDescription.trim());

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center space-x-2 bg-slate-900 border border-sky-500/30 text-sky-300 px-4 py-2.5 rounded-xl shadow-2xl animate-fade-in text-xs font-semibold">
          <CheckCircle className="w-4 h-4 text-sky-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Navbar */}
      <Navbar
        onOpenHistory={() => setIsHistoryOpen(true)}
        onReset={handleReset}
        historyCount={history.length}
        onLoadSample={handleLoadDemoSample}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-8">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto space-y-2">
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
            AI Resume Analyzer &{' '}
            <span className="bg-gradient-to-r from-sky-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Job Matcher
            </span>
          </h1>
          <p className="text-sm sm:text-base text-slate-400">
            Upload your resume PDF, match against any job description, extract missing technical skills, and optimize for ATS algorithms.
          </p>
        </div>

        {/* Global Error Banner */}
        {errorMessage && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center justify-between">
            <span>{errorMessage}</span>
            <button onClick={() => setErrorMessage('')} className="text-rose-400 font-bold ml-4">
              ✕
            </button>
          </div>
        )}

        {/* Top Input Grid: Resume Uploader & Job Description Input */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          <ResumeUploader
            resumeData={resumeData}
            setResumeData={setResumeData}
            rawText={rawText}
            setRawText={setRawText}
            candidateName={candidateName}
            setCandidateName={setCandidateName}
            isUploading={isUploading}
            setIsUploading={setIsUploading}
          />

          <JobDescriptionInput
            jobTitle={jobTitle}
            setJobTitle={setJobTitle}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            sampleJobs={sampleJobs}
            onSelectSampleJob={handleSelectSampleJob}
            onAnalyze={handleRunAnalysis}
            isAnalyzing={isAnalyzing}
            canAnalyze={canAnalyze}
          />
        </div>

        {/* Analysis Results Display */}
        {analysisResult && (
          <div className="space-y-6 pt-4 animate-fade-in">
            {/* Top Bar for Results */}
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-white flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-sky-400" />
                <span>Analysis Report</span>
              </h2>

              <button
                onClick={() => window.print()}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-colors"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print / Save PDF</span>
              </button>
            </div>

            {/* Score Gauges */}
            <MatchScoreCard analysis={analysisResult} />

            {/* Skills Gap Analysis & Breakdown */}
            <SkillsComparison analysis={analysisResult} />

            {/* Recommendations & Section Audit */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <ImprovementSuggestions suggestions={analysisResult.suggestions} />
              </div>
              <div className="lg:col-span-1">
                <ResumeOverview analysis={analysisResult} resumeData={resumeData} />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* History Modal */}
      <HistoryModal
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectHistoryItem={handleSelectHistoryItem}
        onDeleteHistoryItem={handleDeleteHistoryItem}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        AI Resume Analyzer & Job Matcher • Built with FastAPI, NLP, React, and SQLite
      </footer>
    </div>
  );
}

