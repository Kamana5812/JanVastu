import {Link} from 'react-router-dom';
import {useI18n} from '../../i18n/useI18n';
import {Badge, Notice} from '../../components/UI';

export default function DatasetRecord({record}){
 const {t}=useI18n();
 if(!record)return null;
 return <section aria-label={t('Dataset sources')}>
 <Notice message="Supplied dataset: screenshot claims are unverified. Official references apply only to the fields and dates shown."/>
 <h2>{t('Dataset sources')}</h2>
 {record.conflicts.length>0&&<Notice message="Sources differ. Check their dates and project scope before using these figures."/>}
 {record.shared_budget_group&&<Notice message="Related corridor components may share a budget. Do not add their costs together."/>}
 <div className="grid two">{record.claims.map((claim,i)=><article className="card" key={i}>
 <Badge>{claim.source_badge}</Badge>
 {claim.as_of&&<p>{t('Source date')}: {claim.as_of}</p>}
 <dl>{Object.entries(claim.values).map(([key,value])=><div key={key}><dt><strong>{t(key)}</strong>{record.conflicts.includes(key)&&<> · {t('Requires Review')}</>}</dt><dd>{value}</dd></div>)}</dl>
 <ul>{claim.sources.map(sid=>{const source=record.sources[sid];return <li key={sid}>{source.url?<a href={source.url} target="_blank" rel="noreferrer">{source.title}</a>:<>{t('Supplied screenshot')} {sid.replace('image-','')}</>}</li>;})}</ul>
 </article>)}</div>
 {record.related_ids.length>0&&<p>{t('Related records')}: {record.related_ids.map(id=><Link key={id} to={'/accountability/'+id}>{t('View project')} ({id})</Link>)}</p>}
 </section>;
}
