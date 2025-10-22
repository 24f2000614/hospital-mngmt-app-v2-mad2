<script setup>
// import WelcomeItem from './WelcomeItem.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
// const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<template>
  <div class="row">
    <div class="col-md-8 border rounded p-3">
      <h1>Login</h1>
      <form>
        <div class="mb-3">
          <label for="loginEmail" class="form-label">Email address</label>
          <input type="email" class="form-control" id="loginEmail" aria-describedby="LoginEmail">
        </div>
        <div class="mb-3">
          <label for="loginPassword" class="form-label">Password</label>
          <input type="password" class="form-control" id="loginPassword">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>
