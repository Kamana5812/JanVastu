import {useEffect,useState} from 'react';
import {api} from '../api/client';
export function useResource(path) {
  const [result, setResult] = useState({path:null,revision:-1,data:null,error:''});
  const [revision, setRevision] = useState(0);
  useEffect(() => {
    if (!path) { return; }
    let active = true;
    api(path).then(data => { if (active) setResult({path,revision,data,error:''}); })
      .catch(e => { if (active) setResult({path,revision,data:null,error:e.message}); });
    return () => { active = false; };
  }, [path, revision]);
  // Route changes must never render the previous route's response shape.
  const current=result.path===path&&result.revision===revision;
  return {data:current?result.data:null,error:current?result.error:'',loading:!current,reload:()=>setRevision(r=>r+1)};
}
