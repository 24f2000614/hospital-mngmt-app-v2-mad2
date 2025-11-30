<script setup>
import 'bootstrap/dist/css/bootstrap.min.css';
import { reactive } from 'vue';
const registrationForm = reactive({
  name:'',
  email:'',
  password:'',
  dob:'',
  sex:'',
  phoneNum:'',
})
const date = new Date().toISOString().split("T")[0]
const registerUser = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(registrationForm)
    })
    const data = await response.json()
    if(!response.ok) {
      alert(data.error || 'Registration failed');
      return 
    }
    alert("Successfully Registered")
  } catch (error) {
    alert(`${error}`)
  }
}
</script>

<template>
  <div class="row">
    <div class="col-md-8 border rounded p-3">
      <h1>Register</h1>
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label for="newEmail" class="form-label">Email address</label>
          <input type="email" class="form-control" v-model="registrationForm.email" id="newEmail" aria-label="Email Address"required >
        </div>
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input type="text" class="form-control" v-model="registrationForm.name" id="name" aria-label="Full Name"required >
        </div>
        <div class="mb-3">
          <label for="newPassword" class="form-label">Password</label>
          <input type="password" class="form-control" v-model="registrationForm.password" id="newPassword" required aria-label="newPassword">
        </div>
        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth</label>
          <input type="date" class="form-control" v-model="registrationForm.dob" id="dob" aria-label="dob" :max="date" required >
        </div>
        <label for="sex" class="form-label">Gender</label>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="sex" id="female" value="F" v-model="registrationForm.sex" checked>
          <label class="form-check-label" for="female">
            Female
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="radio" name="sex" id="male" v-model="registrationForm.sex" value="M">
          <label class="form-check-label" for="male">
            Male
          </label>
        </div>
        <div class="mb-3">
          <label for="phoneNum" class="form-label">Phone number</label>
          <input type="string" class="form-control" id="phoneNum" v-model="registrationForm.phoneNum" aria-label="Phone Number" maxlength="10" minlength="10" required>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>
