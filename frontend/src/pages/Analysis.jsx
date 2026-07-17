import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../api/axios';
import { FiTarget, FiCheck, FiX, FiTrendingUp, FiTrendingDown, FiDownload } from 'react-icons/fi';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell } from 'recharts';
import './Analysis.css';

export default function Analysis() {
  const [searchParams] = useSearchParams();
  const [resumes, setResumes] = useState([]);
  const [jds, setJds] = useState([]);
  const [selectedResume, setSelectedResume] = useState(searchParams.get('resume_id') || '');
  const [selectedJd, setSelectedJd] = useState(searchParams.get('jd_id') || '');
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [rRes, jRes] = await Promise.all([api.get('/api/resume/list'), api.get('/api/jd/list')]);
        setResumes(rRes.data);
        setJds(jRes.data);
      } catch (err) { console.error(err); }
    };
    fetchData();
  }, []);

  const runAnalysis = async () => {
    if (!selectedResume || !selectedJd) { setError('Please select both a resume and job description.'); return; }
    setLoading(true); setError('');
    try {
      const res = await api.post('/api/analysis/score', { resume_id: parseInt(selectedResume), jd_id: parseInt(selectedJd) });
      setScoreData(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed.');
    } finally { setLoading(false); }
  };

  const downloadReport = async () => {
    try {
      const res = await api.post('/api/report/generate', { resume_id: parseInt(selectedResume), jd_id: parseInt(selectedJd) });
      const dl = await api.get(`/api/report/${res.data.id}/download`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([dl.data]));
      const link = document.createElement('a'); link.href = url;
      link.setAttribute('download', `report_${res.data.id}.pdf`);
      document.body.appendChild(link); link.click(); link.remove();
    } catch (err) { console.error('Report download error:', err); }
  };

  const scoreBreakdown = scoreData?.score_breakdown;
  const matchResult = scoreData?.match_result;

  const radarData = scoreBreakdown ? [
    { category: 'Skills', score: scoreBreakdown.skills_score },
    { category: 'Experience', score: scoreBreakdown.experience_score },
    { category: 'Education', score: scoreBreakdown.education_score },
    { category: 'Keywords', score: scoreBreakdown.keyword_score },
    { category: 'Formatting', score: scoreBreakdown.formatting_score },
    { category: 'Projects', score: scoreBreakdown.projects_score },
    { category: 'Certs', score: scoreBreakdown.certifications_score },
  ] : [];

  const barData = radarData.map(d => ({ ...d, fill: d.score >= 70 ? '#10b981' : d.score >= 40 ? '#f59e0b' : '#ef4444' }));

  return (
    <div className="analysis-page animate-fadeIn">
      <div className="page-header">
        <h1>Resume Analysis</h1>
        <p>Compare your resume against a job description for detailed ATS scoring.</p>
      </div>

      {/* Selection */}
      <div className="glass-card analysis-selector">
        <div className="grid-2">
          <div className="input-group">
            <label>Select Resume</label>
            <select className="input-field" value={selectedResume} onChange={e => setSelectedResume(e.target.value)}>
              <option value="">Choose a resume...</option>
              {resumes.map(r => <option key={r.id} value={r.id}>{r.filename} {r.candidate_name ? `(${r.candidate_name})` : ''}</option>)}
            </select>
          </div>
          <div className="input-group">
            <label>Select Job Description</label>
            <select className="input-field" value={selectedJd} onChange={e => setSelectedJd(e.target.value)}>
              <option value="">Choose a job description...</option>
              {jds.map(j => <option key={j.id} value={j.id}>{j.title} {j.company ? `- ${j.company}` : ''}</option>)}
            </select>
          </div>
        </div>
        {error && <div className="alert alert-error" style={{ marginTop: '12px' }}>{error}</div>}
        <button className="btn btn-primary btn-lg" onClick={runAnalysis} disabled={loading} style={{ marginTop: '16px' }}>
          {loading ? <><div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }}></div> Analyzing...</> : <><FiTarget size={18} /> Run Analysis</>}
        </button>
      </div>

      {/* Results */}
      {scoreData && (
        <div className="analysis-results">
          {/* Overall Score */}
          <div className="glass-card score-main-card">
            <div className="score-circle-large">
              <svg width="180" height="180" viewBox="0 0 180 180">
                <circle cx="90" cy="90" r="80" fill="none" stroke="var(--border-color)" strokeWidth="8" />
                <circle cx="90" cy="90" r="80" fill="none" stroke={scoreBreakdown.overall_score >= 70 ? '#10b981' : scoreBreakdown.overall_score >= 40 ? '#f59e0b' : '#ef4444'}
                  strokeWidth="8" strokeDasharray={`${(scoreBreakdown.overall_score / 100) * 502.6} 502.6`}
                  strokeLinecap="round" transform="rotate(-90 90 90)" style={{ transition: 'stroke-dasharray 1.5s ease' }} />
              </svg>
              <div className="score-center">
                <span className="score-number">{scoreBreakdown.overall_score.toFixed(0)}</span>
                <span className="score-label-text">ATS Score</span>
              </div>
            </div>
            <div className="score-summary">
              <h2>ATS Score: {scoreBreakdown.overall_score.toFixed(1)}/100</h2>
              <p>Match: {matchResult.match_percentage.toFixed(1)}% | Semantic: {(matchResult.semantic_similarity * 100).toFixed(1)}%</p>
              <button className="btn btn-success btn-sm" onClick={downloadReport}><FiDownload size={14} /> Download Report</button>
            </div>
          </div>

          <div className="grid-2">
            {/* Score Breakdown Radar */}
            <div className="glass-card chart-card">
              <h3 className="chart-title">Score Breakdown</h3>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="var(--border-color)" />
                  <PolarAngleAxis dataKey="category" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                  <PolarRadiusAxis domain={[0, 100]} tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                  <Radar dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.25} />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Score Bar Chart */}
            <div className="glass-card chart-card">
              <h3 className="chart-title">Category Scores</h3>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={barData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                  <XAxis dataKey="category" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                  <Tooltip contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
                  <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                    {barData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Skills Match */}
          <div className="grid-2">
            <div className="glass-card skill-card">
              <h3><FiCheck size={18} style={{ color: 'var(--accent-emerald)' }} /> Matched Skills ({matchResult.matched_skills?.length || 0})</h3>
              <div className="skill-tags">
                {matchResult.matched_skills?.map((s, i) => <span key={i} className="badge badge-green">{s}</span>)}
                {!matchResult.matched_skills?.length && <p className="text-muted">No matched skills</p>}
              </div>
            </div>
            <div className="glass-card skill-card">
              <h3><FiX size={18} style={{ color: 'var(--accent-red)' }} /> Missing Skills ({matchResult.missing_skills?.length || 0})</h3>
              <div className="skill-tags">
                {matchResult.missing_skills?.map((s, i) => <span key={i} className="badge badge-red">{s}</span>)}
                {!matchResult.missing_skills?.length && <p className="text-muted">No missing skills!</p>}
              </div>
            </div>
          </div>

          {/* Strengths & Weaknesses */}
          <div className="grid-2">
            <div className="glass-card sw-card">
              <h3><FiTrendingUp size={18} style={{ color: 'var(--accent-emerald)' }} /> Strengths</h3>
              <ul className="sw-list">
                {matchResult.strengths?.map((s, i) => <li key={i} className="sw-item sw-strength">{s}</li>)}
                {!matchResult.strengths?.length && <li className="text-muted">No strengths identified</li>}
              </ul>
            </div>
            <div className="glass-card sw-card">
              <h3><FiTrendingDown size={18} style={{ color: 'var(--accent-amber)' }} /> Areas to Improve</h3>
              <ul className="sw-list">
                {matchResult.weaknesses?.map((w, i) => <li key={i} className="sw-item sw-weakness">{w}</li>)}
                {!matchResult.weaknesses?.length && <li className="text-muted">No weaknesses found!</li>}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
