<template>
  <div class="project-manager">
    <div class="projekct-manager__header">
      <Navbar />
      <h1>Projects</h1>
      <button v-if="$store.state.isAuthenticated" @click="showForm = !showForm">
        Add Project
      </button>
      <label>
        <input type="checkbox" v-model="showOnlyUserProjects"> Show only my projects
      </label>
    </div>

    <form v-if="showForm" @submit.prevent="addProject" class="project-form">
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
      <input v-model="newProject.status" placeholder="Status" required />
<div class="user-list" v-if="users.length > 0">
  <div v-for="user in users" :key="user.id">
    <input type="checkbox" :id="'user_' + user.id" v-model="newProject.team_members" :value="user.id">
    <label :for="'user_' + user.id">{{ user.username }}</label>
  </div>
</div>
<div v-else>No users available.</div>


      <button type="submit">Add Project</button>
    </form>

    <form
      v-if="projectToEdit"
      @submit.prevent="saveProject"
      class="edit-project-form"
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
      <input v-model="newProject.status" placeholder="Status" required />
<div class="user-list" v-if="users.length > 0">
  <div v-for="user in users" :key="user.id">
    <input type="checkbox" :id="'user_' + user.id" v-model="newProject.team_members" :value="user.id">
    <label :for="'user_' + user.id">{{ user.username }}</label>
  </div>
</div>
<div v-else>No users available.</div>



      <button type="submit">Save Project</button>
    </form>

    <div class="project-grid">
      <div v-for="project in filteredProjects" :key="project.id" class="project-item">
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
        <p>Start Date: {{ project.start_date }}</p>
        <p>End Date: {{ project.end_date }}</p>
        <p>Status: {{ project.status }}</p>
        <p>Team Members:</p>
        <ul>
          <li v-for="memberId in project.team_members" :key="memberId">
            {{ getUserUsername(memberId) }}
          </li>
        </ul>
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
      showForm: false,
      projectToEdit: null,
      users: [],
      currentUser: null,
      showOnlyUserProjects: false,
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    this.getProjects();
    document.title = "Projects";
    this.getUsers();
  },
    computed: {
    filteredProjects() {
      if (this.showOnlyUserProjects) {
        return this.Projects.filter(project =>
          project.team_members.includes(this.currentUser.id)
        );
      } else {
        return this.Projects;
      }
    }
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
    getCurrentUser(){
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
      axios
        .post("/api/v1/projects/", this.newProject, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          this.Projects.push(response.data);
          this.newProject = {
            title: "",
            description: "",
            start_date: "",
            end_date: "",
            status: "",
            team_members: [],
          };
          this.showForm = false;
        })
        .catch((error) => {
          console.error("Error creating project:", error);
        });
    },
    editProject(project) {
      this.newProject.title = project.title;
      this.newProject.description = project.description;
      this.newProject.start_date = project.start_date;
      this.newProject.end_date = project.end_date;
      this.newProject.status = project.status;
      this.newProject.team_members = project.team_members;

      this.projectToEdit = project;
    },
    saveProject() {
      this.projectToEdit.title = this.newProject.title;
      this.projectToEdit.description = this.newProject.description;
      this.projectToEdit.start_date = this.newProject.start_date;
      this.projectToEdit.end_date = this.newProject.end_date;
      this.projectToEdit.status = this.newProject.status;
      this.projectToEdit.team_members = this.newProject.team_members;

      axios
        .put(`/api/v1/projects/${this.projectToEdit.id}/`, this.projectToEdit, {
          headers: {
            Authorization: `token ${localStorage.token}`,
          },
        })
        .then((response) => {
          const index = this.Projects.findIndex(
            (project) => project.id === this.projectToEdit.id
          );
          this.Projects[index] = response.data;
          this.projectToEdit = null;
          this.showForm = false;
        })
        .catch((error) => {
          console.error("Error updating Project:", error);
        });
    },
    deleteProject(project) {
      axios
        .delete(`/api/v1/projects/${project.id}/`)
        .then(() => {
          this.Projects = this.Projects.filter((p) => p.id !== project.id);
          console.log("Project deleted successfully");
        })
        .catch((error) => {
          console.error("Error deleting Project:", error);
        });
    },
    getUserUsername(memberId) {
      const user = this.users.find((user) => user.id === memberId);
      return user ? user.username : "Unknown";
    },
  },
};
</script>


<style scoped>
.project-manager {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.project-manager__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-form {
  margin-bottom: 20px;
}

.edit-project-form {
  margin-bottom: 20px;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-gap: 20px;
}

.project-item {
  border: 1px solid #ccc;
  padding: 10px;
}

.project-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.project-item button {
  margin-right: 10px;
}

.project-item h2 {
  margin: 0;
}

.project-item p {
  margin: 5px 0;
}

.user-list {
  max-height: 50px; 
  overflow-y: auto;
  width:25%;
}

</style>