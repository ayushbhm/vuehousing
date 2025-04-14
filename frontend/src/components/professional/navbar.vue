<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary w-100">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">MyApp</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/professional_dashboard">Home</router-link>
          </li>
          
          <li class="nav-item">
            <router-link class="nav-link" to="/professional/summary">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
          </li>
          <li class="nav-item">
            <span class="nav-link" @click="showProfileBox = true">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
              </svg>
            </span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Profile Box Popup -->
    <div v-if="showProfileBox" class="profile-popup" @click.self="showProfileBox = false">
      <view-profile-box @close="showProfileBox = false" />
    </div>
  </nav>
</template>

<script>
import ViewProfileBox from '@/components/professional/view_profile_box.vue';

export default {
  name: 'ProfessionalNavbar',
  components: {
    ViewProfileBox,
  },
  data() {
    return {
      showProfileBox: false, // State to control visibility of the profile box
    };
  },
  methods: {
    logout() {
      console.log('Logging out...');
      localStorage.removeItem('token'); // Clear the token
      this.$router.push('/login'); // Redirect to login page
    },
  },
};
</script>

<style scoped>
.navbar {
  width: 100%; /* Ensure the navbar takes the full width */
}

.nav-link {
  display: flex; /* Use flex to align items */
  align-items: center; /* Center items vertically */
}

/* Profile Box Popup Styles */
.profile-popup {
  position: fixed; /* Fixed position to cover the entire viewport */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  z-index: 1000; /* Ensure it appears above other content */
}

.profile-popup > * {
  background: rgb(48, 12, 12); /* Background color for the profile box */
  padding: 20px; /* Padding around the profile box */
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Optional shadow for depth */
}
</style>