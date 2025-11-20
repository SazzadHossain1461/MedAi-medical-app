import React from 'react';
import { useTranslation } from 'react-i18next';
import { useStore } from '../store/store';

export const LanguageSwitcher = () => {
  const { i18n } = useTranslation();
  const { language, setLanguage } = useStore();

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    i18n.changeLanguage(lang);
  };

  return (
    <div className="flex gap-2 bg-white/20 backdrop-blur-md rounded-full p-1">
      <button
        onClick={() => handleLanguageChange('en')}
        className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
          language === 'en'
            ? 'bg-white text-purple-600 shadow-lg'
            : 'text-white hover:bg-white/10'
        }`}
      >
        English
      </button>
      <button
        onClick={() => handleLanguageChange('bn')}
        className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
          language === 'bn'
            ? 'bg-white text-purple-600 shadow-lg'
            : 'text-white hover:bg-white/10'
        }`}
      >
        বাংলা
      </button>
    </div>
  );
};