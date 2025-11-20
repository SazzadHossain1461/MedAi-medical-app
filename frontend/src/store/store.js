import create from 'zustand';

export const useStore = create((set) => ({
  language: localStorage.getItem('language') || 'en',
  setLanguage: (lang) => {
    localStorage.setItem('language', lang);
    set({ language: lang });
  },

  dengueResult: null,
  setDengueResult: (result) => set({ dengueResult: result }),

  kidneyResult: null,
  setKidneyResult: (result) => set({ kidneyResult: result }),

  mentalHealthResult: null,
  setMentalHealthResult: (result) => set({ mentalHealthResult: result }),

  loading: false,
  setLoading: (loading) => set({ loading }),

  error: null,
  setError: (error) => set({ error })
}));