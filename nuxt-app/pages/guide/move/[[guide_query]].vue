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
        namespace: 'move',
        prefix: 'move',
        name: 'Dataset',
        guide: '/guide/move/dataset',
        description:
          'This is the schema for describing the Dataset schema used for MOVE.',
      },
    ]"
  ></Guide>
</template>
