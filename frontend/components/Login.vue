<script setup>
// import WelcomeItem from './WelcomeItem.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import { reactive } from 'vue';
import { useRouter } from 'vue-router'

const router = useRouter()

const loginForm = reactive({
  email:'',
  password:''
})

const loginUser = async () => {
  try{
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type':'application/json'
        },
        body: JSON.stringify(loginForm)
      })
      const data = await response.json()
      if(!response.ok) {
        throw new Error(JSON.stringify(data.error));
      } else {
        localStorage.setItem('token', data.tokens["access_token"])
        localStorage.setItem('role', data.role)
        if (data.role === 'Admin') {
          router.push({name: 'adminHome'})
        }
        else {
          router.push('/user')
        }
      }
  } catch( error ) {
    console.log(error)
  }
}
</script>

<template>
  <div class="row">
    <div class="col-md-8 border rounded p-3">
      <h1>Login</h1>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label for="loginEmail" class="form-label">Email address</label>
          <input type="email" class="form-control" id="loginEmail" v-model="loginForm.email" aria-describedby="LoginEmail">
        </div>
        <div class="mb-3">
          <label for="loginPassword" class="form-label">Password</label>
          <input type="password" class="form-control" v-model="loginForm.password" id="loginPassword">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>
