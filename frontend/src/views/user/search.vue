<template>
    <div>
      <UserNavbar />
      
      <search_customer_services />
    </div>
  </template>
  
  <script>
  import UserNavbar from '@/components/user/navbar.vue';
  import search_customer_services from '@/components/user/search_services.vue';
  
  export default {
    name: 'UserSearchPage',
    components: {
      UserNavbar,
      search_customer_services,
    },
  };
  </script>