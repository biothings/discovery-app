<script setup>
const props = defineProps(["title", "subtitle"]);
</script>
<template>
  <div class="p-5 text-dde-dark text-center mt-5">
    <h1>{{ title }}</h1>
    <h5 v-if="subtitle">{{ subtitle }}</h5>
  </div>
</template>
