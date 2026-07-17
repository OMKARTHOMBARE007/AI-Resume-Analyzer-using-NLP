import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { FiSun, FiMoon, FiLogOut, FiUser, FiMenu } from 'react-icons/fi';
import { useState } from 'react';
import './Navbar.css';

export default function Navbar({ onToggleSidebar }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar-left">
        {user && (
          <button className="navbar-menu-btn" onClick={onToggleSidebar}>
            <FiMenu size={20} />
          </button>
        )}
        <Link to={user ? '/dashboard' : '/'} className="navbar-brand">
          <div className="navbar-logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">Resume<span className="gradient-text">AI</span></span>
          </div>
        </Link>
      </div>

      <div className="navbar-right">
        <button className="theme-toggle" onClick={toggleTheme} title="Toggle theme">
          {theme === 'dark' ? <FiSun size={18} /> : <FiMoon size={18} />}
        </button>

        {user ? (
          <div className="user-menu" onClick={() => setShowDropdown(!showDropdown)}>
            <div className="user-avatar">
              {user.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <span className="user-name">{user.name}</span>

            {showDropdown && (
              <div className="dropdown-menu" onClick={e => e.stopPropagation()}>
                <Link to="/profile" className="dropdown-item" onClick={() => setShowDropdown(false)}>
                  <FiUser size={16} /> Profile
                </Link>
                <button className="dropdown-item danger" onClick={() => { logout(); setShowDropdown(false); }}>
                  <FiLogOut size={16} /> Logout
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="auth-buttons">
            <Link to="/login" className="btn btn-ghost btn-sm">Login</Link>
            <Link to="/register" className="btn btn-primary btn-sm">Get Started</Link>
          </div>
        )}
      </div>
    </nav>
  );
}
