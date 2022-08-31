import { createStore } from "vuex";
import { auth } from "./modules/auth";
import { faq } from "./modules/faq";
import { compatibility } from "./modules/compatibility";
import { json_schema_viewer } from "./modules/json_schema_viewer";
import { resource_registry } from "./modules/resource_registry";

export default createStore({
  modules: {
    auth,
    faq,
    compatibility,
    json_schema_viewer,
    resource_registry,
  },
  state: () => ({
    loading: false,
  }),
  mutations: {
    setLoading(state, payload) {
      state.loading = payload.value;
    },
  },
  getters: {
    loading: (state) => {
      return state.loading;
    },
  },
});
