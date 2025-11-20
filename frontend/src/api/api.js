import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const dengueAPI = {
  predict: (data) => axiosInstance.post('/dengue/predict', data)
};

export const kidneyAPI = {
  predict: (data) => axiosInstance.post('/kidney/predict', data)
};

export const mentalHealthAPI = {
  predict: (data) => axiosInstance.post('/mental-health/assessment', data)
};

export const healthAPI = {
  check: () => axiosInstance.get('/health')
};

export default axiosInstance;