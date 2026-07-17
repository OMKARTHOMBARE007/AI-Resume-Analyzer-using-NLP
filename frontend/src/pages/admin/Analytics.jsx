import { useState, useEffect } from 'react';
import api from '../../api/axios';
import { FiTrendingUp } from 'react-icons/fi';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function Analytics() {
  const [rankings, setRankings] = useState([]);
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [rRes, sRes] = await Promise.all([api.get('/api/admin/ranking?limit=20'), api.get('/api/admin/skills/trending?limit=20')]);
        setRankings(rRes.data);
        setSkills(sRes.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loading-container"><div className="spinner"></div></div>;

  return (
    <div className="animate-fadeIn">
      <div className="page-header">
        <h1><FiTrendingUp size={28} /> Analytics</h1>
        <p>Platform-wide analytics and candidate rankings.</p>
      </div>

      {/* Trending Skills */}
      <div className="glass-card chart-card" style={{ marginBottom: '24px' }}>
        <h3 className="chart-title">Most Common Skills</h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={skills} layout="vertical" margin={{ left: 80 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
            <XAxis type="number" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
            <YAxis dataKey="name" type="category" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} width={100} />
            <Tooltip contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
            <Bar dataKey="count" fill="url(#skillGrad)" radius={[0, 4, 4, 0]} />
            <defs>
              <linearGradient id="skillGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#3b82f6" />
                <stop offset="100%" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Candidate Rankings */}
      {rankings.length > 0 && (
        <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700 }}>Candidate Rankings</h3>
          </div>
          <table className="data-table">
            <thead>
              <tr><th>Rank</th><th>Candidate</th><th>Email</th><th>ATS Score</th><th>File</th></tr>
            </thead>
            <tbody>
              {rankings.map((r, i) => (
                <tr key={i}>
                  <td style={{ fontWeight: 700 }}>#{i + 1}</td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{r.candidate_name}</td>
                  <td>{r.candidate_email}</td>
                  <td><span className={`badge ${r.overall_score >= 70 ? 'badge-green' : r.overall_score >= 40 ? 'badge-amber' : 'badge-red'}`}>{r.overall_score.toFixed(1)}%</span></td>
                  <td>{r.filename}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
