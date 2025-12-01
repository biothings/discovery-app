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
        namespace: 'revampp',
        prefix: 'revampp',
        name: 'Dataset',
        guide: '/guide/revampp', //Will be used in _meta.guide
        description: 'Dataset schema for the NIAID ReVAMPP Network',
      },
    ]"
  ></Guide>
</template>
