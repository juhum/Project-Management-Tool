<template>
<div>
  <section>
  <router-view style/>
  </section>
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


section{
  padding: 50px;
  margin-bottom: 50px;
  // min-height: 100vh;
}

.footer {
  position: absolute;
  left: 0;
  right: 0;
  text-align: center;
  color: #fff;
  background-color: black;
}


</style>
<script>
import axios from 'axios'
import Footer from "@/components/Footer.vue";
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
  components: {
    Footer,
  },
}
</script>