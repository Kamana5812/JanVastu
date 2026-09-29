import {useState} from 'react';
import {useParams, Link} from 'react-router-dom';
import {api} from '../../api/client';
import {useI18n} from '../../i18n/useI18n';
import {State, Field, Notice, Empty} from '../../components/UI';
import {useResource} from '../../components/useResource';
import {EvidenceMedia} from '../citizen/CitizenDashboard';
export default function ReviewEvidence(){
 const {id}=useParams(),{t}=useI18n(),r=useResource('/admin/requests/'+id),[error,setError]=useState(''),[message,setMessage]=useState(''),[busy,setBusy]=useState(false);
 async function publish(e,evidenceId){e.preventDefault();const body=new FormData(e.currentTarget);setBusy(true);setError('');try{await api('/admin/evidence/'+evidenceId+'/publish',{method:'POST',body});setMessage('Reviewed evidence published.');r.reload();}catch(e){setError(e.message);}finally{setBusy(false);}}
 return <section className="narrow"><Link to="/admin">{t('Administration')}</Link><h1>{t('Review evidence')}</h1><Notice message={error} error/><Notice message={message}/><Notice message="Upload a redacted image with faces, names, contact details and identifying locations removed. Publication requires active reporting consent."/><State resource={r}>{n=><><p>{n.description}</p>{n.evidence.length?n.evidence.map(item=><article className="card" key={item.id}><EvidenceMedia item={item}/><form onSubmit={e=>publish(e,item.id)}><Field type="file" name="file" label="Redacted image" required accept="image/jpeg,image/png,image/webp"/><label className="check"><input type="checkbox" name="reviewed" value="true" required/>{t('I reviewed this derivative and removed identifying information.')}</label><button disabled={busy||!n.project_id}>{t('Publish reviewed evidence')}</button></form>{!n.project_id&&<p>{t('Public evidence requires a linked project.')}</p>}</article>):<Empty/>}</>}</State></section>;
}
