<template>
  <div>
    <nav class="navbar">
      <ul>
        <li><router-link to="/" class="navbar-item">Home</router-link></li>
        <li>
          <router-link to="/projects" class="navbar-item">Projects</router-link>
        </li>
        <li>
          <router-link to="/tasks" class="navbar-item">My tasks</router-link>
        </li>
      </ul>
      <ul class="navbar-right">
        <template v-if="$store.state.isAuthenticated">
          <li @click="showNotifications" class="navbar-item">
            <span
              :class="{
                pulse: hasUnreadNotifications,
                'unread-notifications': hasUnreadNotifications,
              }"
              >Notifications</span
            >
          </li>
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
        <p class="notifications-text">Recent notifications</p>
        <div
          v-for="notification in notifications.slice(0, 3)"
          :key="notification.id"
          :class="{ notification: true, read: notification.read }"
          class="notification"
        >
          {{ notification.message }}
          <router-link
            :to="getNotificationLink(notification)"
            @click="markAsRead(notification)"
          >
            Check
          </router-link>
        </div>
        <router-link to="/notifications" class=""
          ><p class="notifications-text">All Notifications</p></router-link
        >
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
  computed: {
    hasUnreadNotifications() {
      return this.notifications.some((notification) => !notification.read);
    },
  },
  mounted() {
    this.getCurrentUser();
    this.getNotifications();
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
      this.showNotificationBox = !this.showNotificationBox;
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
    getNotifications() {
      axios
        .get("/api/v1/notifications")
        .then((response) => {
          this.notifications = response.data
            .filter((notification) =>
              notification.recipients.includes(this.currentUser.id)
            )
            .reverse();
        })
        .catch((error) => {
          console.error("Error fetching notifications:", error);
        });
    },
    markAsRead(notification) {
      // Check if the notification is unread
      console.log(notification.read);
      console.log(notification.id);
      if (!notification.read) {
        notification.read = true;

        axios
          .patch(`/api/v1/notifications/${notification.id}/`, { read: true })
          .then((response) => {
            console.log("Notification marked as read");
          })
          .catch((error) => {
            console.error("Error marking notification as read:", error);
            notification.read = false;
          });
      }
    },
    getNotificationLink(notification) {
      if (notification.project) {
        return `/projects/${notification.project}`;
      } else if (notification.task) {
        return `/tasks/${notification.task}`;
      }
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
  top: 50px;
  right: 60px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 120px;
}

.notification {
  margin-bottom: 5px;
}

.notification-content {
  padding: 10px;
  text-align: left; /* Center-align all content */
}

.notifications-text {
  margin-top: 0;
  margin-bottom: 10px;
  text-align: center;
}

.notification-badge {
  background-color: red;
  color: white;
  font-size: 12px;
  border-radius: 50%;
  padding: 4px 6px;
  margin-left: 5px;
}

.notification {
  margin-bottom: 5px;
  animation: pulseUnread 2s infinite alternate both;
}

@keyframes pulseUnread {
  from {
    background-color: #fff; /* Initial background color */
  }
  to {
    background-color: #ff6347;
  }
}

.notification.read {
  animation: none;
}

.unread-notifications {
  color: red;
}

.pulse {
  animation: pulseUnreadText 2s infinite alternate both;
}
@keyframes pulseUnreadText {
  from {
    color: white;
  }
  to {
    color: red;
  }
}
</style>
