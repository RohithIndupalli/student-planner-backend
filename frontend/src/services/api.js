import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getCurrentUser: () => api.get('/api/auth/me'),
};

// Courses API
export const coursesAPI = {
  getAll: () => api.get('/api/courses/'),
  getById: (id) => api.get(`/api/courses/${id}`),
  create: (data) => api.post('/api/courses/', data),
  update: (id, data) => api.put(`/api/courses/${id}`, data),
  delete: (id) => api.delete(`/api/courses/${id}`),
};

// Assignments API
export const assignmentsAPI = {
  getAll: () => api.get('/api/assignments/'),
  getById: (id) => api.get(`/api/assignments/${id}`),
  create: (data) => api.post('/api/assignments/', data),
  update: (id, data) => api.put(`/api/assignments/${id}`, data),
  toggleComplete: (id) => api.patch(`/api/assignments/${id}/complete`),
  delete: (id) => api.delete(`/api/assignments/${id}`),
};

// Schedules API
export const schedulesAPI = {
  getAll: () => api.get('/api/schedules/'),
  getById: (id) => api.get(`/api/schedules/${id}`),
  create: (data) => api.post('/api/schedules/', data),
  update: (id, data) => api.put(`/api/schedules/${id}`, data),
  delete: (id) => api.delete(`/api/schedules/${id}`),
};

// Chat API
export const chatAPI = {
  sendMessage: (message) => api.post('/api/chat/', { message }),
};

export default api;
