<template>
  <div class="task-list-view">
    <div class="task-list-view__header">
      <Navbar />
      <h1>My Tasks</h1>
    </div>

    <div class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task-item">
        <h2>{{ task.title }}</h2>
        <p>{{ task.description }}</p>
        <p>Deadline: {{ task.deadline }}</p>
        <p>Priority Level: {{ task.priority_level }}</p>
        <p>Status: {{ task.status }}</p>
        <button @click="goToProject(task.project)">View Project</button>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "TaskListView",
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
    this.getCurrentUser();
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
          this.getTasks();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.task-list-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.task-list-view__header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.task-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-gap: 20px;
}

.task-item {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
  border: 1px solid #ddd;
}

.task-item h2 {
  margin-bottom: 10px;
}

.task-item button {
  padding: 8px 16px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.task-item button:hover {
  background-color: #0056b3;
}
</style>
