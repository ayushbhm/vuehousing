<template>
    <div class="service-history-container">
        <h1>Your Service History</h1>
        <div v-if="serviceRequests.length > 0">
            <div class="service-box">
                <div class="service-header">
                    <h2>Service Requests</h2>
                </div>
                <div class="service-columns">
                    <div class="service-column">
                        <strong>Request ID</strong>
                    </div>
                    <div class="service-column">
                        <strong>Service Name</strong>
                    </div>
                    <div class="service-column">
                        <strong>Professional Name</strong>
                    </div>
                    <div class="service-column">
                        <strong>Professional Phone</strong>
                    </div>
                    <div class="service-column">
                        <strong>Date of Request</strong>
                    </div>
                    <div class="service-column">
                        <strong>Status</strong>
                    </div>
                    <div class="service-column">
                        <strong>Remarks</strong>
                    </div>
                    <div class="service-column">
                        <strong>Action</strong>
                    </div>
                </div>
                <div v-for="request in serviceRequests" :key="request.id" class="service-row">
                    <div class="service-column">{{ request.id }}</div>
                    <div class="service-column">{{ request.service_name }}</div>
                    <div class="service-column">{{ request.professional_name }}</div>
                    <div class="service-column">{{ request.professional_phone }}</div>
                    <div class="service-column">{{ request.date_of_request }}</div>
                    <div class="service-column">{{ request.service_status }}</div>
                    <div class="service-column">{{ request.remarks }}</div>
                    <div class="service-column">
                        <button v-if="request.service_status === 'assigned'" @click="openServiceRemarks(request)">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <p>No service history found.</p>
        </div>

        <!-- Modal for Service Remarks -->
        <div v-if="selectedService" class="modal-overlay" @click="closeModal">
            <div class="modal-content" @click.stop>
                <service-remarks :service="selectedService" @close="closeModal" />
            </div>
        </div>
    </div>
</template>

<script>
import customerService from '@/services/customerService'; // Import the customerService
import ServiceRemarks from '@/components/user/service_remarks.vue'; // Import the ServiceRemarks component

export default {
    data() {
        return {
            serviceRequests: [], // Array to hold the service requests
            selectedService: null // To hold the selected service for remarks
        };
    },
    created() {
        const token = localStorage.getItem('token'); // Assuming you store the token in local storage
        this.fetchServiceRequests(token); // Fetch service requests when the component is created
    },
    methods: {
        fetchServiceRequests(token) {
            customerService.getServiceRequests(token)
                .then(response => {
                    this.serviceRequests = response.data; // Store the service requests in the component's data
                })
                .catch(error => {
                    console.error('Error fetching service requests:', error); // Handle errors
                });
        },
        openServiceRemarks(service) {
            this.selectedService = service; // Set the selected service for remarks
        },
        closeModal() {
            this.selectedService = null; // Clear the selected service to close the modal
        }
    },
    components: {
        ServiceRemarks // Register the ServiceRemarks component
    }
};
</script>

<style scoped>
.service-history-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center the content horizontally */
    margin-top: 20px; /* Add some space at the top */
    padding: 20px; /* Add padding for more space */
    min-height: 100vh; /* Ensure it takes at least the full height of the viewport */
}

.service-box {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    background-color: #100404;
    width: 90%; /* Set the width of the details box */
    max-width: 800px; /* Set a maximum width for larger screens */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add a subtle shadow for depth */
}

.service-header {
    margin-bottom: 10px;
    color: #fff; /* Change header text color for better visibility */
}

.service-columns {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    color: #fff; /* Change column header text color for better visibility */
}

.service-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-top: 1px solid #e0e0e0;
    color: #fff; /* Change row text color for better visibility */
}

.service-column {
    flex: 1; /* Each column takes equal space */
    padding: 5px;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Ensure it appears above other content */
}

.modal-content {
    background-color: #140115; /* White background for the modal */
    border-radius: 10px;
    padding: 5px;
    width: 90%; /* Set width of the modal */
    max-width: 600px; /* Set a maximum width for larger screens */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add a subtle shadow for depth */
}
</style>