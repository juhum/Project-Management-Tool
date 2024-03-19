<template>
  <Pie v-if="loaded" :data="chartData" />
</template>

<script>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import axios from "axios";
// way to integrate chart with projectdetailview, reduce similiar code, components? , button to show hide chart
ChartJS.register(ArcElement, Tooltip, Legend);
export default {
  name: "PieChart",
  components: { Pie },
  data() {
    return {
      loaded: false,
      chartData: null,
      statuses: [],
      currentUser: null,
            statusColors: {
        "New": "#FF6384",
        "Open": "#36A2EB",
        "In Progress": "#FFCE56",
        "Completed": "#4BC0C0",
        "On Hold": "#9966FF",
        "Cancelled": "#FF9F40"
      }
    };
  },
  props: {
    showOnlyUserProjects: {
      type: Boolean,
      default: false,
    },
  },
  async mounted() {
    try {
      await this.loadData();
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get("/api/v1/projects");
        let projectData = response.data;
        this.getCurrentUser()

        if (this.showOnlyUserProjects) {
          projectData = projectData.filter((project) =>
            project.team_members.includes(this.currentUser.id)
          );
        }

        const projectTitles = projectData.map((project) => project.title);
        const projectStatuses = projectData.map((project) => project.status);

        await this.getStatuses();

        const statusNames = projectStatuses.map((statusId) =>
          this.getStatusName(statusId)
        );

        const statusCounts = this.countStatuses(statusNames);

        this.chartData = {
          labels: Object.keys(statusCounts),
          datasets: [
            { data: Object.values(statusCounts), backgroundColor: Object.keys(statusCounts).map(status => this.statusColors[status]), label: "Projects Number" },
          ],
        };

        this.loaded = true;
      } catch (error) {
        console.error(error);
      }
    },
    async getStatuses() {
      try {
        const response = await axios.get("/api/v1/statuses/", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        });
        this.statuses = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    getStatusName(statusId) {
      const status = this.statuses.find((status) => status.id === statusId);
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
    },
        getCurrentUser() {
      axios
        .get("/api/v1/users/me", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.currentUser = response.data;
          this.currentUser.id = response.data.id;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
