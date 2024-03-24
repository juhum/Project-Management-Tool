<template>
  <div>
    <nav class="navbar">
      <ul>
        <li><router-link to="/" class="navbar-item">Home</router-link></li>
        <li>
          <router-link to="/projects" class="navbar-item">Projects</router-link>
        </li>
      </ul>
      <ul class="navbar-right">
        <template v-if="$store.state.isAuthenticated">
          <li @click="showNotifications" class="navbar-item">Notifications</li>
          <li @click="logout" class="navbar-item">Logout</li>
        </template>
        <template v-else>
          <li>
            <router-link to="/login" class="navbar-item">Login</router-link>
          </li>
        </template>
      </ul>
    </nav>
    <div v-if="showNotificationBox" class="notification-box">
      <div class="notification-content">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
        >
          {{ notification.message }} <a>Check</a>
        </div>
        <router-link to="/notifications" class="">All Notifications</router-link>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      showNotificationBox: false,
      notifications: [],
    };
  },
  mounted() {
    this.getCurrentUser();
  },
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = "";

      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("userid");

      this.$store.commit("removeToken");

      this.$router.push("/login");
    },
    showNotifications() {
      if (this.showNotificationBox) {
        this.showNotificationBox = false;
        return; 
      }

      axios
        .get("/api/v1/notifications")
        .then((response) => {
          this.notifications = response.data.filter(notification => notification.recipients.includes(this.currentUser.id));
          this.showNotificationBox = true;
        })
        .catch((error) => {
          console.error("Error fetching notifications:", error);
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
  },
};
</script>

<style scoped>
.navbar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  color: #fff;
  background-color: black;
  display: flex;
  justify-content: space-between;
}

.navbar-item {
  color: #fff;
  text-decoration: none;
  cursor: pointer;
}

.navbar-item.router-link-exact-active {
  color: #42b983;
}

.navbar-item:hover {
  background-color: #555;
}

.navbar-right {
  display: flex;
  align-items: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline;
  margin-right: 10px;
}

.notification-box {
  position: absolute;
  top: 50px; /* Adjust based on your navbar height */
  right: 60px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 120px;
}

.notification-content {
  padding: 10px;
}

.notification {
  margin-bottom: 5px;
}
</style>
