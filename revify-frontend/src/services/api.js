import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const revifyAPI = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Failed to connect to Revify API');
    }
  },

  // Extract features only (new endpoint - async, starts background task)
  extractFeatures: async (productUrl, productName = '') => {
    try {
      const response = await api.post('/extract-features', {
        product_url: productUrl,
        product_name: productName
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to extract features');
    }
  },

  // Get feature extraction status (for polling)
  getFeatureStatus: async () => {
    try {
      const response = await api.get('/feature-status');
      return response.data;
    } catch (error) {
      throw new Error('Failed to get feature extraction status');
    }
  },

  // Start product analysis with optional selected features
  startAnalysis: async (productUrl, productName = '', selectedFeatures = null) => {
    try {
      const payload = {
        product_url: productUrl,
        product_name: productName
      };
      
      // Only include selected_features if provided
      if (selectedFeatures && selectedFeatures.length > 0) {
        payload.selected_features = selectedFeatures;
      }
      
      const response = await api.post('/analyze', payload);
      return response.data;
    } catch (error) {
      if (error.response?.status === 409) {
        throw new Error('Analysis is already running. Please wait for it to complete.');
      }
      throw new Error(error.response?.data?.error || 'Failed to start analysis');
    }
  },

  // Get analysis status
  getAnalysisStatus: async () => {
    try {
      const response = await api.get('/status');
      return response.data;
    } catch (error) {
      throw new Error('Failed to get analysis status');
    }
  },

  // Get analysis results
  getResults: async () => {
    try {
      const response = await api.get('/results');
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        throw new Error('No results available yet');
      }
      throw new Error('Failed to get results');
    }
  },

  // Download analysis file
  downloadFile: async (filename) => {
    try {
      const response = await api.get(`/download/${filename}`, {
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error('Failed to download file');
    }
  }
};

export default api;