import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { FiMail, FiArrowRight } from 'react-icons/fi';
import './Auth.css';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      await api.post('/api/auth/forgot-password', { email });
      setSent(true);
    } catch (err) { setError('Something went wrong. Please try again.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-bg"><div className="hero-orb hero-orb-1"></div><div className="hero-orb hero-orb-2"></div></div>
      <div className="auth-card glass-card animate-scaleIn">
        <div className="auth-header">
          <Link to="/" className="auth-logo"><span className="logo-icon">⚡</span><span className="logo-text">Resume<span className="gradient-text">AI</span></span></Link>
          <h1>Reset Password</h1>
          <p>Enter your email to receive a reset link</p>
        </div>

        {sent ? (
          <div className="alert alert-success">If the email exists, a reset link has been sent. Check your inbox.</div>
        ) : (
          <>
            {error && <div className="alert alert-error">{error}</div>}
            <form onSubmit={handleSubmit} className="auth-form">
              <div className="input-group">
                <label>Email</label>
                <div className="input-icon-wrapper">
                  <FiMail className="input-icon" />
                  <input type="email" className="input-field input-with-icon" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
                </div>
              </div>
              <button type="submit" className="btn btn-primary btn-lg auth-submit" disabled={loading}>
                {loading ? 'Sending...' : 'Send Reset Link'} {!loading && <FiArrowRight size={18} />}
              </button>
            </form>
          </>
        )}

        <div className="auth-footer">
          <p>Remember your password? <Link to="/login" className="auth-link">Sign in</Link></p>
        </div>
      </div>
    </div>
  );
}
