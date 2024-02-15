<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="submitForm" class="login-form">
      <div class="form-field">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" class="input-field">
      </div>

      <div class="form-field">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" class="input-field">
      </div>

      <div v-if="errors.length" class="error-notification">
        <p v-for="error in errors" :key="error">{{ error }}</p>
      </div>

      <div class="form-field">
        <button type="submit" class="login-btn">Login</button>
      </div>
    </form>

    <hr>

    <router-link to="/signup" class="signup-link">Create new account</router-link>
  </div>
</template>

<script>
import axios from 'axios'
export default{
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    mounted(){
        document.title = "Login"
    },
 methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token

                    this.$store.commit('setToken', token)
                    
                    axios.defaults.headers.common["Authorization"] = "Token " + token

                    localStorage.setItem("token", token)

                this.$router.push('/')
                })
                .catch(error => {
                    if (error.response.status === 400 && error.response.data.non_field_errors) {
                    this.errors.push('Invalid username or password. Please try again.')
                    }
                    else if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                        
                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>


<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
      border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-field {
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
}

.input-field {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
  width: 100%; 
}

.error-notification {
  margin-top: 10px;
  background-color: red;
  padding: 10px;
  border: 1px solid #ff9999;
  border-radius: 3px;
}

.login-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #0056b3;
}

.signup-link {
  display: block;
  margin-top: 20px;
  text-align: center;
  color: #007bff;
  text-decoration: none;
}

.signup-link:hover {
  text-decoration: underline;
}

.navbar{
  display: none;
}
</style>