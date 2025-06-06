<script setup>
import Nav from "./components/Nav.vue";
import Footer from "./components/Footer.vue";
import { useStore } from "vuex";
import { onMounted, computed } from "vue";

// scroll to top on page change
const nuxtApp = useNuxtApp();

nuxtApp.hook("page:finish", () => {
  window.scrollTo(0, 0);
});

const store = useStore();
let isLoading = computed(() => store.getters.loading);

onMounted(() => {
  store.dispatch("setUpTips");
  store.dispatch("getSchemaOrgVersion");
});

useHead({
  meta: [
    {
      property: "og:site_name",
      content: "Data Discovery Engine",
    },
    {
      property: "og:title",
      content: "Data Discovery Engine",
    },
    {
      name: "twitter:title",
      content: "Data Discovery Engine",
    },
    {
      name: "HandheldFriendly",
      content: "True",
    },
    {
      name: "author",
      content: "WuLab @ Scripps Research",
    },
    {
      name: "robots",
      content: "follow",
    },
    {
      name: "copyright",
      content: "https://creativecommons.org/licenses/by/4.0/",
    },
    {
      name: "keywords",
      content: "metadata, schema, discovery",
    },
    {
      name: "msapplication-config",
      content: "@/assets/img/dde/browserconfig.xml",
    },
    {
      name: "theme-color",
      content: "#43318d",
    },
    {
      name: "msapplication-TileColor",
      content: "#43318d",
    },
    {
      property: "og:image:type",
      content: "image/jpg",
    },
    {
      property: "og:image:width",
      content: "1200",
    },
    {
      property: "og:image:height",
      content: "630",
    },
    {
      property: "og:locale",
      content: "en_US",
    },
    {
      property: "og:type",
      content: "website",
    },
  ],
  link: [
    {
      rel: "apple-touch-icon",
      sizes: "180x180",
      href: "@/assets/img/dde/apple-touch-icon.png",
    },
    {
      rel: "icon",
      type: "image/png",
      sizes: "32x32",
      href: "@/assets/img/dde/favicon-32x32.png",
    },
    {
      rel: "icon",
      type: "image/png",
      sizes: "16x16",
      href: "@/assets/img/dde/favicon-16x16.png",
    },
    {
      rel: "mask-icon",
      color: "#8824a3",
      href: "@/assets/img/dde/safari-pinned-tab.svg",
    },
    {
      rel: "shortcut icon",
      href: "/favicon.ico",
    },
    {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap",
    },
    {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap",
    },
    {
      src: "https://code.jquery.com/jquery-3.3.1.slim.min.js",
      integrity:
        "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
      crossorigin: "anonymous",
    },
    {
      src: "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
      integrity:
        "sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
      crossorigin: "anonymous",
    },
    {
      src: "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js",
      integrity:
        "sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy",
      crossorigin: "anonymous",
    },
  ],
  script: [
    {
      src: "https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.min.js",
    },
  ],
});
</script>
<template>
  <div class="bg-light" id="tippyRoot">
    <Nav></Nav>
    <div v-if="isLoading" class="loader">
      <img src="@/assets/img/ripple.svg" />
    </div>
    <NuxtLoadingIndicator color="#d83f88" />
    <NuxtPage></NuxtPage>
    <Footer></Footer>
  </div>
</template>
