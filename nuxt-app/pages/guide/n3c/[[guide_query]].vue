<script setup>
import Guide from "../Guide.vue";
const route = useRoute();
const q = route.params.guide_query;
</script>

<template>
  <Guide :guide_query="q" :presets="[]"></Guide>
</template>
