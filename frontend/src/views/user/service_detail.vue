<template>
    <UserNavbar />
    <div class="service-detail-container">
        <h1>Service Details</h1>
        <div class="service-details">
            <div v-if="services && services.length > 0">
                <div class="service-box">
                    <div class="service-header">
                        <h2>Service List</h2>
                    </div>
                    <div class="service-columns">
                        <div class="service-column">
                            <strong>Name</strong>
                        </div>
                        <div class="service-column">
                            <strong>Description</strong>
                        </div>
                        <div class="service-column">
                            <strong>Price</strong>
                        </div>
                        <div class="service-column">
                            <strong>Time Required</strong>
                        </div>
                        <div class="service-column">
                            <strong>Action</strong>
                        </div>
                    </div>
                    <div v-for="service in services" :key="service.id" class="service-row">
                        <div class="service-column">{{ service.name }}</div>
                        <div class="service-column">{{ service.description }}</div>
                        <div class="service-column">${{ service.base_price }}</div>
                        <div class="service-column">{{ service.time_required }} minutes</div>
                        <div class="service-column">
                            <button @click="openBookingModal(service.id)" class="book-button">Book Service</button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <p>Loading service details...</p>
            </div>
        </div>
        <router-link to="/user/homepage">Back to Homepage</router-link>

        <!-- Booking Modal -->
        <div v-if="isModalOpen" class="modal-overlay" @click="closeBookingModal">
            <div class="modal-content" @click.stop>
                <book-service-form :service-id="selectedServiceId" @close="closeBookingModal" />
            </div>
        </div>
    </div>
</template>

<script>
import customerService from '@/services/customerService'; // Import the customerService
import BookServiceForm from '@/components/user/book_service_form.vue'; // Import the booking form component
import UserNavbar from '@/components/user/navbar.vue';

export default {
    components: {
        BookServiceForm,
        UserNavbar
    },
    data() {
        return {
            services: [], // Array to hold the details of the selected services
            isModalOpen: false, // Control the visibility of the modal
            selectedServiceId: null // Store the ID of the selected service for booking
        };
    },
    created() {
        const serviceId = this.$route.params.id; // Get the service ID from the route
        this.fetchServiceDetails(serviceId); // Fetch details for the selected service using ID
    },
    methods: {
        async fetchServiceDetails(serviceId) {
            try {
                const response = await customerService.getServiceDetails(serviceId); // Fetch service details by ID
                this.services = response.data; // Store the service details in the component's data as an array
            } catch (error) {
                console.error('Error fetching service details:', error); // Handle errors
            }
        },
        openBookingModal(serviceId) {
            this.selectedServiceId = serviceId; // Store the ID of the selected service for booking
            this.isModalOpen = true; // Show the modal
        },
        closeBookingModal() {
            this.isModalOpen = false; // Hide the modal
        }
    }
};
</script>

<style scoped>
.service-detail-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center the content horizontally */
    margin-top: 20px; /* Add some space at the top */
}

.service-details {
    width: 80%; /* Set the width of the details box */
    max-width: 800px; /* Set a maximum width for larger screens */
}

.service-box {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    background-color: #000000;
}

.service-header {
    margin-bottom: 10px;
}

.service-columns {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
}

.service-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-top: 1px solid #e0e0e0;
}

.service-column {
    flex: 1; /* Each column takes equal space */
    padding: 5px;
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