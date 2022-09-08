import { createStore } from "vuex";
import { auth } from "./modules/auth";
import { faq } from "./modules/faq";
import { compatibility } from "./modules/compatibility";
import { json_schema_viewer } from "./modules/json_schema_viewer";
import { resource_registry } from "./modules/resource_registry";
import { schema_registry } from "./modules/schema_registry";
import { schema_viewer } from "./modules/schema_viewer";
import { editor } from "./modules/editor";
import { guide } from "./modules/guide";

export default createStore({
  modules: {
    auth,
    faq,
    compatibility,
    json_schema_viewer,
    resource_registry,
    schema_registry,
    schema_viewer,
    editor,
    guide,
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
