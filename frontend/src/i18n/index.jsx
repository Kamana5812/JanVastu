import { createContext, useContext, useState } from 'react';
import en from './en.json';
import hi from './hi.json';
import or from './or.json';
const dictionaries = { en, hi, or };
const Context = createContext();
export function LanguageProvider({ children }) {
  const [language, update] = useState(localStorage.getItem('janvastu.language') || 'en');
  const setLanguage = value => { update(value); localStorage.setItem('janvastu.language', value); document.documentElement.lang = value; };
  const t = key => dictionaries[language]?.[key] || en[key] || key;
  return <Context.Provider value={{ language, setLanguage, t }}>{children}</Context.Provider>;
}
export const useI18n = () => useContext(Context);
