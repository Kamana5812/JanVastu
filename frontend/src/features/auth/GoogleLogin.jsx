import {useEffect, useRef} from 'react';
import {api} from '../../api/client';
import {useI18n} from '../../i18n/useI18n';
let scriptPromise;
function load(){
 if(window.google?.accounts)return Promise.resolve();
 if(!scriptPromise)scriptPromise=new Promise((resolve,reject)=>{const script=document.createElement('script');script.src='https://accounts.google.com/gsi/client';script.async=true;script.onload=resolve;script.onerror=()=>{scriptPromise=null;reject(Error('google_unavailable'));};document.head.appendChild(script);});
 return scriptPromise;
}
export default function GoogleLogin({clientId,onResult,onError}){
 const target=useRef(),{t}=useI18n(),callbacks=useRef({onResult,onError});useEffect(()=>{callbacks.current={onResult,onError};});
 useEffect(()=>{if(!clientId)return;let active=true;Promise.all([load(),api('/auth/google/challenge',{method:'POST'})]).then(([,challenge])=>{if(!active)return;window.google.accounts.id.initialize({client_id:clientId,nonce:challenge.nonce,callback:async response=>{try{const result=await api('/auth/google',{method:'POST',body:{credential:response.credential,nonce:challenge.nonce}});callbacks.current.onResult(result);}catch(e){callbacks.current.onError(e.message);}}});window.google.accounts.id.renderButton(target.current,{theme:'outline',size:'large'});}).catch(e=>callbacks.current.onError(e.message));return()=>{active=false;};},[clientId]);
 return clientId?<div ref={target}/>:<p className="muted">{t('Google sign-in is not configured. Use password or demo OTP.')}</p>;
}
