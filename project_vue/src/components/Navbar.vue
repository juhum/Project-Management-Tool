<template>
  <nav class="navbar">
    <ul>
      <li><router-link to="/" class="navbar-item">Home</router-link></li>
     <li><router-link to="/projects" class="navbar-item">Projects</router-link></li>
     <li><router-link to="/projects" class="navbar-item">Calendar</router-link></li>
    </ul>
    <ul class="navbar-right">
      <template v-if="$store.state.isAuthenticated">
                <li @click="logout" class="navbar-item">Notifications</li>
        <li @click="logout" class="navbar-item">Logout</li>
      </template>
      <template v-else>
        <li><router-link to="/login" class="navbar-item">Login</router-link></li>
      </template>
    </ul>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = "";

      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("userid");

      this.$store.commit('removeToken');

      this.$router.push('/login');
    }
  }
}
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
</style>
