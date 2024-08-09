<script setup>
import { useStore } from "vuex";

let store = useStore();
let portals = store.getters.getPortals;

useHead({
  title: "DDE | Data Portals",
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
  <div id="portals" class="container-fluid bg-light text-dde-dark min-100">
    <Title
      title="Data Portals"
      subtitle="Explore data portals and learn how you can contribute and access their
        data."
    ></Title>
    <div class="container">
      <div class="d-flex justify-content-center flex-wrap">
        <template v-for="portal in portals" :key="portal.name">
          <div
            class="card mb-1 col-sm-4 m-2 p-2"
            :style="{ borderLeft: portal.colors[0].hex + ' solid 30px' }"
          >
            <div>
              <div class="d-flex justify-content-start align-items-center">
                <img
                  :src="portal.portalicon"
                  :alt="portal.name"
                  width="50"
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
          </div>
        </template>
      </div>
      <div class="alert bg-light text-dde-dark m-5 bold">
        <h2>
          Apply to feature your project here and enjoy all these features:
        </h2>
        <ul class="text-left">
          <li>Register a custom schema</li>
          <li>Advanced metadata intake guides</li>
          <li>Share and embed your metadata easily</li>
          <li>Metadata field coverage</li>
          <li>Schema/Metadata management dashboard</li>
        </ul>
        <h4>
          <a
            href="https://github.com/biothings/discovery-app/issues/new/choose"
            target="_blank"
            rel="nonreferrer"
            >Fill out an application to get started today</a
          >.
        </h4>
      </div>
    </div>
  </div>
</template>
