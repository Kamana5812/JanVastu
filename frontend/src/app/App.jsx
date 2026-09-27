import { Link, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '../auth/AuthContext';
import { LanguageProvider, useI18n } from '../i18n';
import AppRoutes from './routes';
import { roleHome } from '../features/auth/AuthPages';
import '../design-system/tokens.css';
import '../index.css';
function Shell(){
 const {user,logout}=useAuth(),{t,language,setLanguage}=useI18n(),navigate=useNavigate();
 return <><a className="skip-link" href="#main">{t('Skip to content')}</a><header className="site-header"><Link className="brand" to="/">JanVastu</Link><nav aria-label={t('Main navigation')}><Link to="/accountability">{t('Accountability')}</Link>{user?<><Link to={roleHome(user.role)}>{t('Dashboard')}</Link><Link to="/profile">{t('Profile')}</Link><button className="text-button" onClick={async()=>{try{await logout();}finally{navigate('/auth/login');}}}>{t('Sign out')}</button></>:<Link to="/auth/login">{t('Sign in')}</Link>}<label><span className="sr-only">{t('Language')}</span><select value={language} onChange={e=>setLanguage(e.target.value)}><option value="en">English</option><option value="hi">हिन्दी</option><option value="or">ଓଡ଼ିଆ</option></select></label></nav></header><main id="main" tabIndex={-1}><AppRoutes/></main><footer>{t('JanVastu supports human decisions. Public sample data is labeled.')}</footer></>;
}
export default function App(){return <LanguageProvider><AuthProvider><Shell/></AuthProvider></LanguageProvider>;}
