<template>
  <div class="task-detail-view">
    <div class="task-detail-view__header">
      <Navbar />
      <h1>Task Details</h1>
    </div>

    <div class="task-detail">
      <h2>{{ task.title }}</h2>
      <p>{{ task.description }}</p>
      <p>Deadline: {{ task.deadline }}</p>
      <p>Priority Level: {{ task.priority_level }}</p>
      <p>Status: {{ task.status }}</p>
      <button @click="goToProject(task.project)">View Project</button>
    </div>


    <Footer />
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "TaskDetailView",
  data() {
    return {
      task: {},
      currentUserId: null,
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    const taskId = this.$route.params.taskId;
    this.getTask(taskId);
  },
  methods: {
    getTask(taskId) {
      axios
        .get(`/api/v1/tasks/${taskId}`)
        .then((response) => {
          this.task = response.data;
          document.title = this.task.title;
        })
        .catch((error) => {
          console.error("Error fetching task details:", error);
        //   if (error.response && error.response.status === 404) {
        //     this.$router.push({ name: "notfound" });
        //   }
        });
    },
    goToProject(projectId) {
      this.$router.push({
        name: "ProjectDetailView",
        params: { projectId: projectId },
      });
    },
    getCurrentUser() {
      axios
        .get("/api/v1/users/me", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.currentUserId = response.data.id;
          const taskId = this.$route.params.id; // Assuming the route parameter is named 'id'
          this.getTask(taskId);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.task-detail-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.task-detail-view__header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.task-detail {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
  border: 1px solid #ddd;
}

.task-detail h2 {
  margin-bottom: 10px;
}

.task-detail button {
  padding: 8px 16px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.task-detail button:hover {
  background-color: #0056b3;
}
</style>
