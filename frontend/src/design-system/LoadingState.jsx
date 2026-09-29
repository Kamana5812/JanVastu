import {useI18n} from '../i18n/useI18n';
export function LoadingState({message='Loading…'}){const {t}=useI18n();return <p role="status">{t(message)}</p>;}
