<script setup>
import Guide from "./Guide.vue";
const route = useRoute();
const q = route.params.guide_query;
</script>

<template>
  <Guide
    :guide_query="q"
    :presets="[
      {
        namespace: 'biomedical',
        prefix: 'bts',
        name: 'BioMedicalDataset',
        guide: '/guide',
        description: 'A schema describing a BioMedical Dataset',
      },
    ]"
  ></Guide>
</template>
