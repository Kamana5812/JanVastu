import {useI18n} from '../i18n';
export function Button({children,variant='primary',isLoading=false,disabled=false,as:Tag='button',style={},className='',...props}){
 const {t}=useI18n();
 return <Tag className={[(variant==='outline'||variant==='secondary')?'secondary':variant==='ghost'?'text-button':'',className].join(' ')} style={style} disabled={Tag==='button'?(disabled||isLoading):undefined} aria-busy={isLoading} {...props}>{isLoading?t('Loading…'):children}</Tag>;
}
