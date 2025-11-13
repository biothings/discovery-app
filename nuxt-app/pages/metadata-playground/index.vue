<script setup>
import validator_img from "@/assets/img/validator.svg";
import generator_img from "@/assets/img/generator.svg";

useHead({
  title: "DDE | Registries",
  meta: [
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/wTG3pgRY/featured.jpg",
    },
    {
      property: "og:image",
      content: "https://i.postimg.cc/wTG3pgRY/featured.jpg",
    },
    {
      property: "og:url",
      content: "http://discovery.biothings.io/registries",
    },
    {
      name: "twitter:url",
      content: "http://discovery.biothings.io/registries",
    },
    {
      property: "og:description",
      content:
        "Browse structured resource metadata or available namespaces and schemas on the DDE",
    },
    {
      name: "description",
      content:
        "Browse structured resource metadata or available namespaces and schemas on the DDE",
    },
    {
      name: "twitter:card",
      content:
        "Browse structured resource metadata or available namespaces and schemas on the DDE",
    },
  ],
});
</script>

<template>
  <div class="min-100">
    <PageTitle title="Validate and Create Metadata"></PageTitle>
    <div
      class="jumbotron bg-light d-flex justify-content-center align-items-center"
    >
      <div class="row m-0 w-100">
        <div class="col-sm-6 jumbotron text-center bg-dde-dark">
          <img :src="validator_img" width="150" alt="validate" />
          <hr />
          <router-link to="/validator" class="btn btn-light mainTextDark"
            >Validate your metadata against an existing schema
            <font-awesome-icon icon="fas fa-chevron-right"
          /></router-link>
        </div>
        <div class="col-sm-6 jumbotron text-center bg-dde-mid">
          <img :src="generator_img" width="150" alt="generate" />
          <hr />
          <router-link
            to="/markup-generator"
            class="btn btn-light mainTextLight"
            >Create new metadata based off an existing schema
            <font-awesome-icon icon="fas fa-chevron-right"
          /></router-link>
        </div>
      </div>
    </div>
  </div>
</template>
