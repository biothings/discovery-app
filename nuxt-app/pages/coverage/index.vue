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
      content: "https://i.postimg.cc/FsGxPZJG/coverage.jpg",
    },
    {
      property: "og:image",
      content: "https://i.postimg.cc/FsGxPZJG/coverage.jpg",
    },
    {
      property: "og:url",
      content: "http://discovery.biothings.io/coverage",
    },
    {
      name: "twitter:url",
      content: "http://discovery.biothings.io/coverage",
    },
    {
      property: "og:description",
      content: "View complete metadata coverage across resources available on the Data Discovery Engine",
    },
    {
      name: "description",
      content: "View complete metadata coverage across resources available on the Data Discovery Engine",
    },
    {
      name: "twitter:card",
      content: "View complete metadata coverage across resources available on the Data Discovery Engine",
    },
  ],
});
</script>

<template>
  <main class="bg-light p-4 container">
    <div class="jumbotron mt-4 text-center bg-dark text-light lines">
      <h1>Resource Coverage</h1>
    </div>
    <div class="d-flex justify-content-start align-items-center">
        <figure>
          <img
          class="rounded"
          src="/assets/img/coverage-grad.png"
          alt="coverage legend"
          width="100px"
        />
        <figcaption class="text-muted">
          <small>Indicates percentage property full coverage (0-100%)</small>
        </figcaption>
      </figure>
    </div>
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
