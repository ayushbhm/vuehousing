<template>
  <div class="service-list">
    <h2>Accepted Service Requests</h2>
    <div class="service-container">
      <div class="service-header">
        <span class="header-item">Request ID</span>
        <span class="header-item">Customer Name</span>
        <span class="header-item">Customer Phone</span>
        <span class="header-item">Customer Pincode</span>
        <span class="header-item">Date of Request</span>
        <span class="header-item">Remarks</span>
        <span class="header-item">Status</span>
      </div>
      <div class="service-row" v-for="request in acceptedRequests" :key="request.id">
        <span>{{ request.id }}</span>
        <span>{{ request.customer_name }}</span>
        <span>{{ request.customer_phone }}</span>
        <span>{{ request.customer_pincode }}</span>
        <span>{{ request.date_of_request }}</span>
        <span>{{ request.remarks }}</span>
        <span>{{ request.service_status }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import professionalService from '@/services/professionalService';

export default {
  data() {
    return {
      acceptedRequests: []
    };
  },
  methods: {
    async fetchAcceptedRequests() {
      try {
        const requests = await professionalService.fetchAcceptedServiceRequests();
        this.acceptedRequests = requests; // Store the fetched requests
      } catch (error) {
        console.error('Error fetching accepted service requests:', error);
      }
    }
  },
  mounted() {
    this.fetchAcceptedRequests(); // Fetch requests when the component is mounted
  }
};
</script>

<style scoped>
.service-list {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  color: #f5fef5;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #022607;
  box-shadow: 0 0 30px #d244b5; 
}

.service-container {
  max-height: 400px; /* Fixed height for scrolling */
  overflow-y: auto; /* Enable vertical scrolling */
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

.service-row span {
  flex: 1; 
}

.header-item {
  flex: 1; /* Equal space for each column */
  padding: 10px; /* Add padding for spacing */
  margin-right: 15px; /* Add margin to the right for spacing */
}

.header-item:last-child {
  margin-right: 0; /* Remove margin from the last item */
}
</style>
