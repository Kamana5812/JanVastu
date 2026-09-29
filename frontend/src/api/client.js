const BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '').replace(/\/api\/v1$/, '');
const SESSION_KEY = 'janvastu.session';
export function session() {
  try { return JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null'); }
  catch { return null; }
}
export function saveSession(value) {
  if (value) sessionStorage.setItem(SESSION_KEY, JSON.stringify(value));
  else sessionStorage.removeItem(SESSION_KEY);
  window.dispatchEvent(new Event('janvastu-session'));
}
let refreshing;
export async function api(path, options = {}, retry = true) {
  const current = session();
  const headers = { ...options.headers };
  if (!(options.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  if (current?.access_token) headers.Authorization = 'Bearer ' + current.access_token;
  const response = await fetch(BASE + '/api/v1' + path, { ...options, headers,
    body: options.body && !(options.body instanceof FormData) ? JSON.stringify(options.body) : options.body }).catch(()=>{throw Error('network_error');});
  if (response.status === 401 && current?.refresh_token && retry && !path.startsWith('/auth/')) {
    if (!refreshing) refreshing = fetch(BASE + '/api/v1/auth/refresh', { method: 'POST',
      headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh_token: current.refresh_token })
    }).then(async r => { if (!r.ok) throw Error('session_expired'); const s = await r.json(); saveSession(s); })
      .finally(() => { refreshing = null; });
    try { await refreshing; return api(path, options, false); }
    catch { saveSession(null); throw Error('session_expired'); }
  }
  const data = response.status === 204 ? null : response.headers.get('content-type')?.includes('application/json') ? await response.json() : await response.blob();
  if (!response.ok) throw Error(typeof data?.detail === 'string' ? data.detail : 'request_failed');
  return data;
}
export const downloadUrl = path => BASE + '/api/v1' + path;
