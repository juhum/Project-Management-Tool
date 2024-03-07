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
      <div>
        <h1>Tasks</h1>
        <!-- <div > v-if="Tasks" -->
      <div class="task-manager__actions">
      <button v-if="$store.state.isAuthenticated" @click="cancelTask()">
        {{ showForm ? 'Cancel' : 'Add Task' }}
      </button>
      <label>
        <input type="checkbox" v-model="showOnlyUserTasks"> Enrolled Tasks Only
      </label>
    </div>

    <form v-if="showForm" @submit.prevent="isEditing ? saveTask() : addTask()" class="task-form">
    <input v-model="newTask.title" placeholder="Task Title" required />
    <textarea v-model="newTask.description" placeholder="Task Description"></textarea>
    <input v-model="newTask.status" placeholder="Status" required />
    <div class="user-list" v-if="users.length > 0">
        <div v-for="user in users" :key="user.id">
            <input type="checkbox" :id="'user_' + user.id" v-model="newTask.team_members" :value="user.id">
            <label :for="'user_' + user.id">{{ user.username }}</label>
        </div>
    </div>
    <div v-else>No users available.</div>

    <button type="submit">{{ isEditing ? 'Save Task' : 'Add Task' }}</button>
</form>

<div class="Task-grid">
    <div v-for="task in filteredTasks" :key="task.id" class="task-item">
        <button v-if="$store.state.isAuthenticated" @click="editTask(task)">Edit</button>
        <button v-if="$store.state.isAuthenticated" @click="deleteTask(task)">Delete</button>
        <h2>{{ task.title }}</h2>
        <p>{{ task.description }}</p>
        <p>Status: {{ task.status }}</p>
        <p>Assigned to: {{ task.assigned_to.username }}</p>
        <p>Priority: {{ task.priority_level }}</p>
        <p>Deadline: {{ task.deadline }}</p>
    </div>
    </div>
      </div>
      </div>
    <!-- </div>
    <div v-else>
      <p>Loading project details...</p>
      <div class="loading"></div>
    </div> -->
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
      showForm: false,
      isEditing: false,
      newTask: {
          title: '',
          description: '',
          status: '',
          team_members: []
        },
      filteredTasks: [],
      currentUser: null,
      showOnlyUserTasks: false,
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    this.getProjectDetails(this.projectId);
    this.getUsers();
    this.getTasks();
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
      resetForm() {
      this.newTask = {
          title: '',
          description: '',
          status: '',
          team_members: []
      };
      this.taskToEdit = null;
      this.showForm = !this.showForm 
      this.isEditing = false;
    },
    cancelTask() {
      this.resetForm();
    },
    getTasks() {
      axios
        .get(`/api/v1/tasks/?project=${this.projectId}`)
        .then((response) => {
          this.filteredTasks = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

  },
};
</script>

<style scoped>
/* Add styling as needed */
</style>
