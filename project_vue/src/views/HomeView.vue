<template>
  <div class="home">
    <Navbar />
    <h1>Dashboard</h1>
    <p>Your recent tasks</p>
    <Footer />
  </div>
</template>


<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import priorityLevelUtil from "@/utils/notifications.js";

export default {
  name: "HomeView",
  data() {
    return {
      tasks: [],
      currentUserId: null,
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    document.title = "Home";
  },
  methods: {
    getTasks() {
      axios
        .get(`/api/v1/tasks`, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.tasks = response.data.filter(
            (task) => task.assigned_to === this.currentUserId
          );
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
