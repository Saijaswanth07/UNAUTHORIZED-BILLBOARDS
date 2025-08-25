import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Public API endpoints
export const publicApi = {
  // Fetch heatmap data with optional filters
  fetchHeatmapData: async (params = {}) => {
    try {
      const response = await api.get('/public/heatmap', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching heatmap data:', error);
      throw error;
    }
  },
  
  // Get public statistics
  fetchPublicStats: async () => {
    try {
      const response = await api.get('/public/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching public stats:', error);
      throw error;
    }
  },
  
  // Get leaderboard data
  fetchLeaderboard: async (limit = 100) => {
    try {
      const response = await api.get(`/public/leaderboard?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
      throw error;
    }
  },
  
  // Get reward tiers
  fetchRewardTiers: async () => {
    try {
      const response = await api.get('/public/rewards/tiers');
      return response.data;
    } catch (error) {
      console.error('Error fetching reward tiers:', error);
      throw error;
    }
  },
};

// User API endpoints
export const userApi = {
  // Submit a new report
  submitReport: async (reportData) => {
    try {
      const formData = new FormData();
      
      // Append basic fields
      formData.append('title', reportData.title);
      formData.append('description', reportData.description);
      formData.append('latitude', reportData.location.latitude);
      formData.append('longitude', reportData.location.longitude);
      
      // Append images
      reportData.images.forEach((image, index) => {
        formData.append(`images`, image);
      });
      
      const response = await api.post('/reports', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error submitting report:', error);
      throw error;
    }
  },
  
  // Get user's reports
  getUserReports: async (status = null) => {
    try {
      const params = status ? { status } : {};
      const response = await api.get('/user/reports', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching user reports:', error);
      throw error;
    }
  },
  
  // Get user's points and rewards
  getUserRewards: async () => {
    try {
      const response = await api.get('/user/rewards');
      return response.data;
    } catch (error) {
      console.error('Error fetching user rewards:', error);
      throw error;
    }
  },
};

// Admin API endpoints
export const adminApi = {
  // Get all reports with filters
  getReports: async (filters = {}) => {
    try {
      const response = await api.get('/admin/reports', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Error fetching reports:', error);
      throw error;
    }
  },
  
  // Update report status
  updateReportStatus: async (reportId, status, notes = '') => {
    try {
      const response = await api.patch(`/admin/reports/${reportId}/status`, {
        status,
        notes,
      });
      return response.data;
    } catch (error) {
      console.error('Error updating report status:', error);
      throw error;
    }
  },
  
  // Get system statistics
  getSystemStats: async () => {
    try {
      const response = await api.get('/admin/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching system stats:', error);
      throw error;
    }
  },
};

export default api;
