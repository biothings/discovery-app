<template>
  <form id="linkForm" class="w-100 m-auto">
    <div v-if="!loading" class="input-group mb-3 shadow rounded">
      <input
        type="text"
        class="form-control"
        v-model="input"
        id="urlform"
        autocomplete=""
        required
        ref="my_input"
        aria-label="Paste your link here"
        placeholder="Paste your link here"
        aria-describedby="button-addon2"
      />
      <div class="input-group-append">
        <button
          :disabled="!input.length"
          :class="{ heartbeat: input.length }"
          @click.prevent="getFormValues()"
          id="button-addon2"
          class="btn btn-success"
          type="submit"
        >
          Let's Go!
        </button>
      </div>
    </div>
    <div v-else>
      <h3 class="text-light">
        <font-awesome-icon icon="fas fa-cog fa-spin" class="text-success" />
        Please Wait...
      </h3>
    </div>
    <small>Examples: </small>
    <small
      class="badge badge-dark pointer mr-1"
      @click="
        input =
          'https://raw.githubusercontent.com/NIAID-Data-Ecosystem/nde-schemas/main/combined_schema_DO_NOT_EDIT/NIAID_schema.json'
      "
    >
      NIAID Data Ecosystem Schema
    </small>
    <small
      class="badge badge-dark pointer mr-1"
      @click="
        input =
          'https://raw.githubusercontent.com/NIAID-Data-Ecosystem/nde-schemas/main/NDE_schema.jsonld'
      "
    >
      NDE Dataset & ComputationalTool
    </small>
  </form>
</template>

<script>
import axios from "axios";
import woohoo from "@/assets/img/woohoo-01.svg";
import oh_no from "@/assets/img/oh_no-01.svg";
import dde_logo from "@/assets/img/dde-logo-o.svg";
import not_right from "@/assets/img/not_right-01.svg";
export default {
  data: function () {
    return {
      input: "",
      loading: false,
    };
  },
  watch: {
    input: function (value) {
      if (value.includes("blob") || value.includes("github.com")) {
        this.suggestedURL = value
          .replace("blob/", "")
          .replace("github.com", "raw.githubusercontent.com")
          .replace("www.github.com", "raw.githubusercontent.com");
        this.$swal({
          title: "Link Converted",
          imageUrl: dde_logo,
          imageHeight: 100,
          imageAlt: "Warning",
          customClass: "scale-in-center",
          html:
            "<p>We noticed that was not a raw data link. We have converted it to: </p> " +
            '<p><a target="_blank" href="' +
            this.suggestedURL +
            '">' +
            this.suggestedURL +
            "</a></p>" +
            "<p>Proceed with this link?</p>",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          confirmButtonText: "Yes, use this link!",
        }).then((result) => {
          if (result.value) {
            this.input = this.suggestedURL;
          }
        });
      }
    },
  },
  methods: {
    getFormValues() {
      this.input = this.$refs.my_input.value;
      this.$refs.my_input.value = "";
      this.sendRequest();
    },
    assignTempName(hits) {
      let self = this;
      if (hits.length) {
        if (hits[0].hasOwnProperty("namespace")) {
          self.slug = hits[0]["namespace"];
        } else if (hits[0].hasOwnProperty("name")) {
          self.slug = hits[0]["name"].split(":")[0];
        } else {
          self.slug = "temp";
        }
        self.makeURLandRedirect();
      } else {
        this.$swal({
          imageUrl: not_right,
          imageHeight: 200,
          imageAlt: "Error",
          title: "Error parsing schema",
          text: "No classes found",
          type: "error",
        });
      }
    },
    handleGoodSchema(data) {
      let self = this;
      localStorage.setItem("user-schema-classes", JSON.stringify(data));
      localStorage.setItem("user-schema-url", self.input);
      if (data.hits.length) {
        if (data.hits[0].hasOwnProperty("namespace")) {
          self.slug = data.hits[0]["namespace"];
        } else if (data.hits[0].hasOwnProperty("name")) {
          self.slug = data.hits[0]["name"].split(":")[0];
        } else {
          self.slug = "temp";
        }
        self.makeURLandRedirect();
      } else {
        this.$swal({
          imageUrl: oh_no,
          imageHeight: 200,
          icon: "Error",
          title: "Something went wrong",
          text: JSON.stringify(data.validation.errors),
        });
      }
    },
    getErrorHtml(type, messages) {
      let msg_html = "<div>";
      switch (type) {
        case "no_path_to_root":
          msg_html += `<img src="@/assets/img/broken_root-01.svg" height="50px" alt="broken path to root"/>
                    <small class="text-primary d-block">Tip: A broken path can generate more errors, 
                        we recommend fixing this first and see if this fixes other issues.</small>`;
          break;
        case "invalid_validation_schema":
          msg_html += `<img src="@/assets/img/check_validation-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "undefined_rangeincludes":
          msg_html += `<img src="@/assets/img/check_range-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "non_class_or_property_@type":
          msg_html += `<img src="@/assets/img/check_range-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "invalid_property":
          msg_html += `<img src="@/assets/img/check_definition-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "invalid_class":
          msg_html += `<img src="@/assets/img/check_definition-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "dup_label":
          msg_html += `<img src="@/assets/img/label_issue-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "unmatched_label":
          msg_html += `<img src="@/assets/img/label_issue-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "missing_rangeincludes":
          msg_html += `<img src="@/assets/img/check_range-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "undefined_domainincludes_class":
          msg_html += `<img src="@/assets/img/check_definition-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "invalid_property_label":
          msg_html += `<img src="@/assets/img/label_issue-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        case "invalid_class_label":
          msg_html += `<img src="@/assets/img/label_issue-01.svg" height="50px" alt="broken path to root"/>`;
          break;
        default:
          msg_html += `<img src="@/assets/img/not_right-01.svg" height="50px" alt="broken path to root"/>`;
          break;
      }
      msg_html +=
        '<div style="max-height:200px; overflow-y:scroll;"><table class="table table-striped table-sm"><tbody>';
      messages.forEach((err) => {
        let warning = "";
        let field = "";
        // special styling
        err.message = err.message.replace(
          "$validation",
          "<b class='text-dark'>$validation</b>"
        );
        err.message = err.message.replace(
          "schema:Thing",
          "<b class='text-primary'>schema:Thing</b>"
        );
        err.message = err.message.replace(
          "not defined",
          "<b class='text-dark'>not defined</b>"
        );
        //warning
        if (err && err.warning) {
          warning = `🟡`;
        } else {
          warning = `🟡`;
        }
        //field
        if (err && err.field) {
          // expandable report
          field = `<b class="mainTextDark">${err.field}</b> from <b class="text-info">${err.record_id}</b>`;
          msg_html += `<tr class="text-left">
                    <td>
                        <details>
                        <summary>
                            <small>${warning}&nbsp;${field}</small>
                        </summary>
                        <small class="d-block">${err.message}</small>
                        </details>
                    </td>
                    </tr>`;
        } else {
          //inline report
          msg_html += `<tr class="text-left">
                    <td>
                        <small>${warning}&nbsp;${err.message}</small>
                    </td>
                    </tr>`;
        }
      });
      msg_html += "</tbody></table></div></div>";
      return msg_html;
    },
    showErrorDetails(validation, data) {
      let self = this;
      let html = "";
      let groupedErrors = {};
      //error list can be skipped if only warnings
      let only_warnings = true;
      // console.log(validation)
      validation.errors.forEach((error) => {
        //CLEAN UP MSG
        error.message = error.message.replace(/\\"/g, '"');
        // WARNINGS ONLY
        if (!Object.hasOwnProperty.call(error, "warning")) {
          only_warnings = false;
        }
        // ADD NEW PROP
        if (!Object.hasOwnProperty.call(groupedErrors, error.error_type)) {
          groupedErrors[error.error_type] = [error];
        }
        // ALREADY HAS PROP
        else {
          groupedErrors[error.error_type].push(error);
        }
      });
      for (const type in groupedErrors) {
        html += self.getErrorHtml(type, groupedErrors[type]);
      }
      // show modal
      if (only_warnings) {
        this.$swal
          .fire({
            position: "center",
            title: `There ${
              validation.errors.length > 1 ? "are warnings" : "is a warning"
            } with your schema:`,
            html: html,
            customClass: "scale-in-center",
            footer: `<small class="text-muted">🟡: warning - optional</small>
                    <p>These appear to be small warnings only but we recommend fixing them to prevent future issues.</p>`,
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonText: "Continue Anyway",
            cancelButtonText: "Download Report",
          })
          .then((result) => {
            if (result && result.value) {
              self.handleGoodSchema(data);
            } else if (result && result.dismiss == "cancel") {
              self.downloadReport(validation);
            }
          });
      } else {
        this.$swal
          .fire({
            position: "center",
            title: `There ${
              validation.errors.length > 1 ? "are problems" : "is a problem"
            } with your schema:`,
            html: html,
            customClass: "scale-in-center",
            footer: `<small class="text-muted">🔴 : error - must be resolved, 
                    🟡: warning - optional</small>`,
            showCancelButton: true,
            confirmButtonText: "Download Report",
            cancelButtonText: "Close",
          })
          .then((result) => {
            if (result.value) {
              self.downloadReport(validation);
            }
          });
      }
    },
    downloadReport(report) {
      var self = this;
      this.$swal
        .fire({
          title: "Name your file",
          input: "text",

          customClass: "scale-in-center",
          inputAttributes: {
            autocapitalize: "off",
          },
          showCancelButton: true,
          confirmButtonText: "Download Report",
          allowOutsideClick: () => !this.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (result.value) {
            self.download(
              JSON.stringify(report, null, 2),
              result.value + ".json",
              "text/plain"
            );
          }
        });
    },
    download(content, fileName, contentType) {
      var a = document.createElement("a");
      var file = new Blob([content], { type: contentType });
      a.href = URL.createObjectURL(file);
      a.download = fileName;
      a.click();
    },
    sendRequest() {
      let self = this;
      self.$store.commit("setLoading", { value: true });
      const runtimeConfig = useRuntimeConfig();
      axios
        .get(runtimeConfig.public.apiUrl + "/api/view?url=" + self.input)
        .then((res) => {
          self.$store.commit("setLoading", { value: false });
          if (res.data.validation.valid && !res.data.validation.errors.length) {
            self.handleGoodSchema(res.data);
          } else {
            self.showErrorDetails(res.data.validation, res.data);
          }
        })
        .catch((err) => {
          self.$store.commit("setLoading", { value: false });
          console.log(err);
          let culprit = "<h6>" + err.response.data.error + "</h6>";
          if (err.response.data && err.response.data.path) {
            culprit +=
              "<h5>Culprit -> <b class='text-danger'>" +
              err.response.data.path +
              "</b></h5>";
          }
          if (err.response.data.parent && err.response.data.parent.path) {
            if (true) {
              culprit +=
                "<h5>Under -> <b class='text-danger'>" +
                err.response.data.parent.path +
                "</b></h5>";
            }
            if (err.response.data.parent && err.response.data.parent.reason) {
              culprit +=
                "<div class='alert alert-warning'><small>" +
                err.response.data.parent.reason +
                "</small></div>";
            }
          }
          if (
            err.response.data.hasOwnProperty("validator_value") &&
            err.response.data.validator_value.length
          ) {
            culprit +=
              "<div class='alert alert-info'><small> Hint: " +
              err.response.data.validator_value +
              "</small></div>";
          }
          this.$swal.fire({
            imageUrl: oh_no,
            imageHeight: 200,

            customClass: "scale-in-center",
            imageAlt: "Error",
            position: "center",
            title: "Details: ",
            html: culprit,
          });
          throw err;
        });
    },
    makeURLandRedirect() {
      let self = this;
      let timerInterval;
      this.$swal
        .fire({
          imageUrl: woohoo,
          imageHeight: 200,
          imageAlt: "Error",
          title: "Everything looks good!",
          html: "Taking you to your schema in <b></b> seconds..",
          timer: 3000,
          timerProgressBar: true,
          didOpen: () => {
            self.$swal.showLoading();
            const b = self.$swal.getHtmlContainer().querySelector("b");
            timerInterval = setInterval(() => {
              b.textContent = Math.ceil(self.$swal.getTimerLeft() / 1000);
            }, 100);
          },
          didClose: () => {
            clearInterval(timerInterval);
          },
        })
        .then((result) => {
          /* Read more about handling dismissals below */
          if (result.dismiss === self.$swal.DismissReason.timer) {
            this.number = Math.floor(Math.random() * 90000) + 10000;
            this.setLastViewed();
            navigateTo({ path: "/ns/" + this.slug + this.number });
          }
        });
    },
    setLastViewed() {
      let temp = this.slug + this.number;
      sessionStorage.clear();
      sessionStorage.setItem(temp, localStorage.getItem("user-schema-classes"));
      sessionStorage.setItem(
        temp + "-url",
        localStorage.getItem("user-schema-url")
      );
    },
  },
};
</script>
