<template>
    <Navbar/>
    <div>
        <h1>Summary</h1>

        <professionalsummary/>
    </div>
</template>

<script>
import Navbar from '@/components/professional/navbar.vue';
import professionalsummary from '@/components/professional/summary.vue';   
export default {
    name: 'ProfessionalSummaryPage',
    components: {
        Navbar,
        professionalsummary,
    }
}
</script>

