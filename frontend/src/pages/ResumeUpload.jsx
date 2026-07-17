import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import FileUpload from '../components/FileUpload';
import { FiCheck, FiUser, FiMail, FiPhone, FiBook, FiBriefcase, FiCode } from 'react-icons/fi';
import './ResumeUpload.css';

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post('/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-page animate-fadeIn">
      <div className="page-header">
        <h1>Upload Resume</h1>
        <p>Upload your resume in PDF or DOCX format for AI-powered analysis.</p>
      </div>

      {!result ? (
        <div className="upload-section glass-card">
          <FileUpload onFileSelect={setFile} />

          {file && (
            <div className="upload-actions">
              <button className="btn btn-primary btn-lg" onClick={handleUpload} disabled={uploading}>
                {uploading ? (
                  <><div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }}></div> Analyzing...</>
                ) : (
                  <><FiCheck size={18} /> Analyze Resume</>
                )}
              </button>
            </div>
          )}

          {error && <div className="alert alert-error" style={{ marginTop: '16px' }}>{error}</div>}
        </div>
      ) : (
        <div className="upload-result">
          <div className="alert alert-success" style={{ marginBottom: '24px' }}>
            <FiCheck size={18} /> {result.message}
          </div>

          <div className="result-grid">
            <div className="glass-card result-card">
              <h3>Candidate Info</h3>
              <div className="result-items">
                <div className="result-item"><FiUser size={16} /><span>{result.candidate_name || 'Not detected'}</span></div>
                <div className="result-item"><FiMail size={16} /><span>{result.candidate_email || 'Not detected'}</span></div>
                <div className="result-item"><FiPhone size={16} /><span>{result.candidate_phone || 'Not detected'}</span></div>
              </div>
            </div>

            <div className="glass-card result-card">
              <h3>File Details</h3>
              <div className="result-items">
                <div className="result-item"><FiBook size={16} /><span>{result.filename}</span></div>
                <div className="result-item"><FiBriefcase size={16} /><span>Type: {result.file_type?.toUpperCase()}</span></div>
                <div className="result-item"><FiCode size={16} /><span>Size: {(result.file_size / 1024).toFixed(1)} KB</span></div>
              </div>
            </div>
          </div>

          <div className="result-actions">
            <button className="btn btn-primary" onClick={() => navigate('/job-description')}>
              Add Job Description →
            </button>
            <button className="btn btn-ghost" onClick={() => navigate(`/analysis?resume_id=${result.id}`)}>
              View Full Analysis
            </button>
            <button className="btn btn-secondary" onClick={() => { setResult(null); setFile(null); }}>
              Upload Another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
