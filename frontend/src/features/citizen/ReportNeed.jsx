import { useEffect, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Mic, Square, MapPin, Send } from 'lucide-react';
import { api } from '../../api/client';
import { useAuth } from '../../auth/AuthContext';
import { useI18n } from '../../i18n';
import { Field, Notice } from '../../components/UI';
import { saveQueued } from '../volunteer/queue';
export const categories=['water','sanitation','electricity','health','school','transport','road','housing','other'];
export default function ReportNeed(){
 const {user}=useAuth(),{t,language}=useI18n(),navigate=useNavigate(),[params]=useSearchParams();
 const [location,setLocation]=useState({latitude:'',longitude:'',address:'',state:user.state||'',district:user.district||''});
 const [description,setDescription]=useState(''),[category,setCategory]=useState('other'),[analysis,setAnalysis]=useState(null);
 const [files,setFiles]=useState([]),[busy,setBusy]=useState(false),[error,setError]=useState(''),[message,setMessage]=useState(''),[created,setCreated]=useState(null),[recording,setRecording]=useState(false);
 const recorder=useRef(),stream=useRef(),timer=useRef();
 const clientId=useRef(crypto.randomUUID());
 useEffect(()=>()=>{clearTimeout(timer.current);stream.current?.getTracks().forEach(track=>track.stop());},[]);
 async function locate(){
  setBusy(true);setError('');
  try {
   if(!navigator.geolocation)throw Error('location_unavailable');
   const position=await new Promise((resolve,reject)=>navigator.geolocation.getCurrentPosition(resolve,reject,{enableHighAccuracy:true,timeout:15000}));
   const {latitude,longitude}=position.coords;
   setLocation(p=>({...p,latitude,longitude}));
   const geo=await api('/citizen/geocode?'+new URLSearchParams({latitude,longitude}));
   setLocation(p=>({...p,address:geo.address||p.address,state:geo.state||p.state,district:geo.district||p.district}));
   if(geo.source==='user_provided')setMessage('Address lookup is unavailable. Confirm the location below.');
  }catch{setError('Location access failed. Enter coordinates manually.');}finally{setBusy(false);}
 }
 async function record(){
  if(recording){recorder.current.stop();return;}
  try{
   stream.current=await navigator.mediaDevices.getUserMedia({audio:true});
   const mime=MediaRecorder.isTypeSupported('audio/webm')?'audio/webm':'audio/ogg';
   recorder.current=new MediaRecorder(stream.current,{mimeType:mime});
   const chunks=[];recorder.current.ondataavailable=e=>chunks.push(e.data);
   recorder.current.onstop=()=>{setFiles(f=>[...f,new File(chunks,'voice.webm',{type:mime})]);setRecording(false);stream.current.getTracks().forEach(track=>track.stop());clearTimeout(timer.current);};
   recorder.current.start();setRecording(true);timer.current=setTimeout(()=>recorder.current?.state==='recording'&&recorder.current.stop(),60000);
  }catch{setError('Microphone access failed. You can type your report.');}
 }
 async function understand(){
  setBusy(true);setError('');
  try{const result=await api('/citizen/analyze',{method:'POST',body:{description}});setAnalysis(result);setCategory(result.category);}
  catch(e){setError(e.message);}finally{setBusy(false);}
 }
 async function submit(event){
  event.preventDefault();setError('');setBusy(true);
  const form=Object.fromEntries(new FormData(event.currentTarget));
  const payload={...location,latitude:Number(location.latitude),longitude:Number(location.longitude),description,category,
   affected_people:form.affected_people?Number(form.affected_people):null,locality:form.locality,ward_village:form.ward_village,
   client_id:clientId.current,consent:!!form.consent,citizen_consent:!!form.citizen_consent,language,project_id:params.get('project')||null};
  try{
   if(files.length>5)throw Error('media_count_limit');
   if(!navigator.onLine && user.role==='volunteer'){
    await saveQueued(user.id,{payload,files});setMessage('Saved in your offline queue. Sync when you are online.');return;
   }
   if(!analysis)throw Error('Review the AI summary before submitting.');
   const result=created||await api('/citizen/needs',{method:'POST',body:payload});setCreated(result);
   const remaining=[...files];
   while(remaining.length){const file=remaining[0],body=new FormData();body.append('file',file);await api('/citizen/needs/'+result.id+'/media',{method:'POST',body});remaining.shift();setFiles([...remaining]);}
   navigate((user.role==='volunteer'?'/volunteer/requests/':'/citizen/requests/')+result.id);
  }catch(e){setError(e.message);}finally{setBusy(false);}
 }
 return <section className="card narrow"><h1>{t(user.role==='volunteer'?'Capture citizen request':'Report a need')}</h1>
 <p>{t('Tell us what is happening in your own language.')}</p><Notice message={error} error/><Notice message={message}/>
 {created&&<Notice message="Your report is saved. Retry to attach the remaining evidence."/>}
 <form onSubmit={submit}>
 <label className="field">{t('Description')}<textarea value={description} onChange={e=>{setDescription(e.target.value);setAnalysis(null);}} minLength={10} maxLength={4000} required disabled={!!created}/></label>
 <button type="button" className="secondary" onClick={record} disabled={busy||files.length>=5||!!created}>{recording?<Square size={18}/>:<Mic size={18}/>} {t(recording?'Stop recording':'Record voice')}</button>
 <p className="muted">{t('Audio is attached as evidence. Add a text summary; automatic speech transcription is not connected.')}</p>
 <Field label="Photo, video or audio evidence" type="file" accept="image/jpeg,image/png,image/webp,video/mp4,video/webm,audio/webm,audio/ogg,audio/wav,audio/mpeg" multiple onChange={e=>setFiles([...files,...e.target.files])}/>
 <p>{t('Up to 5 files, 20 MB each. Audio and video: at most 60 seconds.')}</p>
 <ul>{files.map((file,i)=><li key={i}>{file.name} <button type="button" className="text-button" onClick={()=>setFiles(files.filter((_,n)=>n!==i))}>{t('Remove')}</button></li>)}</ul>
 <button type="button" className="secondary" onClick={locate} disabled={busy||!!created}><MapPin size={18}/>{t('Use current location')}</button>
 <div className="grid two">{['latitude','longitude'].map(key=><Field key={key} label={key} type="number" step="any" required min={key==='latitude'?-90:-180} max={key==='latitude'?90:180} value={location[key]} onChange={e=>setLocation({...location,[key]:e.target.value})} disabled={!!created}/>)}</div>
 {['address','state','district'].map(key=><Field key={key} label={key} value={location[key]} required={key!=='address'} minLength={key==='address'?0:2} onChange={e=>setLocation({...location,[key]:e.target.value})} disabled={!!created}/>)}
 <div className="grid two"><Field name="locality" label="Locality"/><Field name="ward_village" label="Ward or village"/></div>
 <Field label="People affected" name="affected_people" type="number" min={1} max={10000000}/>
 <button type="button" className="secondary" onClick={understand} disabled={busy||description.length<10||!!created}>{t('Review AI understanding')}</button>
 {analysis&&<div className="notice"><p>{t('Suggested language')}: {analysis.language}</p><p>{t('Matched categories')}: {analysis.categories.map(t).join(', ')}</p><p>{analysis.description}</p><p>{t('Keyword suggestions support your decision. Confirm or change the category below.')}</p></div>}
 <Field label="Category" value={category} onChange={e=>setCategory(e.target.value)}>{categories.map(c=><option key={c} value={c}>{t(c)}</option>)}</Field>
 <label className="check"><input type="checkbox" name="consent" required/>{t('I consent to this report and evidence being used for civic planning. Private evidence requires review before public sharing.')}</label>
 {user.role==='volunteer'&&<label className="check"><input type="checkbox" name="citizen_consent" required/>{t('I explained the notice and the citizen agreed. I have not entered their name or phone number.')}</label>}
 <button disabled={busy||recording}><Send size={18}/>{t(busy?'Loading…':!navigator.onLine&&user.role==='volunteer'?'Save offline':'Submit report')}</button>
 </form></section>;
}
