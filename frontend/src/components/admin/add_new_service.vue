<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="add-new-service" @click.stop>
      <h1>Add New Service</h1>
      <form @submit.prevent="submitService">
        <input type="text" v-model="service.name" placeholder="Service Name" required />
        <input type="number" v-model="service.base_price" placeholder="Base Price" required />
        <input type="number" v-model="service.time_required" placeholder="Time Required (min)" required />
        <textarea v-model="service.description" placeholder="Description"></textarea>
        <button type="submit">Add Service</button>
        <p v-if="message">{{ message }}</p>
      </form>
      
    </div>
  </div>
</template>

<script>
import adminService from '@/services/adminService';

export default {
  data() {
    return {
      service: {
        name: '',
        base_price: null,
        time_required: null,
        description: ''
      },
      message: ''
    };
  },
  methods: {
    async submitService() {
      try {
        await adminService.addService(this.service);
        this.message = 'Service added successfully!';
        this.resetForm();
        this.$emit('service-added'); // Emit event to notify parent
      } catch (error) {
        this.message = 'Error adding service.';
      }
    },
    resetForm() {
      this.service = {
        name: '',
        base_price: null,
        time_required: null,
        description: ''
      };
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

.add-new-service {
  color: #45a049;
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); 
}

h1 {
  text-align: center;
}

input, textarea {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
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