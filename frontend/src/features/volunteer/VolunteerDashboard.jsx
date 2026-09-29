import {useEffect, useState, useCallback, useRef} from 'react';
import {Link} from 'react-router-dom';
import {useI18n} from '../../i18n/useI18n';
import {useAuth} from '../../auth/useAuth';
import {api} from '../../api/client';
import {State, Notice, Empty, Badge} from '../../components/UI';
import {useResource} from '../../components/useResource';
import {queued, removeQueued, saveQueued} from './queue';
export default function VolunteerDashboard(){
 const {t}=useI18n(),{user}=useAuth(),[queue,setQueue]=useState([]),[error,setError]=useState(''),[busy,setBusy]=useState(false),[online,setOnline]=useState(navigator.onLine);
 const stats=useResource('/volunteer/stats'),tasks=useResource('/volunteer/tasks');
 const syncing=useRef(false),syncAction=useRef(null);
 const loadQueue=useCallback(()=>queued(user.id).then(setQueue).catch(e=>setError(e.message)),[user.id]);
 useEffect(()=>{loadQueue();const update=()=>setOnline(navigator.onLine);window.addEventListener('online',update);window.addEventListener('offline',update);return()=>{window.removeEventListener('online',update);window.removeEventListener('offline',update);};},[loadQueue]);
 async function sync(){
  if(syncing.current)return;
  syncing.current=true;
  setBusy(true);setError('');
  try{
   const records=await queued(user.id);
   for(const record of records){
    const result=record.need_id?{items:[{id:record.need_id}]}:await api('/volunteer/sync',{method:'POST',body:{items:[record.payload]}});
    record.need_id=result.items[0].id;await saveQueued(user.id,record);
    while(record.files.length){const form=new FormData();form.append('file',record.files[0]);await api('/citizen/needs/'+record.need_id+'/media',{method:'POST',body:form});record.files.shift();await saveQueued(user.id,record);}
    await removeQueued(record.key);
   }
   tasks.reload();stats.reload();
  }catch(e){setError(e.message);}finally{syncing.current=false;setBusy(false);loadQueue();}
 }
 useEffect(()=>{syncAction.current=sync;});
 useEffect(()=>{const run=()=>syncAction.current();window.addEventListener('online',run);return()=>window.removeEventListener('online',run);},[]);
 return <section><header className="page-heading"><h1>{t('Volunteer dashboard')}</h1><div className="actions"><Link className="button" to="/volunteer/capture">{t('Capture citizen request')}</Link><Link to="/volunteer/requests">{t('My requests')}</Link><Link to="/profile">{t('Notifications and profile')}</Link></div></header>
 {!online&&<Notice message="Offline — requests will sync when connectivity returns."/>}<Notice message={error} error/>
 <State resource={stats}>{s=><div className="grid four">{[['Requests captured',s.captured],['Pending verification',s.pending_verification],['Verified today',s.verified_today],['Sync pending',queue.length]].map(([label,value])=><article className="card" key={label}><h2>{t(label)}</h2><strong className="metric">{value}</strong></article>)}</div>}</State>
 <section className="card"><h2>{t('Offline queue')}</h2><p>{t('Offline drafts stay in this browser until synced or removed. Do not use a shared device for sensitive evidence.')}</p>{queue.length?<ul>{queue.map(item=><li key={item.key}>{t(item.payload.category)} — {item.payload.description.slice(0,80)} <button className="text-button" disabled={busy} onClick={async()=>{await removeQueued(item.key);loadQueue();}}>{t('Remove')}</button></li>)}</ul>:<Empty/>}<button onClick={sync} disabled={!online||busy||!queue.length}>{t(busy?'Loading…':'Sync now')}</button></section>
 <h2>{t('Pending verification')}</h2><State resource={tasks}>{rows=>rows.length?<div className="grid two">{rows.map(n=><article key={n.id} className="card"><Badge>{n.status}</Badge><h3>{t(n.category)}</h3><p>{n.description}</p><p>{n.address||n.district}</p><Link className="button secondary" to={'/volunteer/verify/'+n.id}>{t('Review and verify')}</Link></article>)}</div>:<Empty/>}</State></section>;
}
