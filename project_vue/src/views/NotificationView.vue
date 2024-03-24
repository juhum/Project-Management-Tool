<template>
<div>
    <Navbar />
    <h1>Notifications</h1>
        <div class="notification-box">
      <div class="notification-content">
        <div
          v-for="notification in Notifications"
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
// show only assigned to user notifications
export default {
  name: "NotificationView",
  data() {
    return {
        Notifications: [],
    };
  },
  components: {
    Navbar,
    Footer,
  },
  mounted() {
    this.getNotifications();
  },
  methods: {
      getNotifications() {
      axios
        .get("/api/v1/notifications")
        .then((response) => {
          this.Notifications = response.data;
        })
        .catch((error) => {
          console.error("Error fetching notifications:", error);
        });
    },
  },
}
</script>


<style scoped>

</style>