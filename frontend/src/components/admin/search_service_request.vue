<template>
    <div class="search-container">
      <h2>Search</h2>
      <div class="search-bar">
        <select v-model="searchCategory" @change="resetSearch">
          <option value="service_requests">Service Requests</option>
          <option value="professionals">Professionals</option>
          <option value="customers">Customers</option>
        </select>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Enter search term..."
          @input="filterResults"
        />
      </div>
      <div class="results-list">
        <div v-if="searchCategory === 'service_requests'">
          <div class="service-header">
            <span class="header-item">ID</span>
            <span class="header-item">Assigned Professional</span>
            <span class="header-item">Requested Date</span>
            <span class="header-item">Status</span>
          </div>
          <div class="service-row" v-for="request in filteredServiceRequests" :key="request.id">
            <span>{{ request.id }}</span>
            <span>{{ request.professional_name || 'Unassigned' }}</span>
            <span>{{ request.date_of_request }}</span>
            <span>{{ request.service_status }}</span>
          </div>
        </div>
  
        <div v-if="searchCategory === 'professionals'">
          <div class="professional-header">
            <span class="header-item">ID</span>
            <span class="header-item">Name</span>
            <span class="header-item">Email</span>
            <span class="header-item">Blocked</span>
            <span class="header-item">Verified</span> <!-- New column for verification status -->
            <span class="header-item">Actions</span>
          </div>
          <div class="professional-row" v-for="professional in filteredProfessionals" :key="professional.id">
            <span>{{ professional.id }}</span>
            <span>{{ professional.fullname }}</span>
            <span>{{ professional.email }}</span>
            <span>{{ professional.is_blocked ? 'Yes' : 'No' }}</span>
            <span>{{ professional.is_verified ? 'Yes' : 'No' }}</span> <!-- Show verification status -->
            <span>
              <button @click="openViewModal(professional)">View/Edit</button>
              <button @click="deleteProfessional(professional.id)">Delete</button>
            </span>
          </div>
        </div>
  
        <div v-if="searchCategory === 'customers'">
          <div class="customer-header">
            <span class="header-item">ID</span>
            <span class="header-item">Name</span>
            <span class="header-item">Email</span>
          </div>
          <div class="customer-row" v-for="customer in filteredCustomers" :key="customer.id">
            <span>{{ customer.id }}</span>
            <span>{{ customer.fullname }}</span>
            <span>{{ customer.email }}</span>
          </div>
        </div>
      </div>
  
      <!-- Modal for viewing professional details -->
      <view-professional-detail-box v-if="isViewModalVisible" :professional="selectedProfessional" @close="closeViewModal" />
    </div>
  </template>
  
  <script>
  import adminService from '@/services/adminService';
  import viewProfessionalDetailBox from '@/components/admin/view_professional_detail_box.vue';
  
  export default {
    data() {
      return {
        searchCategory: 'service_requests', // Default category
        searchQuery: '',
        serviceRequests: [],
        professionals: [],
        customers: [],
        isViewModalVisible: false,
        selectedProfessional: null, // To hold the selected professional's details
      };
    },
    computed: {
      filteredServiceRequests() {
        return this.serviceRequests.filter(request => {
          return (
            request.id.toString().includes(this.searchQuery) ||
            request.service_status.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            (request.professional_name || '').toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        });
      },
      filteredProfessionals() {
        return this.professionals.filter(professional => {
          return (
            professional.id.toString().includes(this.searchQuery) ||
            professional.fullname.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            professional.email.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        });
      },
      filteredCustomers() {
        return this.customers.filter(customer => {
          return (
            customer.id.toString().includes(this.searchQuery) ||
            customer.fullname.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            customer.email.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        });
      },
    },
    methods: {
      async fetchData() {
        try {
          const serviceRequestsResponse = await adminService.all_service_requests();
          this.serviceRequests = serviceRequestsResponse.data;
  
          const professionalsResponse = await adminService.get_all_professionals();
          this.professionals = professionalsResponse.data;
  
          const customersResponse = await adminService.get_all_customers();
          this.customers = customersResponse.data;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      resetSearch() {
        this.searchQuery = ''; // Reset search query when category changes
      },
      filterResults() {
        // This method is called when the search query changes
        // It will automatically filter the results based on the selected category
      },
      openViewModal(item) {
        this.selectedProfessional = item; // Set the selected professional
        this.isViewModalVisible = true; // Show the view modal
      },
      closeViewModal() {
        this.isViewModalVisible = false; // Hide the view modal
        this.selectedProfessional = null; // Clear the selected professional
      },
      async deleteProfessional(id) {
        try {
          await adminService.delete_professional_entry(id); // Call the delete API
          this.fetchData(); // Refresh the data after deletion
        } catch (error) {
          console.error('Error deleting professional:', error);
        }
      },
    },
    mounted() {
      this.fetchData(); // Fetch all data when the component is mounted
    },
    components: {
      viewProfessionalDetailBox, // Register the new component
    },
  };
  </script>
  
  <style scoped>
  .search-container {
    margin: 20px;
  }
  
  .search-bar {
    display: flex;
    margin-bottom: 20px;
  }
  
  input {
    flex: 1;
    padding: 10px;
    margin-right: 10px;
  }
  
  select {
    padding: 10px;
  }
  
  .results-list {
    max-height: 400px;
    overflow-y: auto;
  }
  
  .service-header,
  .professional-header,
  .customer-header {
    display: flex;
    font-weight: bold;
    border-bottom: 1px solid #ccc;
    padding: 10px 0;
  }
  
  .service-row,
  .professional-row,
  .customer-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #eee;
  }
  
  .service-row span,
  .professional-row span,
  .customer-row span {
    flex: 1;
  }
  
  button {
    margin-left: 5px;
    padding: 5px 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
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