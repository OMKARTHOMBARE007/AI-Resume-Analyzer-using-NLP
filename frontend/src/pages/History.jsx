import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { FiFileText, FiTrash2, FiBarChart2, FiDownload } from 'react-icons/fi';

export default function History() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/api/resume/list').then(res => setResumes(res.data)).catch(console.error).finally(() => setLoading(false));
  }, []);

  const deleteResume = async (id) => {
    if (!confirm('Delete this resume?')) return;
    try {
      await api.delete(`/api/resume/${id}`);
      setResumes(prev => prev.filter(r => r.id !== id));
    } catch (err) { console.error(err); }
  };

  if (loading) return <div className="loading-container"><div className="spinner"></div></div>;

  return (
    <div className="animate-fadeIn">
      <div className="page-header">
        <h1>Resume History</h1>
        <p>All your uploaded resumes.</p>
      </div>

      {resumes.length === 0 ? (
        <div className="glass-card empty-state">
          <div className="empty-icon">📄</div>
          <h3>No resumes yet</h3>
          <p>Upload your first resume to get started.</p>
          <Link to="/upload" className="btn btn-primary" style={{ marginTop: '16px' }}>Upload Resume</Link>
        </div>
      ) : (
        <div className="glass-card" style={{ padding: '0', overflow: 'hidden' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>File</th>
                <th>Candidate</th>
                <th>Skills</th>
                <th>Experience</th>
                <th>Uploaded</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {resumes.map(r => (
                <tr key={r.id}>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <FiFileText size={16} style={{ color: 'var(--accent-blue)' }} />
                      {r.filename}
                    </div>
                  </td>
                  <td>{r.candidate_name || '—'}</td>
                  <td><span className="badge badge-blue">{r.skill_count}</span></td>
                  <td>{r.total_experience_years ? `${r.total_experience_years} yrs` : '—'}</td>
                  <td>{new Date(r.uploaded_at).toLocaleDateString()}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <Link to={`/analysis?resume_id=${r.id}`} className="btn btn-ghost btn-sm"><FiBarChart2 size={14} /></Link>
                      <button className="btn btn-ghost btn-sm" onClick={() => deleteResume(r.id)}><FiTrash2 size={14} style={{ color: 'var(--accent-red)' }} /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
