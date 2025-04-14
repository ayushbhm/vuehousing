import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/admin';

const adminService = {
    addService: async (serviceData) => {
        return await axios.post(`${API_URL}/add_service`, serviceData);
    },

    editService: async (serviceId, serviceData) => {
        return await axios.put(`${API_URL}/edit_service/${serviceId}`, serviceData);
    },

    deleteService: async (serviceId) => {
        return await axios.delete(`${API_URL}/delete_service/${serviceId}`);
    },

    getServices: async () => {
        
        return await axios.get(`${API_URL}/all_services`);
        
    },

    getService: async (serviceId) => {
        return await axios.get(`${API_URL}/services/${serviceId}`);
    },



    get_all_professionals: async()=>{
        return await axios.get(`${API_URL}/get_all_professionals`)
    },
    get_all_customers: async()=>{
        return await axios.get(`${API_URL}/get_all_customers`)
    },

    delete_professional_entry: async (professional_id) =>{
          return await axios.delete(`${API_URL}/delete_professional_entry/${professional_id}`)
    },
    verify_professional: async (professional_id) =>{
        return await axios.patch(`${API_URL}/verify_professional/${professional_id}`)
    },
    block_professional: async(professional_id) =>{
        return await axios.post(`${API_URL}/block_professional/${professional_id}`)
    },
    toggle_professional_verification: async (professional_id) =>{
        return await axios.patch(`${API_URL}/toggle_professional_verification/${professional_id}`)
    },
    all_service_requests: async() =>{
        return await axios.get(`${API_URL}/all_service_requests`)
    },
    getSummary: async () => {
        return await axios.get(`${API_URL}/summary`);
    },
    allreviews: async () => {
        return await axios.get(`${API_URL}/all_reviews`);
    },

};

export default adminService;