import {useState} from 'react';
import {useI18n} from '../../i18n/useI18n';
import {useAuth} from '../../auth/useAuth';
import {api} from '../../api/client';
import {State, Field, Notice, Empty, Badge} from '../../components/UI';
import {useResource} from '../../components/useResource';
import CivicMap from '../../components/CivicMap';
import {categories} from '../citizen/categories';
const label='JanVastu Analytical Indicator — not an official government metric.';
export default function PlannerDashboard({level}){
 const {t}=useI18n(),{user}=useAuth();
 const [filters,setFilters]=useState({state:level==='national'?'':user.state||'',district:level==='district'?user.district||'':'',locality:'',ward_village:'',category:'',days:'90',project_status:''});
 const [layer,setLayer]=useState('Citizen demand'),[error,setError]=useState(''),[busy,setBusy]=useState('');
 const query=new URLSearchParams(Object.entries(filters).filter(([,value])=>value)).toString();
 const resource=useResource('/planner/dashboard?'+query),needs=useResource('/planner/needs?'+query);
 function change(key,value){setFilters(f=>({...f,[key]:value,...(key==='state'?{district:'',locality:'',ward_village:''}:key==='district'?{locality:'',ward_village:''}:key==='locality'?{ward_village:''}:{})}));}
 async function update(id,status){setBusy(id);setError('');try{await api('/planner/needs/'+id+'/status',{method:'PATCH',body:{status}});resource.reload();needs.reload();}catch(e){setError(e.message);}finally{setBusy('');}}
 const hierarchy=resource.data?.hierarchy||[];
 const choices=key=>[...new Set(hierarchy.filter(h=>(key==='state'||!filters.state||h.state===filters.state)&&(key==='state'||key==='district'||!filters.district||h.district===filters.district)&&(key!=='ward_village'||!filters.locality||h.locality===filters.locality)).map(h=>h[key]).filter(Boolean))];
 return <section><h1>{t(level==='district'?'District infrastructure pulse':level==='state'?'State infrastructure pulse':'National infrastructure pulse')}</h1>
 <p className="notice">{t(label)}</p><p>{t('Infrastructure and investment values are normalized sample indices, not rupee amounts.')}</p><Notice message={error} error/>
 <div className="filter-bar">{['state','district','locality','ward_village'].map(key=><Field key={key} label={key} value={filters[key]} disabled={(key==='state'&&level!=='national')||(key==='district'&&level==='district')} onChange={e=>change(key,e.target.value)}><option value="">{t('All')}</option>{[...new Set([...choices(key),filters[key]].filter(Boolean))].map(v=><option key={v}>{v}</option>)}</Field>)}
 <Field label="Category" value={filters.category} onChange={e=>change('category',e.target.value)}><option value="">{t('All')}</option>{categories.map(c=><option key={c} value={c}>{t(c)}</option>)}</Field>
 <Field label="Time period" value={filters.days} onChange={e=>change('days',e.target.value)}>{['7','30','90'].map(d=><option key={d} value={d}>{d} {t('days')}</option>)}</Field>
 <Field label="Project status" value={filters.project_status} onChange={e=>change('project_status',e.target.value)}><option value="">{t('All')}</option>{['planned','in_progress','completed'].map(s=><option key={s} value={s}>{t(s)}</option>)}</Field></div>
 <State resource={resource}>{data=>{
  let points=data.hotspots.map(h=>({...h,value:layer==='Infrastructure'?h.infrastructure_stock:layer==='Investment'?h.planned_investment:layer==='Vulnerability'?h.vulnerability:layer==='Infrastructure gap'?h.gap_ratio:h.requests,color:layer==='Infrastructure gap'?'#C65353':'#176B73'}));
  if(layer==='Projects')points=data.projects;
  return <>{data.sample_requests>0&&<Notice message="Synthetic demonstration requests are included in these figures."/>}<div className="grid three">{[['Citizen demands','total'],['Verified demands','verified'],['High-gap areas','high_gap'],['Active projects','active_projects'],['Resolved requests','resolved'],['Pending review','pending_review']].map(([name,key])=><article className="card" key={key}><h2>{t(name)}</h2><strong className="metric">{data.kpis[key]}</strong></article>)}</div>
  <h2>{t('Demand and infrastructure map')}</h2><div className="tabs" aria-label={t('Map layers')}>{['Citizen demand','Infrastructure','Infrastructure gap','Projects','Vulnerability','Investment'].map(name=><button key={name} className={layer===name?'':'secondary'} aria-pressed={layer===name} onClick={()=>setLayer(name)}>{t(name)}</button>)}</div><CivicMap points={points}/>
  <h2>{t('Gap analysis and recommendations')}</h2>{data.hotspots.length?data.hotspots.map((h,i)=><article className="card" key={i}><h3>{h.ward_village||h.locality||h.district} · {t(h.category)}</h3>{h.is_sample_context&&<Badge>Synthetic sample</Badge>}
  <div className="grid four">{[['Demand intensity',h.demand_intensity],['Infrastructure stock',h.infrastructure_stock],['Planned investment',h.planned_investment],['JanVastu gap indicator',h.unbounded?t('No supply context'):h.gap_ratio]].map(([name,value])=><p key={name}>{t(name)}<br/><strong>{value??t('Information Not Available')}</strong></p>)}</div>
  <p className="muted">{t(label)}</p><details><summary>{t('Why was this area surfaced?')}</summary><p>{t('Requests')}: {h.requests}; {t('Independent contributors')}: {h.independent_signals}</p><p>{t('Reports in the last seven days')}: {h.recent_reports}; {t('Previous seven days')}: {h.previous_reports}</p><p>{t('Vulnerability multiplier')}: {h.vulnerability??t('Information Not Available')}</p><p>{t('Formula: recency-weighted demand × vulnerability / (infrastructure stock + planned investment).')}</p>{h.supply_missing&&<p>{t('Supply data is unavailable; no gap ratio is inferred.')}</p>}<p>{t('Review the evidence before deciding whether to commission a project.')}</p></details></article>):<Empty/>}</>;
 }}</State>
 <h2>{t('Actionable requests')}</h2><State resource={needs}>{rows=>rows.length?<div className="table-wrap"><table><thead><tr>{['Category','District','Status','Action'].map(h=><th key={h}>{t(h)}</th>)}</tr></thead><tbody>{rows.map(n=><tr key={n.id}><td>{t(n.category)}<details><summary>{t('Description')}</summary>{n.is_sample&&<Badge>Synthetic Sample</Badge>}{n.description}</details></td><td>{n.district}</td><td>{t(n.status)}</td><td>{['verified','planned'].includes(n.status)&&<button disabled={busy===n.id} onClick={()=>update(n.id,n.status==='verified'?'planned':'resolved')}>{t(n.status==='verified'?'Mark planned':'Mark resolved')}</button>}</td></tr>)}</tbody></table></div>:<Empty/>}</State></section>;
}
