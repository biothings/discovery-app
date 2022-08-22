import { createApp } from "vue";

import App from "./App.vue";
// Vue Ecosystem
import router from "./router";
import store from "./store";
// Plugins
import VueGtag from "vue-gtag-next";
import VueSweetalert2 from "vue-sweetalert2";
// Global Components
import CopyBtn from "./components/CopyBtn.vue"

import "./assets/main.css";
import "./assets/css/styles.css";
import "tippy.js/dist/tippy.css";
import "tippy.js/themes/light.css";
import "sweetalert2/dist/sweetalert2.min.css";

const app = createApp(App);

app
  .use(router)
  .use(VueGtag, {
    property: {
      id: "G-JDB8QD7ZPZ",
    },
  })
  .use(VueSweetalert2)
  .use(store);

app.component('CopyBtn', CopyBtn);

// dev base api url
app.config.globalProperties.$apiUrl =
  process.env.NODE_ENV == "development"
    ? "http://localhost:8000/"
    : "https://discovery.biothings.io/";

app.mount("#app");
