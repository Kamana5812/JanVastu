import { createContext, useContext, useEffect, useState } from 'react';
import { api, session, saveSession } from '../api/client';
const AuthContext = createContext();
export function AuthProvider({ children }) {
  const [value, setValue] = useState(session);
  useEffect(() => {
    const update = () => setValue(session());
    window.addEventListener('janvastu-session', update);
    return () => window.removeEventListener('janvastu-session', update);
  }, []);
  const logout = async () => { try { await api('/auth/logout', { method: 'POST' }); } finally { saveSession(null); } };
  return <AuthContext.Provider value={{ user: value?.user, login: saveSession, logout }}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
