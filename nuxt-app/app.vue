<script setup>
import Nav from "./components/Nav.vue";
import Footer from "./components/Footer.vue";
import { useStore } from "vuex";
import { onMounted, computed } from "vue";

const store = useStore();
let isLoading = computed(() => store.getters.loading);

onMounted(() => {
  store.dispatch("setUpTips");
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
      content: "#63296b",
    },
    {
      name: "msapplication-TileColor",
      content: "#63296b",
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
      href: "@/assets/img/dde/favicon.ico",
    },
    {
      rel: "manifest",
      href: "@/assets/img/dde/site.webmanifest",
    },
    {
      rel: "stylesheet",
      href: "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
      integrity:
        "sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
      crossorigin: "anonymous",
    },
    {
      href: "https://fonts.googleapis.com/css?family:Sulphur+Point&display:swap",
      rel: "stylesheet",
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
    {
      type: "text/css",
      rel: "stylesheet",
      href: "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.0/normalize.min.css",
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
    <NuxtLoadingIndicator color="#63286b" />
    <NuxtPage></NuxtPage>
    <Footer></Footer>
  </div>
</template>
