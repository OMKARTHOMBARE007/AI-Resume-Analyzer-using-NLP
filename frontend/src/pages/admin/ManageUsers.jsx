import { useState, useEffect } from 'react';
import api from '../../api/axios';
import { FiTrash2, FiShield, FiUser } from 'react-icons/fi';

export default function ManageUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/api/admin/users').then(res => setUsers(res.data)).catch(console.error).finally(() => setLoading(false));
  }, []);

  const deleteUser = async (id) => {
    if (!confirm('Delete this user and all their data?')) return;
    try {
      await api.delete(`/api/admin/users/${id}`);
      setUsers(prev => prev.filter(u => u.id !== id));
    } catch (err) { console.error(err); }
  };

  if (loading) return <div className="loading-container"><div className="spinner"></div></div>;

  return (
    <div className="animate-fadeIn">
      <div className="page-header">
        <h1>Manage Users</h1>
        <p>View and manage all platform users.</p>
      </div>

      <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td>#{u.id}</td>
                <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{u.name}</td>
                <td>{u.email}</td>
                <td>
                  <span className={`badge ${u.role === 'admin' ? 'badge-purple' : 'badge-blue'}`}>
                    {u.role === 'admin' ? <><FiShield size={12} /> Admin</> : <><FiUser size={12} /> User</>}
                  </span>
                </td>
                <td><span className={`badge ${u.is_active ? 'badge-green' : 'badge-red'}`}>{u.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>{new Date(u.created_at).toLocaleDateString()}</td>
                <td>
                  {u.role !== 'admin' && (
                    <button className="btn btn-ghost btn-sm" onClick={() => deleteUser(u.id)}>
                      <FiTrash2 size={14} style={{ color: 'var(--accent-red)' }} />
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
