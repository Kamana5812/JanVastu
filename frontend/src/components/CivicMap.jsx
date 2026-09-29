import {MapContainer, TileLayer, CircleMarker, Popup, useMap} from 'react-leaflet';
import {useEffect} from 'react';
import 'leaflet/dist/leaflet.css';
import {useI18n} from '../i18n/useI18n';
function Bounds({points}){const map=useMap();useEffect(()=>{if(points.length)map.fitBounds(points.map(p=>[p.latitude,p.longitude]),{padding:[35,35],maxZoom:12});},[points,map]);return null;}
export default function CivicMap({points=[]}){
 const {t}=useI18n();
 points=points.filter(p=>Number.isFinite(p.latitude)&&Number.isFinite(p.longitude));
 return <MapContainer className="map" center={[20.3,85.8]} zoom={6} scrollWheelZoom={false} aria-label={t('Demand and infrastructure map')}>
 <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'/>
 <Bounds points={points}/>
 {points.map((p,i)=><CircleMarker key={p.id||i} center={[p.latitude,p.longitude]} radius={Math.min(22,7+Math.sqrt(Math.max(0,p.value||0))*3)} pathOptions={{color:p.color||'#176B73',fillOpacity:.5}}><Popup><strong>{p.name||p.district}</strong><p>{t(p.category||p.status||'Projects')}</p>{p.value!==undefined&&<p>{t('Value')}: {p.value??t('Information Not Available')}</p>}{(p.is_sample||p.is_sample_context)&&<p>{t('Synthetic sample')}</p>}</Popup></CircleMarker>)}
 </MapContainer>;
}
