import {createContext,useContext} from 'react';
export const LanguageContext=createContext();
export const useI18n=()=>useContext(LanguageContext);
