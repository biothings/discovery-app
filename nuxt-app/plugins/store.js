import { defineNuxtPlugin } from "#app";

import store from "@/store";

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(store);
});
