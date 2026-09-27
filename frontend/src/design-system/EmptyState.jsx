import {useI18n} from '../i18n';
export function EmptyState({title='No records found.',message,description,action,actionLabel,onAction,icon}){
 const {t}=useI18n();return <div className="empty">{icon}<h3>{t(title)}</h3><p>{t(message||description||'')}</p>{action}{actionLabel&&<button onClick={onAction}>{t(actionLabel)}</button>}</div>;
}
