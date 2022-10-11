// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    css: [
      '@fortawesome/fontawesome-svg-core/styles.css',
      '@/assets/css/styles.css',
      "tippy.js/dist/tippy.css",
      "tippy.js/animations/scale.css",
      "tippy.js/themes/light.css",
      "sweetalert2/dist/sweetalert2.min.css",
      "tabulator-tables/dist/css/tabulator.min.css",
      'simple-notify/dist/simple-notify.min.css'
    ],
    runtimeConfig: {
      // The private keys which are only available within server-side
      apiSecret: '123',
      // Keys within public, will be also exposed to the client-side
      public: {
        apiUrl: ''
      }
    },
    // https://github.com/nuxt/framework/discussions/3823
    build: {
      transpile: [
          '@fortawesome/vue-fontawesome',
          '@fortawesome/fontawesome-svg-core',
          '@fortawesome/free-regular-svg-icons',
          '@fortawesome/free-solid-svg-icons',
          '@fortawesome/free-brands-svg-icons',
          'chart.js',
          'tabulator-tables',
          // 'lodash'
      ]
  }
  })
