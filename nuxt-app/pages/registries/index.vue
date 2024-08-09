<script setup>
import res_reg from "@/assets/img/resource_reg.svg";
import schema_reg from "@/assets/img/schema-reg.svg";

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
    <Title title="Search"></Title>
    <div
      class="jumbotron bg-light d-flex justify-content-center align-items-center"
    >
      <div class="row m-0 w-100">
        <div class="col-sm-6 jumbotron text-center bg-dde-dark">
          <img :src="schema_reg" width="150" alt="resource registry" />
          <hr />
          <router-link to="/registry" class="btn btn-light mainTextDark"
            >Schemas <font-awesome-icon icon="fas fa-chevron-right"
          /></router-link>
        </div>
        <div class="col-sm-6 jumbotron text-center bg-dde-accent">
          <img :src="res_reg" width="150" alt="resource registry" />
          <hr />
          <router-link to="/resource" class="btn btn-light mainTextLight"
            >Metadata <font-awesome-icon icon="fas fa-chevron-right"
          /></router-link>
        </div>
      </div>
    </div>
  </div>
</template>
