import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../api/axios';
import { FiZap, FiCode, FiAward, FiFileText, FiEdit3, FiBookOpen, FiLayout, FiTarget } from 'react-icons/fi';
import './Suggestions.css';

const categoryIcons = {
  skills: FiCode, certifications: FiAward, projects: FiFileText,
  action_verbs: FiEdit3, grammar: FiBookOpen, formatting: FiLayout, ats_tips: FiTarget,
};

const priorityColors = { high: 'red', medium: 'amber', low: 'blue' };

export default function Suggestions() {
  const [searchParams] = useSearchParams();
  const [resumes, setResumes] = useState([]);
  const [jds, setJds] = useState([]);
  const [selectedResume, setSelectedResume] = useState(searchParams.get('resume_id') || '');
  const [selectedJd, setSelectedJd] = useState(searchParams.get('jd_id') || '');
  const [suggestions, setSuggestions] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const [rRes, jRes] = await Promise.all([api.get('/api/resume/list'), api.get('/api/jd/list')]);
      setResumes(rRes.data); setJds(jRes.data);
    };
    fetchData().catch(console.error);
  }, []);

  const getSuggestions = async () => {
    if (!selectedResume) return;
    setLoading(true);
    try {
      const res = await api.post('/api/analysis/suggestions', { resume_id: parseInt(selectedResume), jd_id: selectedJd ? parseInt(selectedJd) : 0 });
      setSuggestions(res.data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  const groupedSuggestions = suggestions?.suggestions?.reduce((acc, s) => {
    if (!acc[s.category]) acc[s.category] = [];
    acc[s.category].push(s);
    return acc;
  }, {}) || {};

  return (
    <div className="suggestions-page animate-fadeIn">
      <div className="page-header">
        <h1><FiZap size={28} /> AI Suggestions</h1>
        <p>Get intelligent recommendations to improve your resume.</p>
      </div>

      <div className="glass-card analysis-selector">
        <div className="grid-2">
          <div className="input-group">
            <label>Select Resume</label>
            <select className="input-field" value={selectedResume} onChange={e => setSelectedResume(e.target.value)}>
              <option value="">Choose a resume...</option>
              {resumes.map(r => <option key={r.id} value={r.id}>{r.filename}</option>)}
            </select>
          </div>
          <div className="input-group">
            <label>Job Description (Optional)</label>
            <select className="input-field" value={selectedJd} onChange={e => setSelectedJd(e.target.value)}>
              <option value="">None - General analysis</option>
              {jds.map(j => <option key={j.id} value={j.id}>{j.title}</option>)}
            </select>
          </div>
        </div>
        <button className="btn btn-primary btn-lg" onClick={getSuggestions} disabled={loading || !selectedResume} style={{ marginTop: '16px' }}>
          {loading ? 'Generating...' : 'Get AI Suggestions'}
        </button>
      </div>

      {suggestions && (
        <div className="suggestions-results">
          <div className="suggestions-summary glass-card">
            <h3>📋 {suggestions.total_suggestions} Suggestions Found</h3>
          </div>

          {Object.entries(groupedSuggestions).map(([category, items]) => {
            const Icon = categoryIcons[category] || FiZap;
            return (
              <div key={category} className="suggestion-category">
                <h3 className="category-header">
                  <Icon size={18} /> {category.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                  <span className="badge badge-blue">{items.length}</span>
                </h3>
                <div className="suggestion-cards">
                  {items.map((item, i) => (
                    <div key={i} className={`glass-card suggestion-card priority-${priorityColors[item.priority]}`}>
                      <div className="suggestion-header">
                        <span className={`badge badge-${priorityColors[item.priority]}`}>{item.priority}</span>
                        <h4>{item.title}</h4>
                      </div>
                      <p className="suggestion-desc">{item.description}</p>
                      {item.details?.length > 0 && (
                        <ul className="suggestion-details">
                          {item.details.map((d, j) => <li key={j}>{d}</li>)}
                        </ul>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
