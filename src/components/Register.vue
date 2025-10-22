<script setup>
// import WelcomeItem from './WelcomeItem.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
// const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<template>
  <div class="row">
    <div class="col-md-8 border rounded p-3">
      <h1>Register</h1>
      <form>
        <div class="mb-3">
          <label for="loginEmail" class="form-label">Email address</label>
          <input type="email" class="form-control" id="loginEmail" aria-label="Email Address">
        </div>
        <div class="mb-3">
          <label for="fullName" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="fullName" aria-label="Full Name">
        </div>
        <div class="mb-3">
          <label for="newPassword" class="form-label">Password</label>
          <input type="password" class="form-control" id="newPassword" aria-label="newPassword">
        </div>
        <div class="mb-3">
          <label for="phoneNum" class="form-label">Phone number</label>
          <input type="string" class="form-control" id="phoneNum" aria-label="Phone Number" maxlength="10" minlength="10">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>
