<template>
<div>
  <nav class="navbar" id="navbar">
    <ul>
      <li><router-link to="/" class="navbar-item">Home</router-link></li>
    </ul>
    <ul class="navbar-right">
      <template v-if="$store.state.isAuthenticated">
        <li @click="logout" class="navbar-item">Logout</li>
      </template>
      <template v-else>
        <li><router-link to="/login" class="navbar-item">Login</router-link></li>
      </template>
    </ul>
  </nav>
  <section>
  <router-view style/>
  </section>

  <footer class="footer">
    <p>test</p>
    </footer>
  </div>
</template>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200&family=Roboto:wght@100&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inconsolata:wght@200;500&family=Nunito:wght@200&family=Roboto:wght@100&display=swap');
#app {
  font-family: 'Inconsolata', monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body{
    background-color: #f8f9fa;
    color: black;
}


.navbar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  color: #fff;
  background-color: black;
  display: flex; 
  justify-content: space-between;

  a {
  color: #fff;
  text-decoration: none;

    &.router-link-exact-active {
      color: #42b983;
    }
  }

  a:hover{
    background-color: #555;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline;
    margin-right: 10px;
  }
  .navbar-right{
    display: flex; 
    align-items: center; 
  }
}

section{
  padding: 50px;
  margin-bottom: 50px;
  min-height: 100vh;
}

.footer {
  position: absolute;
  left: 0;
  right: 0;
  text-align: center;
  color: #fff;
  background-color: black;
}


button {
  padding: 10px 20px;
  background-color: #121212;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: black;
}

</style>
<script>
import axios from 'axios'
export default {
  beforeCreate(){
    this.$store.commit('initializeStore')
    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    }
    else{
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
    methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("userid")

      this.$store.commit('removeToken')

      this.$router.push('/')
    }
  },
  
}
</script>