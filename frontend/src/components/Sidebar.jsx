import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  FiHome, FiUpload, FiFileText, FiBarChart2,
  FiZap, FiUser, FiClock, FiSettings, FiShield,
  FiUsers, FiTrendingUp, FiX
} from 'react-icons/fi';
import './Sidebar.css';

const userLinks = [
  { to: '/dashboard', icon: FiHome, label: 'Dashboard' },
  { to: '/upload', icon: FiUpload, label: 'Upload Resume' },
  { to: '/job-description', icon: FiFileText, label: 'Job Description' },
  { to: '/analysis', icon: FiBarChart2, label: 'Analysis' },
  { to: '/suggestions', icon: FiZap, label: 'AI Suggestions' },
  { to: '/history', icon: FiClock, label: 'History' },
  { to: '/profile', icon: FiUser, label: 'Profile' },
];

const adminLinks = [
  { to: '/admin', icon: FiShield, label: 'Admin Dashboard' },
  { to: '/admin/users', icon: FiUsers, label: 'Manage Users' },
  { to: '/admin/analytics', icon: FiTrendingUp, label: 'Analytics' },
];

export default function Sidebar({ isOpen, onClose }) {
  const { user } = useAuth();
  const location = useLocation();

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <span className="sidebar-title">Navigation</span>
          <button className="sidebar-close" onClick={onClose}>
            <FiX size={18} />
          </button>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section">
            <span className="nav-section-label">Main</span>
            {userLinks.map(link => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={onClose}
              >
                <link.icon size={18} />
                <span>{link.label}</span>
              </NavLink>
            ))}
          </div>

          {user?.role === 'admin' && (
            <div className="nav-section">
              <span className="nav-section-label">Admin</span>
              {adminLinks.map(link => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                  onClick={onClose}
                >
                  <link.icon size={18} />
                  <span>{link.label}</span>
                </NavLink>
              ))}
            </div>
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user-info">
            <div className="sidebar-user-avatar">
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div>
              <div className="sidebar-user-name">{user?.name}</div>
              <div className="sidebar-user-role">{user?.role}</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
