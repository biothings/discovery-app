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
        namespace: 'ndetest',
        prefix: 'nde',
        name: 'Dataset',
        guide: '/guide/ndetest',
        description:
          'Test',
      },
    ]"
  ></Guide>
</template>
