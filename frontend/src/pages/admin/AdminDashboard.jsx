import { useState, useEffect } from 'react';
import api from '../../api/axios';
import { FiUsers, FiFileText, FiBarChart2, FiTrendingUp } from 'react-icons/fi';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899'];

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [trendingSkills, setTrendingSkills] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aRes, sRes] = await Promise.all([api.get('/api/admin/analytics'), api.get('/api/admin/skills/trending?limit=15')]);
        setAnalytics(aRes.data);
        setTrendingSkills(sRes.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loading-container"><div className="spinner"></div></div>;

  const stats = [
    { icon: FiUsers, label: 'Total Users', value: analytics?.total_users || 0, color: 'blue' },
    { icon: FiFileText, label: 'Total Resumes', value: analytics?.total_resumes || 0, color: 'purple' },
    { icon: FiBarChart2, label: 'Total Analyses', value: analytics?.total_analyses || 0, color: 'emerald' },
    { icon: FiTrendingUp, label: 'Avg Score', value: `${analytics?.average_score || 0}%`, color: 'amber' },
  ];

  const scoreDistData = analytics?.score_distribution ? Object.entries(analytics.score_distribution).map(([range, count]) => ({ range, count })) : [];

  return (
    <div className="animate-fadeIn">
      <div className="page-header">
        <h1>Admin Dashboard</h1>
        <p>Platform overview and analytics.</p>
      </div>

      <div className="grid-4" style={{ marginBottom: '28px' }}>
        {stats.map((s, i) => (
          <div key={i} className="stat-card glass-card">
            <div className={`stat-card-icon stat-icon-${s.color}`}><s.icon size={22} /></div>
            <div className="stat-card-info"><span className="stat-card-value">{s.value}</span><span className="stat-card-label">{s.label}</span></div>
          </div>
        ))}
      </div>

      <div className="grid-2">
        <div className="glass-card chart-card">
          <h3 className="chart-title">Score Distribution</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={scoreDistData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="range" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
              <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
              <Tooltip contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
              <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-card chart-card">
          <h3 className="chart-title">Trending Skills</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={trendingSkills.slice(0, 7)} dataKey="count" nameKey="name" cx="50%" cy="50%" outerRadius={100} label={({ name }) => name}>
                {trendingSkills.slice(0, 7).map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
