<template>
    <div>
        <UserNavbar/>
        <h1>Summary</h1>
        <UserSummary /> <!-- Include the UserSummary component here -->
    </div>
</template>

<script>
import UserSummary from '@/components/user/summary.vue'; // Import the UserSummary component
import UserNavbar from '@/components/user/navbar.vue';
export default {
    name: 'UserSummaryPage',
    components: {
            UserSummary,
            UserNavbar
    }
};
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>