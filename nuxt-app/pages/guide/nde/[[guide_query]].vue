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
        namespace: 'nde',
        prefix: 'nde',
        name: 'Dataset',
        guide: '/guide/nde',
        description:
          'Datasets contained in the NIAID Data Ecosystem. The NIAID Data Ecosystem is an environment to find and access and infectious and immune-mediated disease data and computational tools to speed the development of diagnostics, therapeutics, and vaccines.',
      },
      {
        namespace: 'nde',
        prefix: 'nde',
        name: 'ResourceCatalog',
        guide: '/guide/nde/ResourceCatalog',
        description:
          'ResourceCatalogs (collections of scientific information or research outputs) contained in the NIAID Data Ecosystem. Resource catalogs include databases, repositories, knowledge bases, citation indices, software indices, browser-based data portals (web portals), etc.',
      },
      {
        namespace: 'nde',
        prefix: 'nde',
        name: 'ComputationalTool',
        guide: '/guide/nde/ComputationalTool',
        description:
          'ComputationalTools (software, workflows, computational tools, code) contained in the NIAID Data Ecosystem. The NIAID Data Ecosystem is a secure environment to find, access and analyze immune-mediated and infectious disease data and computational tools to speed the development of diagnostics, therapeutics, and vaccines. The NIAID Data Ecosystem Discovery Portal harvests metadata from dataset repository and harmonizes them to this schema to enable easy cross-platform dataset searching and filtering.',
      },
    ]"
  ></Guide>
</template>
