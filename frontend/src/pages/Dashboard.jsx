import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { FiFileText, FiBarChart2, FiTrendingUp, FiAward, FiUpload, FiZap } from 'react-icons/fi';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import './Dashboard.css';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [charts, setCharts] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sumRes, chartRes] = await Promise.all([
          api.get('/api/dashboard/summary'),
          api.get('/api/dashboard/charts'),
        ]);
        setSummary(sumRes.data);
        setCharts(chartRes.data);
      } catch (err) {
        console.error('Dashboard fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="loading-container"><div className="spinner"></div><p>Loading dashboard...</p></div>;
  }

  const statCards = [
    { icon: FiFileText, label: 'Resumes', value: summary?.total_resumes || 0, color: 'blue' },
    { icon: FiBarChart2, label: 'Analyses', value: summary?.total_analyses || 0, color: 'purple' },
    { icon: FiTrendingUp, label: 'Avg Score', value: `${summary?.average_score || 0}%`, color: 'emerald' },
    { icon: FiAward, label: 'Best Score', value: `${summary?.best_score || 0}%`, color: 'amber' },
  ];

  const radarData = charts?.skill_radar ? Object.entries(charts.skill_radar).map(([key, val]) => ({
    skill: key, count: val, fullMark: Math.max(...Object.values(charts.skill_radar)) + 2,
  })) : [];

  const topSkillsData = summary?.top_skills?.slice(0, 10) || [];

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Welcome back! Here's your resume analysis overview.</p>
      </div>

      {/* Stats */}
      <div className="grid-4" style={{ marginBottom: '32px' }}>
        {statCards.map((card, i) => (
          <div key={i} className={`stat-card glass-card stat-card-${card.color}`}>
            <div className={`stat-card-icon stat-icon-${card.color}`}>
              <card.icon size={22} />
            </div>
            <div className="stat-card-info">
              <span className="stat-card-value">{card.value}</span>
              <span className="stat-card-label">{card.label}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Quick actions */}
      {(summary?.total_resumes === 0) && (
        <div className="glass-card quick-start-card" style={{ marginBottom: '32px' }}>
          <h3>🚀 Get Started</h3>
          <p>Upload your first resume to begin analyzing it with AI.</p>
          <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
            <Link to="/upload" className="btn btn-primary"><FiUpload size={16} /> Upload Resume</Link>
            <Link to="/job-description" className="btn btn-ghost"><FiZap size={16} /> Add Job Description</Link>
          </div>
        </div>
      )}

      <div className="grid-2">
        {/* Skills Radar */}
        <div className="glass-card chart-card">
          <h3 className="chart-title">Skills Distribution</h3>
          {radarData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="var(--border-color)" />
                <PolarAngleAxis dataKey="skill" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                <PolarRadiusAxis tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                <Radar name="Skills" dataKey="count" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state"><p>Upload a resume to see skill distribution</p></div>
          )}
        </div>

        {/* Top Skills Bar Chart */}
        <div className="glass-card chart-card">
          <h3 className="chart-title">Top Skills</h3>
          {topSkillsData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topSkillsData} layout="vertical" margin={{ left: 60 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis type="number" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
                <YAxis dataKey="name" type="category" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} width={80} />
                <Tooltip contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-primary)' }} />
                <Bar dataKey="count" fill="url(#barGradient)" radius={[0, 4, 4, 0]} />
                <defs>
                  <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#3b82f6" />
                    <stop offset="100%" stopColor="#8b5cf6" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state"><p>No skills data yet</p></div>
          )}
        </div>
      </div>

      {/* Recent Scores */}
      {summary?.recent_scores?.length > 0 && (
        <div className="glass-card" style={{ marginTop: '24px', padding: '24px' }}>
          <h3 className="chart-title">Recent Analyses</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Resume ID</th>
                <th>JD ID</th>
                <th>ATS Score</th>
                <th>Match %</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {summary.recent_scores.map((score, i) => (
                <tr key={i}>
                  <td>#{score.resume_id}</td>
                  <td>#{score.jd_id}</td>
                  <td>
                    <span className={`badge ${score.overall_score >= 70 ? 'badge-green' : score.overall_score >= 40 ? 'badge-amber' : 'badge-red'}`}>
                      {score.overall_score.toFixed(1)}%
                    </span>
                  </td>
                  <td>{score.match_percentage.toFixed(1)}%</td>
                  <td>{new Date(score.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
