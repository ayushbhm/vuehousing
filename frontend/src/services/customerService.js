import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/customer';

const customerService = {
    getServices: async () => {
        return await axios.get(`${API_URL}/services_available`);
    },
    getServiceDetails: async (id) => {  
        return await axios.get(`${API_URL}/service_details/${id}`);  // Use id in the API call
    },
    getParticularService: async (id) => {  // New method to get a particular service by ID
        return await axios.get(`${API_URL}/get_particular_service/${id}`);  // Use id in the API call
    },
    getServiceRequests: async (token) => {
        return await axios.get(`${API_URL}/customer_service_requests`, {
            headers: {
                Authorization: `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        });
    },
    getCustomerSummary: async (token) => {
        return await axios.get(`${API_URL}/summary`, {
            headers: {
                Authorization: `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        });
    },
    closeServiceRequest: async (token, request_id) => {
        return await axios.put(`${API_URL}/close_service_request/${request_id}/close`, {
            headers: { Authorization: `Bearer ${token}` }
        });
    },
    bookService: async (token, serviceId) => {  // Change parameter from serviceName to serviceId
        return await axios.post(`${API_URL}/book_service/${serviceId}`, {}, {  // Use serviceId in the API call
            headers: {
                Authorization: `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        });
    },
    submitReview: async (requestId, reviewData) => {
        const token = localStorage.getItem('token'); // Get the token from localStorage
        if (!token) {
            throw new Error('No token found'); // Optionally handle the case where the token is not found
        }
        
        return await axios.post(`${API_URL}/submit_review/${requestId}`, reviewData, {
            headers: {
                Authorization: `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        });
    },
}

export default customerService;