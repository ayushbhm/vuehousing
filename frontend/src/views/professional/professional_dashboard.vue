<template>
  <ProfessionalNavbar/>
    <div>
      <h1>Professional Dashboard</h1>
      <upcoming-services-box /> <!-- Use the upcoming services box component here -->
    </div>

    <accepted-service-request />  
    <closed-services-box /> <!-- Use the closed services box component here -->
    <!-- Use the accepted service request component here -->
   

    
  </template>
  
  <script>
  import ViewProfileBox from '@/components/professional/view_profile_box.vue'; // Import the view profile box component
  import UpcomingServicesBox from '@/components/professional/upcoming_services_box.vue'; // Import the upcoming services box component
  import ClosedServicesBox from '@/components/professional/closed_services_box.vue'; // Import the closed services box component
  import AcceptedServiceRequest from '@/components/professional/accepted_service_request.vue'; // Import the accepted service request
  import Summaryvu from '@/components/professional/summary.vue'; // Import the summary component
  import ProfessionalNavbar from '@/components/professional/navbar.vue'; // Import the navbar component
  export default {
    components: {
      ViewProfileBox, // Register the component
      UpcomingServicesBox, // Register the component
      ClosedServicesBox, // Register the component
      AcceptedServiceRequest, // Register the component
      Summaryvu, // Register the component
      ProfessionalNavbar // Register the component
    }
  };
  </script>
  
  <style scoped>
  /* Add any additional styles for the dashboard here */
  </style>