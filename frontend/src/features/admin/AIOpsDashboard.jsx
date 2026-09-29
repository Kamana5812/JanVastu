import {useI18n} from '../../i18n/useI18n';
import {State, Notice} from '../../components/UI';
import {useResource} from '../../components/useResource';
import {DataTable} from './AdminDashboard';
export default function AIOpsDashboard(){
 const {t}=useI18n(),r=useResource('/ai-ops/pipelines');
 return <section><h1>{t('AI and data operations')}</h1><button className="secondary" onClick={r.reload}>{t('Refresh')}</button><State resource={r}>{d=><><Notice message={d.scope}/><div className="grid two"><article className="card"><h2>{t('Pipeline runs')}</h2><strong className="metric">{d.total_runs}</strong></article><article className="card"><h2>{t('Requires Review')}</h2><strong className="metric">{d.review_required}</strong></article></div><h2>{t('Measured pipeline activity')}</h2><DataTable rows={d.pipelines}/><div className="grid two"><section><h2>{t('Languages')}</h2><DataTable rows={d.languages}/></section><section><h2>{t('Categories')}</h2><DataTable rows={d.categories}/></section></div><h2>{t('Integration Planned')}</h2><ul>{d.planned.map(p=><li key={p}>{t(p)}</li>)}</ul></>}</State></section>;
}
