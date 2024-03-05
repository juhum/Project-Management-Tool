<template>
  <div class="project-page" v-if="project">
    <Navbar />
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
    <Footer />
  </div>
  <div v-else>
    <!-- Placeholder or loading message when project data is being fetched -->
    <p>Loading project details...</p>
    <Footer />
  </div>
  
</template>

<script>
import axios from 'axios';
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: 'ProjectPage',
  props: ['projectId'],
  data() {
    return {
      project: null,
      users: []
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
      axios.get(`/api/v1/projects/${projectId}`)
        .then(response => {
          this.project = response.data;
          document.title = this.project.title;
        })
        .catch(error => {
          console.error('Error fetching project details:', error);
        });
    },
    getUserName(userId) {
      const user = this.users.find(user => user.id === userId);
      return user ? user.username : 'Unknown';
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
          console.error('Error fetching users:', error);
        });
    },
  }
};
</script>

<style scoped>
/* Add styling as needed */
</style>
