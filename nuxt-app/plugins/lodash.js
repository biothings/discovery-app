import { defineNuxtPlugin } from "#app";
import lodash from "lodash";

export default defineNuxtPlugin(() => {
  return {
    provide: {
      _: lodash,
    },
  };
});
