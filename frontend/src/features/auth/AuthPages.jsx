import {useState, useEffect} from 'react';
import {Link, Navigate, useNavigate, useSearchParams} from 'react-router-dom';
import {Eye, EyeOff, Mic, Camera, Video, Languages, CheckCircle, Smartphone, MapPin, Building2, ShieldCheck, ArrowLeft, HeartHandshake, PhoneCall, Globe} from 'lucide-react';
import {useAuth} from '../../auth/useAuth';
import {api} from '../../api/client';
import {useI18n} from '../../i18n/useI18n';
import {Field, Notice} from '../../components/UI';
import GoogleLogin from './GoogleLogin';
import {roleHome} from './roles';
import citizenImg from '../../assets/citizen-auth.jpg';
import volunteerImg from '../../assets/volunteer-auth.jpg';
import './Auth.css';

// Side Panel Component - Embedded inside the auth-card
const AuthSidePanel = ({ kind }) => {
  const { t } = useI18n();
  let img = citizenImg;
  let title = "Report in your language in the way that feels natural.";
  let features = [
    { icon: Mic, text: "Voice" },
    { icon: Camera, text: "Photo" },
    { icon: Video, text: "Video" },
    { icon: Languages, text: "Multilingual" }
  ];

  if (kind === 'volunteer') {
    img = volunteerImg;
    features = [
      { icon: Camera, text: "Capture requests" },
      { icon: CheckCircle, text: "Verify submissions" },
      { icon: MapPin, text: "Work in field mode" },
      { icon: HeartHandshake, text: "Support your community" }
    ];
  }

  if (kind === 'official') return null;

  return (
    <div className="auth-info-side">
      <div className="auth-info-text">{t(title)}</div>
      <img src={img} alt="Authentication" className="auth-info-image-arch" />
      <div className="auth-info-features">
        {features.map((f, i) => (
          <div key={i} className="auth-info-feature">
            <f.icon size={20} className="auth-info-icon" />
            {t(f.text)}
          </div>
        ))}
      </div>
      <p style={{ fontSize: '0.75rem', color: '#6B7280', margin: '2rem 0 0', display: 'flex', alignItems: 'center', gap: '0.25rem', textAlign: 'left' }}>
        <Globe size={14} style={{flexShrink:0}}/> {t('Your information is safe with us. We use it only to improve public services and follow data protection guidelines.')}
      </p>
    </div>
  );
};

// Header Component
const AuthHeader = () => {
  const { t, language, setLanguage } = useI18n();
  return (
    <header className="auth-header-top">
      <Link to="/" className="brand" style={{ display: 'flex', alignItems: 'center' }}>
        <img src="/janvastu-logo.png" alt="JanVastu" style={{ height: '48px', objectFit: 'contain' }} />
      </Link>
      <div className="auth-lang-dropdown">
        <Globe size={16} color="#6B7280" />
        <select value={language} onChange={e => setLanguage(e.target.value)} style={{border: 'none', background: 'transparent', outline: 'none'}}>
          <option value="en">English</option>
          <option value="hi">हिन्दी</option>
          <option value="or">ଓଡ଼ିଆ</option>
        </select>
      </div>
    </header>
  );
};

export function Login({ admin = false }) {
  const { t } = useI18n();
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const destination = role => (['citizen','volunteer'].includes(role) && params.get('next')?.startsWith('/citizen/report-need?project=')) ? params.get('next') : roleHome(role);
  
  const [error,setError]=useState('');
  const [busy,setBusy]=useState(false);
  const [show,setShow]=useState(false);
  const [mode,setMode]=useState(admin ? 'password' : 'otp');
  const [challenge,setChallenge]=useState(null);
  const [message,setMessage]=useState('');
  const [options,setOptions]=useState(null);

  useEffect(() => { api('/auth/options').then(setOptions).catch(() => {}); }, []);
  
  if (user) return <Navigate to={destination(user.role)} replace/>;

  async function submit(event) {
    event.preventDefault(); setBusy(true); setError(''); const f = Object.fromEntries(new FormData(event.currentTarget));
    try {
      let result;
      if (challenge) {
        let code = '';
        if (f.code) code = f.code;
        else {
          for(let i=0; i<6; i++) code += (f[`digit_${i}`] || '');
        }

        result = await await api(mode==='reset' ? '/auth/password/reset' : '/auth/otp/verify',
          {method:'POST', body:{challenge_id:challenge.challenge_id,code:code,...(mode==='reset'?{password:f.password}:{})}});
        if (mode==='reset') { setChallenge(null);setMode('password');setMessage(result.message);return; }
      } else {
        const path = mode==='reset' ? '/auth/password/reset-request' : mode==='otp' ? '/auth/otp/request' : admin ? '/admin/login' : '/auth/login';
        result = await api(path,{method:'POST',body:f});
      }
      if (result.requires_otp) setChallenge(result);
      else { login(result); navigate(destination(result.user.role)); }
    } catch(e) { setError(e.message); } finally { setBusy(false); }
  }

  return (
    <div className={`auth-page-wrapper ${admin ? 'admin-theme' : ''}`}>
      <AuthHeader />
      
      <div className="auth-card-container">
        <div className={`auth-card narrow`}>
          <div className="auth-form-side">
            {!challenge && (
              <>
                <h1 className="auth-title">{t(admin ? 'JanVastu Administration' : 'Welcome Back')}</h1>
                <p className="auth-subtitle">{t(admin ? 'Authorized platform administrators only.' : 'Sign in to your JanVastu account.')}</p>

                {!admin && (
                  <div className="auth-tabs">
                    <button className={`auth-tab ${mode === 'otp' ? 'active' : ''}`} onClick={() => setMode('otp')}>Mobile OTP</button>
                    <button className={`auth-tab ${mode === 'password' ? 'active' : ''}`} onClick={() => setMode('password')}>Email & Password</button>
                  </div>
                )}
              </>
            )}

            {challenge && (
              <>
                <button type="button" className="text-button" style={{marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', alignSelf: 'flex-start'}} onClick={() => setChallenge(null)}>
                  <ArrowLeft size={16} /> Back
                </button>
                <h1 className="auth-title">{t('Verify Your Mobile Number')}</h1>
                <p className="auth-subtitle">{t('We sent a 6-digit code.')} <Notice message="Demo verification: use code 123456. No SMS or email is sent."/></p>
              </>
            )}

            <Notice message={error} error/>
            <Notice message={message}/>

            <form onSubmit={submit}>
              {!challenge && (
                <>
                  <Field name="identifier" label={mode === 'otp' ? "Mobile Number" : admin ? "Admin ID / Email" : "Email or mobile"} required autoComplete="username" />
                  
                  {mode === 'password' && (
                    <div style={{ position: 'relative' }}>
                      <Field name="password" label="Password" required type={show ? 'text' : 'password'} autoComplete="current-password" maxLength={72} />
                      <button type="button" style={{ position: 'absolute', right: '0.5rem', top: '2rem', background: 'none', border: 'none', cursor: 'pointer', color: '#6B7280' }} onClick={() => setShow(!show)}>
                        {show ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  )}

                  {mode === 'password' && !admin && (
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <label className="check" style={{ margin: 0 }}><input type="checkbox" /> {t('Keep me signed in')}</label>
                      <button type="button" className="text-button" onClick={() => setMode('reset')}>{t('Forgot Password?')}</button>
                    </div>
                  )}
                  {admin && (
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <label className="check" style={{ margin: 0 }}><input type="checkbox" /> {t('Keep me signed in')}</label>
                    </div>
                  )}
                </>
              )}

              {challenge && (
                <>
                  <div className="otp-container">
                    {[...Array(6)].map((_, i) => (
                      <input key={i} name={`digit_${i}`} type="text" maxLength={1} className="otp-input" required
                        onChange={(e) => {
                          if (e.target.value && e.target.nextSibling) e.target.nextSibling.focus();
                        }}
                      />
                    ))}
                  </div>
                  {mode === 'reset' && <Field name="password" label="New password" type="password" required minLength={8} maxLength={72}/>}
                </>
              )}

              <button className="auth-button-primary" disabled={busy}>
                {admin && !challenge && <ShieldCheck size={18} style={{marginRight: '0.5rem', verticalAlign: 'middle'}}/>}
                {t(busy ? 'Loading…' : challenge ? 'Verify' : mode === 'reset' ? 'Reset password' : mode === 'otp' ? 'Send OTP' : admin ? 'Secure Sign In' : 'Sign In')}
              </button>
            </form>

            {!challenge && !admin && (
              <>
                <div className="auth-divider">or</div>
                <button type="button" className="auth-button-secondary" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }} onClick={() => setMode(mode === 'otp' ? 'password' : 'otp')}>
                  {mode === 'otp' ? <Eye size={18} /> : <Smartphone size={18} />}
                  {t(mode === 'otp' ? 'Continue with Password' : 'Continue with Mobile OTP')}
                </button>
                <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                  <span style={{ color: '#6B7280' }}>{t("Don't have an account?")}</span> <Link to="/auth/role" style={{ color: 'var(--color-primary)', fontWeight: '600' }}>{t('Create one')}</Link>
                </div>
              </>
            )}
            
            {!challenge && admin && (
              <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'space-between' }}>
                <Link to="/" style={{ color: '#9CA3AF', textDecoration: 'none' }}><ArrowLeft size={14} style={{verticalAlign: 'middle'}}/> Back to Home</Link>
                <a href="#" style={{ color: '#9CA3AF', textDecoration: 'none' }}>Need Help?</a>
              </div>
            )}

            {!challenge && !admin && (
              <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>{t('Need help signing in? Use assisted access')}</p>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginTop: '1rem' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', color: 'var(--color-primary)', cursor: 'pointer' }}>
                    <div style={{ background: '#F3F4F6', padding: '0.75rem', borderRadius: '50%' }}><PhoneCall size={20} /></div>
                    <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>IVR</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', color: 'var(--color-primary)', cursor: 'pointer' }}>
                    <div style={{ background: '#F3F4F6', padding: '0.75rem', borderRadius: '50%' }}><Building2 size={20} /></div>
                    <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>CSC Assistance</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', color: 'var(--color-primary)', cursor: 'pointer' }}>
                    <div style={{ background: '#F3F4F6', padding: '0.75rem', borderRadius: '50%' }}><HeartHandshake size={20} /></div>
                    <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>Volunteer</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export function Signup({ kind = 'citizen' }) {
  const { t, language } = useI18n();
  const { user, login } = useAuth();
  const navigate = useNavigate();
  
  const [error,setError]=useState('');
  const [busy,setBusy]=useState(false);
  const [done,setDone]=useState(false);
  const [otpMode,setOtpMode]=useState(kind !== 'official');
  const [signupChallenge,setSignupChallenge]=useState(null);

  if(user) return <Navigate to={roleHome(user.role)} replace/>;

  async function submit(event) {
    event.preventDefault();setBusy(true);setError('');
    const f=Object.fromEntries(new FormData(event.currentTarget));
    if(!otpMode && f.password !== f.confirm_password){setError('Passwords do not match.');setBusy(false);return;}
    delete f.confirm_password; f.consent=!!f.consent;
    if(!f.email)f.email=null; if(!f.mobile)f.mobile=null;
    
    try {
      const result=await api(otpMode?'/auth/signup/otp/request':kind==='official'?'/auth/access-request':'/auth/signup/'+kind,{method:'POST',body:f});
      if(result.requires_otp){setSignupChallenge(result);return;}
      if(kind==='citizen'){login(result);navigate('/citizen');}else setDone(true);
    }catch(e){setError(e.message);}finally{setBusy(false);}
  }

  // --- Success State ---
  if(done || (user && !signupChallenge)) {
    return (
      <div className="auth-page-wrapper">
        <AuthHeader />
        <div className="auth-card-container">
          <div className="auth-card narrow">
            <div className="auth-form-side success-container">
              <div className="success-icon"><CheckCircle size={40} /></div>
              <h1 className="auth-title">{t('Welcome to JanVastu!')}</h1>
              <p className="auth-subtitle" style={{marginBottom:0}}>{kind === 'official' ? t('Application submitted. An administrator must review your application before you can sign in.') : t('Your account is ready.')}</p>
              
              {kind !== 'official' && (
                <>
                  <div className="success-actions">
                    <div className="success-action-card">
                      <div className="success-action-icon"><MapPin size={20} /></div>
                      <div>
                        <h3 style={{ margin: 0, fontSize: '1rem', color: '#111827' }}>{t('Report a Need')}</h3>
                        <p style={{ margin: 0, fontSize: '0.875rem', color: '#6B7280' }}>{t('Tell us what your community needs.')}</p>
                      </div>
                    </div>
                    <div className="success-action-card">
                      <div className="success-action-icon"><ShieldCheck size={20} /></div>
                      <div>
                        <h3 style={{ margin: 0, fontSize: '1rem', color: '#111827' }}>{t('Track Your Requests')}</h3>
                        <p style={{ margin: 0, fontSize: '0.875rem', color: '#6B7280' }}>{t('See updates and status.')}</p>
                      </div>
                    </div>
                  </div>
                  <button className="auth-button-primary" onClick={() => navigate('/auth/login')}>{t('Go to Dashboard')} &rarr;</button>
                </>
              )}
              {kind === 'official' && <Link to="/auth/login" className="auth-button-secondary" style={{ display: 'inline-block', marginTop: '2rem' }}>{t('Sign in')}</Link>}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`auth-page-wrapper ${kind === 'official' ? 'official-theme' : ''}`}>
      {kind === 'official' && <div className="official-bg-image"></div>}
      <AuthHeader />

      <div className="auth-card-container">
        <div className={`auth-card ${kind === 'official' ? 'narrow' : ''}`}>
          
          <div className="auth-form-side">
            {!signupChallenge ? (
              <>
                <Link to="/auth/role" className="text-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: '#6B7280', alignSelf: 'flex-start' }}>
                  <ArrowLeft size={16} /> {t('Back to Role Selection')}
                </Link>
                <h1 className="auth-title">
                  {t(kind==='official'?'Official / Planner Access':kind==='volunteer'?'Join JanVastu as a Volunteer':'Create Your JanVastu Account')}
                </h1>
                <p className="auth-subtitle">
                  {t(kind==='official'?'Authorized access for government and planning users.':kind==='volunteer'?'Help communities report and verify infrastructure needs.':'Join as a Citizen to report needs and track requests.')}
                </p>

                <Notice message={error} error/>

                <form onSubmit={submit}>
                  <Field label="Full Name" name="name" required minLength={2} maxLength={120} autoComplete="name" />
                  
                  <div className="grid two">
                    <Field label={kind === 'official' ? "Official Email / User ID" : "Mobile Number"} name={kind==='official'?'email':'mobile'} type={kind==='official'?'email':'tel'} required pattern={kind!=='official'?"[+]?[0-9]{10,15}":undefined} autoComplete={kind==='official'?'email':'tel'}/>
                    <Field label={kind === 'official' ? "Password" : "Email (Optional)"} name={kind==='official'?'password':'email'} type={kind==='official'?'password':'email'} required={kind==='official'}/>
                  </div>

                  {kind === 'volunteer' && (
                    <div className="grid two" hidden={otpMode}>
                      <Field label="Password" name="password" type="password" disabled={otpMode} required={!otpMode} minLength={8} maxLength={72} autoComplete="new-password"/>
                      <Field label="Confirm Password" name="confirm_password" type="password" disabled={otpMode} required={!otpMode} minLength={8} maxLength={72} autoComplete="new-password"/>
                    </div>
                  )}

                  <Field label="Preferred Language" name="preferred_language" defaultValue={language}>
                    <option value="en">English</option>
                    <option value="hi">हिन्दी</option>
                    <option value="or">ଓଡ଼ିଆ</option>
                  </Field>

                  {kind !== 'official' && (
                    <div className="grid two">
                      <Field label="State" name="state" required minLength={2}/>
                      <Field label="District" name="district" required minLength={2}/>
                    </div>
                  )}
                  
                  {kind === 'citizen' && (
                    <div className="grid two">
                      <Field label="Ward / Village / Locality" name="ward_village"/>
                      <Field label="Locality Info" name="locality"/>
                    </div>
                  )}

                  {kind==='volunteer'&& (
                    <>
                      <Field label="Area / Organization" name="area" required/>
                      <Field label="Experience / Role (Optional)" name="experience" placeholder="E.g., community worker, student, NGO member"/>
                    </>
                  )}

                  {kind==='official'&& (
                    <>
                      <div className="grid two">
                        <Field label="Role requested" name="role_requested">{['district_official','state_planner','national_planner','auditor'].map(r=><option key={r} value={r}>{t(r)}</option>)}</Field>
                        <Field label="Organization" name="organization" required minLength={2}/>
                      </div>
                      <Field label="Designation" name="designation" required minLength={2}/>
                      <Field label="Reason for access" name="reason" required minLength={10}/>
                      <Field label="Verification information" name="verification_info" required minLength={3}/>
                    </>
                  )}

                  <label className="check" style={{ fontSize: '0.875rem' }}>
                    <input name="consent" type="checkbox" required/>
                    <span>{t('I agree to JanVastu\'s')} <a href="#" style={{ color: 'var(--color-primary)' }}>{t('Terms of Service')}</a> {t('and')} <a href="#" style={{ color: 'var(--color-primary)' }}>{t('Privacy Policy')}</a>.</span>
                  </label>

                  <button className="auth-button-primary" disabled={busy}>
                    {t(busy ? 'Loading…' : kind === 'official' ? 'Submit Application' : otpMode ? 'Create Account' : 'Create Account')}
                  </button>
                </form>

                {kind === 'volunteer' && (
                  <>
                    <div className="auth-divider">or</div>
                    <button type="button" className="auth-button-secondary" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }} onClick={() => setOtpMode(!otpMode)}>
                      {otpMode ? <Eye size={18} /> : <Smartphone size={18} />}
                      {t(otpMode ? 'Continue with Password' : 'Continue with Mobile OTP')}
                    </button>
                  </>
                )}
                {kind === 'citizen' && (
                  <>
                    <div className="auth-divider">or</div>
                    <Link to="/auth/login" className="auth-button-secondary" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem', textDecoration: 'none' }}>
                      <Smartphone size={18} />
                      {t('Continue with Mobile OTP')}
                    </Link>
                  </>
                )}
              </>
            ) : (
              <>
                <button type="button" className="text-button" style={{marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', alignSelf: 'flex-start'}} onClick={() => setSignupChallenge(null)}>
                  <ArrowLeft size={16} /> Back
                </button>
                <h1 className="auth-title">{t('Verify Your Mobile Number')}</h1>
                <p className="auth-subtitle">{t('We sent a 6-digit code.')} <Notice message="Demo verification: use code 123456. No SMS or email is sent."/></p>

                <Notice message={error} error/>

                <form onSubmit={async e => {
                  e.preventDefault(); setBusy(true); setError('');
                  const f=Object.fromEntries(new FormData(e.currentTarget));
                  let code = '';
                  if (f.code) code = f.code;
                  else {
                    for(let i=0; i<6; i++) code += (f[`digit_${i}`] || '');
                  }
                  
                  try {
                    const result=await api('/auth/signup/otp/verify',{method:'POST',body:{challenge_id:signupChallenge.challenge_id,code}});
                    login(result);
                  } catch(err) {
                    setError(err.message);
                  } finally {
                    setBusy(false);
                  }
                }}>
                  <div className="otp-container">
                    {[...Array(6)].map((_, i) => (
                      <input key={i} name={`digit_${i}`} type="text" maxLength={1} className="otp-input" required
                        onChange={(e) => {
                          if (e.target.value && e.target.nextSibling) e.target.nextSibling.focus();
                        }}
                      />
                    ))}
                  </div>
                  <button className="auth-button-primary" disabled={busy}>{t('Verify')}</button>
                </form>
              </>
            )}
          </div>
          
          {/* Include side panel inside the card! */}
          {!signupChallenge && kind !== 'official' && <AuthSidePanel kind={kind} />}
          
        </div>
      </div>
    </div>
  );
}
