import {Link} from 'react-router-dom';
import {
  Mic, FileText, Camera, Video, Languages, Target, Network, Share2, AlertCircle, Eye, 
  MessageCircle, BarChart3, ShieldCheck, MapPin, Search, Database, Fingerprint, Activity, Layers, ArrowRight
} from 'lucide-react';
import {useI18n} from '../../i18n/useI18n';
import './Landing.css';
import heroImage from '../../assets/landing-hero.jpg';

export default function Landing() {
  const {t} = useI18n();
  
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="landing-hero">
        <div className="landing-hero-content">
          <span className="landing-hero-eyebrow">{t("PEOPLE'S INFRASTRUCTURE BRIDGE")}</span>
          <h1>{t('Every Community Knows What It Needs.')} <span>{t('JanVastu')}</span> {t('Helps Make That Voice Visible.')}</h1>
          <p>{t('Tell us what your community needs through voice, text, photos or video. JanVastu transforms those signals into structured civic intelligence that can help inform infrastructure planning and public accountability.')}</p>
          
          <div className="landing-hero-actions">
            <Link className="landing-hero-btn primary" to="/auth/role">
              {t('Report a Need')} <ArrowRight size={18} />
            </Link>
            <Link className="landing-hero-btn secondary" to="/accountability">
              <BarChart3 size={18} /> {t('Explore Projects')}
            </Link>
          </div>
          
          <div className="landing-hero-features">
            <div className="landing-hero-feature"><Mic size={16} /> {t('Voice')}</div>
            <div className="landing-hero-feature"><FileText size={16} /> {t('Text')}</div>
            <div className="landing-hero-feature"><Camera size={16} /> {t('Photo')}</div>
            <div className="landing-hero-feature"><Video size={16} /> {t('Video')}</div>
            <div className="landing-hero-feature"><Languages size={16} /> {t('Multilingual')}</div>
          </div>
        </div>
        <div className="landing-hero-image-wrapper">
          <img src={heroImage} alt="JanVastu Hero" className="landing-hero-image" />
        </div>
      </section>

      {/* Value Prop Bar */}
      <div className="value-prop-bar">
        <div className="value-prop-title">
          {t('BUILT FOR INCLUSIVE CIVIC PARTICIPATION')}
        </div>
        <div className="value-prop-items">
          <div className="value-prop-item">
            <Mic className="value-prop-icon" size={24} />
            <div className="value-prop-text">
              <h3>{t('Voice-first')}</h3>
              <p>{t('Accessible for everyone')}</p>
            </div>
          </div>
          <div className="value-prop-item">
            <Languages className="value-prop-icon" size={24} />
            <div className="value-prop-text">
              <h3>{t('Multilingual')}</h3>
              <p>{t('Designed for india')}</p>
            </div>
          </div>
          <div className="value-prop-item">
            <Camera className="value-prop-icon" size={24} />
            <div className="value-prop-text">
              <h3>{t('Evidence-based')}</h3>
              <p>{t('With photos, location and context')}</p>
            </div>
          </div>
          <div className="value-prop-item">
            <ShieldCheck className="value-prop-icon" size={24} />
            <div className="value-prop-text">
              <h3>{t('Accountability-focused')}</h3>
              <p>{t('Connecting people to progress')}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Problems Section */}
      <section className="section-problems">
        <div className="section-problems-header">
          <h2>{t('Development Problems Are Everywhere. The Signals Are Scattered.')}</h2>
          <p>{t('Citizen needs are often reported through different channels, while infrastructure, demographic and project information can exist separately.')}</p>
        </div>
        <div className="problem-cards">
          <div className="problem-card">
            <div className="problem-icon"><MessageCircle size={24} /></div>
            <h3>{t('Fragmented Voices')}</h3>
            <p>{t('Citizen needs can arrive through different channels.')}</p>
          </div>
          <div className="problem-card">
            <div className="problem-icon"><Database size={24} /></div>
            <h3>{t('Limited Context')}</h3>
            <p>{t('Demand and infrastructure information may not be visible together.')}</p>
          </div>
          <div className="problem-card">
            <div className="problem-icon"><BarChart3 size={24} /></div>
            <h3>{t('Planning Gaps')}</h3>
            <p>{t('Understanding where demand intersects with infrastructure requires combining multiple signals.')}</p>
          </div>
          <div className="problem-card">
            <div className="problem-icon"><FileText size={24} /></div>
            <h3>{t('Accountability')}</h3>
            <p>{t('Citizens need clear information about projects, progress and responsibility.')}</p>
          </div>
        </div>
      </section>

      {/* Journey Section */}
      <section className="section-journey">
        <div className="section-journey-inner">
          <h2>{t('From One Voice to a Policy Signal.')}</h2>
          <div className="journey-steps">
            <div className="journey-step">
              <div className="journey-icon"><Mic size={28} /></div>
              <h3>01. VOICE</h3>
              <p>{t('Citizen reports a need.')}</p>
            </div>
            <ArrowRight className="journey-arrow" size={24} />
            <div className="journey-step">
              <div className="journey-icon"><FileText size={28} /></div>
              <h3>02. UNDERSTAND</h3>
              <p>{t('AI identifies language, intent, category and location.')}</p>
            </div>
            <ArrowRight className="journey-arrow" size={24} />
            <div className="journey-step">
              <div className="journey-icon"><Share2 size={28} /></div>
              <h3>03. CONNECT</h3>
              <p>{t('Similar signals become geographic demand patterns.')}</p>
            </div>
            <ArrowRight className="journey-arrow" size={24} />
            <div className="journey-step">
              <div className="journey-icon"><Database size={28} /></div>
              <h3>04. CONTEXT</h3>
              <p>{t('Infrastructure and planning information provide additional context.')}</p>
            </div>
            <ArrowRight className="journey-arrow" size={24} />
            <div className="journey-step">
              <div className="journey-icon"><Target size={28} /></div>
              <h3>05. INSIGHT</h3>
              <p>{t('JanVastu surfaces explainable areas for attention.')}</p>
            </div>
            <ArrowRight className="journey-arrow" size={24} />
            <div className="journey-step">
              <div className="journey-icon"><ShieldCheck size={28} /></div>
              <h3>06. ACCOUNTABILITY</h3>
              <p>{t('Projects and public information can be followed.')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Split Section */}
      <section className="section-split">
        <div className="split-left">
          <h2>{t('Just Speak.')}<br/><span style={{color: 'var(--color-primary)'}}>{t('JanVastu')}</span> {t('Understands.')}</h2>
          <p>{t('Report a community need in the way that feels natural to you.')}</p>
          
          <h3 style={{fontSize: '1.25rem', marginTop: '2rem', marginBottom: '1rem', color: '#111827'}}>{t('Your Language. Your Community. Your Voice.')}</h3>
          <p>{t('JanVastu is designed for multilingual civic participation.')}</p>
          
          <div className="lang-grid">
            <div className="lang-pill active">English</div>
            <div className="lang-pill">हिन्दी</div>
            <div className="lang-pill">ଓଡ଼ିଆ</div>
            <div className="lang-pill">বাংলা</div>
            <div className="lang-pill">தமிழ்</div>
            <div className="lang-pill">తెలుగు</div>
            <div className="lang-pill">मराठी</div>
            <div className="lang-pill">ગુજરાતી</div>
            <div className="lang-pill">ಕನ್ನಡ</div>
            <div className="lang-pill">മലയാളം</div>
            <div className="lang-pill">ਪੰਜਾਬੀ</div>
            <div className="lang-pill">اردو</div>
            <div className="lang-pill" style={{background: 'transparent', border: 'none', color: 'var(--color-primary)'}}>+10 more languages</div>
          </div>
        </div>
        
        <div className="split-right">
          <h2>{t("Reporting Shouldn't Feel Like Filling Out a Form.")}</h2>
          <p>{t('We made it simple to provide rich, evidence-based reports.')}</p>
          
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-card-icon"><Mic size={20} /></div>
              <div>
                <h3>{t('Speak')}</h3>
                <p>{t('Tell JanVastu what is happening in your own language.')}</p>
              </div>
            </div>
            <div className="feature-card">
              <div className="feature-card-icon"><Camera size={20} /></div>
              <div>
                <h3>{t('Show')}</h3>
                <p>{t('Upload photos or short videos as evidence.')}</p>
              </div>
            </div>
            <div className="feature-card">
              <div className="feature-card-icon"><MapPin size={20} /></div>
              <div>
                <h3>{t('Locate')}</h3>
                <p>{t('Attach the relevant location.')}</p>
              </div>
            </div>
            <div className="feature-card">
              <div className="feature-card-icon"><FileText size={20} /></div>
              <div>
                <h3>{t('Track')}</h3>
                <p>{t('Follow what happens to your request.')}</p>
              </div>
            </div>
          </div>
          
          <div style={{marginTop: '3rem'}}>
            <Link className="landing-hero-btn primary" style={{width: '100%', justifyContent: 'center'}} to="/auth/role">
              {t('Report a Need')} <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section-stats">
        <div className="stat-brand">
          <img src="/janvastu-logo.png" alt="JanVastu" style={{ height: '40px', objectFit: 'contain' }} />
          <div>
            <h3>{t('See the JanVastu Signal')}</h3>
            <p>{t('Illustrative demo data')}</p>
          </div>
        </div>
        
        <div className="stat-items">
          <div className="stat-item">
            <div className="stat-icon"><Mic size={20} /></div>
            <div className="stat-content">
              <h4>12,482</h4>
              <p>{t('Citizen Reports')}</p>
            </div>
          </div>
          <div className="stat-item">
            <div className="stat-icon"><ShieldCheck size={20} /></div>
            <div className="stat-content">
              <h4>9,816</h4>
              <p>{t('Verified Signals')}</p>
            </div>
          </div>
          <div className="stat-item">
            <div className="stat-icon"><Database size={20} /></div>
            <div className="stat-content">
              <h4>326</h4>
              <p>{t('Infrastructure Signals')}</p>
            </div>
          </div>
          <div className="stat-item">
            <div className="stat-icon"><MapPin size={20} /></div>
            <div className="stat-content">
              <h4>146</h4>
              <p>{t('Projects Tracked')}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
