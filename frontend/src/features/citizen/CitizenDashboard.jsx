import {useState} from 'react';
import {Link,useParams} from 'react-router-dom';
import {useI18n} from '../../i18n';
import {useAuth} from '../../auth/AuthContext';
import {useResource,State,Field,Empty,Badge,DateText} from '../../components/UI';
import {api} from '../../api/client';
import {useEffect} from 'react';
export default function CitizenDashboard(){
 const {t}=useI18n(),{user}=useAuth(),[status,setStatus]=useState(''),[sort,setSort]=useState('newest');
 const resource=useResource('/citizen/needs?'+new URLSearchParams({...(status?{status}:{}),sort}));
 const base=user.role==='volunteer'?'/volunteer':'/citizen';
 return <section><header className="page-heading"><h1>{t('How can we improve your area?')}</h1><div className="actions"><Link className="button" to={base+'/capture'}>{t('Report a need')}</Link><Link to={'/accountability?'+new URLSearchParams({state:user.state||'',district:user.district||''})}>{t('Nearby projects')}</Link><Link to="/profile">{t('Notifications and profile')}</Link></div></header>
 <h2>{t('My requests')}</h2><div className="filter-bar"><Field label="Status" value={status} onChange={e=>setStatus(e.target.value)}><option value="">{t('All')}</option>{['reported','verified','planned','resolved','rejected'].map(s=><option key={s}>{s}</option>)}</Field><Field label="Sort" value={sort} onChange={e=>setSort(e.target.value)}><option value="newest">{t('Newest first')}</option><option value="oldest">{t('Oldest first')}</option></Field></div>
 <State resource={resource}>{rows=>rows.length?<div className="grid two">{rows.map(n=><article className="card" key={n.id}><Badge>{n.status}</Badge><h3>{t(n.category)}</h3><p>{n.description}</p><p>{n.district} · <DateText value={n.created_at}/></p><Link to={base+'/requests/'+n.id}>{t('Track request')}</Link></article>)}</div>:<Empty/>}</State></section>;
}
export function EvidenceMedia({item}){
 const [url,setUrl]=useState(''),[failed,setFailed]=useState(false),{t}=useI18n();
 useEffect(()=>{let object,active=true;api('/citizen/media/'+item.id).then(blob=>{object=URL.createObjectURL(blob);if(active)setUrl(object);else URL.revokeObjectURL(object);}).catch(()=>setFailed(true));return()=>{active=false;if(object)URL.revokeObjectURL(object);};},[item.id]);
 if(failed)return <p>{t('media_unavailable')}</p>;
 if(!url)return <p role="status">{t('Loading…')}</p>;
 return item.content_type?.startsWith('image')?<img className="evidence" src={url} alt={t('Submitted evidence')}/>:item.content_type?.startsWith('video')?<video className="evidence" src={url} controls/>:<audio src={url} controls/>;
}
export function RequestDetail(){
 const {id}=useParams(),{t}=useI18n(),resource=useResource('/citizen/needs/'+id);
 return <State resource={resource}>{n=><section className="card narrow"><h1>{t('Request tracking')}</h1><p>{t('Tracking ID')}: {n.id}</p><Badge>{n.status}</Badge><h2>{t(n.category)}</h2><p>{n.description}</p><p>{n.address||n.district}</p><h2>{t('Timeline')}</h2><ol>{n.events.map((e,i)=><li key={i}>{t(e.status)} · <DateText value={e.created_at}/></li>)}</ol><h2>{t('Evidence')}</h2>{n.evidence.length?n.evidence.map(e=><EvidenceMedia key={e.id} item={e}/>):<Empty/>}</section>}</State>;
}
