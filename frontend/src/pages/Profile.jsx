import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import { FiUser, FiMail, FiPhone, FiSave } from 'react-icons/fi';

export default function Profile() {
  const { user, updateUser } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true); setMessage('');
    try {
      const res = await api.put('/api/auth/profile', { name, phone, bio });
      updateUser(res.data);
      setMessage('Profile updated successfully!');
    } catch (err) { setMessage('Failed to update profile.'); }
    finally { setSaving(false); }
  };

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '600px' }}>
      <div className="page-header">
        <h1>Profile</h1>
        <p>Manage your account settings.</p>
      </div>

      <div className="glass-card" style={{ padding: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '28px' }}>
          <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'var(--gradient-primary)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px', fontWeight: '800' }}>
            {user?.name?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: '700' }}>{user?.name}</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>{user?.email} · <span className="badge badge-blue">{user?.role}</span></p>
          </div>
        </div>

        {message && <div className={`alert ${message.includes('success') ? 'alert-success' : 'alert-error'}`} style={{ marginBottom: '20px' }}>{message}</div>}

        <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="input-group">
            <label><FiUser size={14} style={{ marginRight: '6px' }} />Full Name</label>
            <input type="text" className="input-field" value={name} onChange={e => setName(e.target.value)} required />
          </div>
          <div className="input-group">
            <label><FiMail size={14} style={{ marginRight: '6px' }} />Email</label>
            <input type="email" className="input-field" value={user?.email} disabled style={{ opacity: 0.6 }} />
          </div>
          <div className="input-group">
            <label><FiPhone size={14} style={{ marginRight: '6px' }} />Phone</label>
            <input type="text" className="input-field" placeholder="+1 234 567 8900" value={phone} onChange={e => setPhone(e.target.value)} />
          </div>
          <div className="input-group">
            <label>Bio</label>
            <textarea className="input-field" placeholder="Tell us about yourself..." value={bio} onChange={e => setBio(e.target.value)} rows={3} />
          </div>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            <FiSave size={16} /> {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </form>
      </div>
    </div>
  );
}
