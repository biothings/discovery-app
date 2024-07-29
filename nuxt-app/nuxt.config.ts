// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  css: [
    "@fortawesome/fontawesome-svg-core/styles.css",
    "@/assets/css/styles.css",
    "tippy.js/dist/tippy.css",
    "tippy.js/animations/scale.css",
    "tippy.js/themes/light.css",
    "sweetalert2/dist/sweetalert2.min.css",
    "tabulator-tables/dist/css/tabulator.min.css",
    "simple-notify/dist/simple-notify.min.css",
    "aos/dist/aos.css",
  ],
  runtimeConfig: {
    // The private keys which are only available within server-side
    apiSecret: "123",
    // Keys within public, will be also exposed to the client-side
    public: {
      // to test CRUD operations you must use a proxy server, a localhost will only work
      //with GET calls, for prod a proxy server/handler must be used.
      apiUrl: process.env.NODE_ENV == "development" ? "http://localhost" : "",
    },
  },
  // https://github.com/nuxt/framework/discussions/3823
  build: {
    transpile: [
      "@fortawesome/vue-fontawesome",
      "@fortawesome/fontawesome-svg-core",
      "@fortawesome/free-regular-svg-icons",
      "@fortawesome/free-solid-svg-icons",
      "@fortawesome/free-brands-svg-icons",
      "chart.js",
      "tabulator-tables",
      // 'lodash'
    ],
  },
});
