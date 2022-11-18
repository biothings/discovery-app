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
import { portals } from "./modules/portals";
import { validator } from "./modules/validator";
import { delegate } from "tippy.js";
import axios from "axios";

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
    portals,
    validator,
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
  actions: {
    setUpTips() {
      console.log("Setting up Tippy");
      delegate("#tippyRoot", {
        target: "[data-tippy-content]",
        content: "loading",
        animation: "scale",
        theme: "ddeDark",
        trigger: "mouseenter",
        allowHTML: true,
        onShow(instance) {
          let info = instance.reference.dataset.tippyContent;
          if (info.substring(0, 4) == "http") {
            info = info.replace(/['"]+/g, "");
            // EBI API LOOKUP TIP DESCRIPTION
            axios
              .get(
                "https://www.ebi.ac.uk/ols/api/search?q=" +
                  encodeURI(info) +
                  "&exact=1"
              )
              .then((res) => {
                if (
                  res.data.response.hasOwnProperty("docs") &&
                  res.data.response.docs.length >= 1
                ) {
                  for (var i = 0; i < res.data.response.docs.length; i++) {
                    if (res.data.response.docs[i]["iri"] === info) {
                      instance.setContent(res.data.response.docs[i]["label"]);
                    }
                  }
                } else {
                  instance.setContent(info);
                }
              })
              .catch((err) => {
                instance.setContent(info);
              });
          } else {
            let html =
              '<table class="table table-sm table-striped table-dark m-0">';
            try {
              if (instance.reference.dataset.tippyContent.includes("{")) {
                let json = JSON.parse(instance.reference.dataset.tippyContent);
                for (const k in json) {
                  html += `<tr>
                      <td><small><b>${k}</b></small></td>
                      <td><small>${JSON.stringify(json[k])}</small></td>
                      </tr>`;
                }
                html += "</table>";
                instance.setContent(html);
              }
            } catch (error) {
              instance.setContent(instance.reference.dataset.tippyContent);
            }
          }
        },
      });
    },
  },
});
