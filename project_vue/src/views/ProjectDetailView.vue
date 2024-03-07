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
    <input type="date" v-model="newTask.deadline" placeholder="Deadline" required />
<textarea v-model="newTask.status" placeholder="Task status"></textarea>
    <select v-model="newTask.assigned_to" required>
        <option value="" disabled>Select Assigned To</option>
        <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
    </select>

<select v-model="newTask.priority_level" required>
  <option value="" disabled>Select Priority Level</option>
  <option v-for="priorityLevel in priorityLevels" :key="priorityLevel.id" :value="priorityLevel.id">{{ priorityLevel.level }}</option>
</select>

    <button type="submit">{{ isEditing ? 'Save Task' : 'Add Task' }}</button>
</form>


<div class="Task-grid">
    <div v-for="task in filteredTasks" :key="task.id" class="task-item">
        <button v-if="$store.state.isAuthenticated" @click="editTask(task)">Edit</button>
        <button v-if="$store.state.isAuthenticated" @click="deleteTask(task)">Delete</button>
        <h2>{{ task.title }}</h2>
        <p>{{ task.description }}</p>
        <p>Deadline: {{ task.deadline }}</p>
        <p>Project: {{ task.project }}</p>
        <p>Assigned To: {{ task.assigned_to }}</p>
        <p>Priority Level: {{ task.priority_level }}</p>
        <p>Status: {{ task.status }}</p>
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
          project: '', 
          assigned_to: '', 
          priority_level: '', 
          deadline: '', 
          status: '' 
      },
      filteredTasks: [],
      currentUser: null,
      showOnlyUserTasks: false,
      priorityLevels: [],
      Tasks: [],
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
    this.getPriorityLevels();
  },
  computed: {
  filteredTasks() {
    if (this.showOnlyUserTasks) {
      return this.filteredTasks.filter(task =>
        task.team_members.includes(this.currentUser.id)
      );
    } else {
      return this.filteredTasks;
    }
  }
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
    getPriorityLevels(){
        axios
        .get(`/api/v1/priority-levels`)
        .then((response) => {
          this.priorityLevels = response.data;
        })
        .catch((error) => {
          console.log(error);
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
addTask() {
  // Include projectId in the newTask object
  this.newTask.project = this.projectId;

  axios
    .post("/api/v1/tasks/", this.newTask, {
      headers: {
        Authorization: `token ${localStorage.token}`,
      },
    })
    .then((response) => {
      this.Tasks.push(response.data);
      this.resetForm();
    })
    .catch((error) => {
      console.error("Error creating task:", error);
    });
},
    editTask(task) {
      this.isEditing = true;
      this.newTask.title = task.title;
      this.newTask.description = task.description;
      this.newTask.status = task.status;
      this.newTask.team_members = task.team_members;
      this.taskToEdit = task;
      this.showForm = true; // Show the form
    },
    saveTask() {
      axios
        .put(`/api/v1/tasks/${this.taskToEdit.id}/`, this.newTask, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          const index = this.filteredTasks.findIndex(
            (task) => task.id === this.taskToEdit.id
          );
          this.filteredTasks[index] = response.data;
          this.resetForm();
          this.isEditing = false;
        })
        .catch((error) => {
          console.error("Error updating task:", error);
        });
    },
    deleteTask(task) {
      axios
        .delete(`/api/v1/tasks/${task.id}/`)
        .then(() => {
          this.filteredTasks = this.filteredTasks.filter((t) => t.id !== task.id);
          console.log("Task deleted successfully");
        })
        .catch((error) => {
          console.error("Error deleting task:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Add styling as needed */
</style>
