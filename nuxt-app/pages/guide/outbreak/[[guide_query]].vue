<script setup>
    import Guide from "../Guide.vue"
    const route = useRoute();
    const q = route.params.guide_query;
</script>

<template>
    <Guide :guide_query="q" :presets='[
        {
          namespace: "outbreak",
          prefix: "outbreak",
          name: "Dataset",
          guide: "/guide/outbreak/dataset",
          description:
            "This is the schema for describing the Dataset schema used for outbreak.info.",
        },
      ]'></Guide>
</template>