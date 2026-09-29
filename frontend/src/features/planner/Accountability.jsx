import {useState} from 'react';
import {Link, useParams, useSearchParams} from 'react-router-dom';
import {useI18n} from '../../i18n/useI18n';
import {State, Empty, Badge, Field, DateText, Notice} from '../../components/UI';
import {useResource} from '../../components/useResource';
import {downloadUrl} from '../../api/client';
import CivicMap from '../../components/CivicMap';
import DatasetRecord from './DatasetRecord';
export default function Accountability(){
 const [params]=useSearchParams(),{t}=useI18n(),{id}=useParams(),[q,setQ]=useState(params.get('district')||''),[query,setQuery]=useState(params.get('district')||''),[geo,setGeo]=useState(null),[error,setError]=useState('');
 const resource=useResource(id?'/projects/'+id:'/projects/search?'+new URLSearchParams({q:query,...geo}));
 async function nearby(){try{const p=await new Promise((ok,no)=>navigator.geolocation.getCurrentPosition(ok,no,{timeout:15000}));setGeo({lat:p.coords.latitude,lng:p.coords.longitude});setError('');}catch{setError('Location access failed. Search by district instead.');}}
 return <section><h1>{t('Public accountability')}</h1><p>{t('Explore project records, sources and timelines.')}</p><Notice message={error} error/>
 {!id&&<><form className="filter-bar" onSubmit={e=>{e.preventDefault();setQuery(q);}}><Field label="Search projects or districts" value={q} onChange={e=>setQ(e.target.value)}/><button>{t('Search')}</button><button type="button" className="secondary" onClick={nearby}>{t('Nearby projects')}</button>{geo&&<button type="button" onClick={()=>setGeo(null)}>{t('Clear location filter')}</button>}</form></>}
 <State resource={resource}>{data=>id?<><Link to="/accountability">{t('All projects')}</Link><h2>{data.name}</h2>{data.is_sample&&<Notice message="Synthetic sample project. Names, organizations and figures are fictional."/>}
 <DatasetRecord record={data.dataset_record}/><div className="grid three">{Object.entries(data.fields).map(([key,field])=><article key={key} className="card"><h3>{t(key)}</h3><p>{field.value===null?t('Information Not Available'):key.includes('start')||key.includes('completion')?<DateText value={field.value}/>:typeof field.value==='number'?field.value.toLocaleString():t(field.value)}</p><Badge>{field.source_badge}</Badge></article>)}</div>
 <section className="card"><h2>{t('Project timeline')}</h2>{data.timeline.length?<ol>{data.timeline.map((e,i)=><li key={i}>{t(e.stage)} · <DateText value={e.occurred_at}/> <Badge>{e.source_badge}</Badge></li>)}</ol>:<Empty/>}</section>
 <h2>{t('Citizen evidence')}</h2>{data.evidence.length?data.evidence.map(e=><figure key={e.id}><img className="evidence" src={downloadUrl('/projects/evidence/'+e.id+'/media')} alt={t('Reviewed citizen evidence')}/><figcaption><Badge>{e.source_badge}</Badge></figcaption></figure>):<p>{t('No reviewed public evidence is available. Submitted media stays private.')}</p>}
 <Link className="button" to={'/citizen/report-need?project='+data.id}>{t('Report an issue')}</Link></>:data.length?<>{data.some(p=>p.has_dataset)&&<Notice message="Records without confirmed coordinates are listed below and excluded from the map and nearby search."/>}<CivicMap points={data}/><div className="grid three">{data.map(p=><article className="card" key={p.id}>{p.is_sample&&<Badge>Synthetic Sample</Badge>}{p.has_dataset&&<Badge>User supplied — unverified</Badge>}<h2>{p.name}</h2><p>{p.district||t(p.has_dataset?'Bhubaneswar region (supplied dataset)':'Information Not Available')} · {t(p.category)}</p><Badge>{p.status}</Badge><p>{t('Progress')}: {p.progress===null?t('Information Not Available'):p.progress+'%'}</p><Link to={'/accountability/'+p.id}>{t('View project')}</Link></article>)}</div></>:<Empty/>}</State></section>;
}
