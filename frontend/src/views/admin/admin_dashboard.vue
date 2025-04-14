<template>
  <div class="dashboard-container" @click="handleClick">
    <Navbar />
    <h1>Admin Dashboard</h1>
    <button class="add-service-btn" @click="showModal">Add New Service</button>
    
    <!-- Include the AddNewServiceModal -->
    <AddNewServiceModal v-if="isModalVisible" @close="closeModal" @service-added="showSuccessPopup" />

    <!-- Include the Service List Component -->
    <AllServicesBox /> <!-- Ensure this component is registered and included -->
    <br>
    <br>
     <all_professional_box/>
    <div v-if="isSuccessPopupVisible" class="success-popup" ref="successPopup">
      <p>Service added successfully!</p>
      <button @click="closeSuccessPopup">Close</button>
    </div>
  </div>
  <br>
  <br>
  <all_service_request_box/>

  <button class="export-btn" @click="triggerExport">Export All Service Requests</button>

</template>

<script>
import axios from 'axios';
import Navbar from '@/components/admin/navbar.vue';
import AddNewServiceModal from '@/components/admin/add_new_service.vue'; // Import the AddNewServiceModal
import AllServicesBox from '@/components/admin/all_services_box.vue'; // Import the AllServicesBox component
import all_professional_box from '@/components/admin/all_professional_box.vue';
import all_service_request_box from '@/components/admin/all_service_request_box.vue';
import adminsummary from '@/components/admin/summary.vue';
import services_widget from '@/components/user/services_widget.vue';

export default {
  name: 'AdminDashboard',
  components: {
    Navbar,
    AddNewServiceModal,
    AllServicesBox, // Register the AllServicesBox component
    all_professional_box,
    all_service_request_box,
    adminsummary,
    services_widget
  },
  data() {
    return {
      isModalVisible: false,
      isSuccessPopupVisible: false
    };
  },
  methods: {
    showModal() {
      this.isModalVisible = true; // Show the add service modal
    },
    closeModal() {
      this.isModalVisible = false; // Hide the add service modal
    },
    showSuccessPopup() {
      this.isModalVisible = false; // Close the add service modal
      this.isSuccessPopupVisible = true; // Show success popup
    },
    closeSuccessPopup() {
      this.isSuccessPopupVisible = false; // Hide success popup
    },
    handleClick(event) {
      // Check if the click is outside the success popup
      if (this.isSuccessPopupVisible && !this.$refs.successPopup.contains(event.target)) {
        this.closeSuccessPopup(); // Close the popup if clicked outside
      }
    },
    async triggerExport() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/admin/trigger_export_all');
        alert('Export job triggered successfully. Task ID: ' + response.data.task_id);
      } catch (error) {
        alert('Failed to trigger export job: ' + error.message);
      }
    }
  }
};
</script>

<style scoped>
.add-service-btn {
  margin: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-service-btn:hover {
  background-color: #45a049;
}

.success-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
</style>