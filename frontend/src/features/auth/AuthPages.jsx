import {useState, useEffect} from 'react';
import {Link, Navigate, useNavigate, useSearchParams} from 'react-router-dom';
import {ShieldCheck, Eye, EyeOff} from 'lucide-react';
import {useAuth} from '../../auth/useAuth';
import {api} from '../../api/client';
import {useI18n} from '../../i18n/useI18n';
import {Field, Notice} from '../../components/UI';
import GoogleLogin from './GoogleLogin';
import {roleHome} from './roles';

export function Login({ admin = false }) {
  const { t } = useI18n(), { user, login } = useAuth(), navigate = useNavigate();
  const [params] = useSearchParams();
  const destination = role => (['citizen','volunteer'].includes(role) && params.get('next')?.startsWith('/citizen/report-need?project=')) ? params.get('next') : roleHome(role);
  const [error,setError]=useState(''), [busy,setBusy]=useState(false), [show,setShow]=useState(false);
  const [mode,setMode]=useState('password'), [challenge,setChallenge]=useState(null), [message,setMessage]=useState('');
  const [options,setOptions]=useState(null);
  useEffect(() => { api('/auth/options').then(setOptions).catch(() => {}); }, []);
  if (user) return <Navigate to={destination(user.role)} replace/>;
  async function submit(event) {
    event.preventDefault(); setBusy(true); setError(''); const f = Object.fromEntries(new FormData(event.currentTarget));
    try {
      let result;
      if (challenge) {
        result = await api(mode==='reset' ? '/auth/password/reset' : '/auth/otp/verify',
          {method:'POST', body:{challenge_id:challenge.challenge_id,code:f.code,...(mode==='reset'?{password:f.password}:{})}});
        if (mode==='reset') { setChallenge(null);setMode('password');setMessage(result.message);return; }
      } else {
        const path = mode==='reset' ? '/auth/password/reset-request' : mode==='otp' ? '/auth/otp/request' : admin ? '/admin/login' : '/auth/login';
        result = await api(path,{method:'POST',body:f});
      }
      if (result.requires_otp) setChallenge(result);
      else { login(result); navigate(destination(result.user.role)); }
    } catch(e) { setError(e.message); } finally { setBusy(false); }
  }
  return <div className="auth-layout"><section className="auth-brand"><h1>{t('JanVastu')}</h1><p>{t('Every voice can improve a community.')}</p><ShieldCheck size={64}/></section>
    <section className="card auth-form"><h1>{t(admin?'Admin secure login':'Sign in')}</h1>
      {admin && <p>{t('Authorized access only. Actions are recorded in the audit log.')}</p>}
      <Notice message={error} error/><Notice message={message}/>
      <form onSubmit={submit}>
        {!challenge && <Field name="identifier" label="Email or mobile" required autoComplete="username"/>}
        {!challenge && mode==='password' && <div><Field name="password" label="Password" required type={show?'text':'password'} autoComplete="current-password" maxLength={72}/>
          <button type="button" className="text-button" onClick={()=>setShow(!show)}>{show?<EyeOff size={16}/>:<Eye size={16}/>} {t(show?'Hide password':'Show password')}</button></div>}
        {challenge && <><Notice message="Demo verification: use code 123456. No SMS or email is sent."/><Field label="Verification code" name="code" required pattern="[0-9]{6}" autoComplete="one-time-code"/>
          {mode==='reset' && <Field name="password" label="New password" type="password" required minLength={8} maxLength={72}/>}</>}
        <button disabled={busy}>{t(busy?'Loading…':challenge?'Verify':mode==='reset'?'Reset password':'Sign in')}</button>
      </form>
      {options?.demo_otp && !challenge && <div className="actions"><button className="secondary" onClick={()=>setMode(mode==='otp'?'password':'otp')}>{t(mode==='otp'?'Use password':'Use demo OTP')}</button><button className="text-button" onClick={()=>setMode('reset')}>{t('Forgot password?')}</button></div>}
      {challenge && <button className="text-button" onClick={()=>setChallenge(null)}>{t('Start again')}</button>}
      {!challenge&&<GoogleLogin clientId={options?.google_client_id} onError={setError} onResult={result=>{if(result.requires_otp)setChallenge(result);else{login(result);navigate(destination(result.user.role));}}}/>}
      <p><Link to="/auth/role">{t('Create an account')}</Link></p>
    </section></div>;
}

export function Signup({kind='citizen'}) {
  const {t,language}=useI18n(), {user,login}=useAuth(), navigate=useNavigate();
  const [error,setError]=useState(''),[busy,setBusy]=useState(false),[done,setDone]=useState(false),[otpMode,setOtpMode]=useState(false),[signupChallenge,setSignupChallenge]=useState(null);
  if(user) return <Navigate to={roleHome(user.role)} replace/>;
  async function submit(event) {
    event.preventDefault();setBusy(true);setError('');
    const f=Object.fromEntries(new FormData(event.currentTarget));
    if(!otpMode&&f.password!==f.confirm_password){setError('Passwords do not match.');setBusy(false);return;}
    delete f.confirm_password;f.consent=!!f.consent;
    if(!f.email)f.email=null;if(!f.mobile)f.mobile=null;
    try {
      const result=await api(otpMode?'/auth/signup/otp/request':kind==='official'?'/auth/access-request':'/auth/signup/'+kind,{method:'POST',body:f});
      if(result.requires_otp){setSignupChallenge(result);return;}
      if(kind==='citizen'){login(result);navigate('/citizen');}else setDone(true);
    }catch(e){setError(e.message);}finally{setBusy(false);}
  }
  if(signupChallenge)return <section className="card narrow"><h1>{t('Verify mobile signup')}</h1><Notice message={error} error/><Notice message="Demo verification: use code 123456. No SMS or email is sent."/><form onSubmit={async e=>{e.preventDefault();setBusy(true);setError('');const code=new FormData(e.currentTarget).get('code');try{const result=await api('/auth/signup/otp/verify',{method:'POST',body:{challenge_id:signupChallenge.challenge_id,code}});login(result);navigate('/citizen');}catch(e){setError(e.message);}finally{setBusy(false);}}}><Field label="Verification code" name="code" required pattern="[0-9]{6}"/><button disabled={busy}>{t('Verify')}</button></form><button className="text-button" onClick={()=>setSignupChallenge(null)}>{t('Start again')}</button></section>;
  if(done)return <section className="card narrow"><h1>{t('Application submitted')}</h1><p>{t('An administrator must review your application before you can sign in.')}</p><Link to="/auth/login">{t('Sign in')}</Link></section>;
  return <section className="card narrow"><h1>{t(kind==='official'?'Request official or auditor access':kind==='volunteer'?'Volunteer registration':'Citizen registration')}</h1>
    {kind==='citizen'&&<button className="secondary" onClick={()=>setOtpMode(!otpMode)}>{t(otpMode?'Use password':'Register with demo mobile OTP')}</button>}
    <Notice message={error} error/><form onSubmit={submit}>
      <Field label="Full name" name="name" required minLength={2} maxLength={120} autoComplete="name"/>
      <div className="grid two"><Field label="Mobile number" name="mobile" required={kind!=='official'} pattern="[+]?[0-9]{10,15}" autoComplete="tel"/><Field label="Email" name="email" type="email" required={kind==='official'} autoComplete="email"/></div>
      <div className="grid two" hidden={otpMode}><Field label="Password" name="password" type="password" disabled={otpMode} required={!otpMode} minLength={8} maxLength={72} autoComplete="new-password"/><Field label="Confirm password" name="confirm_password" type="password" disabled={otpMode} required={!otpMode} minLength={8} maxLength={72} autoComplete="new-password"/></div>
      <Field label="Preferred language" name="preferred_language" defaultValue={language}><option value="en">English</option><option value="hi">हिन्दी</option><option value="or">ଓଡ଼ିଆ</option></Field>
      <div className="grid two"><Field label="State" name="state" required minLength={2}/><Field label="District" name="district" required minLength={2}/></div>
      <Field label="Locality" name="locality"/><Field label="Ward or village" name="ward_village"/>
      {kind==='volunteer'&&<><Field label="Organization or area" name="area" required/><Field label="Relevant experience" name="experience"/></>}
      {kind==='official'&&<><Field label="Role requested" name="role_requested">{['district_official','state_planner','national_planner','auditor'].map(r=><option key={r} value={r}>{t(r)}</option>)}</Field><Field label="Organization" name="organization" required minLength={2}/><Field label="Designation" name="designation" required minLength={2}/><Field label="Reason for access" name="reason" required minLength={10}/><Field label="Verification information" name="verification_info" required minLength={3}/></>}
      <label className="check"><input name="consent" type="checkbox" required/>{t('I consent to account and reporting data being used for civic planning. I can withdraw consent in my profile.')}</label>
      <button disabled={busy}>{t(busy?'Loading…':kind==='citizen'?'Create account':'Submit application')}</button>
    </form></section>;
}
