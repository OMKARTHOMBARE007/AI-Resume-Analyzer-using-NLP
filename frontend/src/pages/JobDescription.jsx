import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { FiCheck, FiCode, FiBook, FiBriefcase } from 'react-icons/fi';
import './JobDescription.css';

export default function JobDescription() {
  const [title, setTitle] = useState('');
  const [company, setCompany] = useState('');
  const [rawText, setRawText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (rawText.length < 10) { setError('Job description is too short.'); return; }
    setLoading(true); setError('');

    try {
      const res = await api.post('/api/jd/create', { title, company, raw_text: rawText });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process job description.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="jd-page animate-fadeIn">
      <div className="page-header">
        <h1>Job Description</h1>
        <p>Add a job description to compare with your resume.</p>
      </div>

      {!result ? (
        <div className="glass-card jd-form-card">
          <form onSubmit={handleSubmit} className="jd-form">
            <div className="grid-2">
              <div className="input-group">
                <label>Job Title *</label>
                <input type="text" className="input-field" placeholder="e.g., Senior Software Engineer" value={title} onChange={e => setTitle(e.target.value)} required />
              </div>
              <div className="input-group">
                <label>Company (Optional)</label>
                <input type="text" className="input-field" placeholder="e.g., Google" value={company} onChange={e => setCompany(e.target.value)} />
              </div>
            </div>

            <div className="input-group">
              <label>Job Description *</label>
              <textarea className="input-field jd-textarea" placeholder="Paste the full job description here..." value={rawText} onChange={e => setRawText(e.target.value)} required />
              <span className="char-count">{rawText.length} characters</span>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
              {loading ? 'Processing...' : 'Analyze Job Description'}
            </button>
          </form>
        </div>
      ) : (
        <div className="jd-result">
          <div className="alert alert-success" style={{ marginBottom: '24px' }}>
            <FiCheck size={18} /> {result.message}
          </div>

          <div className="grid-2" style={{ marginBottom: '24px' }}>
            <div className="glass-card result-card">
              <h3><FiCode size={18} /> Required Skills ({result.required_skills?.length || 0})</h3>
              <div className="skill-tags">
                {(result.required_skills || []).map((skill, i) => (
                  <span key={i} className="badge badge-blue">{skill}</span>
                ))}
                {(!result.required_skills?.length) && <p className="text-muted">No skills detected</p>}
              </div>
            </div>

            <div className="glass-card result-card">
              <h3><FiBook size={18} /> Key Details</h3>
              <div className="result-items">
                <div className="result-item"><FiBriefcase size={16} /><span>Experience: {result.required_experience || 'Not specified'}</span></div>
                <div className="result-item"><FiBook size={16} /><span>Education: {result.required_education || 'Not specified'}</span></div>
                <div className="result-item"><FiCode size={16} /><span>Keywords: {result.keywords?.length || 0} detected</span></div>
              </div>
            </div>
          </div>

          <div className="result-actions">
            <button className="btn btn-primary" onClick={() => navigate(`/analysis?jd_id=${result.id}`)}>
              Run Analysis →
            </button>
            <button className="btn btn-secondary" onClick={() => { setResult(null); setTitle(''); setCompany(''); setRawText(''); }}>
              Add Another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
