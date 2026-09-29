import {useEffect, useRef} from 'react';
import {useI18n} from '../i18n/useI18n';
export function Modal({isOpen,onClose,title,children}){
 const ref=useRef(),{t}=useI18n();
 useEffect(()=>{if(isOpen)ref.current.showModal();else ref.current.close();},[isOpen]);
 return <dialog ref={ref} aria-label={t(title)} onCancel={onClose} onClose={onClose}><h2>{t(title)}</h2>{children}<button onClick={onClose}>{t('Close')}</button></dialog>;
}
