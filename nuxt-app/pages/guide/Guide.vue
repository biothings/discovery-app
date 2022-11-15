<template>
  <div
    id="guide"
    class="container-fluid pt-5 m-auto col-sm-12 col-md-10 col-lg-10 col-xl-8"
    style="min-height: 90vh"
    v-cloak
  >
    <div id="tip-cont">
      <img id="puff" src="@/assets/img/puff.gif" />
      <audio id="pop-sound" :src="popSound"></audio>
      <div class="p-2 bg-light text-center mt-5">
        <h6 class="logoText">DISCOVERY GUIDE</h6>
        <p class="text-muted">
          Follow best practices to make your metadata more findable
        </p>
        <a :href="'/dataset?guide=' + $router.currentRoute"
          >Browse other registered metadata using this guide
          <font-awesome-icon icon="fas fa-chevron-right"></font-awesome-icon
        ></a>
      </div>
      <h4 v-text="readableName(schemaName)" class="text-center logoText"></h4>
      <div id="jsonTable">
        <!-- BULK -->
        <div v-if="jsonItems.length" class="alert grad">
          <div class="p-1 d-flex justify-content-around align-items-center">
            <small
              class="text-light"
              v-text="jsonItems.length + ' documents found'"
            ></small>
            <div class="alert p-1 m-1 d-flex">
              <span
                v-for="(value, field) in bulkReport"
                :key="field"
                class="mr-2 pillType"
              >
                <span class="alert-muted" v-text="field"></span>
                <span
                  :class="{
                    'bg-success text-light': field == 'Registered',
                    'bg-info text-light': field == 'Updated',
                    'bg-danger text-light': field == 'Failed',
                    'warning-light text-dark': field == 'Exists',
                  }"
                  v-text="value.length"
                ></span>
              </span>
            </div>
            <small
              @click="restartBulk()"
              class="pointer text-light badge badge-danger"
              ><font-awesome-icon icon="fas fa-undo"></font-awesome-icon> Start
              Over</small
            >
            <button
              v-if="!beginBulkRegistration"
              @click.prevent="startBulk()"
              class="btn btn-success text-light m-1"
              aria-label="Bulk Register Metadata"
            >
              <font-awesome-icon icon="fas fa-registered"></font-awesome-icon>
              Register Metadata
            </button>
          </div>
          <div style="height: 700px; overflow: scroll; resize: vertical">
            <table
              class="m-0 table table-sm table-light table-hover table-striped"
            >
              <thead>
                <th>
                  <small>Name</small>
                </th>
                <th>
                  <small>Result/Details</small>
                </th>
                <th>
                  <small>Options</small>
                </th>
                <th>
                  <small>Status</small>
                </th>
              </thead>
              <colgroup>
                <col span="1" style="width: 30%" />
                <col span="1" style="width: 30%" />
                <col span="1" style="width: 30%" />
                <col span="1" style="width: 10%" />
              </colgroup>
              <tbody style="max-height: 500px; overflow: scroll">
                <template v-for="(item, i) in jsonItems">
                  <JSONItem
                    :item="item"
                    :number="i + 1"
                    :username="userInfo.login"
                  ></JSONItem>
                </template>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- bulk end -->
      <div id="widget" class="mb-5 grad rounded">
        <!-- EDIT EXISTING -->
        <div id="editMessage" v-if="editingID">
          <div class="p-1 alert-warning d-flex">
            <h4 class="text-info d-inline-block p-2">
              <span class="fa-stack">
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="fa-stack-2x"
                ></font-awesome-icon>
                <font-awesome-icon
                  icon="fas fa-pencil-alt"
                  class="fa-stack-1x fa-inverse"
                ></font-awesome-icon>
              </span>
            </h4>
            <small class="d-inline-block">
              <b class="text-danger">Edit Mode:</b> You are editing an existing
              record. You can add or change any allowed field.
              <code>identifier</code> field is disabled as this is the unique
              identifier for each entry. If this is not what you intend to do
              please start over.
            </small>
          </div>
        </div>
        <div>
          <div
            class="actions bg-dark p-2 rounded d-flex align-items-center justify-content-start"
          >
            <span
              class="fa-stack fa-1x pointer tip mr-2"
              :data-tippy-content="'Logged in as ' + userInfo.login"
              v-if="userInfo && userInfo.login"
            >
              <font-awesome-icon
                icon="fas fa-circle"
                class="text-success fa-stack-2x"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-user-check"
                class="fa-stack-1x fa-inverse"
              ></font-awesome-icon>
            </span>
            <a
              class="nav-link active text-primary mr-2"
              :href="'/login?next=' + $router.currentRoute"
              v-if="userInfo && !userInfo.login"
            >
              <span
                class="fa-stack fa-1x pointer tip"
                data-tippy-content="Click to log in"
              >
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="text-primary fa-stack-2x"
                ></font-awesome-icon>
                <font-awesome-icon
                  icon="fas fa-sign-in-alt"
                  class="fa-stack-1x fa-inverse"
                ></font-awesome-icon>
              </span>
            </a>
            <span
              class="fa-stack fa-1x pointer tip mr-2"
              data-tippy-content="Start Over"
              @click="reset()"
              :class="{
                'disabled notallowed': !validation,
                pointer: validation,
              }"
            >
              <font-awesome-icon
                icon="fas fa-circle"
                class="text-success fa-stack-2x"
                :class="{
                  'text-muted': !validation,
                  'text-danger': validation,
                }"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-undo"
                class="fa-stack-1x fa-inverse"
              ></font-awesome-icon>
            </span>
            <span
              class="fa-stack fa-1x pointer tip mr-2"
              data-tippy-content="Preview Progress"
              @click="getPreview()"
              :class="{
                'disabled notallowed': !validation,
                pointer: validation,
              }"
            >
              <font-awesome-icon
                icon="fas fa-circle"
                class="text-success fa-stack-2x"
                :class="{
                  'text-muted': !validation,
                  mainTextDark: validation,
                }"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-code"
                class="fa-stack-1x fa-inverse"
              ></font-awesome-icon>
            </span>
            <span
              class="fa-stack fa-1x pointer tip mr-2"
              data-tippy-content="Import Metadata"
              @click="loadData()"
              v-show="validation"
            >
              <font-awesome-icon
                icon="fas fa-circle"
                class="text-success fa-stack-2x"
                :class="{ 'text-muted': !validation, mainTextDark: validation }"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-file-import"
                class="fa-stack-1x fa-inverse"
              ></font-awesome-icon>
            </span>
            <span
              class="fa-stack fa-1x pointer tip mr-2"
              data-tippy-content="Bulk Registration"
              @click="handleBulk()"
              v-show="validation"
            >
              <font-awesome-icon
                icon="fas fa-circle"
                class="text-success fa-stack-2x"
                :class="[bulkMode ? 'text-warning' : 'mainTextDark']"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-registered"
                class="fa-stack-1x fa-inverse"
              ></font-awesome-icon>
            </span>
            <div
              class="pillType tip pointer"
              @click="viewErrors()"
              data-tippy-content="Issues Details"
              :class="{ 'shake-horizontal': !valid }"
              style="outline: none !important"
            >
              <span class="alert-muted">issues</span>
              <span
                class="text-light"
                v-text="errors.length"
                :class="[valid ? 'bg-success' : 'bg-danger']"
              ></span>
            </div>
          </div>
        </div>

        <div
          v-if="userInfo && !userInfo.login"
          class="widgetContainer bg-light jumbotron text-center m-1"
        >
          <div class="alert text-danger text-center p-5">
            <h5>You must be logged in to proceed</h5>
            <h6>
              <a :href="'/login?next=' + $router.currentRoute"
                >click here to log in</a
              >
            </h6>
          </div>
        </div>

        <div v-else class="widgetContainer bg-light text-center">
          <template v-if="step === 1 && !bulkMode">
            <!-- STARTING POINT -->
            <h4 class="logoText">Metadata</h4>
            <p class="text-muted">
              Select the type of metadata you are interested in creating.
            </p>
            <div>
              <template v-for="item in presets">
                <button
                  @click="setStartingPoint(item)"
                  class="btn themeButton text-light mr-2 tip"
                  v-text="item.name"
                  :data-tippy-content="item.description"
                ></button>
              </template>
            </div>
          </template>
          <!-- OPTIONAL PORTALS -->
          <template v-if="step === 2 && !bulkMode">
            <h4 class="logoText">Discovery Portals</h4>
            <p class="text-muted">
              Select the portals you are interested in. Each will add fields
              required in order to be discovered by that portal.
            </p>
            <form @submit.prevent="getFormValues()">
              <template v-for="item in portals">
                <div class="p-2 text-left w-50 m-auto">
                  <input
                    class="form-check-input slider"
                    type="checkbox"
                    name="portal"
                    :id="item.displayName"
                    :value="item.name"
                    :checked="item.selected"
                    @click="item.selected = !item.selected"
                  />
                  <label class="form-check-label" :for="item.displayName">
                    <span v-text="item.displayName"></span>
                    <font-awesome-icon
                      icon="fas fa-info-circle"
                      class="text-info desc"
                      :data-tippy-content="item.description"
                    ></font-awesome-icon>
                  </label>
                </div>
              </template>
              <button class="btn themeButton text-light mt-3" type="submit">
                NEXT
                <font-awesome-icon
                  icon="fas fa-chevron-right"
                ></font-awesome-icon>
              </button>
            </form>
          </template>

          <template v-if="step === 3 && !bulkMode">
            <Property v-show="validation" :type="'REQUIRED'"></Property>
          </template>

          <template v-if="step === 4 && !bulkMode">
            <Property v-show="validation" :type="'RECOMMENDED'"></Property>
          </template>

          <template v-if="step === 5 && !bulkMode">
            <template v-if="editingID">
              <h1 class="logoText">Save Your Changes</h1>
              <div class="p-5 text-center m-3">
                <p class="text-muted text-center">
                  <b>Are you all done?</b> Click <b>Save Changes</b> to proceed.
                  <br />You will leave this page after successfully saving
                  changes to this metadata.
                </p>
                <a
                  class="btn btn-lg btn-success text-light desc"
                  :class="{
                    'disabled text-muted notallowed': !isComplete,
                    'bg-success text-light pointer': isComplete,
                  }"
                  @click="handleEdits()"
                  :data-tippy-content="[
                    !isComplete
                      ? 'Available when all required fields are complete'
                      : 'Click to register your metadata',
                  ]"
                >
                  <small>
                    <font-awesome-icon icon="fas fa-check"></font-awesome-icon>
                    Save Changes
                  </small>
                </a>
              </div>
            </template>
            <template v-else>
              <template v-if="$router.currentRoute == '/guide/n3c/dataset'">
                <h1 class="logoText">N3C Dataset Request</h1>
                <div class="p-5 text-center m-3">
                  <img
                    src="@/assets/img/N3C.png"
                    width="250px"
                    alt="N3C"
                    class="text-center"
                  />
                  <p class="text-muted text-center">
                    <b>Are you all done?</b> Click <b>Submit Request</b> to
                    proceed.
                  </p>
                  <a
                    class="btn btn-lg btn-success text-light"
                    :class="{
                      'disabled text-muted notallowed': !isComplete,
                      'bg-success text-light pointer': isComplete,
                    }"
                    @click="handleRegistration()"
                  >
                    <small>
                      <font-awesome-icon
                        icon="fas fa-check"
                      ></font-awesome-icon>
                      Submit Request
                    </small>
                  </a>
                </div>
              </template>
              <template v-else>
                <h1 class="logoText">Registration</h1>
                <div class="p-5 text-center m-3">
                  <p class="text-muted text-center">
                    <b>Are you all done?</b> Click <b>Register</b> to proceed.
                    <br />You will leave this page after successfully
                    registering this metadata.
                  </p>
                  <a
                    class="btn btn-lg btn-success text-light desc"
                    :class="{
                      'disabled text-muted notallowed': !isComplete,
                      'bg-success text-light pointer': isComplete,
                    }"
                    @click="handleRegistration()"
                    :data-tippy-content="[
                      !isComplete
                        ? 'Available when all required fields are complete'
                        : 'Click to register your metadata',
                    ]"
                  >
                    <small>
                      <font-awesome-icon
                        icon="fas fa-check"
                      ></font-awesome-icon>
                      Register
                    </small>
                  </a>
                </div>
              </template>
            </template>
            <div class="col-sm-12">
              <div class="row">
                <div class="col-sm-12 text-center p-3">
                  <h4
                    class="bold"
                    :class="{
                      'text-info': fieldsleftRegistration !== 0,
                      'text-success': fieldsleftRegistration !== 0,
                    }"
                  >
                    <span v-show="fieldsleftRegistration === 0"
                      >Great Job!
                    </span>
                    <span
                      v-text="
                        Math.ceil((totals.complete / totals.total) * 100) +
                        '% COMPLETE'
                      "
                    ></span>
                  </h4>
                  <small class="text-info">
                    (<span v-text="totals.complete"></span>/<span
                      v-text="totals.total"
                    ></span
                    >)</small
                  >
                </div>
              </div>
              <div
                v-if="fieldsleftRegistration !== 0"
                class="col-sm-12 text-center p-3 rounded alert-light m-2"
              >
                <h4 class="text-muted">
                  Only
                  <span
                    class="text-danger bold"
                    v-text="fieldsleftRegistration"
                  ></span>
                  fields left!
                </h4>
                <button class="btn themeButton text-light" @click="goToStep(4)">
                  Fill Out Now
                </button>
              </div>
              <div v-else class="col-sm-12 text-center p-3 rounded m-2">
                <button
                  class="btn btn-danger text-light"
                  @click="goToStep(step - 1)"
                >
                  <font-awesome-icon
                    icon="fas fa-chevron-left"
                  ></font-awesome-icon>
                  BACK
                </button>
              </div>
              <div
                class="d-flex justify-content-center flex-wrap"
                v-if="categoryTotals"
              >
                <template
                  v-for="(subcats, cat, i) in categoryTotals"
                  :key="cat + i"
                >
                  <Category
                    class="fade-in"
                    :cat="cat"
                    :subcats="subcats"
                  ></Category>
                </template>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import tippy from "tippy.js";
import Papa from "papaparse";
import { mapGetters } from "vuex";
import Notify from "simple-notify";

import popSound from "@/assets/img/pop.wav";
import metaPic from "@/assets/img/metadata.png";

import Property from "~~/components/guide/Property.vue";
import Category from "~~/components/guide/Category.vue";
import JSONItem from "~~/components/guide/JSONItem.vue";

export default {
  name: "Guide",
  head() {
    return {
      title: "DDE | Resource Discovery Guide",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/m2HH6cYD/guide.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/m2HH6cYD/guide.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/guide",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/guide",
        },
        {
          property: "og:description",
          content: "Follow best practices to make your metadata more findable",
        },
        {
          name: "description",
          content: "Follow best practices to make your metadata more findable",
        },
        {
          name: "twitter:card",
          content: "Follow best practices to make your metadata more findable",
        },
      ],
    };
  },
  props: ["guide_query", "presets"],
  components: {
    Property,
    Category,
    JSONItem,
  },
  data: function () {
    return {
      popSound: popSound,
      //   portals: [
      //          {'namespace': 'google',
      //           'prefix': 'bts',
      //           'name': 'Google',
      //           'displayName': 'Google Dataset Search',
      //           'description': 'A list of metadata fields required and recommended by Google Dataset Search Engine. <a target="_blank" href="https://developers.google.com/search/docs/data-types/dataset">Learn More<a/>',
      //           'selected': 1},
      //          {'namespace': 'datacite',
      //           'prefix': 'bts',
      //           'name': 'DataCite',
      //           'displayName': 'DataCite',
      //           'description': 'A list of core metadata properties chosen for an accurate and consistent identification of a resource for citation and retrieval purposes by DataCite. <a target="_blank" href="https://schema.datacite.org/">Learn More<a/>',
      //           'selected': 0},
      //          ],
      portals: [],
      guideQuery: "",
      bulkMode: false,
      apiUrl: "",
    };
  },
  computed: {
    ...mapGetters({
      bulkReport: "getBulkReport",
      beginBulkRegistration: "beginBulkRegistration",
      schemaName: "getSchemaName",
      editingID: "editingID",
      validation: "getValidation",
      valid: "getValidStatus",
      errors: "getErrors",
      isComplete: "isComplete",
      totals: "getTotals",
      categoryTotals: "getCategoryTotals",
      startingPoint: "startingPoint",
      step: "getStep",
      jsonItems: "getBulkJSONItems",
      fieldsleftRegistration: "fieldsLeft",
      userInfo: "userInfo",
      loading: "loading",
    }),
  },
  watch: {
    step: function (s) {
      if (s === "5") {
        this.$store.getters.getCategoryTotals;
        this.$store.getters.getTotals;
      }
    },
  },
  methods: {
    startBulk() {
      this.$store.commit("toggleBeginBulkRegistration");
    },
    checkOverriddenID(id) {
      let self = this;
      axios
        .get(
          self.apiUrl +
            `/api/dataset/query?size=100&q=identifier:"${encodeURIComponent(
              id
            )}"&meta=true`
        )
        .then((res) => {
          if (
            res.data.hits.length == 1 &&
            Object.hasOwnProperty.call(res.data.hits[0], "_id")
          ) {
            //turn on edit mode
            self.$store.commit("setEditMode", { id: res.data.hits[0]["_id"] });
            return true;
          } else {
            return false;
          }
        })
        .catch((err) => {
          return false;
        });
    },
    handleEdits() {
      var self = this;

      if (self.isComplete && self.editingID) {
        self.$store.commit("formPreviewForGuide");
        let output = self.$store.getters.getOutput;
        self.$store.commit("setLoading", { value: true });

        let schema = self.$store.getters.schema;

        let config = {
          headers: {
            "content-type": "application/json",
          },
        };

        axios
          .put(self.apiUrl + "/api/dataset/" + self.editingID, output, config)
          .then((res) => {
            self.$store.commit("setLoading", { value: false });
            if (res.data.success) {
              sessionStorage.removeItem("guideProgress");

              self.$gtag.event("click", {
                event_category: "dataset_edited",
                event_label: self.$router.currentRoute,
                event_value: 1,
              });

              let timerInterval;
              self.$swal.fire({
                icon: "success",
                title: "Changes saved!",
                confirmButtonColor: "#5C3069",
                cancelButtonColor: "#006476",

                customClass: "scale-in-center",
                html: "Taking you to your dataset page in <strong></strong> seconds.",
                timer: 3000,
                onBeforeOpen: () => {
                  const content = self.$swal.getContent();
                  const $ = content.querySelector.bind(content);
                  self.$swal.showLoading();
                  timerInterval = setInterval(() => {
                    self.$swal
                      .getContent()
                      .querySelector("strong").textContent = (
                      self.$swal.getTimerLeft() / 1000
                    ).toFixed(0);
                  }, 100);
                },
                onClose: () => {
                  clearInterval(timerInterval);
                  self.$store.dispatch("reset");
                  self.$router.push({ path: "/dataset/" + self.editingID });
                },
              });
            } else {
              try {
                self.$swal.fire({
                  type: "error",
                  position: "top center",
                  confirmButtonColor: "#5C3069",
                  cancelButtonColor: "#006476",
                  title: "Saving edits failed because: ",

                  customClass: "scale-in-center",
                  text: res.data.reason,
                });
              } catch (e) {
                throw e;
              }
            }
          })
          .catch((err) => {
            self.$store.commit("setLoading", { value: false });
            let culprit = "<h6>" + err.response.data.error + "</h6>";
            if (err.response.data && err.response.data.path) {
              culprit +=
                "<h5>Culprit: <b class='text-danger'>" +
                err.response.data.path +
                "</b></h5>";
            }
            if (err.response.data.parent && err.response.data.parent.path) {
              if (true) {
                culprit +=
                  "<h5>Under: <b class='text-danger'>" +
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
            self.$swal.fire({
              type: "error",
              position: "top center",
              title: "Saving edits failed because: ",
              confirmButtonColor: "#5C3069",
              cancelButtonColor: "#006476",

              customClass: "scale-in-center",
              html: culprit,
              footer: "<small>Validation Error</small>",
            });
            throw err;
          });

        self.$store.commit("setLoading", { value: true });
      }
    },
    getAndLoadSchema(url) {
      var self = this;
      self.$store.commit("setLoading", { value: true });
      axios
        .get(url)
        .then((res) => {
          self.$store.commit("setLoading", { value: false });
          var payload = {};
          payload["schema"] = res.data;
          self.$store.commit("saveSchema", payload);
        })
        .catch((err) => {
          self.$store.commit("setLoading", { value: false });
          new Notify({
            status: "error",
            title: "Guide Error",
            text: "Failed to load schema",
            effect: "fade",
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: true,
            autotimeout: 3000,
            gap: 20,
            distance: 20,
            type: 1,
            position: "right top",
          });
          throw err;
        });
    },
    getStartingPointSchema(item) {
      let self = this;
      self.$store.commit("setLoading", { value: true });
      let url =
        self.apiUrl +
        "/api/registry/" +
        item.namespace +
        "/" +
        item.prefix +
        ":" +
        item.name;
      axios
        .get(url)
        .then((res) => {
          var payload = {};
          payload["name"] = item.name;
          self.$store.commit("saveSchemaName", payload);
          self.parseData(res.data);

          // IF ANY PORTALS AND IF ANY ARE SELECTED
          if (self.portals && self.portals.length) {
            for (var i = 0; i < self.portals.length; i++) {
              if (self.portals[i]["selected"]) {
                axios
                  .get(
                    self.apiUrl +
                      "/api/registry/" +
                      self.portals[i].namespace +
                      "/" +
                      self.portals[i].prefix +
                      ":" +
                      self.portals[i].name
                  )
                  .then((result) => {
                    var payload = {};
                    payload["portal"] = result.data;
                    self.$store.commit("addPortalSchema", payload);

                    var payload = {};
                    payload["origin"] = result.data.label;
                    payload["catprops"] = result.data.validation.properties;
                    if (result.data.validation.required) {
                      payload["catpropsrequired"] =
                        result.data.validation.required;
                      self.reqfields = result.data.validation.required;
                    } else {
                      payload["catpropsrequired"] = [];
                    }
                    self.$store.commit("mergeCategoryProps", payload);
                  })
                  .catch((error) => {
                    throw error;
                  });
              }
            }
          }
          self.$store.commit("setLoading", { value: false });
        })
        .catch((err) => {
          self.$store.commit("setLoading", { value: false });
          try {
            self.$swal.fire({
              type: "error",
              position: "center",
              title: "Failed because: ",
              text: err,
            });
          } catch (e) {
            throw e;
          }
          throw err;
        });
    },
    parseData(data) {
      let self = this;
      let schemaName = self.$store.getters.getSchemaName;
      console.log("SN", schemaName);

      if (data.hits) {
        for (var i = 0; i < data.hits.length; i++) {
          if (data.hits[i].hasOwnProperty("name")) {
            if (data.hits[i].name.includes(schemaName)) {
              var payload = {};
              payload["schema"] = self.assignCategories(data.hits[i]);
              self.$store.commit("saveSchema", payload);
            }
          } else if (data.hits[i].hasOwnProperty("label")) {
            if (data.hits[i].label.includes(schemaName)) {
              var payload = {};
              payload["schema"] = self.assignCategories(data.hits[i]);
              self.$store.commit("saveSchema", payload);
            }
          }
        }
      } else {
        if (data.hasOwnProperty("name")) {
          if (data.name.includes(schemaName)) {
            var payload = {};
            payload["schema"] = data;
            self.$store.commit("saveSchema", payload);
          }
        } else if (data.hasOwnProperty("label")) {
          if (data.label.includes(schemaName)) {
            var payload = {};
            payload["schema"] = data;
            self.$store.commit("saveSchema", payload);
          }
        }
      }
      // check for saved progress
      self.checkProgress();
    },
    assignCategories(schema) {
      var self = this;
      if (schema.hasOwnProperty("validation")) {
        for (prop in schema["validation"]["properties"]) {
          //assign if found
          schema["validation"]["properties"][prop]["categories"] = [];
          for (category in self.categories) {
            for (var subcategory in self.categories[category]) {
              if (self.categories[category][subcategory].includes(prop)) {
                let cat = {
                  category: category,
                  subcategory: subcategory,
                };
                schema["validation"]["properties"][prop]["categories"].unshift(
                  cat
                );
              }
            }
          }
        }
        return schema;
      } else {
        return schema;
      }
    },
    reset() {
      let self = this;
      if (this.validation) {
        self.$swal
          .fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",

            customClass: "scale-in-center",
            showCancelButton: true,
            confirmButtonColor: "#5C3069",
            cancelButtonColor: "#006476",
            confirmButtonText: "Yes, start over",
          })
          .then((result) => {
            if (result.value) {
              self.$store.dispatch("reset");
              sessionStorage.removeItem("guideProgress");
              self.$router.go();
            }
          });
      }
    },
    restartBulk() {
      let self = this;
      self.$swal
        .fire({
          title: "Are you sure?",
          text: "You will lose any changes to this file...",

          customClass: "scale-in-center",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          confirmButtonText: "Yes, start over",
        })
        .then((result) => {
          if (result.value) {
            location.reload();
          }
        });
    },
    isRequired(propname) {
      let req = this.$store.getters.getValidation["required"];
      if (req.includes(propname)) {
        return true;
      } else {
        return false;
      }
    },
    selectProp(propname) {
      var payload = {};
      payload["select"] = propname;
      this.$store.commit("markSelected", payload);
    },
    getPreview() {
      let self = this;
      this.$store.commit("formPreviewForGuide");
      this.$swal.fire({
        position: "center",
        confirmButtonColor: "#5C3069",
        cancelButtonColor: "#006476",
        customClass: "scale-in-center",
        html: `<h6 class="text-center mainTextDark">Preview</h6><div class="text-left p-1 previewBox bg-dark"><pre id="previewJSON"></pre></div>`,
        didOpen: function () {
          renderjson.set_show_to_level(5);
          document
            .getElementById("previewJSON")
            .appendChild(renderjson(self.$store.getters.getPreview));
        },
      });
    },
    handleRegistration() {
      var self = this;

      if (this.isComplete) {
        self.$store.commit("formPreviewForGuide");
        let output = self.$store.getters.getOutput;
        self.$store.commit("setLoading", { value: true });

        let schema = self.$store.getters.schema;

        let config = {
          headers: {
            "content-type": "application/json",
          },
        };

        axios
          .post(
            self.apiUrl +
              "/api/dataset?schema=" +
              schema["namespace"] +
              "::" +
              schema["prefix"] +
              ":" +
              schema["label"] +
              "&guide=" +
              self.startingPoint["guide"],
            output,
            config
          )
          .then((res) => {
            self.$store.commit("setLoading", { value: false });
            if (res.data.success) {
              sessionStorage.removeItem("guideProgress");

              self.$gtag.event("click", {
                event_category: "dataset_added",
                event_label: self.$router.currentRoute,
                event_value: 1,
              });

              if (self.$router.currentRoute == "/guide/n3c/dataset") {
                self.$swal.fire({
                  icon: "success",
                  title: "Registration Successful",
                  position: "center",
                  confirmButtonColor: "#5C3069",
                  cancelButtonColor: "#006476",

                  customClass: "scale-in-center",
                  html:
                    `<div class="row m-0">
                            <div class="col-sm-12 logoText">
                              <h3>Your request is submitted, we will review it and get back to you soon.</h3>
                            </div>
                            <div class="col-sm-12">
                              <h5>
                                <a href="/dataset/` +
                    res.data.id +
                    `" target="_blank" rel="nonreferrer">Click here</a> to view your submission.
                              </h5>
                            </div>
                            <div class="col-sm-12">
                              <h5>
                                <a href="/guide/n3c/dataset">Click here</a> to submit another request.
                              </h5>
                            </div>
                            <div class="col-sm-12">
                              <h5>
                                <a class="text-danger" href="/">I'm all done!</a>
                              </h5>
                            </div>
                          </div>`,
                  onClose: () => {
                    self.$store.dispatch("reset");
                    self.$router.push('/dataset');
                  },
                });
              } else {
                let timerInterval;
                self.$swal.fire({
                  icon: "success",
                  title: "Registration Successful",
                  confirmButtonColor: "#5C3069",
                  cancelButtonColor: "#006476",

                  customClass: "scale-in-center",
                  html: "Taking you to your dataset page in <strong></strong> seconds.",
                  timer: 3000,
                  onBeforeOpen: () => {
                    const content = self.$swal.getContent();
                    const $ = content.querySelector.bind(content);
                    self.$swal.showLoading();
                    timerInterval = setInterval(() => {
                      self.$swal
                        .getContent()
                        .querySelector("strong").textContent = (
                        self.$swal.getTimerLeft() / 1000
                      ).toFixed(0);
                    }, 100);
                  },
                  onClose: () => {
                    clearInterval(timerInterval);
                    self.$store.dispatch("reset");
                    self.$router.push({ path: "/dataset/" + res.data.id });
                  },
                });
              }
            } else {
              try {
                self.$swal.fire({
                  type: "error",
                  position: "top center",
                  confirmButtonColor: "#5C3069",
                  cancelButtonColor: "#006476",
                  title: "Registration failed because: ",

                  customClass: "scale-in-center",
                  text: res.data.reason,
                });
              } catch (e) {
                throw e;
              }
            }
          })
          .catch((err) => {
            self.$store.commit("setLoading", { value: false });
            let culprit = "<h6>" + err.response.data.error + "</h6>";
            if (err.response.data && err.response.data.path) {
              culprit +=
                "<h5>Culprit: <b class='text-danger'>" +
                err.response.data.path +
                "</b></h5>";
            }
            if (err.response.data.parent && err.response.data.parent.path) {
              if (true) {
                culprit +=
                  "<h5>Under: <b class='text-danger'>" +
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
            self.$swal.fire({
              type: "error",
              position: "top center",
              title: "Registration failed because: ",
              confirmButtonColor: "#5C3069",
              cancelButtonColor: "#006476",

              customClass: "scale-in-center",
              html: culprit,
              footer: "<small>Validation Error</small>",
            });
            throw err;
          });

        self.$store.commit("setLoading", { value: true });
      }
    },
    showHelp() {
      self.$swal.fire({
        title: "Dataset Guide",
        html: `<p>
                    After selecting a starting point you will be able complete a series of fields. It's really easy and fast! Here's a quick introduction to the layout:
                  </p>
                  <small>
                    <ul class="text-left">
                      <li>
                        1. Log-in status
                      </li>
                      <li>
                        2. Start over from scratch
                      </li>
                      <li>
                        3. Preview your progress
                      </li>
                      <li>
                        4. Download your progress (Available after completing all required fields)
                      </li>
                      <li>
                        5. Register your dataset (Available after completing all required fields)
                      </li>
                      <li>
                        6. All fields available to complete (* Required)
                      </li>
                      <li>
                        7. Progress bar
                      </li>
                      <li>
                        8. Complete fields
                      </li>
                      <li>
                        9. Current field clicked
                      </li>
                      <li>
                        10. Actions: Save & Close and Clear Field
                      </li>
                    </ul>
                  </small>`,
        footer: "",
        width: "52em",
        confirmButtonColor: "#5C3069",
        cancelButtonColor: "#006476",
        confirmButtonText: "Ready!",

        customClass: "scale-in-center",
        imageUrl: metaPic,
        imageAlt: "Dataset Editor",
      });
    },
    handleBulk() {
      var self = this;
      self.bulkMode = !self.bulkMode;
      if (self.bulkMode) {
        self.getFile("json");
      }
    },
    async getFile(type) {
      var self = this;

      if (type == "json") {
        const { value: file } = await self.$swal.fire({
          title: "Bulk registration",
          html: `<p>Select JSON file to start.</p>`,
          input: "file",
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",

          customClass: "scale-in-center",
          footer: `<p class="text-danger"><strong>🚨 Please note there is a 100 document limit.</strong></p>`,
          inputAttributes: {
            accept: "json",
            "aria-label": "Upload your file",
          },
        });

        if (file) {
          try {
            const blob = new Blob([file], { type: "application/json" });

            const fr = new FileReader();

            fr.addEventListener("load", (e) => {
              var payload = {};
              let json = JSON.parse(fr.result);
              if (json.length < 101) {
                payload["items"] = json;
                self.$store.commit("saveBulkItems", payload);
              } else {
                self.$swal.fire({
                  icon: "error",
                  title: "Over Limit",
                  text:
                    json.length + " items. Please submit 100 items at a time.",
                });
              }
            });

            fr.readAsText(blob);
          } catch (e) {
            self.$swal.fire({
              icon: "error",
              title: "Something is wrong..",
              text: e,
            });
          }
        }
      } else if (type == "csv") {
        const { value: file } = await self.$swal.fire({
          title: "Select file",
          input: "file",
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",

          customClass: "scale-in-center",
          footer: `<small class="text-danger">Registration will be triggered automatically when upload finishes.</small>`,
          inputAttributes: {
            accept: "csv",
            "aria-label": "Upload your file",
          },
        });
        if (file) {
          Papa.parse(file, {
            header: true,
            delimeter: ";",
            complete: function (results) {
              self.parseCSVData(results.data);
            },
          });
        }
      }
    },
    parseCSVData(data) {
      let self = this;
      let items = [];
      for (let i = 0; i < data.length; i++) {
        let currentDoc = data[i];
        let newDoc = {};
        for (let key in currentDoc) {
          if (key.includes(".")) {
            let keyPath = self.separateByDelimeter(key, ".");
            self.createNested(newDoc, keyPath, currentDoc[key]);
          } else {
            let v = currentDoc[key];
            if (key && v) {
              self.createNested(newDoc, [key], v);
            }
          }
        }
        items.push(newDoc);
        // console.log("%c --------------------------------------------",'color:green')
        // console.log('%c '+JSON.stringify(items,null,2),'color:lightgreen')
        // console.log("%c --------------------------------------------",'color:green')

        var payload = {};
        payload["items"] = items;
        self.$store.commit("saveBulkItems", payload);
      }
    },
    createNested(obj, keyPath, value) {
      var self = this;
      lastKeyIndex = keyPath.length - 1;
      for (var i = 0; i < lastKeyIndex; ++i) {
        key = keyPath[i];
        if (!(key in obj)) {
          obj[key] = {};
        }
        obj = obj[key];
      }
      obj[keyPath[lastKeyIndex]] = value;
      return obj;
    },
    separateByDelimeter(value, delimeter) {
      if (value.includes(delimeter)) {
        return value.split(delimeter);
      } else {
        return value;
      }
    },
    loadData() {
      var self = this;
      self.$swal
        .fire({
          title: "Import Metadata",
          text: "Select the source of metadata",
          input: "select",
          inputOptions: {
            giturl: "Hosted metadata on GitHub (raw url)",
            registered:
              "Copy metadata from an existing dataset authored by you",
            text: "JSON metadata text",
          },
          footer:
            "Note: If you are loading an already registered item, this will trigger edit mode in which you are only allowed to change allowed fields.",
          inputPlaceholder: "Select method",
          showCancelButton: true,

          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          customClass: "scale-in-center",
          confirmButtonText: "Next",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (result.value) {
            switch (result.value) {
              case "giturl":
                // URL
                self.$swal
                  .fire({
                    title: "Enter the URL here",
                    input: "text",
                    inputAttributes: {
                      autocapitalize: "off",
                    },
                    confirmButtonColor: "#5C3069",
                    cancelButtonColor: "#006476",

                    customClass: "scale-in-center",
                    showCancelButton: true,
                    confirmButtonText: "Go",
                    allowOutsideClick: () => !self.$swal.isLoading(),
                    backdrop: true,
                  })
                  .then((result) => {
                    if (result.value) {
                      let url = result.value;
                      axios
                        .get(url)
                        .then((res) => {
                          let selected = res.data;
                          for (let key in selected) {
                            if (!["@context", "@type", "_id"].includes(key)) {
                              if (key == "identifier") {
                                self.checkOverriddenID(selected[key]);
                              }
                              var payload = {};
                              if (typeof selected[key] === "object") {
                                let value = [selected[key]];
                                payload["completed"] = {
                                  name: key,
                                  value: value,
                                };
                                self.$store.commit("markCompleted", payload);
                              } else {
                                let value = selected[key];
                                payload["completed"] = {
                                  name: key,
                                  value: value,
                                };
                                self.$store.commit("markCompleted", payload);
                              }
                            }
                          }
                        })
                        .catch((err) => {
                          self.$swal.fire({
                            type: "error",
                            title: "Oops...",
                            text: "Something went wrong!",
                          });
                          throw err;
                        });
                    }
                  });
                break;
              case "registered":
                axios
                  .get(
                    self.apiUrl + "/api/dataset?&user=" + self.userInfo.login
                  )
                  .then((publicres) => {
                    let list = publicres.data.hits;
                    self.$store.commit("setLoading", { value: true });
                    axios
                      .get(
                        self.apiUrl +
                          "/api/dataset?private=true&user=" +
                          self.userInfo.login
                      )
                      .then((privateres) => {
                        self.$store.commit("setLoading", { value: false });
                        list = list.concat(privateres.data.hits);
                        let options = {};
                        for (var i = 0; i < list.length; i++) {
                          options[list[i]["name"]] = list[i]["name"];
                        }
                        self.$swal
                          .fire({
                            title: "Select Metadata To Import",
                            input: "select",
                            inputOptions: options,

                            confirmButtonColor: "#5C3069",
                            cancelButtonColor: "#006476",

                            customClass: "scale-in-center",
                            footer: `<p>
                        WARNING: <span class='text-danger'>You are loading already registered metadata.</span> If -identifier- field <b>IS NOT</b> changed, changes will override current saved data. If -identifier- field <b>IS</b> changed this this create a new entry.
                        </p>`,
                            customClass: "scale-in-center",
                            inputPlaceholder: "Select an item",
                            showCancelButton: true,
                          })
                          .then((result) => {
                            if (result.value) {
                              for (var i = 0; i < list.length; i++) {
                                if (result.value === list[i]["name"]) {
                                  let selected = list[i];
                                  for (let key in selected) {
                                    if (
                                      !["@context", "@type", "_id"].includes(
                                        key
                                      )
                                    ) {
                                      //check existing identifier for edit mode
                                      if (key == "identifier") {
                                        self.checkOverriddenID(selected[key]);
                                      }
                                      var payload = {};
                                      if (typeof selected[key] === "object") {
                                        let value = [selected[key]];
                                        payload["completed"] = {
                                          name: key,
                                          value: value,
                                        };
                                        self.$store.commit(
                                          "markCompleted",
                                          payload
                                        );
                                      } else {
                                        let value = selected[key];
                                        payload["completed"] = {
                                          name: key,
                                          value: value,
                                        };
                                        self.$store.commit(
                                          "markCompleted",
                                          payload
                                        );
                                      }
                                    }
                                  }
                                  self.$store.commit("formPreviewForGuide");
                                }
                              }
                            }
                          });
                      })
                      .catch((err) => {
                        throw err;
                      });
                  })
                  .catch((err) => {
                    throw err;
                  });

                break;
              case "text":
                self.$swal
                  .fire({
                    title: "Enter JSON here:",
                    input: "textarea",
                    inputAttributes: {
                      autocapitalize: "off",
                    },
                    showCancelButton: true,
                    confirmButtonColor: "#5C3069",
                    cancelButtonColor: "#006476",

                    customClass: "scale-in-center",
                    confirmButtonText: "Go",
                    allowOutsideClick: () => !self.$swal.isLoading(),
                    backdrop: true,
                  })
                  .then((result) => {
                    if (result.value) {
                      try {
                        let selected = JSON.parse(result.value);
                        console.log(selected);
                        for (let key in selected) {
                          if (!["@context", "@type", "_id"].includes(key)) {
                            if (key == "identifier") {
                              self.checkOverriddenID(selected[key]);
                            }
                            var payload = {};
                            if (self.$_.isPlainObject(selected[key])) {
                              //look at keys and check for dates
                              let obj = selected[key];
                              for (var k in obj) {
                                if (k.includes("date")) {
                                  let v = moment(obj[k]).format("YYYY-MM-DD");
                                  obj[k] = v;
                                  console.log("date checked obj", obj[k]);
                                }
                              }
                              //make obj an array of obj,
                              payload["completed"] = {
                                name: key,
                                value: [obj],
                              };
                              self.$store.commit("markCompleted", payload);
                            } else if (self.$_.isArray(selected[key])) {
                              let list = selected[key];

                              for (var i = 0; i < list.length; i++) {
                                let item = list[i];
                                if (self.$_.isPlainObject(item)) {
                                  let arrObj = item;

                                  for (var k in arrObj) {
                                    if (k.includes("date")) {
                                      let v = moment(arrObj[k]).format(
                                        "YYYY-MM-DD"
                                      );
                                      arrObj[k] = v;
                                      console.log(
                                        "date checked obj",
                                        arrObj[k]
                                      );
                                    }
                                  }
                                } else if (
                                  self.$_.isString(item) &&
                                  item.includes("date")
                                ) {
                                  item = moment(item).format("YYYY-MM-DD");
                                  console.log("date checked string", item);
                                } else {
                                }
                              }
                              payload["completed"] = { name: key, value: list };
                              self.$store.commit("markCompleted", payload);
                            } else {
                              let value = selected[key];
                              if (key.includes("date")) {
                                let v = moment(value).format("YYYY-MM-DD");
                                payload["completed"] = { name: key, value: v };
                              } else {
                                payload["completed"] = {
                                  name: key,
                                  value: value,
                                };
                              }

                              self.$store.commit("markCompleted", payload);
                            }
                          }
                        }
                      } catch (e) {
                        self.$swal.fire({
                          icon: "error",
                          title: "Oops...",
                          confirmButtonColor: "#5C3069",
                          cancelButtonColor: "#006476",

                          customClass: "scale-in-center",
                          text: e,
                          footer: "Oh no, something looks wrong...",
                        });
                      }
                    }
                  });
                break;
              default:
                return false;
            }
          }
        });
    },
    checkAutoLoad() {
      var self = this;
      let payload = {};
      //if GUIDE_PRESETS is only ONE
      if (self.presets && self.presets.length === 1) {
        payload["startingPoint"] = self.presets[0];
        self.$store.commit("setStartingPoint", payload);
        if (self.portals && self.portals.length) {
          payload["step"] = 2;
          self.$store.commit("changeStep", payload);
        } else {
          payload["step"] = 3;
          self.$store.commit("changeStep", payload);
          self.getFormValues();
        }
      }
      // if GUIDE_PRESETS is more than one
      else {
        // if url QUERY
        if (self.guideQuery) {
          let found = self.presets.find(
            (guide) => guide.name.toLowerCase() == self.guideQuery.toLowerCase()
          );
          console.log("Loading from context Query", found);
          if (found) {
            self.$store.commit("setStartingPoint", { startingPoint: found });
            payload["step"] = 3;
            self.$store.commit("changeStep", payload);
            self.getFormValues();
          } else {
            payload["step"] = 1;
            self.$store.commit("changeStep", payload);
          }
        }
        // Choose first item from GUIDE_PRESETS as default
        else {
          payload["startingPoint"] = self.presets[0];
          self.$store.commit("setStartingPoint", payload);
          if (self.portals && self.portals.length) {
            payload["step"] = 2;
            self.$store.commit("changeStep", payload);
          } else {
            payload["step"] = 3;
            self.$store.commit("changeStep", payload);
            self.getFormValues();
          }
        }
      }
    },
    getFormValues() {
      var self = this;
      // Handle selections for startingPoint and Portals IF any
      self.getStartingPointSchema(self.$store.getters.startingPoint);
      let payload = {};
      payload["step"] = 3;
      self.$store.commit("changeStep", payload);
    },
    readableName(text) {
      if (text) {
        let result = text.replace(/([A-Z])/g, " $1");
        result = result.charAt(0).toUpperCase() + result.slice(1);
        return result.replaceAll("_", " ");
      }

      return text.replaceAll("_", " ");
    },
    setStartingPoint(startingPointInfo) {
      var self = this;
      let payload = {};
      payload["startingPoint"] = startingPointInfo;
      self.$store.commit("setStartingPoint", payload);
      if (self.portals && self.portals.length) {
        // IF PORTALS AVAILABLE
        payload["step"] = 2;
        self.$store.commit("changeStep", payload);
      } else {
        // IF NO PORTALS AVAILABLE
        self.getFormValues();
        payload["step"] = 3;
        self.$store.commit("changeStep", payload);
      }
    },
    goToStep(s) {
      var self = this;
      let payload = {};
      payload["step"] = s;
      self.$store.commit("changeStep", payload);
    },
    checkProgress() {
      let self = this;
      let p = sessionStorage.getItem("guideProgress");
      if (p) {
        new Notify({
          status: "success",
          title: "Guide Progress",
          text: "Progress recovered",
          effect: "fade",
          speed: 300,
          customClass: null,
          customIcon: null,
          showIcon: true,
          showCloseButton: true,
          autoclose: true,
          autotimeout: 3000,
          gap: 20,
          distance: 20,
          type: 1,
          position: "right top",
        });
        let selected = JSON.parse(p);

        for (let key in selected) {
          if (!["@context", "@type", "_id"].includes(key)) {
            var payload = {};
            let value = selected[key];
            payload["completed"] = { name: key, value: value };
            self.$store.commit("markCompleted", payload);
          }
        }
      }
    },
    viewErrors() {
      var self = this;

      if (self.errors.length) {
        self.$swal.fire({
          title: "Issues",

          customClass: "scale-in-center",
          showConfirmButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          html: `<h6 class="text-center mainTextDark">Preview</h6><div class="text-left p-1 previewBox bg-dark"><pre id="previewJSON2"></pre></div>`,
          didOpen: function () {
            renderjson.set_show_to_level(5);
            document
              .getElementById("previewJSON2")
              .appendChild(renderjson(self.errors));
          },
        });
      } else {
        self.$swal.fire({
          icon: "success",
          toast: true,
          title: "Everything Looks Good!",
          showConfirmButton: false,
          timer: 2000,
        });
      }
    },
  },
  mounted: function () {
    const runtimeConfig = useRuntimeConfig();
    this.apiUrl = runtimeConfig.public.apiUrl;
    if (this.guide_query) {
      this.guideQuery = this.guide_query;
    }
    this.checkAutoLoad();

    tippy(".bar", {
      content: "Loading...",
      maxWidth: "200px",
      placement: "top",
      animation: "fade",
      theme: "light",
      onShow(instance) {
        let totals = self.$store.getters.getTotals;
        let percentage = Math.ceil((totals.complete / totals.total) * 100);
        instance.setContent(
          "<div class='text-success bold m-0'>" +
            percentage +
            "% Completed</div>"
        );
      },
    });
    tippy(".required", {
      maxWidth: "200px",
      placement: "top",
      content: "This field is required",
      animation: "fade",
      theme: "light",
    });

    tippy(".info", {
      maxWidth: "200px",
      placement: "left",
      animation: "fade",
      theme: "light",
      onShow(instance) {
        let info = instance.reference.dataset.tippyInfo;
        instance.setContent("<div class='text-muted m-0'>" + info + "</div>");
      },
    });

    tippy(".desc", {
      placement: "top",
      animation: "fade",
      interactive: true,
      theme: "light",
      onShow(instance) {
        let info = instance.reference.dataset.tippyInfo;
        if (info.substring(0, 5) == '"http') {
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
                    instance.setContent(
                      "<div class='text-muted m-0 p-1'>" +
                        res.data.response.docs[i]["label"] +
                        "</div>"
                    );
                  }
                }
              } else {
                instance.setContent(
                  "<div class='text-muted m-0 p-1'>" + info + "</div>"
                );
              }
            })
            .catch((err) => {
              instance.setContent(
                "<div class='text-muted m-0 p-1'><pre>" + info + "</pre></div>"
              );
            });
        } else {
          function getContent(value) {
            return value.constructor === String
              ? value
              : JSON.stringify(value, null, 2);
          }

          // REGULAR TIP DESCRIPTION
          try {
            let json = JSON.parse(info);
            if (typeof json == "string") {
              instance.setContent(
                "<div class='text-info text-left m-0 p-1 bg-white'><pre style='margin:0px !important;word-break:break-all;'>" +
                  info +
                  "</pre></div>"
              );
            } else {
              let html = "";
              for (key in json) {
                html +=
                  `<tr>
                                <td><small><b>` +
                  key +
                  `</b></small></td>
                                <td style="word-break:break-all;"><small>` +
                  getContent(json[key]) +
                  `</small></td>
                              </tr>`;
              }
              instance.setContent(
                "<table class='table table-sm table-striped'>" +
                  html +
                  "</table>"
              );
            }
          } catch (err) {
            instance.setContent(
              "<div class='text-info text-left m-0 p-1 bg-white'><pre style='margin:0px !important;word-break:break-all;'>" +
                info +
                "</pre></div>"
            );
          }
        }
      },
    });
  },
};
</script>
