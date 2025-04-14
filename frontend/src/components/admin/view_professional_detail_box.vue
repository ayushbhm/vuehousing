<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="view-professional" @click.stop>
      <h1>Professional Details</h1>
      <div class="detail-item">
        <strong>ID:</strong> <span>{{ professional.id }}</span>
      </div>
      <div class="detail-item">
        <strong>Full Name:</strong> <span>{{ professional.fullname }}</span>
      </div>
      <div class="detail-item">
        <strong>Email:</strong> <span>{{ professional.email }}</span>
      </div>
      <div class="detail-item">
        <strong>Phone:</strong> <span>{{ professional.phone }}</span>
      </div>
      <div class="detail-item">
        <strong>Address:</strong> <span>{{ professional.address }}</span>
      </div>
      <div class="detail-item">
        <strong>Pincode:</strong> <span>{{ professional.pincode }}</span>
      </div>
      <div class="detail-item">
        <strong>Service Type:</strong> <span>{{ professional.service_type }}</span>
      </div>
      <div class="detail-item">
        <strong>Experience:</strong> <span>{{ professional.experience }}</span>
      </div>
      <div class="detail-item">
        <strong>Verified:</strong> <span>{{ professional.is_verified ? 'Yes' : 'No' }}</span>
        <button @click="toggleVerification">{{ professional.is_verified ? 'Unverify' : 'Verify' }}</button>
      </div>
      <div class="detail-item">
        <strong>Blocked:</strong> <span>{{ professional.is_blocked ? 'Yes' : 'No' }}</span>
        <button @click="toggleBlock">{{ professional.is_blocked ? 'Unblock' : 'Block' }}</button> <!-- Block/Unblock button -->
      </div>
      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import adminService from '@/services/adminService';

export default {
  props: {
    professional: {
      type: Object,
      required: true
    }
  },
  methods: {
    async toggleVerification() {
      try {
        await adminService.toggle_professional_verification(this.professional.id);
        // Toggle the local state
        this.professional.is_verified = !this.professional.is_verified;
      } catch (error) {
        console.error('Error toggling verification:', error);
      }
    },
    async toggleBlock() {
      try {
        // Call the block/unblock API using the correct method
        await adminService.block_professional(this.professional.id); 
        // Toggle the local state
        this.professional.is_blocked = !this.professional.is_blocked;
      } catch (error) {
        console.error('Error toggling block status:', error);
      }
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.view-professional {
  color: #45a049;
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
}

.detail-item {
  margin: 10px 0;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>