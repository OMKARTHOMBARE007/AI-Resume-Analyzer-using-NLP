import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FiUser, FiMail, FiLock, FiArrowRight } from 'react-icons/fi';
import './Auth.css';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-bg">
        <div className="hero-orb hero-orb-1"></div>
        <div className="hero-orb hero-orb-2"></div>
      </div>
      <div className="auth-card glass-card animate-scaleIn">
        <div className="auth-header">
          <Link to="/" className="auth-logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">Resume<span className="gradient-text">AI</span></span>
          </Link>
          <h1>Create Account</h1>
          <p>Start analyzing your resumes with AI</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <label>Full Name</label>
            <div className="input-icon-wrapper">
              <FiUser className="input-icon" />
              <input type="text" className="input-field input-with-icon" placeholder="John Doe" value={name} onChange={e => setName(e.target.value)} required />
            </div>
          </div>

          <div className="input-group">
            <label>Email</label>
            <div className="input-icon-wrapper">
              <FiMail className="input-icon" />
              <input type="email" className="input-field input-with-icon" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>
          </div>

          <div className="input-group">
            <label>Password</label>
            <div className="input-icon-wrapper">
              <FiLock className="input-icon" />
              <input type="password" className="input-field input-with-icon" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} required minLength={6} />
            </div>
          </div>

          <div className="input-group">
            <label>Confirm Password</label>
            <div className="input-icon-wrapper">
              <FiLock className="input-icon" />
              <input type="password" className="input-field input-with-icon" placeholder="••••••••" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-lg auth-submit" disabled={loading}>
            {loading ? 'Creating account...' : 'Create Account'}
            {!loading && <FiArrowRight size={18} />}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account? <Link to="/login" className="auth-link">Sign in</Link></p>
        </div>
      </div>
    </div>
  );
}
