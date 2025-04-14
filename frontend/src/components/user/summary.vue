<template>

  
    <div class="summary">
      <h2>Customer Summary</h2>
      <div class="stats">
        <div class="stat-item">
          <h3>Total Requested Services</h3>
          <div class="stat-value">{{ summaryData.requested }}</div>
        </div>
        <div class="stat-item">
          <h3>Total Closed Services</h3>
          <div class="stat-value">{{ summaryData.closed }}</div>
        </div>
        <div class="stat-item">
          <h3>Total Assigned Services</h3>
          <div class="stat-value">{{ summaryData.assigned }}</div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import customerService from '@/services/customerService'; // Import the customer service
  
  export default {
    data() {
      return {
        summaryData: {
          requested: 0,
          closed: 0,
          assigned: 0,
        },
      };
    },
    mounted() {
      this.fetchSummary(); // Fetch summary when the component is mounted
    },
    methods: {
      fetchSummary() {
        const token = localStorage.getItem('token'); // Get the JWT token from local storage
        customerService.getCustomerSummary(token) // Call the API
          .then(response => {
            console.log('API Response:', response.data); // Log the response data for debugging
            this.summaryData = response.data; // Store the summary data
          })
          .catch(error => {
            console.error('Error fetching customer summary:', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .summary {
    max-width: 800px;
    margin: auto;
    padding: 20px;
    background-color: #211e1e; /* Light background for the summary */
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(36, 25, 54, 0.1);
  }
  
  .stats {
    display: flex;
    flex-wrap: wrap; /* Allow items to wrap to the next line */
    justify-content: space-between; /* Space out items */
  }
  
  .stat-item {
    flex: 1 1 calc(30% - 20px); /* Responsive width */
    margin: 10px; /* Space between items */
    padding: 20px;
    background-color: #4CAF50; /* Green background for each stat item */
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s; /* Smooth transition */
  }
  
  .stat-item:hover {
    transform: translateY(-5px); /* Lift effect on hover */
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2); /* Increase shadow on hover */
  }
  
  .stat-item h3 {
    margin: 0;
    font-size: 1.2em;
    color: #ffffff; /* White text color for headings */
  }
  
  .stat-value {
    font-size: 1.5em;
    font-weight: bold;
    color: #ffffff; /* White text color for values */
  }
  </style>