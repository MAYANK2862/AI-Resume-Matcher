import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, Edit3, User, Mail, Phone, Code } from 'lucide-react';
import { uploadResumePdf } from '../api';

export default function ResumeUploader({
  resumeData,
  setResumeData,
  rawText,
  setRawText,
  candidateName,
  setCandidateName,
  isUploading,
  setIsUploading
}) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const [mode, setMode] = useState('pdf'); // 'pdf' or 'text'
  const fileInputRef = useRef(null);

  const handleFiles = async (file) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please select a valid PDF file.');
      return;
    }
    setError('');
    setIsUploading(true);

    try {
      const data = await uploadResumePdf(file);
      setResumeData(data);
      setRawText(data.raw_text);
      if (data.candidate_name) {
        setCandidateName(data.candidate_name);
      }
    } catch (err) {
      setError(err.message || 'Failed to parse resume PDF.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files[0]);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-xl flex flex-col h-full">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-semibold text-slate-100 text-base">Candidate Resume</h2>
            <p className="text-xs text-slate-400">Upload PDF or paste plain text</p>
          </div>
        </div>

        {/* Mode switcher */}
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
          <button
            type="button"
            onClick={() => setMode('pdf')}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              mode === 'pdf' ? 'bg-sky-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            PDF Upload
          </button>
          <button
            type="button"
            onClick={() => setMode('text')}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              mode === 'text' ? 'bg-sky-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Text Editor
          </button>
        </div>
      </div>

      {mode === 'pdf' ? (
        <div className="space-y-4 flex-1 flex flex-col">
          {/* Dropzone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`flex-1 min-h-[180px] border-2 border-dashed rounded-xl flex flex-col items-center justify-center p-6 text-center cursor-pointer transition-all ${
              dragActive
                ? 'border-sky-500 bg-sky-500/10 scale-[0.99]'
                : 'border-slate-700 bg-slate-950/50 hover:border-slate-600 hover:bg-slate-950/80'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={(e) => handleFiles(e.target.files[0])}
            />

            {isUploading ? (
              <div className="flex flex-col items-center space-y-3">
                <div className="w-8 h-8 border-3 border-sky-500 border-t-transparent rounded-full animate-spin" />
                <p className="text-sm font-medium text-sky-400">Extracting text & parsing NLP entities...</p>
              </div>
            ) : resumeData ? (
              <div className="flex flex-col items-center space-y-2">
                <div className="w-12 h-12 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <p className="text-sm font-semibold text-slate-200">{resumeData.filename}</p>
                <p className="text-xs text-emerald-400">
                  Extracted {resumeData.extracted_skills?.length || 0} skills • {resumeData.word_count || 0} words
                </p>
                <span className="text-xs text-slate-400 underline pt-1">Click to replace file</span>
              </div>
            ) : (
              <div className="flex flex-col items-center space-y-2">
                <div className="w-12 h-12 rounded-full bg-slate-800 text-sky-400 flex items-center justify-center">
                  <Upload className="w-6 h-6" />
                </div>
                <p className="text-sm font-medium text-slate-200">
                  Drag & drop your resume PDF here, or <span className="text-sky-400 underline">browse</span>
                </p>
                <p className="text-xs text-slate-500">Supports PDF format (Max 10MB)</p>
              </div>
            )}
          </div>

          {error && (
            <div className="flex items-center space-x-2 text-xs text-rose-400 bg-rose-500/10 border border-rose-500/20 rounded-lg p-2.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-3 flex-1 flex flex-col">
          <textarea
            value={rawText}
            onChange={(e) => setRawText(e.target.value)}
            placeholder="Paste raw resume text here (Summary, Skills, Work Experience, Education)..."
            rows={8}
            className="w-full flex-1 p-3 bg-slate-950 rounded-xl border border-slate-700 text-slate-200 text-xs font-mono placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 transition-all resize-none"
          />
          <div className="flex justify-between items-center text-xs text-slate-400">
            <span>{rawText.split(/\s+/).filter(Boolean).length} words</span>
            <span>Manual input mode</span>
          </div>
        </div>
      )}

      {/* Extracted Candidate Info Cards */}
      {(resumeData || rawText) && (
        <div className="mt-4 pt-3 border-t border-slate-800 space-y-2.5">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-slate-950/70 p-2 rounded-lg border border-slate-800 flex items-center space-x-2">
              <User className="w-3.5 h-3.5 text-slate-400" />
              <input
                type="text"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
                placeholder="Candidate Name"
                className="bg-transparent text-slate-200 font-medium focus:outline-none w-full"
              />
            </div>
            <div className="bg-slate-950/70 p-2 rounded-lg border border-slate-800 flex items-center space-x-2">
              <Mail className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-300 truncate" title={resumeData?.email || 'No email detected'}>
                {resumeData?.email || 'No email detected'}
              </span>
            </div>
          </div>

          {/* Quick Extracted Skills Preview */}
          {resumeData?.extracted_skills && resumeData.extracted_skills.length > 0 && (
            <div>
              <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1.5">
                <span className="flex items-center space-x-1">
                  <Code className="w-3 h-3 text-sky-400" />
                  <span>Detected Candidate Skills ({resumeData.extracted_skills.length}):</span>
                </span>
              </div>
              <div className="flex flex-wrap gap-1 max-h-20 overflow-y-auto pr-1">
                {resumeData.extracted_skills.map((skill, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 text-[10px] font-medium rounded-md bg-slate-800 text-sky-300 border border-slate-700"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

