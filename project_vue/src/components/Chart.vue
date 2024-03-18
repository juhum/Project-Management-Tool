<template>
  <Pie v-if="loaded" :data="chartData" />
</template>

<script>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import axios from 'axios'

ChartJS.register(ArcElement, Tooltip, Legend)
// add colors,
export default {
  name: 'PieChart',
  components: { Pie },
  data() {
    return {
      loaded: false,
      chartData: null,
      statuses: []
    }
  },
  async mounted() {
    try {
      await this.loadData();
    } catch (error) {
      console.error(error)
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get('/api/v1/projects')
        const projectData = response.data
        
        const projectTitles = projectData.map(project => project.title)
        const projectStatuses = projectData.map(project => project.status)

        await this.getStatuses()

        const statusNames = projectStatuses.map(statusId => this.getStatusName(statusId))

        const statusCounts = this.countStatuses(statusNames)

        this.chartData = {
          labels: Object.keys(statusCounts),
          datasets: [{ data: Object.values(statusCounts), label: 'Project Status' }]
        }

        this.loaded = true
      } catch (error) {
        console.error(error)
      }
    },
    async getStatuses() {
      try {
        const response = await axios.get("/api/v1/statuses/", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        this.statuses = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    getStatusName(statusId) {
      const status = this.statuses.find(status => status.id === statusId);
      return status ? status.name : "Unknown";
    },
    countStatuses(statuses) {
      return statuses.reduce((acc, status) => {
        acc[status] = (acc[status] || 0) + 1;
        return acc;
      }, {});
    },
    async refreshData() {
      try {
        await this.loadData();
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>
