<template>
  <div class="dashboard-container">
    <Navbar />
    <h1 class="dashboard-title">Dashboard</h1>
    <h3 v-if="currentUser" class="welcome-message">Welcome {{ currentUser.username }}</h3>

    <Footer />
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "HomeView",
  data() {
    return {
      currentUser: null,
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    this.getCurrentUser();
    document.title = "Home";
  },
  methods: {
    getCurrentUser() {
      axios
        .get("/api/v1/users/me", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.currentUser = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-title {
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

.welcome-message {
  color: #666;
  font-size: 1.2rem;
}
</style>
