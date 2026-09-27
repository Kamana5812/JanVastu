import {useState} from 'react';
import {useNavigate,useParams,Link} from 'react-router-dom';
import {useI18n} from '../../i18n';
import {api} from '../../api/client';
import {useResource,State,Notice,Field,Badge} from '../../components/UI';
import {EvidenceMedia} from '../citizen/CitizenDashboard';
export default function VerifyNeed(){
 const {id}=useParams(),{t}=useI18n(),navigate=useNavigate(),resource=useResource('/volunteer/tasks/'+id);
 const [error,setError]=useState(''),[busy,setBusy]=useState(false);
 async function submit(event){event.preventDefault();setBusy(true);setError('');try{await api('/volunteer/tasks/'+id+'/verify',{method:'PATCH',body:Object.fromEntries(new FormData(event.currentTarget))});navigate('/volunteer');}catch(e){setError(e.message);}finally{setBusy(false);}}
 return <section className="narrow"><Link to="/volunteer">{t('Back to dashboard')}</Link><Notice message={error} error/><State resource={resource}>{n=><article className="card"><h1>{t('Verify infrastructure need')}</h1><Badge>{n.status}</Badge><h2>{t(n.category)}</h2><p>{n.description}</p><p>{n.address||n.district}</p><p>{t('People affected')}: {n.affected_people||t('Information Not Available')}</p>{n.evidence.map(e=><EvidenceMedia key={e.id} item={e}/>)}
 <form onSubmit={submit}><Field label="Decision" name="status"><option value="verified">{t('Verified')}</option><option value="rejected">{t('Unable to verify')}</option></Field><label className="field">{t('Private review notes')}<textarea name="comments" required minLength={5} maxLength={1000}/></label><button disabled={busy||n.status!=='reported'}>{t(busy?'Loading…':'Submit verification')}</button></form></article>}</State></section>;
}
