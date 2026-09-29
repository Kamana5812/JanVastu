import {useI18n} from '../i18n/useI18n';
export function ErrorState({title='Error',message='Something went wrong.',onRetry}){const {t}=useI18n();return <div role="alert" className="notice error"><h3>{t(title)}</h3><p>{t(message)}</p>{onRetry&&<button onClick={onRetry}>{t('Retry')}</button>}</div>;}
