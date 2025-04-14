<template>
    <div class="profile-box">
      <h2>Professional Profile</h2>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="fullname">Full Name:</label>
          <input type="text" id="fullname" v-model="profile.fullname" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="profile.email" required />
        </div>
        <div class="form-group">
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="profile.phone" required />
        </div>
        <div class="form-group">
          <label for="address">Address:</label>
          <input type="text" id="address" v-model="profile.address" required />
        </div>
        <div class="form-group">
          <label for="pincode">Pincode:</label>
          <input type="text" id="pincode" v-model="profile.pincode" required />
        </div>
        <div class="form-group">
          <label for="experience">Experience:</label>
          <input type="number" id="experience" v-model="profile.experience" required min="0" />
        </div>
        <button type="submit">Update Profile</button>
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      </form>
    </div>
  </template>
  
  <script>
  import professionalService from '@/services/professionalService';
  
  export default {
    data() {
      return {
        profile: {
          fullname: '',
          email: '',
          phone: '',
          address: '',
          pincode: '',
          experience: null,
        },
        errorMessage: '',
      };
    },
    mounted() {
      // Fetch profile details when the component is mounted
      professionalService.getProfileDetails()
        .then(response => {
          this.profile = response.data; // Store the profile data
        })
        .catch(error => {
          console.error('Error fetching profile details:', error);
        });
    },
    methods: {
      updateProfile() {
        // Simple validation
        if (this.profile.phone.length !== 10) {
          this.errorMessage = 'Phone must be 10 digits.';
          return;
        }
        if (this.profile.experience < 0) {
          this.errorMessage = 'Experience cannot be negative.';
          return;
        }
        if (!this.profile.email.includes('@')) {
          this.errorMessage = 'Email must contain "@"';
          return;
        }
  
        // Clear error message and proceed to update
        this.errorMessage = '';
        professionalService.updateProfile(this.profile)
          .then(response => {
            alert('Profile updated successfully!'); // Notify the user
            // Optionally, you can refresh the profile data after updating
            return professionalService.getProfileDetails();
          })
          .then(response => {
            this.profile = response.data; // Update the profile data with the latest from the server
          })
          .catch(error => {
            console.error('Error updating profile:', error);
            this.errorMessage = error.message || 'An error occurred while updating the profile.'; // Show error message
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .profile-box {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #06010b;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .error {
    color: red;
    font-size: 0.9em;
  }
  </style>