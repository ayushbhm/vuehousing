<template>
    <Navbar/>
    <div>
        <h1>Summary</h1>

        <adminsummary/>
    </div>
</template>

<script>
import Navbar from '@/components/admin/navbar.vue';
import adminsummary from '@/components/admin/summary.vue';   
export default {
    name: 'SummaryPage',
    components: {
        Navbar,
        adminsummary,
    }
}
</script>

