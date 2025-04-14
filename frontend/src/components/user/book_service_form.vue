<template>
    <div class="book-service-form">
        <h1>Book a Service</h1>
        <div v-if="service" class="service-box">
            <h2>{{ service.name }}</h2>
            <p><strong>Description:</strong> {{ service.description }}</p>
            <p><strong>Price:</strong> ${{ service.base_price }}</p>
            <p><strong>Time Required:</strong> {{ service.time_required }} minutes</p>
            <button @click="bookService" class="book-button">Book Service</button>
        </div>
        <div v-else>
            <p>Loading service details...</p>
        </div>
    </div>
</template>

<script>
import customerService from '@/services/customerService'; // Import the customerService

export default {
    props: {
        serviceId: { // Prop to accept service ID
            type: Number,
            required: true
        }
    },
    data() {
        return {
            service: null, // To hold the service details
        };
    },
    created() {
        this.fetchServiceDetails(); // Fetch service details on component creation
    },
    methods: {
        async fetchServiceDetails() {
            try {
                const response = await customerService.getParticularService(this.serviceId); // Fetch service details by ID
                this.service = response.data; // Store the service details
            } catch (error) {
                console.error('Error fetching service details:', error); // Handle errors
            }
        },
        async bookService() {
            const token = localStorage.getItem('token'); // Get the token from localStorage
            try {
                const response = await customerService.bookService(token, this.service.id); // Book the service using the service ID
                alert(response.data.message); // Show success message
            } catch (error) {
                console.error('Error booking service:', error); // Handle errors
                alert(error.response.data.error || 'An error occurred while booking the service.'); // Show error message
            }
        }
    }
};
</script>

<style scoped>
.book-service-form {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center the content horizontally */
    margin-top: 20px; /* Add some space at the top */
}

.service-box {
    border: 1px solid #170e0e;
    border-radius: 10px;
    padding: 20px;
    background-color: #0e0404;
    width: 80%; /* Set the width of the details box */
    max-width: 600px; /* Set a maximum width for larger screens */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
}

.book-button {
    margin-top: 20px; /* Add some space above the button */
    padding: 10px 20px; /* Add padding to the button */
    background-color: #007bff; /* Button color */
    color: rgb(20, 11, 11); /* Text color */
    border: none; /* Remove border */
    border-radius: 5px; /* Rounded corners */
    cursor: pointer; /* Pointer cursor on hover */
}

.book-button:hover {
    background-color: #0056b3; /* Darker shade on hover */
}
</style>