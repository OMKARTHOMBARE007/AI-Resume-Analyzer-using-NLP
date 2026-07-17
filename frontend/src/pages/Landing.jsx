import { Link } from 'react-router-dom';
import { FiUpload, FiCpu, FiTarget, FiBarChart2, FiZap, FiShield, FiArrowRight } from 'react-icons/fi';
import './Landing.css';

const features = [
  { icon: FiUpload, title: 'Smart Upload', desc: 'Upload PDF or DOCX resumes with drag-and-drop. Instant parsing with AI.', color: 'blue' },
  { icon: FiCpu, title: 'NLP Analysis', desc: 'Advanced NLP pipeline extracts skills, experience, education, and more.', color: 'purple' },
  { icon: FiTarget, title: 'ATS Scoring', desc: 'Get a detailed ATS score across 7 categories with weighted analysis.', color: 'emerald' },
  { icon: FiBarChart2, title: 'Smart Matching', desc: 'TF-IDF and Semantic Similarity compare your resume vs job description.', color: 'cyan' },
  { icon: FiZap, title: 'AI Suggestions', desc: 'Intelligent recommendations for skills, certifications, and formatting.', color: 'amber' },
  { icon: FiShield, title: 'PDF Reports', desc: 'Download detailed analysis reports as professional PDFs.', color: 'pink' },
];

const stats = [
  { value: '500+', label: 'Skills Detected' },
  { value: '7', label: 'Score Categories' },
  { value: '95%', label: 'Parse Accuracy' },
  { value: '<3s', label: 'Analysis Time' },
];

export default function Landing() {
  return (
    <div className="landing">
      {/* Hero */}
      <section className="hero">
        <div className="hero-bg">
          <div className="hero-orb hero-orb-1"></div>
          <div className="hero-orb hero-orb-2"></div>
          <div className="hero-orb hero-orb-3"></div>
        </div>
        <div className="hero-content container">
          <div className="hero-badge">
            <span className="badge badge-blue">⚡ Powered by AI & NLP</span>
          </div>
          <h1 className="hero-title">
            Analyze Your Resume<br />
            <span className="gradient-text">with AI Intelligence</span>
          </h1>
          <p className="hero-subtitle">
            Upload your resume, compare it against job descriptions, get ATS scores,
            and receive intelligent recommendations to land your dream job.
          </p>
          <div className="hero-actions">
            <Link to="/register" className="btn btn-primary btn-lg">
              Get Started Free <FiArrowRight size={18} />
            </Link>
            <Link to="/login" className="btn btn-ghost btn-lg">
              Sign In
            </Link>
          </div>

          <div className="hero-stats">
            {stats.map((stat, i) => (
              <div key={i} className="stat-item">
                <span className="stat-value">{stat.value}</span>
                <span className="stat-label">{stat.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features-section container">
        <div className="section-header">
          <h2>Everything You Need to<br /><span className="gradient-text">Optimize Your Resume</span></h2>
          <p>Our AI-powered platform provides comprehensive resume analysis and optimization tools.</p>
        </div>

        <div className="features-grid">
          {features.map((feature, i) => (
            <div key={i} className="feature-card glass-card animate-fadeIn" style={{ animationDelay: `${i * 0.1}s` }}>
              <div className={`feature-icon feature-icon-${feature.color}`}>
                <feature.icon size={24} />
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="how-it-works container">
        <div className="section-header">
          <h2>How It <span className="gradient-text">Works</span></h2>
          <p>Three simple steps to optimize your resume for any job.</p>
        </div>
        <div className="steps-grid">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Upload Resume</h3>
            <p>Upload your resume in PDF or DOCX format. Our parser extracts all relevant information.</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Add Job Description</h3>
            <p>Paste the job description you're targeting. Our NLP engine identifies key requirements.</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Get Results</h3>
            <p>View your ATS score, matched skills, missing skills, and AI-powered improvement suggestions.</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-card glass-card">
            <h2>Ready to optimize your resume?</h2>
            <p>Join thousands of job seekers using AI to land their dream jobs.</p>
            <Link to="/register" className="btn btn-primary btn-lg">
              Start Free Analysis <FiArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <span className="logo-icon">⚡</span>
              <span className="logo-text">Resume<span className="gradient-text">AI</span></span>
            </div>
            <p className="footer-text">AI-powered resume analysis using NLP. Built with FastAPI, React, spaCy, and Sentence Transformers.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
