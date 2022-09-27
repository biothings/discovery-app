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
import { delegate } from 'tippy.js';

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
  actions:{
    setUpTips(){
      console.log('Setting up Tippy');
      delegate("#tippyRoot", {
        target: "[data-tippy-content]",
        content: 'loading',
        animation: "scale",
        theme: "ddeDark",
        trigger:'hover',
        allowHTML: true,
        onShown(instance) {
          let html =
            '<table class="table table-sm table-striped table-secondary m-0">';
          try {
            if (instance.reference.dataset.tippyContent.includes("{")) {
              let json = JSON.parse(instance.reference.dataset.tippyContent);
              for (const k in json) {
                html += `<tr>
                <td>${k}</td>
                <td>${json[k]}</td>
                </tr>`;
              }
              html += "</table>";
              instance.setContent(html);
            }
          } catch (error) {
            instance.setContent(instance.reference.dataset.tippyContent);
          }
        },
      });
    }
  }
});
