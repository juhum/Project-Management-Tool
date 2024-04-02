<template>
  <div class="project-manager">
    <div class="project-manager__header">
      <Navbar />
      <h1>Projects</h1>
    </div>
    <!-- <div v-if="Projects"> -->
    <div class="project-manager__actions">
      <button v-if="$store.state.isAuthenticated" @click="cancelProject()">
        {{ showForm ? "Cancel" : "Add Project" }}
      </button>
      <select class="status-filter" v-model="selectedStatus">
        <option value="">All Statuses</option>
        <option v-for="status in statuses" :key="status.id" :value="status.id">
          {{ status.name }}
        </option>
      </select>
      <label>
        <input type="checkbox" v-model="showOnlyUserProjects" /> Enrolled
        Projects Only
      </label>
    </div>

    <form
      v-if="showForm"
      @submit.prevent="isEditing ? saveProject() : addProject()"
      class="project-form"
    >
      <input v-model="newProject.title" placeholder="Project Title" required />
      <textarea
        v-model="newProject.description"
        placeholder="Project Description"
      ></textarea>
      <input
        type="date"
        v-model="newProject.start_date"
        placeholder="Start Date"
        required
      />
      <input
        type="date"
        v-model="newProject.end_date"
        placeholder="End Date"
        required
      />
      <select v-model="newProject.status" required>
        <option value="" disabled selected>Select Status</option>
        <option v-for="status in statuses" :key="status.id" :value="status.id">
          {{ status.name }}
        </option>
      </select>

      <div class="user-list" v-if="users.length > 0">
        <div v-for="user in users" :key="user.id">
          <input
            type="checkbox"
            :id="'user_' + user.id"
            v-model="newProject.team_members"
            :value="user.id"
          />
          <label :for="'user_' + user.id">{{ user.username }}</label>
        </div>
      </div>
      <div v-else>No users available.</div>

      <button type="submit">
        {{ isEditing ? "Save Project" : "Add Project" }}
      </button>
    </form>

    <button @click="toggleChart">
      {{ showChart ? "Hide Chart" : "Show Chart" }}
    </button>
    <div class="chart">
      <PieChart
        v-if="showChart"
        ref="pieChart"
        :showOnlyUserChecker="showOnlyUserProjects"
        :responseData="Projects"
        :currentUserId="currentUser.id"
        :dataField="statuses"
      />
    </div>
    <div class="project-grid">
      <div
        v-for="project in filteredProjects"
        :key="project.id"
        class="project-item"
      >
        <button
          v-if="$store.state.isAuthenticated"
          @click="editProject(project)"
        >
          Edit
        </button>
        <button
          v-if="$store.state.isAuthenticated"
          @click="deleteProject(project)"
        >
          Delete
        </button>
        <h2>{{ project.title }}</h2>
        <p>{{ project.description }}</p>
        <p>Start Date: {{ format_date(project.start_date) }}</p>
        <p>End Date: {{ format_date(project.end_date) }}</p>
        <p>Status: {{ getStatusName(project.status) }}</p>
        <p>Team Members:</p>
        <ul>
          <li v-for="memberId in project.team_members" :key="memberId">
            {{ getUserUsername(memberId) }}
          </li>
        </ul>
        <button
          v-if="$store.state.isAuthenticated"
          @click="viewProjectDetails(project.id)"
        >
          Details
        </button>
      </div>
    </div>
    <!-- </div>
      <div v-else>
        <p>Loading project details...</p>
        <div class="loading"></div>
      </div> -->
    <div v-if="showConfirmation" class="modal-wrapper">
      <div class="modal">
        <p>Are you sure you want to delete this project?</p>
        <div class="modal-buttons">
          <button @click="confirmDelete">Delete</button>
          <button @click="cancelDelete">Cancel</button>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import PieChart from "@/components/Chart";
import { postNotification } from "@/utils/notifications.js";
import moment from "moment";

export default {
  name: "ProjectsView",
  data() {
    return {
      Projects: [],
      newProject: {
        title: "",
        description: "",
        start_date: "",
        end_date: "",
        status: "",
        team_members: [],
      },
      projectToEdit: null,
      users: [],
      currentUser: null,
      showOnlyUserProjects: false,
      showForm: false,
      isEditing: false,
      statuses: [],
      selectedStatus: "",
      showChart: false,
      projectToDelete: null,
      showConfirmation: false,
    };
  },
  components: {
    Navbar,
    Footer,
    PieChart,
  },
  mounted() {
    this.getProjects();
    document.title = "Projects";
    this.getUsers();
    this.getStatuses();
  },
  computed: {
    filteredProjects() {
      if (this.showOnlyUserProjects) {
        return this.Projects.filter(
          (project) =>
            project.team_members.includes(this.currentUser.id) &&
            (this.selectedStatus === "" ||
              project.status === this.selectedStatus)
        );
      } else {
        return this.Projects.filter(
          (project) =>
            this.selectedStatus === "" || project.status === this.selectedStatus
        );
      }
    },
  },
  watch: {
    showOnlyUserProjects(newVal, oldVal) {
      if (newVal !== oldVal && this.showChart) {
        this.$nextTick(() => {
          this.$refs.pieChart.loadData();
        });
      }
    },
  },

  methods: {
    getProjects() {
      axios
        .get("/api/v1/projects/")
        .then((response) => {
          this.Projects = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
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
          this.getCurrentUser();
        })
        .catch((error) => {
          console.log(error);
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
          this.currentUser = response.data;
          this.currentUser.id = response.data.id;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    addProject() {
      if (this.newProject.end_date < this.newProject.start_date) {
        toast.error("End date cannot be earlier than start date.");
        return; // Stop execution if end date is earlier than start date
      }

      axios
        .post("/api/v1/projects/", this.newProject, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.Projects.push(response.data);
          this.resetForm();
          toast.success("Project created successfully!");
          postNotification(
            response.data.id,
            "project",
            response.data.team_members,
            false
          );
          if (this.showChart) {
            this.$refs.pieChart.loadData();
          }
        })
        .catch((error) => {
          console.error("Error creating project:", error);
          toast.error("An error occurred while creating the project.");
        });
    },
    editProject(project) {
      this.isEditing = true;
      this.newProject.title = project.title;
      this.newProject.description = project.description;
      this.newProject.start_date = project.start_date;
      this.newProject.end_date = project.end_date;
      this.newProject.status = project.status;
      this.newProject.team_members = project.team_members;
      this.projectToEdit = project;
      this.showForm = true;
    },
    saveProject() {
      if (this.newProject.end_date < this.newProject.start_date) {
        toast.error("End date cannot be earlier than start date.");
        return; // Stop execution if end date is earlier than start date
      }
      axios
        .put(`/api/v1/projects/${this.projectToEdit.id}/`, this.newProject, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          const index = this.Projects.findIndex(
            (project) => project.id === this.projectToEdit.id
          );
          this.Projects[index] = response.data;
          this.resetForm();
          this.isEditing = false;
          this.showForm = false;
          toast.success("Project saved successfully!");
          postNotification(
            response.data.id,
            "project",
            response.data.team_members,
            true
          );
          if (this.showChart) {
            this.$refs.pieChart.loadData();
          }
        })
        .catch((error) => {
          console.error("Error updating Project:", error);
          toast.error("An error occurred while editing the project.");
        });
    },
    deleteProject(project) {
      this.projectToDelete = project;
      this.showConfirmation = true;
    },

    confirmDelete() {
      if (this.projectToDelete) {
        axios
          .delete(`/api/v1/projects/${this.projectToDelete.id}/`)
          .then(() => {
            this.Projects = this.Projects.filter(
              (p) => p.id !== this.projectToDelete.id
            );
            console.log("Project deleted successfully");
            toast.success("Project deleted successfully!");
          })
          .catch((error) => {
            console.error("Error deleting Project:", error);
            toast.error("An error occurred while deleting the project.");
          })
          .finally(() => {
            this.showConfirmation = false;
            this.projectToDelete = null;
            if (this.showChart) {
              this.$refs.pieChart.refreshData();
            }
          });
      }
    },

    cancelDelete() {
      this.showConfirmation = false;
      this.projectToDelete = null;
    },
    getUserUsername(memberId) {
      const user = this.users.find((user) => user.id === memberId);
      return user ? user.username : "Unknown";
    },
    resetForm() {
      this.newProject = {
        title: "",
        description: "",
        start_date: "",
        end_date: "",
        status: "",
        team_members: [],
      };
      this.projectToEdit = null;
      this.showForm = !this.showForm;
      this.isEditing = false;
    },
    cancelProject() {
      this.resetForm();
    },
    viewProjectDetails(projectId) {
      this.$router.push({
        name: "ProjectDetailView",
        params: { projectId: projectId },
      });
    },
    getStatuses() {
      axios
        .get("/api/v1/statuses/", {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.statuses = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getStatusName(statusId) {
      const status = this.statuses.find((status) => status.id === statusId);
      return status ? status.name : "Unknown";
    },
    toggleChart() {
      this.showChart = !this.showChart;
    },
    format_date(value) {
      if (value) {
        return moment(String(value)).format("DD-MM-YYYY");
      }
    },
  },
};
</script>

<style scoped>
.project-manager {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.project-manager__header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.project-form {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}

.project-form input,
.project-form textarea {
  width: 97%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  resize: vertical;
}
.project-form input[type="date"] {
  resize: none;
}

.project-form button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 3px;
  cursor: pointer;
}

.project-form button:hover {
  background-color: #0056b3;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-gap: 20px;
}

.project-item {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
  border: 1px solid #ddd;
}

.project-item button {
  margin-right: 10px;
}

.project-item h2,
.project-item p {
  margin: 10px 0;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.project-manager__actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.project-manager__actions button {
  margin-right: 20px;
}

.user-list {
  max-height: 80px;
  overflow-y: auto;
  width: 30%;
  padding: 0;
  margin: 0;
}

.user-list > div {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  grid-gap: 5px;
  margin-bottom: 5px;
}

.user-list input[type="checkbox"] {
  margin: 0;
}

.project-form select {
  width: 97%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  resize: vertical;
}

.status-filter {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  resize: vertical;
}

.project-manager__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-manager__actions button {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .project-manager__actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .project-manager__actions button {
    margin-right: 0;
  }
}

@media (min-width: 600px) {
  .chart {
    width: 50%;
  }
}

.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: #fff;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}

.modal p {
  margin-bottom: 10px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
}

.modal-buttons button {
  margin-left: 10px;
}
</style>

