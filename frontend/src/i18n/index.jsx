import {useState, useEffect} from 'react';
import en from './en.json';
import hi from './hi.json';
import or from './or.json';
const dictionaries = { en, hi, or };
import {LanguageContext as Context} from './useI18n';
export function LanguageProvider({ children }) {
  const [language, update] = useState(()=>{const stored=localStorage.getItem('janvastu.language');return dictionaries[stored]?stored:'en';});
  useEffect(()=>{document.documentElement.lang=language;},[language]);
  const setLanguage = value => { update(value); localStorage.setItem('janvastu.language', value); document.documentElement.lang = value; };
  const t = key => dictionaries[language]?.[key] || en[key] || key;
  return <Context.Provider value={{ language, setLanguage, t }}>{children}</Context.Provider>;
}
