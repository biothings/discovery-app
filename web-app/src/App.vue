<script setup>
import { RouterView } from "vue-router";
import Nav from './components/Nav.vue'
</script>

<template>
  <Nav></Nav>
  <main>
    <RouterView />
  </main>
</template>

<style scoped></style>
