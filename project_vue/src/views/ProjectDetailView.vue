<template>
  <div class="nav">
    <Navbar />
    <div class="project-page" v-if="project">
      <h2>Project: {{ project.title }}</h2>
      <p>{{ project.description }}</p>
      <p>Start Date: {{ format_date(project.start_date) }}</p>
      <p>End Date: {{ format_date(project.end_date) }}</p>
      <p>Status: {{ getStatusName(project.status) }}</p>
      <p>Team Members:</p>
      <ul>
        <li v-for="memberId in project.team_members" :key="memberId">
          {{ getUserName(memberId) }}
        </li>
      </ul>
      <div>
        <h1>Upload Files</h1>
        <input
          type="file"
          ref="fileInput"
          multiple
          @change="handleFileChange"
        />
        <button class="file-btn" @click="uploadFiles">Upload Files</button>
      </div>
      <h1>Files</h1>
      <div v-if="files.length > 0">
        <ul>
          <li v-for="file in files" :key="file.id">
            {{ getFileName(file.file) }}
            <button class="file-btn" @click="downloadFile(file.id, file.file)">
              Download
            </button>
            <button class="file-btn" @click="deleteFile(file.id)">
              Delete
            </button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No files found.</p>
      </div>
      <div>
        <h1>Tasks</h1>
        <!-- <div > v-if="Tasks" -->
        <div class="task-manager__actions">
          <button v-if="$store.state.isAuthenticated" @click="cancelTask()">
            {{ showForm ? "Cancel" : "Add Task" }}
          </button>
          <div class="filter-option">
            <select class="status-filter" v-model="selectedStatus">
              <option value="">All Statuses</option>
              <option
                v-for="status in statuses"
                :key="status.id"
                :value="status.id"
              >
                {{ status.name }}
              </option>
            </select>
          </div>
          <div class="filter-option">
            <select class="priority-filter" v-model="selectedPriorityLevel">
              <option value="">All Priority Levels</option>
              <option
                v-for="priorityLevel in priorityLevels"
                :key="priorityLevel.id"
                :value="priorityLevel.id"
              >
                {{ priorityLevel.level }}
              </option>
            </select>
          </div>
          <div class="filter-option">
            <label>
              <input type="checkbox" v-model="showOnlyUserTasks" /> Enrolled
              Tasks Only
            </label>
          </div>
        </div>

        <form
          v-if="showForm"
          @submit.prevent="isEditing ? saveTask() : addTask()"
          class="task-form"
        >
          <input v-model="newTask.title" placeholder="Task Title" required />
          <textarea
            v-model="newTask.description"
            placeholder="Task Description"
          ></textarea>
          <input
            type="date"
            v-model="newTask.deadline"
            placeholder="Deadline"
            required
          />
          <select v-model="newTask.status" required>
            <option value="" disabled selected hidden>Select Status</option>
            <option
              v-for="status in statuses"
              :key="status.id"
              :value="status.id"
            >
              {{ status.name }}
            </option>
          </select>
          <select v-model="newTask.assigned_to" required>
            <option value="" disabled selected hidden>
              Select Assigned To
            </option>
            <option
              v-for="user in project.team_members"
              :key="user"
              :value="user"
            >
              {{ getUserName(user) }}
            </option>
          </select>

          <select v-model="newTask.priority_level" required>
            <option value="" disabled selected hidden>
              Select Priority Level
            </option>
            <option
              v-for="priorityLevel in priorityLevels"
              :key="priorityLevel.id"
              :value="priorityLevel.id"
            >
              {{ priorityLevel.level }}
            </option>
          </select>

          <button type="submit">
            {{ isEditing ? "Save Task" : "Add Task" }}
          </button>
        </form>
        <button @click="toggleChart">
          {{ showChart ? "Hide Chart" : "Show Chart" }}
        </button>
        <button class="switch-button" v-if="showChart" @click="toggleDataField">
          {{
            dataField === priorityLevels
              ? "Switch to Status"
              : "Switch to Priority Levels"
          }}
        </button>
        <div class="chart">
          <PieChart
            v-if="showChart"
            ref="pieChart"
            :responseData="Tasks"
            :showOnlyUserChecker="showOnlyUserTasks"
            :currentUserId="currentUser.id"
            :dataField="dataField"
          />
        </div>

        <div class="Task-grid">
          <div v-for="task in filteredTasks" :key="task.id" class="task-item">
            <button v-if="$store.state.isAuthenticated" @click="editTask(task)">
              Edit
            </button>
            <button
              v-if="$store.state.isAuthenticated"
              @click="deleteTask(task)"
            >
              Delete
            </button>
            <h2>{{ task.title }}</h2>
            <p>{{ task.description }}</p>
            <p>Deadline: {{ task.deadline }}</p>
            <p>Assigned To: {{ getUserUsername(task.assigned_to) }}</p>
            <p>
              Priority Level: {{ getPriorityLevelName(task.priority_level) }}
            </p>
            <p>Status: {{ getStatusName(task.status) }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showConfirmation" class="modal-wrapper">
      <div class="modal">
        <p>Are you sure you want to delete this task?</p>
        <div class="modal-buttons">
          <button @click="confirmDelete">Delete</button>
          <button @click="cancelDelete">Cancel</button>
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
import PieChart from "@/components/Chart";
import { toast } from "vue3-toastify";
import { postNotification } from "@/utils/notifications.js";
import "vue3-toastify/dist/index.css";
import moment from "moment";

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
        title: "",
        description: "",
        project: "",
        assigned_to: "",
        priority_level: "",
        deadline: "",
        status: "",
      },
      currentUser: null,
      showOnlyUserTasks: false,
      priorityLevels: [],
      Tasks: [],
      files: [],
      statuses: [],
      selectedStatus: "",
      selectedPriorityLevel: "",
      showChart: false,
      dataField: [],
      taskToDelete: null,
      showConfirmation: false,
    };
  },
  components: {
    Navbar,
    Footer,
    PieChart,
  },
  mounted() {
    this.getProjectDetails(this.projectId);
    this.getUsers();
    this.getTasks();
    this.getPriorityLevels();
    this.getFiles(this.projectId);
    this.getStatuses();
  },
  computed: {
    filteredTasks() {
      if (this.showOnlyUserTasks) {
        return this.Tasks.filter(
          (task) =>
            task.assigned_to === this.currentUser.id &&
            (!this.selectedStatus || task.status === this.selectedStatus) &&
            (!this.selectedPriorityLevel ||
              task.priority_level === this.selectedPriorityLevel)
        );
      } else {
        return this.Tasks.filter(
          (task) =>
            (!this.selectedStatus || task.status === this.selectedStatus) &&
            (!this.selectedPriorityLevel ||
              task.priority_level === this.selectedPriorityLevel)
        );
      }
    },
  },
  watch: {
    showOnlyUserTasks(newVal, oldVal) {
      if (newVal !== oldVal && this.showChart) {
        this.$nextTick(() => {
          this.$refs.pieChart.loadData();
        });
      }
    },
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
            this.$router.push({ name: "notfound" });
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
          this.getCurrentUser();
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
    getPriorityLevels() {
      axios
        .get(`/api/v1/priority-levels`)
        .then((response) => {
          this.priorityLevels = response.data;
          this.dataField = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    resetForm() {
      this.newTask = {
        title: "",
        description: "",
        project: "",
        assigned_to: "",
        priority_level: "",
        deadline: "",
        status: "",
      };
      this.taskToEdit = null;
      this.showForm = !this.showForm;
      this.isEditing = false;
    },
    cancelTask() {
      this.resetForm();
    },
    getTasks() {
      axios
        .get(`/api/v1/tasks/?project=${this.projectId}`)
        .then((response) => {
          this.Tasks = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    addTask() {
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
          toast.success("Task created successfully!");
          const convertAssignedToArray = [response.data.assigned_to];
          postNotification(
            response.data.id,
            "task",
            convertAssignedToArray,
            false
          );
          if (this.showChart) {
            this.$refs.pieChart.refreshData();
          }
        })
        .catch((error) => {
          console.error("Error creating task:", error);
          toast.error("An error occurred while creating the task.");
        });
    },
    editTask(task) {
      this.isEditing = true;
      this.newTask.title = task.title;
      this.newTask.description = task.description;
      this.newTask.status = task.status;
      this.newTask.assigned_to = task.assigned_to;
      this.newTask.deadline = task.deadline;
      this.newTask.priority_level = task.priority_level;
      this.newTask.project = task.project;
      this.taskToEdit = task;
      this.showForm = true;
    },
    saveTask() {
      axios
        .put(`/api/v1/tasks/${this.taskToEdit.id}/`, this.newTask, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          const index = this.Tasks.findIndex(
            (task) => task.id === this.taskToEdit.id
          );
          this.Tasks[index] = response.data;
          this.resetForm();
          this.isEditing = false;
          this.showForm = false;
          toast.success("Task saved successfully!");
          const convertAssignedToArray = [response.data.assigned_to];
          postNotification(
            response.data.id,
            "task",
            convertAssignedToArray,
            true
          );
          if (this.showChart) {
            this.$refs.pieChart.loadData();
          }
        })
        .catch((error) => {
          console.error("Error updating task:", error);
          toast.error("An error occurred while editing the task.");
        });
    },
    deleteTask(task) {
      this.taskToDelete = task;
      this.showConfirmation = true;
    },
    confirmDelete() {
      if (this.taskToDelete) {
        axios
          .delete(`/api/v1/tasks/${this.taskToDelete.id}/`)
          .then(() => {
            this.Tasks = this.Tasks.filter(
              (t) => t.id !== this.taskToDelete.id
            );
            console.log("Task deleted successfully");
            toast.success("Task deleted successfully!");
          })
          .catch((error) => {
            console.error("Error deleting Task:", error);
            toast.error("An error occurred while deleting the task.");
          })
          .finally(() => {
            this.showConfirmation = false;
            this.projectToDelete = null;
            if (this.showChart) {
              this.$refs.pieChart.loadData();
            }
          });
      }
    },
    cancelDelete() {
      this.showConfirmation = false;
      this.taskToDelete = null;
    },
    getUserUsername(memberId) {
      const user = this.users.find((user) => user.id === memberId);
      return user ? user.username : "Unknown";
    },
    getPriorityLevelName(priorityLevelId) {
      const level = this.priorityLevels.find(
        (level) => level.id === priorityLevelId
      );
      return level ? level.level : "Unknown";
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
    handleFileChange() {
      this.selectedFiles = this.$refs.fileInput.files;
    },
    uploadFiles() {
      if (!this.selectedFiles || this.selectedFiles.length === 0) {
        toast.error("No files selected for upload");
        return;
      }
      const fileUploadData = new FormData();
      for (let i = 0; i < this.selectedFiles.length; i++) {
        fileUploadData.append("file", this.selectedFiles[i]);
      }
      fileUploadData.append("project", this.projectId);
      fileUploadData.append("uploaded_by", this.currentUser.id);
      const currentTime = new Date();
      fileUploadData.append("uploaded_at", currentTime.toISOString());
      axios
        .post(`/api/v1/projects/${this.projectId}/upload/`, fileUploadData, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          toast.success("Files uploaded successfully!");
          this.getFiles(this.projectId);
          this.selectedFiles = [];
          this.$refs.fileInput.value = "";
        })
        .catch((error) => {
          console.error(error);
          toast.error("An error occurred while uploading files.");
        });
    },
    getFiles(projectId) {
      axios
        .get(`/api/v1/projects/${projectId}/files/`)
        .then((response) => {
          this.files = response.data;
        })
        .catch((error) => {
          console.error("Error fetching files:", error);
        });
    },
    getFileName(filePath) {
      const parts = filePath.split("/");
      return parts[parts.length - 1];
    },
    async downloadFile(fileId, filePath) {
      try {
        const filename = this.getFileName(filePath);
        const response = await axios.get(filePath, {
          responseType: "blob",
        });

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
        toast.success("File downloaded !");
      } catch (error) {
        console.error("Error downloading file:", error);
        toast.error("An error occurred while downloading file.");
      }
    },
    deleteFile(fileId) {
      axios
        .delete(`/api/v1/projects/${this.projectId}/files/${fileId}/`)
        .then(() => {
          this.files = this.files.filter((f) => f.id !== fileId);
          console.log("File deleted successfully");
          toast.success("File deleted successfully!");
        })
        .catch((error) => {
          console.error("Error deleting file:", error);
          toast.error("An error occurred while deleting the file.");
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
    toggleDataField() {
      if (this.dataField === this.priorityLevels) {
        this.dataField = this.statuses;
      } else {
        this.dataField = this.priorityLevels;
      }
      if (this.showChart) {
        this.$nextTick(() => {
          this.$refs.pieChart.loadData();
        });
      }
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
.project-page {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}

.project-page h2,
.project-page p {
  margin: 10px 0;
}

.project-page ul {
  margin-top: 5px;
  padding-left: 20px;
}

.project-page .task-manager__actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-page .task-manager__actions button {
  margin-right: 20px;
}

.task-form {
  background-color: #f8f9fa;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
}

.task-form input,
.task-form textarea,
.task-form select {
  width: 97%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  resize: vertical;
}

.task-form input[type="date"] {
  resize: none;
}

.task-form button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 3px;
  cursor: pointer;
}

.task-form button:hover {
  background-color: #0056b3;
}

.Task-grid {
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

.task-item button {
  margin-right: 10px;
}

.task-item h2,
.task-item p {
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

.file-btn {
  margin: 10px;
}

.status-filter,
.priority-filter {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  resize: vertical;
}

.switch-button {
  margin-left: 10px;
}

@media (max-width: 414px) {
  .project-page {
    width: calc(100% - 10px);
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 768px) {
  .project-page .task-manager__actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .project-page .task-manager__actions button {
    margin-top: 10px;
  }
  button {
    margin-bottom: 5px;
  }
}

@media (min-width: 700px) {
  .chart {
    width: 50%;
  }
}

@media (min-width: 1000px) {
  .chart {
    width: 25%;
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
