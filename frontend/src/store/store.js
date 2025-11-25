import create from 'zustand';

export const useStore = create((set) => ({
  // Authentication
  isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  
  setUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user));
    set({ user });
  },
  
  setIsAuthenticated: (auth) => {
    localStorage.setItem('isAuthenticated', auth.toString());
    set({ isAuthenticated: auth });
  },
  
  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    localStorage.removeItem('isAuthenticated');
    set({ user: null, isAuthenticated: false });
  },

  // Language
  language: localStorage.getItem('language') || 'en',
  setLanguage: (lang) => {
    localStorage.setItem('language', lang);
    set({ language: lang });
  },

  // Dengue Prediction
  dengueResult: null,
  setDengueResult: (result) => set({ dengueResult: result }),
  
  // Kidney Prediction
  kidneyResult: null,
  setKidneyResult: (result) => set({ kidneyResult: result }),
  
  // Mental Health Prediction
  mentalHealthResult: null,
  setMentalHealthResult: (result) => set({ mentalHealthResult: result }),

  // Loading State
  loading: false,
  setLoading: (loading) => set({ loading }),

  // Error State
  error: null,
  setError: (error) => set({ error }),

  // Clear Results
  clearResults: () => {
    set({
      dengueResult: null,
      kidneyResult: null,
      mentalHealthResult: null,
      error: null
    });
  }
}));
