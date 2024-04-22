import { delegate } from "tippy.js";
import axios from "axios";
import { defineStore } from "pinia";

export const useMainStore = defineStore("mainStore", {
  state: () => ({
    loading: false,
  }),
  actions: {
    setLoading(payload) {
      this.loading = payload.value;
    },
    loadingON() {
      this.loading = true;
    },
    loadingOFF() {
      this.loading = false;
    },
    setUpTips() {
      console.log("Setting up Tippy");
      delegate("#tippyRoot", {
        target: "[data-tippy-content]",
        content: "loading",
        animation: "scale",
        theme: "ddeDark",
        trigger: "mouseenter",
        interactive: true,
        allowHTML: true,
        onShow(instance) {
          let info = instance.reference.dataset.tippyContent;
          if (info.substring(0, 4) == "http") {
            info = info.replace(/['"]+/g, "");
            // EBI API LOOKUP TIP DESCRIPTION
            axios
              .get(
                "https://www.ebi.ac.uk/ols4/api/search?q=" +
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
            let html = '<table class="table table-sm table-borderless m-0">';
            try {
              if (instance.reference.dataset.tippyContent.includes("{")) {
                let json = JSON.parse(instance.reference.dataset.tippyContent);
                for (const k in json) {
                  html += `<tr>
                      <td><small><b>${k}</b></small></td>
                      <td><small class='text-light'><pre class='code-overflow text-light p-1 rounded m-0'>${JSON.stringify(
                        json[k],
                        null,
                        2
                      )}</pre></small></td>
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
      delegate("#tippyRoot", {
        target: ".source-badge",
        content: "loading",
        animation: "scale",
        theme: "light",
        trigger: "mouseenter",
        interactive: true,
        allowHTML: true,
        onShow(instance) {
          instance.setContent(`<div class="p-0">
          <table class="table table-sm m-0">
              <thead>
              <tr>
                  <td colspan="2" class='text-muted text-center'>
                  <b>Schema Source URL Status</b>
                  </td>
              </tr>
              </thead>
              <tbody>
              <tr>
                  <td class='text-success center'>
                  <b>OK</b>
                  </td>
                  <td class="black-text">
                  <small>Schema URL is working and returns valid metadata.</small>
                  </td>
              </tr>
              <tr>
                  <td class='text-danger center'>
                  <b>NOT FOUND</b>
                  </td>
                  <td class="black-text">
                  <small>Schema URL returns not found.</small>
                  </td>
              </tr>
              <tr>
                  <td class='text-invalid center'>
                  <b>INVALID</b>
                  </td>
                  <td class="black-text">
                  <small>Schema URL works but contains invalid metadata.</small>
                  </td>
              </tr>
              <tr>
                  <td class='text-broken center'>
                  <b>BROKEN</b>
                  </td>
                  <td class="black-text">
                  <small>Schema URL is broken.</small>
                  </td>
              </tr>
              <tr class="alert-info">
                  <td colspan='2' class='text-primary'>
                  <p>
                      <small>Note: Schema updates cannot be synchronized with its source URL if the status is not <b class='text-success'>OK</b></small>. 
                  </p>
                  <p>
                      <small>If you wish to update the URL or Once all issues have been resolved on your end you can update manually via your dashboard.</small>
                  </p>
                  </td>
              </tr>
              </tbody>
          </table>
          </div>`);
        },
      });
    },
  },
});
