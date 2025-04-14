<template>
  <div class="service-list">
    <h2>All Professionals</h2>
    <div class="service-container">
      <div class="service-header">
        <span class="header-item">ID</span>
        <span class="header-item">Professional Name</span>
        <span class="header-item">Experience</span>
        <span class="header-item">Service Type</span>
        <span class="header-item">Actions</span>
      </div>
      <div class="service-row" v-for="professional in professionals" :key="professional.id">
        <span>{{ professional.id }}</span>
        <span>{{ professional.fullname }}</span>
        <span>{{ professional.experience }}</span>
        <span>{{ professional.service_type }}</span>
        <span>
          <button @click="openViewModal(professional)">View/Edit</button>
          <button @click="delete_professional_entry(professional.id)">Delete</button>
        </span>
      </div>
    </div>
    <view-professional-detail-box v-if="isViewModalVisible" :professional="selectedProfessional" @close="closeViewModal" />
  </div>
</template>

<script>
import adminService from '@/services/adminService';
import viewProfessionalDetailBox from '@/components/admin/view_professional_detail_box.vue'; // Import the new component

export default {
  data() {
    return {
      professionals: [],
      isViewModalVisible: false,
      selectedProfessional: null // To hold the selected professional's details
    };
  },
  methods: {
    async get_all_professionals() {
      try {
        const response = await adminService.get_all_professionals();
        this.professionals = response.data; // Assuming the response data is an array of professionals
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    },
    openViewModal(professional) {
      this.selectedProfessional = professional; // Set the selected professional
      this.isViewModalVisible = true; // Show the view modal
    },
    closeViewModal() {
      this.isViewModalVisible = false; // Hide the view modal
      this.selectedProfessional = null; // Clear the selected professional
    },
    async delete_professional_entry(professional_id) {
      try {
        await adminService.delete_professional_entry(professional_id);
        this.get_all_professionals(); 
      } catch (error) {
        console.error('Error deleting professional:', error);
      }
    }
  },
  mounted() {
    this.get_all_professionals(); 
  },
  components: {
    viewProfessionalDetailBox 
  }
};
</script>

<style scoped>
/* Existing styles remain unchanged */
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
  padding: 10px; 
  margin-right: 15px; 
}

.header-item:last-child {
  margin-right: 0; 
}
</style>