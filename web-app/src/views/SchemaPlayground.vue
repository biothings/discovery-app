<template>
  <div id="playground" class="container-fluid" style="padding-top: 60px">
    <div class="bg-light text-center mt-5">
      <h1 class="logoText">SCHEMA PLAYGROUND</h1>
      <p class="text-muted">Create, Visualize and Register Your Own Schema</p>
      <p class="text-center">
        <RouterLink to="/registry"
          >Go To Registry <font-awesome-icon icon="fas fa-chevron-right"
        /></RouterLink>
      </p>
    </div>
    <div class="jumbotron bg-light col-sm-12 m-0">
      <div class="container d-flex justify-content-center align-content-center">
        <div class="pt-2 pb-2 text-center">
          <h1 class="mainTextDark text-center">GET STARTED</h1>
          <h4 class="text-muted text-center">What would you like to do?</h4>
          <RouterLink
            type="button"
            :to="{ name: 'SchemaPlayground', query: { action: 'register' } }"
            class="btn themeButton text-light m-2 px-3 py-3 btn-lg"
            :class="{ 'bg-success': choice == 'register' }"
          >
            <font-awesome-icon icon="fas fa-eye" class="text-light" /> Register
            Schema
          </RouterLink>
          <RouterLink
            type="button"
            :to="{ name: 'SchemaPlayground', query: { action: 'create' } }"
            class="btn themeButton text-light m-2 px-3 py-3 btn-lg"
            :class="{ 'bg-success': choice == 'create' }"
          >
            <font-awesome-icon icon="fas fa-code-branch" class="text-light" />
            Create Schema
          </RouterLink>
          <RouterLink
            type="button"
            :to="{ name: 'SchemaPlayground', query: { action: 'search' } }"
            class="btn themeButton text-light m-2 px-3 py-3 btn-lg"
            :class="{ 'bg-success': choice == 'search' }"
          >
            <font-awesome-icon icon="fas fa-search" class="text-light" /> Search
            Existing
          </RouterLink>
        </div>
      </div>
    </div>

    <div
      v-if="!choice"
      class="jumbotron container bg-light row m-auto d-flex justify-content-center align-items-center"
      style="min-height: 40vh"
    >
      <div class="col-sm-12 pt-5 pb-5">
        <h1 class="text-center text-muted caps mb-4 mt-4">
          Why do we need schemas?
        </h1>
        <div class="w-100">
          <div class="row m-0">
            <!-- card -->
            <div class="col-sm-12 col-md-4 p-2">
              <img src="@/assets/img/sp1-01.svg" alt="Planning" />
              <h4 class="text-center mainTextDark caps">Planning</h4>
              <div class="mt-3">
                <p class="text-muted">
                  Organize and structure your data right from the start in a way
                  that not only humans but computers can understand. A schema is
                  a blueprint that graphically depicts the structure of your
                  data.
                </p>
              </div>
            </div>
            <div class="col-sm-12 col-md-4 p-2">
              <img src="@/assets/img/sp2-01.svg" alt="Hierarchy" />
              <h4 class="text-center mainTextDark caps">Hierarchy</h4>
              <div class="mt-3">
                <p class="text-muted">
                  Schemas follow a logical hierarchical structure each with
                  properties inherited to all children. For example:
                  <small>
                    <ul class="text-muted">
                      <li>
                        <i
                          >A
                          <a href="https://schema.org/Person" target="_blank"
                            >Person</a
                          >
                          has a property of
                          <a href="https://schema.org/birthDate" target="_blank"
                            >birthDate</a
                          ></i
                        >
                      </li>
                      <li>
                        <i
                          ><a href="https://schema.org/Thing" target="_blank"
                            >Thing</a
                          >
                          &gt;
                          <a
                            href="https://schema.org/CreativeWork"
                            target="_blank"
                            >CreativeWork</a
                          >
                          &gt;
                          <a href="https://schema.org/Dataset" target="_blank"
                            >Dataset</a
                          ></i
                        >
                      </li>
                    </ul>
                  </small>
                </p>
              </div>
            </div>
            <!-- card -->
            <div class="col-sm-12 col-md-4 p-2">
              <img src="@/assets/img/sp3-01.svg" alt="Reusability" />
              <h4 class="text-center mainTextDark caps">Interoperability</h4>
              <div class="mt-3">
                <p class="text-muted">
                  Schemas allow for data to be completely understood by
                  different interfaces and let computers access, exchange,
                  integrate data in a uniform manner.<br />
                  <small
                    >- Learn about
                    <a
                      data-tippy-content="Learn More About FAIR Principles"
                      target="_blank"
                      href="https://www.go-fair.org/fair-principles/"
                      >FAIR</a
                    >
                    principles.</small
                  >
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="choice == 'register'"
      class="m-0 p-2 alert-secondary row fade-in"
      style="min-height: 50vh"
    >
      <div
        class="col-sm-12 col-md-4 align-items-stretch d-flex p-0 alert-secondary"
      >
        <div class="row m-0 shareBack">
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <img
                src="@/assets/img/paper.gif"
                alt="register"
                width="200px"
                style="border-radius: 50%"
              />
              <h4 class="text-muted caps">
                <div class="box p-top left">
                  <b class="text-muted">what can I do here?</b>
                </div>
              </h4>
            </div>
          </div>
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <span class="fa-stack fa-2x m-2 scale-in-center">
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="text-success fa-stack-2x"
                />
                <font-awesome-icon
                  icon="fas fa-eye"
                  class="fa-stack-1x text-light"
                />
              </span>
              <h6 class="text-muted caps">
                <b class="mainTextDark">Visualize</b> your schema<br />
                and browse it with ease
              </h6>
            </div>
          </div>
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <span class="fa-stack fa-2x m-2 scale-in-center">
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="text-success fa-stack-2x"
                />
                <font-awesome-icon
                  icon="fas fa-check"
                  class="fa-stack-1x text-light"
                />
              </span>
              <h6 class="text-muted caps">
                <b class="mainTextDark">Register</b> your schema<br />
                and share it with the community
              </h6>
            </div>
          </div>
        </div>
      </div>
      <div
        class="jumbotron rounded-0 col-sm-12 col-md-8 m-0 d-flex justify-content-center align-items-center grad"
      >
        <div class="col-sm-12 col-md-8">
          <h4 class="mb-3 mt-3 text-light">
            Visualize
            <font-awesome-icon icon="fas fa-arrow-right" class="text-info" />
            Register Your Schema
          </h4>
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
                  class="btn btn-info"
                  type="submit"
                >
                  Let's Go!
                </button>
              </div>
            </div>
            <div v-else>
              <h3 class="text-light">
                <font-awesome-icon
                  icon="fas fa-cog fa-spin"
                  class="text-success"
                />
                Please Wait...
              </h3>
            </div>
            <small class="text-light">Examples:</small>
            <small
              class="badge badge-dark pointer mr-1"
              @click="
                input =
                  'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'
              "
            >
              BioLink Schema
            </small>
            <small
              class="badge badge-dark pointer mr-1"
              @click="
                input =
                  'https://raw.githubusercontent.com/data2health/schemas/master/Dataset/CTSADataset.json'
              "
            >
              CTSA Dataset Schema
            </small>
          </form>
        </div>
      </div>
    </div>

    <div
      v-if="choice == 'create'"
      class="p-2 m-0 row alert-secondary fade-in"
      style="min-height: 50vh"
    >
      <div
        class="col-sm-12 col-md-4 align-items-stretch d-flex p-0 alert-secondary"
      >
        <div class="row m-0 extendBack">
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <img
                src="@/assets/img/computer.gif"
                alt="create"
                width="200px"
                style="border-radius: 50%"
              />
              <h4 class="text-muted caps">
                <div class="box p-top left">
                  <b class="text-muted">what can I do here?</b>
                </div>
              </h4>
            </div>
          </div>
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <span class="fa-stack fa-2x m-2 scale-in-center">
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="text-success fa-stack-2x"
                />
                <font-awesome-icon
                  icon="fas fa-code-branch"
                  class="fa-stack-1x text-light"
                />
              </span>
              <h6 class="text-muted caps">
                <b class="mainTextDark">Extend</b> an existing schema<br />
                and tailor it to your needs
              </h6>
            </div>
          </div>
        </div>
      </div>
      <div
        class="jumbotron rounded-0 col-sm-12 col-md-8 m-0 d-flex justify-content-center align-items-center grad"
      >
        <div class="col-sm-12 col-md-8">
          <div class="row m-0">
            <div class="col-sm-12">
              <h4 class="text-light mt-3 mb-3">Common starting points:</h4>
              <div class="d-flex align-items-center justify-content-around">
                <template v-for="item in startingPoints" :key="item">
                  <PresetBox :preset="item"></PresetBox>
                </template>
              </div>
            </div>
            <div
              class="col-sm-12 d-flex justify-content-center align-items-center"
            >
              <h4 class="text-light caps pt-3 pb-3">OR</h4>
            </div>
            <div class="col-sm-12">
              <h4 class="text-light mt-3 mb-3">Search for starting point:</h4>
              <div class="message text-center text-muted p-4">
                <h5 class="text-muted">Search for a Class</h5>
                <RouterLink
                  role="button"
                  class="btn btn-lg themeButton text-light m-3"
                  to="/registry"
                  >To Registry</RouterLink
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="choice == 'search'"
      class="p-2 m-0 alert-secondary fade-in row"
      style="min-height: 50vh"
    >
      <div
        class="col-sm-12 col-md-4 align-items-stretch d-flex p-0 alert-secondary"
      >
        <div class="row m-0 extendBack">
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <img
                src="@/assets/img/wave.gif"
                alt="search"
                width="200px"
                style="border-radius: 50%"
              />
              <h4 class="text-muted caps">
                <div class="box p-top left">
                  <b class="text-muted">what can I do here?</b>
                </div>
              </h4>
            </div>
          </div>
          <div
            class="col-sm-12 d-flex justify-content-center align-items-center text-center py-4"
          >
            <div>
              <span class="fa-stack fa-2x m-2 scale-in-center">
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="text-success fa-stack-2x"
                />
                <font-awesome-icon
                  icon="fas fa-search"
                  class="fa-stack-1x text-light"
                />
              </span>
              <h6 class="text-muted caps">
                <b class="text-muted">Search schemas and classes available</b>
              </h6>
            </div>
          </div>
        </div>
      </div>
      <div
        class="jumbotron rounded-0 col-sm-12 col-md-8 m-0 d-flex justify-content-center align-items-center grad"
      >
        <div
          class="alert bg-light text-center text-light p-4 rounded col-sm-12"
        >
          <h5 class="text-muted">Search schemas and classes available</h5>
          <h6 class="text-muted">
            Find and compare existing classes you can extend to create your own.
          </h6>
          <RouterLink
            role="button"
            class="btn btn-lg themeButton text-light m-3"
            to="/registry"
            >To Registry</RouterLink
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PresetBox from "../components/PresetBox.vue";

import woohoo from "@/assets/img/woohoo-01.svg";
import oh_no from "@/assets/img/oh_no-01.svg";
import dde_logo from "@/assets/img/dde-logo-o.svg";
import not_right from "@/assets/img/not_right-01.svg";

export default {
  name: "SchemaPlayground",
  data: function () {
    return {
      choice: "",
      input: "",
      suggestedURL: "",
      slug: "",
      number: "",
      choice: "",
      loading: false,
      startingPoints: [
        {
          namespace: "biomedical",
          prefix: "bts",
          name: "BioMedicalDataset",
          guide: "/guide",
          description: "A schema describing a BioMedical Dataset",
        },
      ],
    };
  },
  components: {
    PresetBox,
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
    "$route.query.action": {
      immediate: true,
      handler: function (v) {
        this.choice = v;
      },
    },
  },
  methods: {
    handleChoice(choice) {
      var self = this;
      if (choice === "register") {
        this.$swal
          .fire({
            title: "Visualize a schema",
            text: "Paste your link here:",
            input: "text",
            inputAttributes: {
              autocapitalize: "off",
            },
            showCancelButton: true,
            confirmButtonText: "Go",
            showLoaderOnConfirm: true,
            preConfirm: (value) => {
              if (value.includes("blob") || value.includes("github.com")) {
                self.suggestedURL = value
                  .replace("blob/", "")
                  .replace("github.com", "raw.githubusercontent.com")
                  .replace("www.github.com", "raw.githubusercontent.com");
                this.$swal({
                  title: "Link Converted",
                  imageAlt: "Warning",

                  customClass: "scale-in-center",
                  html:
                    "<p>We noticed that was not a raw data link. We have converted it to: </p> " +
                    '<p><a target="_blank" href="' +
                    self.suggestedURL +
                    '">' +
                    self.suggestedURL +
                    "</a></p>" +
                    "<p>Proceed with this link?</p>",
                  showCancelButton: true,
                  confirmButtonColor: "#5C3069",
                  cancelButtonColor: "#006476",
                  confirmButtonText: "Yes, use this link!",
                }).then((result) => {
                  if (result.value) {
                    return result.value;
                  }
                });
              }
            },
            allowOutsideClick: () => !this.$swal.isLoading(),
          })
          .then((result) => {
            if (result.value) {
              self.input = result.value;
              this.sendRequest();
            }
          });
      } else {
        self.$router.push({ path: "/registry" });
      }
    },
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
      axios
        .get(self.$apiUrl + "/api/view?url=" + self.input)
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
          willClose: () => {
            clearInterval(timerInterval);
          },
        })
        .then((result) => {
          /* Read more about handling dismissals below */
          if (result.dismiss === self.$swal.DismissReason.timer) {
            this.number = Math.floor(Math.random() * 90000) + 10000;
            this.setLastViewed();
            self.$router.push({ path: "/view/" + this.slug + this.number });
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
  components: { PresetBox },
};
</script>
