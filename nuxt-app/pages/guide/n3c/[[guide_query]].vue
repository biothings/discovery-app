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
        namespace: 'n3c',
        prefix: 'n3c',
        name: 'Dataset',
        guide: '/guide/n3c/dataset',
        description:
          'This is the schema for describing the Dataset schema used for N3C.',
      },
    ]"
  ></Guide>
</template>
