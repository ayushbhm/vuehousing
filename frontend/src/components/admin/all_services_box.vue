<template>
    <div class="service-list">
      <h2>Service List</h2>
      <div class="service-container">
        <div class="service-header">
          <span class="header-item">ID</span> 
          <span class="header-item">Service Name</span>
          <span class="header-item">Base Price</span>
          <span class="header-item">Actions</span>
        </div>
        <div class="service-row" v-for="service in services" :key="service.id">
          <span>{{ service.id }}</span>
          <span>{{ service.name }}</span>
          <span>{{ service.base_price }}</span>
          <span>
            <button @click="openEditModal(service)">View/Edit</button>
            <button @click="deleteService(service.id)">Delete</button>
          </span>
        </div>
      </div>
      <EditServiceModal v-if="isEditModalVisible" :serviceData="selectedService" @close="closeEditModal" @service-updated="fetchServices" />
    </div>
  </template>
  
  <script>
  import adminService from '@/services/adminService';
  import EditServiceModal from '@/components/admin/edit_service_box.vue'; 
  
  export default {
    data() {
      return {
        services: [],
        isEditModalVisible: false,
        selectedService: null // To hold the service being edited
      };
    },
    methods: {
      async fetchServices() {
        try {
          const response = await adminService.getServices();
          this.services = response.data; 
        } catch (error) {
          console.error('Error fetching services:', error);
        }
      },
      openEditModal(service) {
        this.selectedService = service; // Set the selected service
        this.isEditModalVisible = true; // Show the edit modal
      },
      closeEditModal() {
        this.isEditModalVisible = false; // Hide the edit modal
        this.selectedService = null; 
      },
      async deleteService(serviceId) {
        try {
          await adminService.deleteService(serviceId);
          this.fetchServices(); // Refresh the list after deletion
        } catch (error) {
          console.error('Error deleting service:', error);
        }
      }
    },
    mounted() {
      this.fetchServices(); // Fetch services when the component is mounted
    },
    components: {
      EditServiceModal 
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