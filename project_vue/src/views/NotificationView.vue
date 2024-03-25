<template>
  <div class="notification-view">
    <Navbar />
    <h1>Notifications</h1>
    <div class="notification-box">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="{ notification: true, unread: !notification.read }"
      >
        <router-link
          class="notification-link"
          :to="getNotificationLink(notification)"
          @click="markAsRead(notification)"
        >
          <div class="notification-content">
            {{ notification.message }}
          </div>
        </router-link>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import axios from "axios";
// different color background for not readen notification, clicking on notification redirects to project and makes the notification read
export default {
  name: "NotificationView",
  data() {
    return {
      notifications: [],
      currentUser: null,
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
          this.getNotifications();
        })
        .catch((error) => {
          console.log(error);
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
.notification-view {
  padding: 20px;
}

.notification-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}

.notification {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f0f0f0;
  color: black;
}
.notification-link {
  text-decoration: none;
  color: inherit;
}
.unread {
  background-color: #ff6961; 
}

.notification:hover {
  background-color: #e0e0e0;
}

.unread:hover {
  background-color: #ff6347; 
}


</style>
