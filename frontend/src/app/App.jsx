import {Link, useNavigate, useLocation} from 'react-router-dom';
import {ArrowRight, Globe, Menu, X} from 'lucide-react';
import {useState} from 'react';
import {AuthProvider} from '../auth/AuthContext';
import {useAuth} from '../auth/useAuth';
import {LanguageProvider} from '../i18n';
import {useI18n} from '../i18n/useI18n';
import AppRoutes from './routes';
import {roleHome} from '../features/auth/roles';
import '../design-system/tokens.css';
import '../index.css';

function Shell() {
  const {user, logout} = useAuth();
  const {t, language, setLanguage} = useI18n();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const isAppView = location.pathname.startsWith('/citizen') || 
                    location.pathname.startsWith('/volunteer') || 
                    location.pathname.startsWith('/dashboard') || 
                    location.pathname.startsWith('/admin') || 
                    location.pathname.startsWith('/profile');
  const isAuthPage = location.pathname.startsWith('/auth') && location.pathname !== '/auth/role';

  if (isAuthPage || isAppView) {
    return <main id="main" tabIndex={-1} style={{height: '100%', minHeight: '100vh', display: 'flex', flexDirection: 'column'}}><AppRoutes/></main>;
  }

  return (
    <>
      <a className="skip-link" href="#main">{t('Skip to content')}</a>
      <header className="site-header" style={{ position: 'sticky', top: 0, zIndex: 100, padding: '1rem 4%', background: 'white' }}>
        <div className="site-header-top">
          <Link className="brand" to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
            <img src="/janvastu-logo.png" alt="JanVastu" style={{ height: '52px', objectFit: 'contain' }} />
          </Link>
          <button className="hamburger-btn" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        <div className={`site-header-content ${isMenuOpen ? 'open' : ''}`}>
          <nav aria-label={t('Main navigation')} className="main-nav" style={{ fontSize: '0.9rem', fontWeight: 500 }}>
            <Link to="/" style={{ color: '#4B5563', textDecoration: 'none' }} onClick={() => setIsMenuOpen(false)}>{t('How It Works')}</Link>
            <Link to="/auth/signup/citizen" style={{ color: '#4B5563', textDecoration: 'none' }} onClick={() => setIsMenuOpen(false)}>{t('For Citizens')}</Link>
            <Link to="/auth/access-request" style={{ color: '#4B5563', textDecoration: 'none' }} onClick={() => setIsMenuOpen(false)}>{t('For Planners')}</Link>
            <Link to="/accountability" style={{ color: '#4B5563', textDecoration: 'none' }} onClick={() => setIsMenuOpen(false)}>{t('Accountability')}</Link>
            <Link to="/" style={{ color: '#4B5563', textDecoration: 'none' }} onClick={() => setIsMenuOpen(false)}>{t('About')}</Link>
          </nav>

          <div className="actions">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', border: '1px solid #E5E7EB', padding: '0.4rem 0.75rem', borderRadius: '9999px', fontSize: '0.875rem' }}>
              <Globe size={16} color="#6B7280" />
              <select value={language} onChange={e => setLanguage(e.target.value)} style={{ border: 'none', background: 'transparent', outline: 'none', color: '#111827', fontWeight: 500 }}>
                <option value="en">English</option>
                <option value="hi">हिन्दी</option>
                <option value="or">ଓଡ଼ିଆ</option>
              </select>
            </div>

            {user ? (
              <>
                <Link to={roleHome(user.role)} className="button secondary" onClick={() => setIsMenuOpen(false)}>{t('Dashboard')}</Link>
                <button className="button" style={{ background: '#FEE2E2', color: '#B91C1C', border: 'none' }} onClick={async () => { try { await logout(); } finally { navigate('/auth/login'); } }}>{t('Sign out')}</button>
              </>
            ) : (
              <>
                <Link to="/auth/login" className="button secondary" style={{ background: 'transparent', border: '1px solid #E5E7EB', color: '#111827', padding: '0.5rem 1.25rem', borderRadius: '9999px' }} onClick={() => setIsMenuOpen(false)}>{t('Sign In')}</Link>
                <Link to="/auth/role" className="button" style={{ background: 'var(--color-primary)', color: 'white', border: 'none', padding: '0.5rem 1.25rem', borderRadius: '9999px', display: 'flex', gap: '0.5rem', alignItems: 'center' }} onClick={() => setIsMenuOpen(false)}>
                  {t('Report a Need')} <ArrowRight size={16} />
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      <main id="main" tabIndex={-1} style={{ minHeight: 'auto', padding: 0 }}>
        <AppRoutes/>
      </main>

      <footer style={{ background: '#0F172A', color: 'white', padding: '4rem 4% 2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '3rem', marginBottom: '3rem', maxWidth: '1400px', margin: '0 auto 3rem' }}>
          <div style={{ maxWidth: '300px' }}>
            <div style={{ marginBottom: '1.5rem' }}>
              <img src="/janvastu-logo.png" alt="JanVastu Logo" style={{ height: '56px', objectFit: 'contain', filter: 'brightness(0) invert(1)' }} />
            </div>
            <p style={{ color: '#9CA3AF', fontSize: '0.875rem' }}>Har Awaaz, Har Vastu, Har Vikas</p>
          </div>

          <div style={{ display: 'flex', gap: '4rem', flexWrap: 'wrap' }}>
            <div>
              <h4 style={{ color: 'white', marginBottom: '1rem', fontSize: '0.875rem', fontWeight: 600 }}>Platform</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem' }}>
                <li><Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>How It Works</Link></li>
                <li><Link to="/auth/role" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Report a Need</Link></li>
                <li><Link to="/accountability" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Projects</Link></li>
                <li><Link to="/accountability" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Accountability</Link></li>
              </ul>
            </div>
            <div>
              <h4 style={{ color: 'white', marginBottom: '1rem', fontSize: '0.875rem', fontWeight: 600 }}>Participate</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem' }}>
                <li><Link to="/auth/signup/citizen" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Citizens</Link></li>
                <li><Link to="/auth/signup/volunteer" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Volunteers</Link></li>
                <li><Link to="/auth/access-request" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Planners</Link></li>
                <li><Link to="/admin/login" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Auditors</Link></li>
              </ul>
            </div>
            <div>
              <h4 style={{ color: 'white', marginBottom: '1rem', fontSize: '0.875rem', fontWeight: 600 }}>Resources</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem' }}>
                <li><Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Help</Link></li>
                <li><Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Accessibility</Link></li>
                <li><Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Privacy</Link></li>
                <li><Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Data & Consent</Link></li>
              </ul>
            </div>
          </div>

          <div>
            <h4 style={{ color: 'white', marginBottom: '1rem', fontSize: '0.875rem', fontWeight: 600 }}>Stay Updated</h4>
            <p style={{ color: '#9CA3AF', fontSize: '0.875rem', marginBottom: '1rem' }}>Get the latest updates on JanVastu.</p>
            <div style={{ display: 'flex', background: 'white', padding: '0.25rem', borderRadius: '4px' }}>
              <input type="email" placeholder="Enter your email" style={{ border: 'none', outline: 'none', padding: '0.5rem', width: '200px' }} />
              <button style={{ background: 'var(--color-primary)', color: 'white', border: 'none', padding: '0.5rem 1rem', borderRadius: '4px', cursor: 'pointer' }}><ArrowRight size={16}/></button>
            </div>
          </div>
        </div>

        <div style={{ borderTop: '1px solid #334155', paddingTop: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.875rem', color: '#9CA3AF', maxWidth: '1400px', margin: '0 auto' }}>
          <p style={{ margin: 0 }}>© 2026 JanVastu. Digital Public Good Concept.</p>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Privacy</Link>
            <Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Terms</Link>
            <Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Accessibility</Link>
          </div>
        </div>
      </footer>
    </>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <Shell/>
      </AuthProvider>
    </LanguageProvider>
  );
}
