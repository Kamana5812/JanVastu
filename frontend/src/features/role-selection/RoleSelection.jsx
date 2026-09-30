import {Link, useNavigate} from 'react-router-dom';
import {User, Users, Building2, ShieldCheck, ArrowRight} from 'lucide-react';
import {useI18n} from '../../i18n/useI18n';
import '../auth/Auth.css';

export default function RoleSelection() {
  const {t, language, setLanguage} = useI18n();
  const navigate = useNavigate();

  return (
    <div className="auth-page-wrapper">
      <header className="auth-header-top">
        <Link to="/" className="brand">
          <img src="/janvastu-logo.png" alt="JanVastu" style={{ height: '48px', objectFit: 'contain' }} />
        </Link>
        <div className="auth-lang-dropdown">
          🌐
          <select value={language} onChange={e => setLanguage(e.target.value)} style={{border: 'none', background: 'transparent', outline: 'none'}}>
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="or">ଓଡ଼ିଆ</option>
          </select>
        </div>
      </header>

      <div className="auth-card-container">
        <div className="auth-card" style={{ maxWidth: '800px', flexDirection: 'column', padding: '3rem 2rem', textAlign: 'center' }}>
          <h1 className="auth-title">{t('Welcome to JanVastu')}</h1>
          <p className="auth-subtitle">{t('Choose how you want to participate.')}</p>

          <div className="role-grid">
            {[
              ['Citizen', User, 'Report needs, track requests and explore public projects.', '/auth/signup/citizen', '#E8F5E9', '#2E7D32'],
              ['Volunteer', Users, 'Help communities report and verify local infrastructure needs.', '/auth/signup/volunteer', '#E3F2FD', '#1565C0'],
              ['Government / Planner', Building2, 'Explore infrastructure demand and decision-support insights.', '/auth/access-request', '#FFF3E0', '#E65100'],
              ['Auditor', ShieldCheck, 'Review governance, accountability and audit information.', '/admin/login', '#F3E5F5', '#6A1B9A']
            ].map(([label, Icon, desc, path, bg, color]) => (
              <div className="role-card" key={label} onClick={() => navigate(path)}>
                <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                  <div className="role-icon-wrapper" style={{backgroundColor: bg, color: color}}>
                    <Icon size={24} />
                  </div>
                  <h2 style={{fontSize: '1.25rem', fontWeight: '700', margin: 0, color: '#1F2937'}}>{t(`I am a ${label}`)}</h2>
                </div>
                <p style={{color: '#6B7280', margin: 0, fontSize: '0.9rem', flex: 1}}>{t(desc)}</p>
                <div style={{display: 'flex', justifyContent: 'flex-end'}}>
                  <div style={{width: '32px', height: '32px', borderRadius: '50%', backgroundColor: color, color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                    <ArrowRight size={16} />
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div style={{marginTop: '3rem', textAlign: 'center'}}>
            <img src="/janvastu-logo.png" alt="Brand Art" style={{height: '80px', objectFit: 'contain', opacity: 0.8}} />
            <p style={{marginTop: '2rem', color: '#6B7280'}}>
              {t('Already have an account?')} <Link to="/auth/login" style={{color: 'var(--color-primary)', fontWeight: '600'}}>{t('Sign In')}</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
