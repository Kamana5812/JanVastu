import {useId} from 'react';
import {useI18n} from '../i18n/useI18n';
export function State({ resource, children }) {
  const { t } = useI18n();
  if (resource.loading) return <p role="status">{t('Loading…')}</p>;
  if (resource.error) return <div role="alert" className="notice error"><p>{t(resource.error)}</p><button onClick={resource.reload}>{t('Retry')}</button></div>;
  return children(resource.data);
}
export function Field({ label, error, children, ...props }) {
  const id = useId(), { t } = useI18n();
  return <div className="field"><label htmlFor={id}>{t(label)}{props.required && ' *'}</label>
    {children ? <select id={id} {...props}>{children}</select> : <input id={id} aria-invalid={!!error} aria-describedby={error ? id+'-error' : undefined} {...props}/>}
    {error && <span role="alert" id={id+'-error'}>{t(error)}</span>}</div>;
}
export function Notice({ message, error = false }) {
  const { t } = useI18n(); return message ? <p role={error ? 'alert' : 'status'} className={'notice '+(error ? 'error' : '')}>{t(message)}</p> : null;
}
export function Badge({ children }) { const { t } = useI18n(); return <span className="pill">{t(children)}</span>; }
export function Empty() { const { t } = useI18n(); return <p className="empty">{t('No records found.')}</p>; }
export function DateText({ value }) { const { language, t } = useI18n(); return value ? new Date(value).toLocaleString(language === 'or' ? 'or-IN' : language+'-IN') : t('Information Not Available'); }
