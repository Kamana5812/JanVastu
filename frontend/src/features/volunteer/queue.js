function open(){
 return new Promise((resolve,reject)=>{const request=indexedDB.open('janvastu-queue',1);request.onupgradeneeded=()=>request.result.createObjectStore('reports',{keyPath:'key'});request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(Error('offline_storage_failed'));});
}
async function transaction(mode,action){
 const db=await open();return new Promise((resolve,reject)=>{const tx=db.transaction('reports',mode);const request=action(tx.objectStore('reports'));tx.oncomplete=()=>{resolve(request.result);db.close();};tx.onerror=()=>{reject(Error('offline_storage_failed'));db.close();};});
}
export const saveQueued=(owner,item)=>transaction('readwrite',store=>store.put({...item,key:owner+':'+item.payload.client_id,owner,saved_at:new Date().toISOString()}));
export const queued=async owner=>(await transaction('readonly',store=>store.getAll())).filter(x=>x.owner===owner);
export const removeQueued=key=>transaction('readwrite',store=>store.delete(key));
