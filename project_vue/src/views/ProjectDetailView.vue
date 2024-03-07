<template>
  <div class="nav">
    <Navbar />
    <div class="project-page" v-if="project">
      <h2>Project: {{ project.title }}</h2>
      <p>{{ project.description }}</p>
      <p>Start Date: {{ project.start_date }}</p>
      <p>End Date: {{ project.end_date }}</p>
      <p>Status: {{ project.status }}</p>
      <p>Team Members:</p>
      <ul>
        <li v-for="memberId in project.team_members" :key="memberId">
          {{ getUserName(memberId) }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Loading project details...</p>
    </div>
    <Footer />
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "ProjectPage",
  props: ["projectId"],
  data() {
    return {
      project: null,
      users: [],
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    this.getProjectDetails(this.projectId);
    this.getUsers();
  },
  methods: {
    getProjectDetails(projectId) {
      axios
        .get(`/api/v1/projects/${projectId}`)
        .then((response) => {
          this.project = response.data;
          document.title = this.project.title;
        })
        .catch((error) => {
          console.error("Error fetching project details:", error);
          if (error.response && error.response.status === 404) {
            // Emit event only if the error is 404
            this.$router.push({ name: 'notfound' });
          }
        });
    },
    getUserName(userId) {
      const user = this.users.find((user) => user.id === userId);
      return user ? user.username : "Unknown";
    },
    getUsers() {
      axios
        .get("/api/v1/users/", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.users = response.data.results;
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Add styling as needed */
</style>
