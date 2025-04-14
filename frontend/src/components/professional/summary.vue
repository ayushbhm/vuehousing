<template>
  <div class="summary">
    <h2>Professional Summary</h2>
    <div class="stats">
      <div class="stat-item">
        <h3>Total Requests Received</h3>
        <div class="stat-value">{{ totalRequestsReceived }}</div>
      </div>
      <div class="stat-item">
        <h3>Total Closed Requests</h3>
        <div class="stat-value">{{ totalClosedRequests }}</div>
      </div>
      <div class="stat-item">
        <h3>Total Rejected Requests</h3>
        <div class="stat-value">{{ totalRejectedRequests }}</div>
      </div>
      <div class="stat-item">
        <h3>Requests This Month</h3>
        <div class="stat-value">{{ requestsThisMonth }}</div>
      </div>
      <div class="stat-item">
        <h3>Closed Requests This Month</h3>
        <div class="stat-value">{{ closedRequestsThisMonth }}</div>
      </div>
      <div class="stat-item">
        <h3>Rejected Requests This Month</h3>
        <div class="stat-value">{{ rejectedRequestsThisMonth }}</div>
      </div>
      <div class="stat-item">
        <h3>Total Remarks Given</h3>
        <div class="stat-value">{{ totalRemarksGiven }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import professionalService from '@/services/professionalService';

export default {
  data() {
    return {
      totalRequestsReceived: 0,
      totalClosedRequests: 0,
      totalRejectedRequests: 0,
      requestsThisMonth: 0,
      closedRequestsThisMonth: 0,
      rejectedRequestsThisMonth: 0,
      totalRemarksGiven: 0,
    };
  },
  async mounted() {
    await this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const stats = await professionalService.fetchProfessionalStats();
        this.totalRequestsReceived = stats.total_requests_received || 0;
        this.totalClosedRequests = stats.total_closed_requests || 0;
        this.totalRejectedRequests = stats.total_rejected_requests || 0;
        this.requestsThisMonth = stats.requests_this_month || 0;
        this.closedRequestsThisMonth = stats.closed_requests_this_month || 0;
        this.rejectedRequestsThisMonth = stats.rejected_requests_this_month || 0;
        this.totalRemarksGiven = stats.total_remarks_given || 0;
      } catch (error) {
        console.error('Error fetching professional stats:', error);
      }
    }
  }
};
</script>

<style scoped>
.summary {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background-color: #270c2e; /* Light background for the summary */
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stats {
  display: flex;
  flex-wrap: wrap; /* Allow items to wrap to the next line */
  justify-content: space-between; /* Space out items */
}

.stat-item {
  flex: 1 1 calc(30% - 20px); /* Responsive width */
  margin: 10px; /* Space between items */
  padding: 20px;
  background-color: #4CAF50; /* Green background for each stat item */
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s; /* Smooth transition */
}

.stat-item:hover {
  transform: translateY(-5px); /* Lift effect on hover */
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2); /* Increase shadow on hover */
}

.stat-item h3 {
  margin: 0;
  font-size: 1.2em;
  color: #ffffff; /* White text color for headings */
}

.stat-value {
  font-size: 1.5em;
  font-weight: bold;
  color: #ffffff; /* White text color for values */
}
</style>
