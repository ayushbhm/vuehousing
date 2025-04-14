<template>
    <div class="service-list">
      <h2>New Service Requests</h2>
      <div class="service-container">
        <div class="service-header">
          <span class="header-item">Request ID</span>
          <span class="header-item">Customer Name</span>
          <span class="header-item">Customer Phone</span>
          <span class="header-item">Customer Pincode</span>
          <span class="header-item">Date of Request</span>
          <span class="header-item">Status</span>
          <span class="header-item">Actions</span>
        </div>
        <div class="service-row" v-for="request in upcomingRequests" :key="request.id">
          <span>{{ request.id }}</span>
          <span>{{ request.customer_name }}</span>
          <span>{{ request.customer_phone }}</span>
          <span>{{ request.customer_pincode }}</span>
          <span>{{ request.date_of_request }}</span>
          <span>{{ request.service_status }}</span>
          <span>
            <button @click="acceptRequest(request.id)">Accept</button>
            <button @click="rejectRequest(request.id)">Reject</button>
          </span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import professionalService from '@/services/professionalService';
  
  export default {
    data() {
      return {
        upcomingRequests: []
      };
    },
    methods: {
      async fetchUpcomingRequests() {
        try {
          const requests = await professionalService.getUpcomingServiceRequests();
          this.upcomingRequests = requests; // Store the fetched requests
        } catch (error) {
          console.error('Error fetching upcoming service requests:', error);
        }
      },
      async acceptRequest(requestId) {
        try {
          const response = await professionalService.acceptServiceRequest(requestId);
          console.log(response.message); // Log the response message
          this.fetchUpcomingRequests(); // Refresh the list after accepting
        } catch (error) {
          console.error('Error accepting service request:', error);
        }
      },
      async rejectRequest(requestId) {
        try {
          const response = await professionalService.rejectServiceRequest(requestId);
          console.log(response.message); // Log the response message
          this.fetchUpcomingRequests(); // Refresh the list after rejecting
        } catch (error) {
          console.error('Error rejecting service request:', error);
        }
      }
    },
    mounted() {
      this.fetchUpcomingRequests(); // Fetch requests when the component is mounted
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
  
  button {
    margin-left: 5px; /* Add some space between buttons */
    padding: 5px 10px; /* Add padding for better appearance */
    background-color: #4CAF50; /* Green background for accept */
    color: white; /* White text */
    border: none; /* Remove border */
    border-radius: 3px; /* Rounded corners */
    cursor: pointer; /* Pointer cursor on hover */
  }
  
  button:hover {
    background-color: #45a049; /* Darker green on hover */
  }
  </style>