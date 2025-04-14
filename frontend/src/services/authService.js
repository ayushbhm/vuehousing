// frontend/src/services/authService.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/auth';

const authService = {
  login: async (username, password) => {
    try {
      const response = await axios.post(`${API_URL}/login`, { username, password });
      return response.data; 
    } catch (error) {
      throw new Error(error.response.data.msg || 'Login failed. Please try again.');
    }
  },

  logout: () => {
    localStorage.removeItem('token'); 
  },

  register: async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/create_user_account`, userData);
      return response.data; 
    } catch (error) {
      throw new Error(error.response.data.message || 'Registration failed. Please try again.');
    }
  },

  registerProfessional: async (professionalData) => {
    try {
      const response = await axios.post(`${API_URL}/create_professional_account`, professionalData);
      return response.data; 
    } catch (error) {
      throw new Error(error.response.data.message || 'Professional registration failed. Please try again.');
    }
  },

  
};

export default authService;