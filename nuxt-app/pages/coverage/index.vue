<script setup>
import axios from "axios";

const runtimeConfig = useRuntimeConfig();
let coverage = reactive({});

axios
  .get(runtimeConfig.public.apiUrl + "/api/coverage")
  .then((res) => {
    coverage.value = res.data;
  })
  .catch((err) => {
    throw err;
  });

useHead({
  title: "DDE | Resource Coverage",
  meta: [
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/Kj9MSL9k/faq.jpg",
    },
    {
      property: "og:image",
      content: "https://i.postimg.cc/Kj9MSL9k/faq.jpg",
    },
    {
      property: "og:url",
      content: "http://discovery.biothings.io/faq",
    },
    {
      name: "twitter:url",
      content: "http://discovery.biothings.io/faq",
    },
    {
      property: "og:description",
      content: "Get help with some of our most frequently asked questions",
    },
    {
      name: "description",
      content: "Get help with some of our most frequently asked questions",
    },
    {
      name: "twitter:card",
      content: "Get help with some of our most frequently asked questions",
    },
  ],
});
</script>

<template>
  <main class="bg-light p-4 container">
    <div class="jumbotron mt-4 text-center bg-dark text-light lines">
      <h1>Resource Coverage</h1>
    </div>
    <hr />
    <h1 class="text-muted">Datasets</h1>
    <div
      class="mainBackLight py-2 px-2 d-flex flex-wrap justify-content-around align-items-center row"
    >
      <template v-for="(props, cls) in coverage.value" :key="cls">
        <div
          v-if="cls.includes('Dataset')"
          class="shadow bg-light col-sm-12 col-md-6"
        >
          <HorBarChart :name="cls" :totals="props"></HorBarChart>
        </div>
      </template>
    </div>
    <h1 class="text-muted">Other Types</h1>
    <div
      class="mainBackDark py-2 px-2 d-flex flex-wrap justify-content-around align-items-center row"
    >
      <template v-for="(props, cls) in coverage.value" :key="cls">
        <div
          v-if="!cls.includes('Dataset')"
          class="shadow bg-light col-sm12 col-md-6"
        >
          <HorBarChart :name="cls" :totals="props"></HorBarChart>
        </div>
      </template>
    </div>
  </main>
</template>
