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
              'active-route': currentRouteName === 'notifications'
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
          <router-link class="notification-link"
            :to="getNotificationLink(notification)"
            @click="markAsRead(notification)"
          >
            {{ notification.message }}
          </router-link>
        </div>
        <router-link to="/notifications" class="notification-all"
          ><p class="notification-all">All Notifications</p></router-link
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
    currentRouteName() {
        return this.$route.name;
    }
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
  border-radius: 4px;
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
  right: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 120px;
}

.notification {
  margin-bottom: 5px;
  background: #f0f0f0;
  padding: 5px;
}

.notification-content {
  padding: 10px;
  text-align: left;
}

.notifications-text {
  margin-top: 0;
  margin-bottom: 10px;
  text-align: center;
}

.notification {
  margin-bottom: 5px;
  animation: pulseUnread 2s infinite alternate both;
}

@keyframes pulseUnread {
  from {
    background-color: #f0f0f0;
  }
  to {
    background-color: #ff6961;
  }
}

.notification.read {
  animation: none;
}

.unread-notifications {
  color: #ff6961;
}

.pulse {
  animation: pulseUnreadText 2s infinite alternate both;
}
@keyframes pulseUnreadText {
  from {
    color: white;
  }
  to {
    color: #ff6961;
  }
}

.notification-link, .notification-all {
  text-decoration: none;
  color: inherit;
}

.notification-all{
  text-align: center;
  bottom: 0;
  margin: 0;
  margin-top: 15px;
}

.notification:hover {
  background-color: #e0e0e0;
}

.notification-all:hover{
  background-color: #e0e0e0;
}

.active-route{
  color:#42b983;
}
</style>
