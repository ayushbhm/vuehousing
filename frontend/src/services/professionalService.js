import axios from 'axios'; // Import axios directly
const API_URL = 'http://127.0.0.1:5000/prof'; // Adjust the base URL to match your Flask route

const professionalService = {
  // Method to fetch professional services
  getServices: async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/service/professional_services`); // Use axios directly
      return response.data; // Return the list of services
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to fetch services.');
    }
  },

  // Method to fetch upcoming service requests
  getUpcomingServiceRequests: async () => {
    try {
      const token = localStorage.getItem('token'); // Get the token from local storage
      const response = await axios.get(`${API_URL}/upcoming_service_requests`, {
        headers: {
          Authorization: `Bearer ${token}` // Set the Authorization header
        }
      });
      return response.data; // Return the list of upcoming service requests
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to fetch upcoming service requests.');
    }
  },

  // Method to fetch closed service requests
  getClosedServiceRequests: async () => {
    try {
      const token = localStorage.getItem('token'); // Get the token from local storage
      const response = await axios.get(`${API_URL}/closed_service_requests`, {
        headers: {
          Authorization: `Bearer ${token}` // Set the Authorization header
        }
      });
      return response.data; // Return the list of closed service requests
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to fetch closed service requests.');
    }
  },

  // Method to fetch accepted service requests
  fetchAcceptedServiceRequests: async () => {
    try {
      const token = localStorage.getItem('token'); // Get the token from local storage
      const response = await axios.get(`${API_URL}/accepted_service_requests`, {
        headers: {
          Authorization: `Bearer ${token}` // Set the Authorization header
        }
      });
      return response.data; // Return the list of accepted service requests
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to fetch accepted service requests.');
    }
  },

  // Method to fetch professional statistics
  fetchProfessionalStats: async () => {
    try {
      const token = localStorage.getItem('token'); // Get the token from local storage
      const response = await axios.get(`${API_URL}/professional_stats`, {
        headers: {
          Authorization: `Bearer ${token}` // Set the Authorization header
        }
      });
      return response.data; // Return the professional statistics
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to fetch professional statistics.');
    }
  },

  // Method to accept a service request
  acceptServiceRequest: async (requestId) => {
    try {
      const token = localStorage.getItem('token'); // Get the token from local storage
      const response = await axios.post(`${API_URL}/service_request/${requestId}/accept`, {}, {
        headers: {
          Authorization: `Bearer ${token}` // Set the Authorization header
        }
      });
      return response.data; // Return the response message
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to accept service request.');
    }
  },

  // Method to reject a service request
  rejectServiceRequest: async (requestId) => {
    try {
      const token = localStorage.getItem('token'); // Get the token from local storage
      const response = await axios.post(`${API_URL}/service_request/${requestId}/reject`, {}, {
        headers: {
          Authorization: `Bearer ${token}` // Set the Authorization header
        }
      });
      return response.data; // Return the response message
    } catch (error) {
      throw new Error(error.response.data.message || 'Failed to reject service request.');
    }
  },

  // Fetch professional details
  getProfileDetails: async () => {
    const token = localStorage.getItem('token'); // Get the token from local storage
    return await axios.get(`${API_URL}/profile_details`, {
        headers: {
            Authorization: `Bearer ${token}` // Set the Authorization header
        }
    });
},

  // Update professional details
  updateProfile: async (profileData) => {
    const token = localStorage.getItem('token'); // Get the token from local storage
    if (!token) {
        throw new Error('No token found'); // Handle the case where the token is not found
    }
    
    return await axios.post(`${API_URL}/update_profile`, profileData, {
        headers: {
            Authorization: `Bearer ${token}` // Include the JWT token in the Authorization header
        }
    });
  }
};

export default professionalService;