<template>
  <div class="service-list">
    <h2>All Service Requests</h2>
    <div class="service-container">
      <div class="service-header">
        <span class="header-item">ID</span>
        <span class="header-item">Assigned Professional</span>
        <span class="header-item">Requested Date</span>
        <span class="header-item">Status</span>
        <span class="header-item">Actions</span> <!-- New column for actions -->
      </div>
      <div class="service-row" v-for="request in serviceRequests" :key="request.id">
        <span>{{ request.id }}</span>
        <span>{{ request.professional_name || 'Unassigned' }}</span>
        <span>{{ request.date_of_request }}</span>
        <span>{{ request.service_status }}</span>
        <span>
          <button v-if="request.service_status === 'closed'" @click="viewReview(request.id)">View</button>
        </span>
      </div>
    </div>

    <!-- Review Details -->
    <div v-if="selectedReview" class="review-details">
      <h3>Review Details</h3>
      <p><strong>Rating:</strong> {{ selectedReview.rating }}</p>
      <p><strong>Comments:</strong> {{ selectedReview.comments }}</p>
      <button @click="closeReview">Close</button>
    </div>
  </div>
</template>

<script>
import adminService from '@/services/adminService'; 
import { ref, onMounted } from 'vue';

export default {
  name: 'AllServiceRequestBox',
  setup() {
    const serviceRequests = ref([]); // Store service requests
    const selectedReview = ref(null); // Store selected review

    // Fetch all service requests
    const fetchServiceRequests = async () => {
      try {
        const response = await adminService.all_service_requests(); // Fetch all service requests
        serviceRequests.value = response.data; 
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    };

    // Fetch all reviews
    const fetchReviews = async () => {
      try {
        const response = await adminService.allreviews(); // Fetch all reviews
        return response.data; 
      } catch (error) {
        console.error('Error fetching reviews:', error);
        return [];
      }
    };

    // View review for the selected service request
    const viewReview = async (serviceRequestId) => {
      const reviews = await fetchReviews(); // Fetch all reviews
      // Find the review that matches the service_request_id
      selectedReview.value = reviews.find(review => review.service_request_id === serviceRequestId);
      if (!selectedReview.value) {
        console.error('No review found for this service request ID:', serviceRequestId);
      }
    };

    // Close the review details
    const closeReview = () => {
      selectedReview.value = null; // Close the review details
    };

    // Fetch service requests when the component is mounted
    onMounted(() => {
      fetchServiceRequests();
    });

    return {
      serviceRequests,
      selectedReview,
      viewReview,
      closeReview,
    };
  },
};
</script>

<style scoped>
.service-list {
  max-width: 900px;
  margin: auto;
  padding: 20px;
  color: #f5fef5;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #022607;
  box-shadow: 0 0 30px #d244b5;
}

.service-container {
  max-height: 400px;
  overflow-y: auto;
}

.service-header {
  display: flex;
  font-weight: bold;
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}

.service-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.review-details {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #02180c;
}
</style>