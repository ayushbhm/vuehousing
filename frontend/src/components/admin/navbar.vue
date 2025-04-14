<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary w-100"> <!-- Added w-100 for full width -->
    <div class="container-fluid">
      <a class="navbar-brand" href="#">MyApp</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_dashboard">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/search">Search</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/summary">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
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
  width: 100%; 
}
</style>