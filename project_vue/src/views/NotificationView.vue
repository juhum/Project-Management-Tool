<template>
<div>
    <Navbar />
    <h1>Notifications</h1>
        <div class="notification-box">
      <div class="notification-content">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
        >
          {{ notification.message }}
        </div>
      </div>
        </div>
    <Footer />
</div>
</template>
<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import axios from "axios";

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
  },
}
</script>

<style scoped>

</style>
