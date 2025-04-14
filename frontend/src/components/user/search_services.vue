<template>
    <div>
        <h2>Search Services for Customers</h2>
        <div class="search-bar">
            <select v-model="selectedServiceType" @change="fetchServiceDetails">
                <option value="" disabled>Select Service Type</option>
                <option v-for="service in uniqueServices" :key="service.id" :value="service.id">
                    {{ service.name }}
                </option>
            </select>
            <input
                type="text"
                v-model="searchQuery"
                placeholder="Search for a service..."
                @input="filterServices"
            />
        </div>

        <div v-if="filteredServices.length">
            <h3>Available Services</h3>
            <div v-for="service in filteredServices" :key="service.id" class="service-details">
                <h4>{{ service.name }}</h4>
                <p><strong>Description:</strong> {{ service.description }}</p>
                <p><strong>Price:</strong> ${{ service.base_price }}</p>
                <p><strong>Time Required:</strong> {{ service.time_required }} minutes</p>
                <button @click="openBookingModal(service.id)" class="book-button">Book Service</button>
            </div>
        </div>

        <div v-if="!filteredServices.length && selectedServiceType">
            <p>No services available for this category.</p>
        </div>

        <!-- Booking Modal -->
        <div v-if="isModalOpen" class="modal-overlay" @click="closeBookingModal">
            <div class="modal-content" @click.stop>
                <book-service-form :serviceId="selectedServiceId" @close="closeBookingModal" />
            </div>
        </div>
    </div>
</template>

<script>
import customerService from '@/services/customerService';  // Import the customerService
import BookServiceForm from '@/components/user/book_service_form.vue'; // Import the booking form component

export default {
    components: {
        BookServiceForm
    },
    data() {
        return {
            services: [],  // Array to hold all service categories
            allServices: [],  // Array to hold all services related to the selected category
            filteredServices: [],  // Array to hold filtered services
            selectedServiceType: '',
            searchQuery: '',
            isModalOpen: false, // Control the visibility of the modal
            selectedServiceId: null // Store the ID of the selected service for booking
        };
    },
    computed: {
        uniqueServices() {
            const unique = {};
            return this.services.filter(service => {
                if (!unique[service.name]) {
                    unique[service.name] = true;
                    return true;
                }
                return false;
            });
        }
    },
    created() {
        this.fetchServices();  // Fetch service categories when component is created
    },
    methods: {
        async fetchServices() {
            try {
                const response = await customerService.getServices();  // Call the API to get service categories
                this.services = response.data;  // Store service categories in data
            } catch (error) {
                console.error('Error fetching services:', error);  // Handle errors
            }
        },
        async fetchServiceDetails() {
            if (this.selectedServiceType) {
                try {
                    const response = await customerService.getServiceDetails(this.selectedServiceType); // Fetch all services related to the selected type
                    this.allServices = response.data; // Store all services details
                    this.filteredServices = this.allServices; // Initialize filtered services
                    this.searchQuery = ''; // Reset search query when fetching new services
                } catch (error) {
                    console.error('Error fetching service details:', error); // Handle errors
                    this.filteredServices = []; // Reset filtered services if there's an error
                }
            } else {
                this.filteredServices = []; // Reset filtered services if no service is selected
            }
        },
        filterServices() {
            // Filter the services based on the search query
            this.filteredServices = this.allServices.filter(service => {
                const searchLower = this.searchQuery.toLowerCase();
                return (
                    service.name.toLowerCase().includes(searchLower) ||
                    service.description.toLowerCase().includes(searchLower) ||
                    service.base_price.toString().includes(searchLower) || // Convert price to string for comparison
                    service.time_required.toString().includes(searchLower) // Convert time to string for comparison
                );
            });
        },
        openBookingModal(serviceId) {
            this.selectedServiceId = serviceId; // Store the ID of the selected service for booking
            this.isModalOpen = true; // Show the modal
        },
        closeBookingModal() {
            this.isModalOpen = false; // Hide the modal
            this.selectedServiceId = null; // Reset the selected service ID
        }
    },
};
</script>

<style scoped>
.search-bar {
    display: flex;
    margin-bottom: 20px;
}

select {
    padding: 10px;
    margin-right: 10px;
}

input {
    flex: 1;
    padding: 10px;
}

.service-details {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #0d021f;
}

.book-button {
    margin-top: 20px; /* Add some space above the button */
    padding: 10px 20px; /* Add padding to the button */
    background-color: #007bff; /* Button color */
    color: white; /* Text color */
    border: none; /* Remove border */
    border-radius: 5px; /* Rounded corners */
    cursor: pointer; /* Pointer cursor on hover */
}

.book-button:hover {
    background-color: #0056b3; /* Darker shade on hover */
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: #0b0117;
    padding: 20px;
    border-radius: 10px;
    max-width: 30%;
    max-height: 60%;
    overflow: auto;
}
</style>