import { useState, useEffect } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useI18n } from '../../i18n/useI18n';
import { useAuth } from '../../auth/useAuth';
import { State, Empty, Badge, DateText, Field } from '../../components/UI';
import { useResource } from '../../components/useResource';
import { api } from '../../api/client';
import './CitizenDashboard.css';
import { 
  Home, PlusCircle, FileText, MapPin, BarChart2, Shield, Bell, User as UserIcon,
  Search, Globe, Droplet, Trash2, Zap, Cross, GraduationCap, Bus, Navigation, Grid,
  Mic, Camera, ArrowRight, ChevronRight, CheckCircle2, Users, AlertTriangle, MessageSquare
} from 'lucide-react';

export default function CitizenDashboard() {
  const { t, language } = useI18n();
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="dashboard-sidebar-header">
          <Link to="/" className="brand" style={{ display: 'flex', alignItems: 'center' }}>
            <img src="/janvastu-logo.png" alt="JanVastu" style={{ height: '40px', objectFit: 'contain' }} />
          </Link>
        </div>
        <nav className="dashboard-nav">
          <Link to="/citizen" className="dashboard-nav-item active"><Home size={20}/> {t('Home')}</Link>
          <Link to="/citizen/capture" className="dashboard-nav-item"><PlusCircle size={20}/> {t('Report a Need')}</Link>
          <Link to="/citizen" className="dashboard-nav-item"><FileText size={20}/> {t('My Requests')}</Link>
          <Link to="/citizen" className="dashboard-nav-item"><MapPin size={20}/> {t('Nearby')}</Link>
          <Link to="/citizen" className="dashboard-nav-item"><BarChart2 size={20}/> {t('Projects')}</Link>
          <Link to="/accountability" className="dashboard-nav-item"><Shield size={20}/> {t('Accountability')}</Link>
          <Link to="/citizen" className="dashboard-nav-item">
            <Bell size={20}/> {t('Notifications')} <span className="badge">3</span>
          </Link>
          <Link to="/profile" className="dashboard-nav-item"><UserIcon size={20}/> {t('Profile')}</Link>
        </nav>
        <div className="dashboard-promo">
          <img src="/sidebar-illustration.jpg" alt="Voice" style={{width: '100%', borderRadius: '12px', marginBottom: '1rem'}} />
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="dashboard-main">
        {/* Header */}
        <header className="dashboard-header">
          <div className="dashboard-search">
            <Search size={18} color="#9CA3AF" />
            <input type="text" placeholder={t('Search nearby projects, issues or locations...')} />
          </div>
          <div className="dashboard-header-actions">
            <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem', color: '#4B5563', fontWeight: 500}}>
              <MapPin size={18} color="#3B82F6"/> Bhubaneswar, Odisha
            </div>
            <button className="header-icon-btn"><Bell size={20}/> <span className="badge">3</span></button>
            <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.9rem', color: '#4B5563', fontWeight: 500}}>
              <Globe size={18}/> {language === 'en' ? 'English' : 'Hindi'}
            </div>
            <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
              <div style={{width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#1E3A8A', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold'}}>
                {user.full_name?.charAt(0) || 'P'}
              </div>
              <div style={{display: 'flex', flexDirection: 'column'}}>
                <span style={{fontSize: '0.85rem', fontWeight: 600, color: '#111827'}}>{user.full_name || 'Priya Sharma'}</span>
                <span style={{fontSize: '0.75rem', color: '#6B7280'}}>{t('Citizen')}</span>
              </div>
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="dashboard-content-scroll">
          <div className="dashboard-grid">
            
            {/* Center Column */}
            <div className="dash-center-col">
              
              {/* Banner */}
              <div className="dash-banner">
                <div className="dash-banner-content">
                  <div style={{color: '#0369A1', fontWeight: 700, marginBottom: '0.5rem'}}>{t('Welcome back,')}</div>
                  <h1 className="dash-banner-title">{user.full_name || 'Priya Sharma'} 👋</h1>
                  <p className="dash-banner-subtitle">
                    {t('Your voice matters. Together we can build better communities.')}
                  </p>
                </div>
                <img src="/citizen-hero.jpg" alt="Banner" className="dash-banner-img" />
              </div>

              {/* Report a Need */}
              <div className="dash-card">
                <div className="dash-card-header">
                  <div>
                    <h2 className="dash-card-title">{t('Report a Need')}</h2>
                    <p className="dash-card-subtitle">{t('Tell us what\'s happening in your area. Use voice, text, photo or video.')}</p>
                  </div>
                  <Link to="/citizen/capture" className="dash-card-link">{t('View Guide')} <ArrowRight size={16}/></Link>
                </div>

                <div className="category-grid">
                  {[
                    { icon: Droplet, name: 'Water', color: '#3B82F6', active: true },
                    { icon: Trash2, name: 'Sanitation', color: '#10B981' },
                    { icon: Zap, name: 'Electricity', color: '#F59E0B' },
                    { icon: Cross, name: 'Healthcare', color: '#EF4444' },
                    { icon: GraduationCap, name: 'Education', color: '#8B5CF6' },
                    { icon: Bus, name: 'Transport', color: '#3B82F6' },
                    { icon: Navigation, name: 'Roads', color: '#6B7280' },
                    { icon: Grid, name: 'Other', color: '#6B7280' }
                  ].map(c => (
                    <div className={`category-item ${c.active ? 'active' : ''}`} key={c.name}>
                      <div className="category-icon" style={{color: c.color}}>
                        <c.icon size={24} />
                      </div>
                      <span className="category-name">{t(c.name)}</span>
                    </div>
                  ))}
                </div>

                <div className="action-grid">
                  <button className="action-btn green" onClick={() => navigate('/citizen/capture')}>
                    <div className="icon-circle"><Mic size={20}/></div>
                    <div>
                      <div className="action-btn-title">{t('Speak Your Problem')}</div>
                      <div className="action-btn-sub">{t('Supports multiple languages')}</div>
                    </div>
                  </button>
                  <button className="action-btn blue" onClick={() => navigate('/citizen/capture')}>
                    <div className="icon-circle"><FileText size={20}/></div>
                    <div>
                      <div className="action-btn-title">{t('Type a Message')}</div>
                      <div className="action-btn-sub">{t('Describe the issue')}</div>
                    </div>
                  </button>
                  <button className="action-btn light-green" onClick={() => navigate('/citizen/capture')}>
                    <div className="icon-circle"><Camera size={20}/></div>
                    <div>
                      <div className="action-btn-title">{t('Upload Photo / Video')}</div>
                      <div className="action-btn-sub">{t('Show what\'s happening')}</div>
                    </div>
                  </button>
                  <button className="action-btn blue" style={{backgroundColor: '#F3F4F6', color: '#1E3A8A'}} onClick={() => navigate('/citizen/capture')}>
                    <div className="icon-circle" style={{backgroundColor: 'white', color: '#3B82F6'}}><MapPin size={20}/></div>
                    <div>
                      <div className="action-btn-title">{t('Add Location')}</div>
                      <div className="action-btn-sub">{t('Use current or select on map')}</div>
                    </div>
                  </button>
                </div>
              </div>

              {/* Bottom Row */}
              <div className="bottom-grid">
                <div className="dash-card">
                  <div className="dash-card-header" style={{marginBottom: '1rem'}}>
                    <div>
                      <h2 className="dash-card-title"><MapPin size={20} color="#047857"/> {t('Nearby Projects')}</h2>
                      <p className="dash-card-subtitle">{t('Infrastructure projects in your area')}</p>
                    </div>
                    <Link to="/citizen" className="dash-card-link">{t('View All Projects')} <ArrowRight size={16}/></Link>
                  </div>
                  <div className="map-container">
                    <img src="/map-placeholder.jpg" alt="Map" />
                  </div>
                  <div style={{display: 'flex', gap: '1rem', fontSize: '0.75rem', color: '#6B7280', justifyContent: 'center'}}>
                    <span style={{display: 'flex', alignItems: 'center', gap: '0.25rem'}}><span style={{width: 8, height: 8, borderRadius: '50%', backgroundColor: '#3B82F6'}}></span> Water</span>
                    <span style={{display: 'flex', alignItems: 'center', gap: '0.25rem'}}><span style={{width: 8, height: 8, borderRadius: '50%', backgroundColor: '#10B981'}}></span> Sanitation</span>
                    <span style={{display: 'flex', alignItems: 'center', gap: '0.25rem'}}><span style={{width: 8, height: 8, borderRadius: '50%', backgroundColor: '#EF4444'}}></span> Healthcare</span>
                  </div>
                </div>

                <div className="dash-card">
                  <div className="dash-card-header" style={{marginBottom: '1.5rem'}}>
                    <h2 className="dash-card-title"><FileText size={20} color="#047857"/> {t('My Recent Requests')}</h2>
                    <Link to="/citizen" className="dash-card-link">{t('View All')} <ArrowRight size={16}/></Link>
                  </div>
                  <div className="request-list">
                    {[
                      { title: 'Road repair needed near KIIT Square', loc: 'Ward 18', status: 'In Progress', date: '12 Sep 2026', type: 'progress' },
                      { title: 'Irregular water supply in our area', loc: 'Ward 18', status: 'Under Review', date: '2 Sep 2026', type: 'review' },
                      { title: 'Street light not working', loc: 'Ward 19', status: 'Resolved', date: '18 Aug 2026', type: 'progress', color: '#10B981' },
                    ].map((r, i) => (
                      <div className="request-item" key={i}>
                        <div className="request-img"></div>
                        <div className="request-info">
                          <div className="request-title">{r.title}</div>
                          <div className="request-meta"><MapPin size={12}/> {r.loc}</div>
                        </div>
                        <div className="request-status-col">
                          <span className={`status-badge ${r.type}`} style={r.color ? {color: r.color, backgroundColor: '#D1FAE5'} : {}}>{r.status}</span>
                          <span className="request-meta">{r.date}</span>
                        </div>
                        <ChevronRight size={16} color="#9CA3AF"/>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

            </div>

            {/* Right Column */}
            <div className="dash-right-col">
              
              <div className="dash-card">
                <div className="dash-card-header">
                  <h2 className="dash-card-title" style={{color: '#1E3A8A'}}><BarChart2 size={20}/> {t('Your Impact')}</h2>
                  <Link to="/citizen" className="dash-card-link" style={{fontSize: '0.8rem'}}>{t('View details')} <ArrowRight size={14}/></Link>
                </div>
                <div className="impact-grid">
                  <div className="impact-item">
                    <div className="impact-icon" style={{backgroundColor: '#FEE2E2', color: '#EF4444'}}><FileText size={20}/></div>
                    <div><div className="impact-value">5</div><div className="impact-label">{t('Requests Submitted')}</div></div>
                  </div>
                  <div className="impact-item">
                    <div className="impact-icon" style={{backgroundColor: '#D1FAE5', color: '#10B981'}}><CheckCircle2 size={20}/></div>
                    <div><div className="impact-value">2</div><div className="impact-label">{t('In Progress')}</div></div>
                  </div>
                  <div className="impact-item">
                    <div className="impact-icon" style={{backgroundColor: '#D1FAE5', color: '#10B981'}}><CheckCircle2 size={20}/></div>
                    <div><div className="impact-value">1</div><div className="impact-label">{t('Resolved')}</div></div>
                  </div>
                  <div className="impact-item">
                    <div className="impact-icon" style={{backgroundColor: '#DBEAFE', color: '#3B82F6'}}><Users size={20}/></div>
                    <div><div className="impact-value">127</div><div className="impact-label">{t('People Benefited (Estimated)')}</div></div>
                  </div>
                </div>
              </div>

              <div className="dash-card">
                <div className="dash-card-header" style={{marginBottom: '1rem'}}>
                  <h2 className="dash-card-title" style={{color: '#1E3A8A'}}><Zap size={20}/> {t('AI Understanding')}</h2>
                  <span style={{fontSize: '0.7rem', fontWeight: 700, backgroundColor: '#FEF3C7', color: '#D97706', padding: '0.2rem 0.5rem', borderRadius: '4px'}}>DEMO</span>
                </div>
                <div className="ai-card">
                  <p className="ai-quote">"हमारे क्षेत्र में तीन दिन से पानी नहीं आ रहा है।"</p>
                  <table className="ai-table">
                    <tbody>
                      <tr><td>Language</td><td>Hindi</td></tr>
                      <tr><td>Category</td><td>Drinking Water</td></tr>
                      <tr><td>Location</td><td>Ward 18, Bhubaneswar</td></tr>
                      <tr><td>Intent</td><td>Infrastructure Need</td></tr>
                    </tbody>
                  </table>
                </div>
                <div style={{marginTop: '1rem', padding: '0.75rem', backgroundColor: '#EFF6FF', borderRadius: '8px', color: '#1E3A8A', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 500}}>
                  <MapPin size={16}/> {t('47 similar reports found in this area')} <ChevronRight size={16} style={{marginLeft: 'auto'}}/>
                </div>
              </div>

              <div className="dash-card">
                <h2 className="dash-card-title" style={{color: '#1E3A8A', marginBottom: '1rem'}}><Zap size={20}/> {t('Quick Actions')}</h2>
                <div className="quick-actions-grid">
                  <button className="qa-btn"><FileText size={16} color="#EF4444"/> {t('Track Request')}</button>
                  <button className="qa-btn"><MapPin size={16} color="#3B82F6"/> {t('Nearby Projects')}</button>
                  <button className="qa-btn"><AlertTriangle size={16} color="#EF4444"/> {t('Raise an Issue')}</button>
                  <button className="qa-btn"><MessageSquare size={16} color="#10B981"/> {t('Give Feedback')}</button>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
export function EvidenceMedia({item}){
 const [url,setUrl]=useState(''),[failed,setFailed]=useState(false),{t}=useI18n();
 useEffect(()=>{let object,active=true;api('/citizen/media/'+item.id).then(blob=>{object=URL.createObjectURL(blob);if(active)setUrl(object);else URL.revokeObjectURL(object);}).catch(()=>setFailed(true));return()=>{active=false;if(object)URL.revokeObjectURL(object);};},[item.id]);
 if(failed)return <p>{t('media_unavailable')}</p>;
 if(!url)return <p role="status">{t('Loading…')}</p>;
 return item.content_type?.startsWith('image')?<img className="evidence" src={url} alt={t('Submitted evidence')}/>:item.content_type?.startsWith('video')?<video aria-label={t('Submitted evidence')} className="evidence" src={url} controls/>:<audio aria-label={t('Submitted evidence')} src={url} controls/>;
}
export function RequestDetail(){
 const {id}=useParams(),{t}=useI18n(),resource=useResource('/citizen/needs/'+id);
 return <State resource={resource}>{n=><section className="card narrow"><h1>{t('Request tracking')}</h1><p>{t('Tracking ID')}: {n.id}</p><Badge>{n.status}</Badge><h2>{t(n.category)}</h2><p>{n.description}</p><p>{n.address||n.district}</p><h2>{t('Timeline')}</h2><ol>{n.events.map((e,i)=><li key={i}>{t(e.status)} · <DateText value={e.created_at}/></li>)}</ol><h2>{t('Evidence')}</h2>{n.evidence.length?n.evidence.map(e=><EvidenceMedia key={e.id} item={e}/>):<Empty/>}</section>}</State>;
}
