<template>
    <div>
        <h1>Services</h1>
        <div class="services-container">
            <router-link 
                v-for="service in uniqueServices" 
                :key="service.id"  
                :to="{ name: 'ServiceDetail', params: { id: service.id } }" 
                class="service-box"
            >
                {{ service.name }}  <!-- Display the service name -->
            </router-link>
        </div>
    </div>
</template>

<script>
import customerService from '@/services/customerService';  // Import the customerService

export default {
    data() {
        return {
            services: [],  // Array to hold services
            uniqueServices: []  // Array to hold unique services
        };
    },
    created() {
        this.fetchServices();  // Fetch services when component is created
    },
    methods: {
        async fetchServices() {
            try {
                const response = await customerService.getServices();  // Call the API from customerService
                console.log('Fetched services:', response.data); // Log the fetched services
                this.services = response.data;  // Store services in data
                this.filterUniqueServices();  // Filter unique services
            } catch (error) {
                console.error('Error fetching services:', error);  // Handle errors
            }
        },
        filterUniqueServices() {
            const seenNames = new Set();  // Set to track seen service names
            this.uniqueServices = this.services.filter(service => {
                if (!seenNames.has(service.name)) {
                    seenNames.add(service.name);  // Add name to the set
                    return true;  // Keep this service
                }
                return false;  // Skip this service
            });
        }
    }
};
</script>

<style scoped>
.services-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;  /* Increased space between service boxes */
    justify-content: center;  /* Center the boxes */
}

.service-box {
    border: 1px solid #ccc;
    padding: 30px;  /* Increased padding for better appearance */
    border-radius: 10px;  /* Slightly rounded corners */
    cursor: pointer;
    width: 200px;  /* Increased width for larger boxes */
    height: 100px;  /* Fixed height for uniformity */
    text-align: center;  /* Center text inside the box */
    font-size: 18px;  /* Increased font size for better readability */
    transition: background-color 0.3s;  /* Smooth background change on hover */
    text-decoration: none;  /* Remove underline from links */
    color: inherit;  /* Inherit text color */
}

.service-box:hover {
    background-color: #f0f0f0;  /* Highlight on hover */
}
</style>