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
        namespace: 'niaid',
        prefix: 'niaid',
        name: 'Dataset',
        guide: '/guide/niaid',
        description:
          'A schema describing a minimal Dataset for the National Institute of Allergy and Infectious Disease (NIAID). A dataset is a collection of data of a particular experimental type. Additional schema.org and/or custom properties could be added.',
      },
      {
        namespace: 'niaid',
        prefix: 'niaid',
        name: 'ComputationalTool',
        guide: '/guide/niaid/ComputationalTool',
        description:
          'A schema describing a minimal ComputationalTool for the National Institute of Allergy and Infectious Disease (NIAID). A ComputationalTool is a software used for the collection, processing, distribution, analysis, visualization, interpretation, etc. of data. Additional schema.org and/or custom properties could be added.',
      },
    ]"
  ></Guide>
</template>
