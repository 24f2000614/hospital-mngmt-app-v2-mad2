<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 1000;
  font-size: 5rem;
  position: relative;
  margin-bottom: 0;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px ) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
