import { Link } from 'react-router-dom';
import { User, Users, Building2, ShieldCheck } from 'lucide-react';
import { useI18n } from '../../i18n';
export default function RoleSelection(){
 const {t}=useI18n();
 return <section><header className="page-heading"><h1>{t('Join JanVastu')}</h1><p>{t('Choose how you want to participate.')}</p></header><div className="grid four">
 {[['Citizen',User,'Report needs and track their progress.','/auth/signup/citizen'],['Volunteer',Users,'Collect and verify community requests.','/auth/signup/volunteer'],['Government / Planner',Building2,'Use evidence to plan infrastructure.','/auth/access-request'],['Auditor',ShieldCheck,'Review accountability and governance.','/auth/login']].map(([label,Icon,desc,path])=><article className="card" key={label}><Icon size={36}/><h2>{t(label)}</h2><p>{t(desc)}</p><Link className="button" to={path}>{t('Continue')}</Link></article>)}</div><p><Link to="/auth/login">{t('Already registered? Sign in')}</Link></p></section>;
}
