<script setup>
import axios from "axios";
import Notify from "simple-notify";

const runtimeConfig = useRuntimeConfig();
let coverage = reactive({});
let route = useRoute();

let curie = route.params.curie ? route.params.curie : false;

let url = curie
  ? runtimeConfig.public.apiUrl + "/api/coverage/" + curie
  : runtimeConfig.public.apiUrl + "/api/coverage";

axios
  .get(url)
  .then((res) => {
    coverage.value = res.data;
  })
  .catch((err) => {
    new Notify({
      status: "error",
      title: "Coverage not found",
      text: curie,
      effect: "fade",
      speed: 300,
      customClass: null,
      customIcon: null,
      showIcon: true,
      showCloseButton: true,
      autoclose: true,
      autotimeout: 3000,
      gap: 20,
      distance: 20,
      type: 1,
      position: "right top",
    });
  });

useHead({
  title: "DDE | Resource Metadata Coverage",
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
      content:
        "View complete metadata coverage across all resources available on the Data Discovery Engine",
    },
    {
      name: "description",
      content:
        "View complete metadata coverage across all resources available on the Data Discovery Engine",
    },
    {
      name: "twitter:card",
      content:
        "View complete metadata coverage across all resources available on the Data Discovery Engine",
    },
  ],
});
</script>

<template>
  <main class="bg-light p-4 container">
    <div class="jumbotron mt-4 text-center bg-dark text-light lines">
      <h1>
        <span class="badge badge-info" v-if="curie">{{ curie }}</span> Resource
        Metadata Coverage
      </h1>
      <p>
        Display the metadata field usage for each registered resource metadata
        type
      </p>
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
          <small>Indicates field usage percentage (0-100%)</small>
        </figcaption>
      </figure>
    </div>
    <template v-if="curie">
      <h4 class="p-1">
        <NuxtLink :to="{ path: '/coverage/' + curie }">
          {{ curie }} (N={{ coverage.value?.count }})
          <font-awesome-icon icon="fas fa-chevron-right" />
        </NuxtLink>
      </h4>
      <p>
        <NuxtLink
          :to="{
            path: '/ns/' + curie.split(':')[0] + '/' + curie.split(':')[1],
          }"
          target="_blank"
        >
          <small
            >view {{ curie }} schema
            <font-awesome-icon icon="fas fa-external-link-alt"
          /></small>
        </NuxtLink>
      </p>
      <div v-if="coverage?.value">
        <HorBarChart :name="curie" :totals="coverage.value"></HorBarChart>
      </div>
    </template>
    <template v-else>
      <h1 class="text-muted">Datasets</h1>
      <div
        class="mainBackLight py-2 px-2 d-flex flex-wrap justify-content-around align-items-center row"
      >
        <template v-for="(props, cls) in coverage.value" :key="cls">
          <div
            v-if="cls.includes('Dataset')"
            class="shadow bg-light col-sm-12 col-md-6"
          >
            <h4 class="p-1">
              <NuxtLink :to="{ path: '/coverage/' + cls }">
                {{ cls }} (N={{ props.count }})
                <font-awesome-icon icon="fas fa-chevron-right" />
              </NuxtLink>
            </h4>
            <p>
              <NuxtLink
                :to="{
                  path: '/ns/' + cls.split(':')[0] + '/' + cls.split(':')[1],
                }"
                target="_blank"
              >
                <small
                  >view {{ cls }} schema
                  <font-awesome-icon icon="fas fa-external-link-alt"
                /></small>
              </NuxtLink>
            </p>
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
            <h4 class="p-1">
              <NuxtLink :to="{ path: '/coverage/' + cls }">
                {{ cls }} (N={{ props.count }})
                <font-awesome-icon icon="fas fa-chevron-right" />
              </NuxtLink>
            </h4>
            <p>
              <NuxtLink
                :to="{
                  path: '/ns/' + cls.split(':')[0] + '/' + cls.split(':')[1],
                }"
                target="_blank"
              >
                <small
                  >view {{ cls }} schema
                  <font-awesome-icon icon="fas fa-external-link-alt"
                /></small>
              </NuxtLink>
            </p>
            <HorBarChart :name="cls" :totals="props"></HorBarChart>
          </div>
        </template>
      </div>
    </template>
  </main>
</template>
