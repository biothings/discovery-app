<script setup>
import { useStore } from "vuex";

let store = useStore();
let portals = store.getters.getPortals;

useHead({
  title: "DDE | Data Portals",
  meta: [
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
    },
    {
      property: "og:image",
      content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
    },
    {
      property: "og:url",
      content: "http://discovery.biothings.io/portal",
    },
    {
      name: "twitter:url",
      content: "http://discovery.biothings.io/portal",
    },
    {
      property: "og:description",
      content:
        "Explore data portals and learn how you can contribute and access their data.",
    },
    {
      name: "description",
      content:
        "Explore data portals and learn how you can contribute and access their data.",
    },
    {
      name: "twitter:card",
      content:
        "Explore data portals and learn how you can contribute and access their data.",
    },
  ],
});
</script>

<template>
  <div
    id="portals"
    class="container-fluid alert-secondary py-5"
    style="min-height: 80vh"
  >
    <div class="jumbotron bg-none mb-0 text-center">
      <h1 class="logoText">Data Portals</h1>
      <p class="w-75 m-auto text-muted">
        Explore data portals and learn how you can contribute and access their
        data.
      </p>
    </div>
    <div class="container">
      <ul class="list-group">
        <template v-for="portal in portals" :key="portal.name">
          <li
            class="list-group-item mb-1"
            :style="{ borderLeft: portal.colors[1].hex + ' solid 10px' }"
          >
            <div>
              <div class="d-flex justify-content-start align-items-center">
                <img
                  :src="portal.portalicon"
                  :alt="portal.name"
                  width="50px"
                  class="mr-2"
                />
                <RouterLink
                  class="tip"
                  :to="{ path: '/portal/' + portal.linkname }"
                  data-tippy-content="Learn More"
                >
                  <h4 class="d-inline">
                    <span v-text="portal.name"></span>
                    <font-awesome-icon icon="fas fa-chevron-right" />
                  </h4>
                </RouterLink>
              </div>
              <h5 class="mt-3" v-text="portal.header"></h5>
            </div>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>
