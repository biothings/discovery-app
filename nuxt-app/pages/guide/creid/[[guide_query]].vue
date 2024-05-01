<script setup>
import Guide from "../Guide.vue";
const route = useRoute();
const q = route.params.guide_query;
</script>

<template>
  <Guide
    :guide_query="q"
    :presets="[
      {
        namespace: 'creid',
        prefix: 'creid',
        name: 'Dataset',
        guide: '/guide/creid',
        description:
          'Dataset schema for the Centers for Research in Emerging Infectious Disease (CREID) Network',
      },
    ]"
  ></Guide>
</template>
