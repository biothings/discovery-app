<template>
  <section id="dashboard">
    <div
      class="container"
      style="min-height: 100vh; padding-top: 80px"
      v-if="userInfo?.login"
    >
      <h1 class="text-muted caps">My Dashboard</h1>
      <div class="dashboard">
        <div class="row mb-5">
          <!-- uSER BOX -->
          <div class="col-sm-2 p-0 userInfo bg-secondary">
            <div class="pRelative">
              <img
                v-if="userInfo.avatar_url"
                :src="userInfo.avatar_url"
                class="w-100"
                alt="logo"
                style="z-index: 1"
              />
              <img
                v-else
                id="navPhoto"
                class="w-100"
                style="z-index: 1"
                src="@/assets/img/default.png"
                alt="userInfo photo"
              />
              <div class="clip bg-secondary pAbsolute" style="z-index: 2"></div>
            </div>
            <div class="text-light p-3 text-center">
              <template v-if="userInfo && userInfo.name">
                <p class="text-light mt-4 lighter" v-text="userInfo.name"></p>
              </template>
              <a
                class="text-light link"
                target="_blank"
                :href="'http://www.github.com/' + userInfo.login"
              >
                <font-awesome-icon icon="fab fa-github" class="mr-2" />
                <span v-text="userInfo.login"></span>
              </a>
            </div>
          </div>
          <!-- RESULTS -->
          <div class="col-sm-10" id="dashTippyParent">
            <div class="alert-dark p-2">
              <div class="mt-3 mainTextDark">
                ({{total_NS}})
                Registered Schema Namespaces
              </div>
              <div v-if="dashboard && dashboard.length">
                <div v-for="item in dashboard" class="row m-1">
                  <div
                    class="col-sm-8 p-1 mainBackDark d-flex align-items-center justify-content-between"
                  >
                    <nuxt-link
                      :to="'/view/' + item.namespace"
                      v-text="item.namespace"
                      class="d-inline m-2 text-light"
                    ></nuxt-link>
                  </div>
                  <div
                    class="col-sm-4 p-1 bg-dark actions d-flex align-items-center justify-content-around"
                  >
                    <div>
                      <a target="_blank" :href="item.url" :title="item.url">
                        <span
                          class="fa-stack fa-1x pointer tip"
                          data-tippy-content="source URL"
                        >
                          <font-awesome-icon
                            icon="fas fa-circle"
                            class="text-muted fa-stack-2x"
                          />
                          <font-awesome-icon
                            icon="fas fa-code"
                            class="fa-stack-1x text-light"
                          />
                        </span>
                      </a>
                    </div>
                    <div>
                      <nuxt-link
                        :to="'/view/' + item.namespace"
                      >
                        <span
                          class="fa-stack fa-1x pointer tip"
                          data-tippy-content="Visualize"
                        >
                          <font-awesome-icon
                            icon="fas fa-circle"
                            class="text-muted fa-stack-2x"
                          />
                          <font-awesome-icon
                            icon="fas fa-eye"
                            class="fa-stack-1x text-light"
                          />
                        </span>
                      </nuxt-link>
                    </div>
                    <div>
                      <span
                        class="fa-stack fa-1x pointer tip"
                        @click="updateSelected('schema', item.namespace)"
                        data-tippy-content="Update Schema"
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="text-muted fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-sync-alt"
                          class="fa-stack-1x text-light"
                        />
                      </span>
                    </div>
                    <div>
                      <span
                        class="fa-stack fa-1x pointer tip"
                        @click="deleteSelected('schema', item.namespace)"
                        data-tippy-content="Delete"
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="text-muted fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-trash"
                          class="fa-stack-1x text-light"
                        />
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Namespaces Pagination -->
              <div class="mt-1">
                <select
                  class="form-control form-control-sm m-auto w-25"
                  v-model="perPage_NS"
                  @change="
                    getNamespaces();
                    calculatePages_NS();
                  "
                  id="perPage_NS"
                >
                  <option value="" disabled selected>Shown Per Page</option>
                  <option value="5">5 per page</option>
                  <option value="10">10 per page</option>
                  <option value="20">20 per page</option>
                </select>
                <div class="d-flex flex-wrap justify-content-center p-1 mt-2">
                  <div
                    class="page-item rounded-0"
                    :class="{ disabled: page_NS <= 1 }"
                  >
                    <a
                      class="page-link p-1"
                      @click.prevent="
                        prevPage_NS();
                        getNamespaces();
                      "
                      ><font-awesome-icon icon="fas fa-step-backward"
                    /></a>
                  </div>
                  <template v-if="groupPages_NS">
                    <div
                      class="page-item rounded-0"
                      v-show="!startCapLimitReached_NS"
                    >
                      <a
                        href="#"
                        class="page-link p-1"
                        @click.prevent="
                          previousGroup_NS();
                          getNamespaces();
                        "
                        >Previous 20</a
                      >
                    </div>
                  </template>
                  <template v-for="n in pages_NS" :key="n + 'page'">
                    <div
                      v-if="n >= startCap_NS && n <= endCap_NS"
                      class="page-item rounded-0"
                      :class="{
                        active: page_NS == n,
                        'bg-primary': page_NS == n,
                        'white-text': page_NS == n,
                      }"
                    >
                      <a
                        href="#"
                        class="page-link p-1"
                        @click.prevent="
                          page_NS = n;
                          getNamespaces();
                        "
                        v-text="n"
                      ></a>
                    </div>
                  </template>
                  <template v-if="groupPages_NS">
                    <div
                      class="page-item rounded-0"
                      v-show="!endCapLimitReached_NS"
                    >
                      <a
                        href="#"
                        class="page-link p-1"
                        @click.prevent="
                          nextGroup_NS();
                          getNamespaces();
                        "
                        >Next 20</a
                      >
                    </div>
                  </template>
                  <div
                    class="page-item rounded-0"
                    :class="{ disabled: page_NS >= pages_NS }"
                  >
                    <a
                      class="page-link p-1"
                      @click.prevent="
                        nextPage_NS();
                        getNamespaces();
                      "
                      ><font-awesome-icon icon="fas fa-step-forward"
                    /></a>
                  </div>
                </div>
              </div>
            </div>

            <div class="alert-info p-2">
              <div class="mt-3 mainTextLight">
                ({{datasetsTotal}})
                Registered Datasets
              </div>
              <form
                @submit.prevent="getDatasets()"
                class="d-flex justify-content-end align-items-center"
              >
                <input
                  type="text"
                  name="search_datasets"
                  v-model="datasetQuery"
                  placeholder="Search datasets"
                />
                <button
                  type="submit"
                  class="btn btn-sm mainBackLight text-light ml-1"
                >
                  Search Datasets
                </button>
                <button
                  type="button"
                  @click="handleDatasetReset()"
                  class="btn btn-sm bg-danger text-light ml-1"
                >
                  Reset
                </button>
              </form>
              <div class="d-flex justify-content-start align-items-center">
                <input
                  type="checkbox"
                  class="form-control slider mr-2"
                  id="private_dataset"
                  name="private_dataset"
                  v-model="privateOnly"
                  @change="getDatasets()"
                />
                <label for="private_dataset" class="m-0">
                  Show Private Datasets</label
                ><br />
              </div>
              <div v-if="datasets?.length">
                <div
                  v-for="(item, i) in datasets"
                  class="row m-1"
                  :key="i + 'dataset'"
                >
                  <div
                    class="col-sm-12 col-md-8 p-1 mainBackLight d-flex align-items-center justify-content-between"
                  >
                    <nuxt-link
                      :to="'/dataset/' + item._id "
                      class="m-2 text-light d-block"
                      :title="item.name"
                    >
                      <small v-text="trunc(item.name)"></small>
                    </nuxt-link>
                    <small class="text-light">
                      <span v-html="formatDate(item['_meta'])"></span>
                    </small>
                  </div>
                  <div
                    class="col-sm-12 col-md-4 p-1 bg-dark actions d-flex align-items-center justify-content-around"
                  >
                    <div>
                      <nuxt-link :to="'/dataset/' + item._id">
                        <span
                          class="fa-stack fa-1x pointer tip"
                          data-tippy-content="View Dataset"
                        >
                          <font-awesome-icon
                            icon="fas fa-circle"
                            class="text-muted fa-stack-2x"
                          />
                          <font-awesome-icon
                            icon="fas fa-eye"
                            class="fa-stack-1x text-light"
                          />
                        </span>
                      </nuxt-link>
                    </div>
                    <div>
                      <span
                        class="fa-stack fa-1x pointer tip"
                        @click="edit(item._id)"
                        data-tippy-content="Quick Edit"
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="text-muted fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-bolt"
                          class="fa-stack-1x text-light"
                        />
                      </span>
                    </div>
                    <div>
                      <span
                        class="fa-stack fa-1x pointer tip"
                        @click="handlePrivacy(item, 'public')"
                        :data-tippy-content="[
                          item['_meta']['private']
                            ? 'Item is PRIVATE - Edit Privacy'
                            : 'Item is PUBLIC - Edit Privacy',
                        ]"
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="text-muted fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-lock"
                          class="fa-stack-1x text-warning"
                          v-if="item['_meta']['private']"
                        />
                        <font-awesome-icon
                          icon="fas fa-lock-open"
                          class="fa-stack-1x text-light"
                          v-else
                        />
                      </span>
                    </div>
                    <div>
                      <span
                        class="fa-stack fa-1x pointer tip"
                        @click="deleteSelected('metadata', item._id)"
                        data-tippy-content="Delete"
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="text-muted fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-trash"
                          class="fa-stack-1x text-light"
                        />
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Datasets Pagination -->
              <div>
                <select
                  class="form-control form-control-sm m-auto w-25"
                  v-model="perPage"
                  @change="
                    getDatasets();
                    calculatePages();
                  "
                  id="perPage"
                >
                  <option value="" disabled selected>Shown Per Page</option>
                  <option value="5">5 per page</option>
                  <option value="10">10 per page</option>
                  <option value="20">20 per page</option>
                </select>
                <div class="d-flex flex-wrap justify-content-center p-1 mt-2">
                  <div
                    class="page-item rounded-0"
                    :class="{ disabled: page <= 1 }"
                  >
                    <a
                      class="page-link p-1"
                      @click.prevent="
                        prevPage();
                        getDatasets();
                      "
                      ><font-awesome-icon icon="fas fa-step-backward"
                    /></a>
                  </div>
                  <template v-if="groupPages">
                    <div
                      class="page-item rounded-0"
                      v-show="!startCapLimitReached"
                    >
                      <a
                        href="#"
                        class="page-link p-1"
                        @click.prevent="
                          previousGroup();
                          getDatasets();
                        "
                        >Previous 20</a
                      >
                    </div>
                  </template>
                  <template v-for="n in pages" :key="n + 'page'">
                    <div
                      v-if="n >= startCap && n <= endCap"
                      class="page-item rounded-0"
                      :class="{
                        active: page == n,
                        'bg-primary': page == n,
                        'white-text': page == n,
                      }"
                    >
                      <a
                        href="#"
                        class="page-link p-1"
                        @click.prevent="
                          page = n;
                          getDatasets();
                        "
                        v-text="n"
                      ></a>
                    </div>
                  </template>
                  <template v-if="groupPages">
                    <div
                      class="page-item rounded-0"
                      v-show="!endCapLimitReached"
                    >
                      <a
                        href="#"
                        class="page-link p-1"
                        @click.prevent="
                          nextGroup();
                          getDatasets();
                        "
                        >Next 20</a
                      >
                    </div>
                  </template>
                  <div
                    class="page-item rounded-0"
                    :class="{ disabled: page >= pages }"
                  >
                    <a
                      class="page-link p-1"
                      @click.prevent="
                        nextPage();
                        getDatasets();
                      "
                      ><font-awesome-icon icon="fas fa-step-forward"
                    /></a>
                  </div>
                </div>
              </div>
            </div>

            <template v-if="datasets || privateDatasets">
              <div class="alert alert-secondary mt-3">
                <small>
                  Want to edit a registered dataset? Learn how
                  <nuxt-link to="/faq#edit-dataset">HERE</nuxt-link>
                </small>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <a class="nav-link" :href="apiUrl + '/login?next=' + nextPath"
        >Please Login</a
      >
    </div>
  </section>
</template>

<script>
import axios from "axios";
import moment from "moment";
import Notify from 'simple-notify';

import { mapGetters, mapActions } from "vuex";

export default {
  name: "Dashboard",
  data: function () {
    return {
      apiUrl:'',
      dashboard: [],
      privateDatasets: [],
      datasets: [],
      selectedItem: {},
      slugInput: "",
      availableSlug: false,
      invalidChars: false,
      meta: {},
      total: 0,
      // Datasets
      datasetQuery: "",
      datasetsTotal: 0,
      perPage: 5,
      page: 1,
      pages: 1,
      startCap: 0,
      endCap: 20,
      groupPages: false,
      pageLimit: 20,
      startCapLimitReached: true,
      endCapLimitReached: false,
      privateOnly: false,
      // Namespaces
      namespaceQuery: "",
      total_NS: 0,
      perPage_NS: 5,
      page_NS: 1,
      pages_NS: 1,
      startCap_NS: 0,
      endCap_NS: 20,
      groupPages_NS: false,
      pageLimit_NS: 20,
      startCapLimitReached_NS: true,
      endCapLimitReached_NS: false,
    };
  },
  watch: {
    slugInput: function (newInput, oldInput) {
      var self = this;
      self.slugInput = self.slugInput.toLowerCase();
      var re = /^[a-zA-Z0-9_.-]*$/;
      if (!re.test(newInput)) {
        self.invalidChars = true;
      } else {
        self.invalidChars = false;
      }

      if (newInput && !self.invalidChars) {
        axios
          .get(self.apiUrl + `/api/registry/` + self.slugInput)
          .then(function (response) {
            if (response.data.url) {
              self.availableSlug = false;
            }
          })
          .catch((error) => {
            self.availableSlug = true;
            throw error;
          });
      }
    },
    loggedIn: {
      immediate: true,
      handler: function (v) {
        if (!v) {
          console.log('loggedIn', v)
          navigateTo({ path: "/" });
        }
      },
    },
  },
  computed: {
    ...mapGetters(["loggedIn", "userInfo"]),
  },
  methods: {
    // Namespaces
    handleNamespaceReset: function () {
      this.namespaceQuery = "";
      this.getNamespaces();
    },
    calculatePages_NS: function () {
      var self = this;
      self.pages_NS = Math.ceil(this.total_NS / self.perPage_NS);

      if (self.pages_NS > self.pageLimit_NS) {
        self.groupPages_NS = true;
      }
    },
    previousGroup_NS: function () {
      var self = this;

      if (!self.startCapLimitReached) {
        if (self.startCap - 20 > 0) {
          self.page = self.startCap - 20;
          self.startCap = self.startCap - 20;
          self.endCap = self.endCap - 20;
          self.endCapLimitReached = false;
        } else {
          self.page = 1;
          self.startCap = 0;
          self.endCap = 20;
          self.startCapLimitReached = true;
          self.endCapLimitReached = false;
        }
      }
    },
    nextGroup_NS: function () {
      var self = this;

      if (!self.endCapLimitReached) {
        if (self.endCap + 20 < self.pages) {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.endCap + 20;
          self.startCapLimitReached = false;
        } else {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.pages;
          self.endCapLimitReached = true;
          self.startCapLimitReached = false;
        }
      }
    },
    prevPage_NS: function () {
      var self = this;
      if (self.page > 1) self.page -= 1;
    },
    nextPage_NS: function () {
      var self = this;
      if (self.page < self.pages) self.page += 1;
    },
    // Datasets
    handleDatasetReset: function () {
      this.datasetQuery = "";
      this.getDatasets();
    },
    calculatePages: function () {
      var self = this;
      self.pages = Math.ceil(this.datasetsTotal / self.perPage);

      if (self.pages > self.pageLimit) {
        self.groupPages = true;
      }
    },
    previousGroup: function () {
      var self = this;

      if (!self.startCapLimitReached) {
        if (self.startCap - 20 > 0) {
          self.page = self.startCap - 20;
          self.startCap = self.startCap - 20;
          self.endCap = self.endCap - 20;
          self.endCapLimitReached = false;
        } else {
          self.page = 1;
          self.startCap = 0;
          self.endCap = 20;
          self.startCapLimitReached = true;
          self.endCapLimitReached = false;
        }
      }
    },
    nextGroup: function () {
      var self = this;

      if (!self.endCapLimitReached) {
        if (self.endCap + 20 < self.pages) {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.endCap + 20;
          self.startCapLimitReached = false;
        } else {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.pages;
          self.endCapLimitReached = true;
          self.startCapLimitReached = false;
        }
      }
    },
    prevPage: function () {
      var self = this;
      if (self.page > 1) self.page -= 1;
    },
    nextPage: function () {
      var self = this;
      if (self.page < self.pages) self.page += 1;
    },
    edit(id) {
      var self = this;
      axios
        .get(self.apiUrl + "/api/dataset/" + id)
        .then((res) => {
          if (res.data) {
            self.meta = res.data;
            let list = {};
            let notAllowed = [
              "@context",
              "@type",
              "includedInDataCatalog",
              "_id",
              "_meta",
            ];
            for (let key in self.meta) {
              if (!notAllowed.includes(key)) {
                list[key] = key;
              }
            }

            this.$swal
              .fire({
                title: `Quick Edit`,
                text: "Which field would you like to edit?",
                input: "select",
                footer:
                  "<small><b class='text-info'>Note:</b> You can only quick edit existing fields. If you wish to add more fields import this metadata via a guide and add any fields necessary. <br /><b class='text-danger'>Important:</b> Making changes will change privacy to default: <b>PUBLIC</b>. You can change privacy settings again when you are done. Changing the <code>identifier</code> field will result in creating a new entry.</small>",
                inputOptions: list,
                inputPlaceholder: "Select a field to edit",
                showCancelButton: true,
                confirmButtonColor: "#5C3069",
                cancelButtonColor: "#006476",
                confirmButtonText: "Edit",
                inputValidator: (value) => {
                  return new Promise((resolve) => {
                    if (!value) {
                      resolve("You must select something first");
                    } else {
                      resolve();
                    }
                  });
                },
              })
              .then((keyname) => {
                if (keyname.value) {
                  let iValue = "";

                  if (
                    typeof self.meta[keyname.value] === "string" ||
                    typeof self.meta[keyname.value] === "number" ||
                    typeof self.meta[keyname.value] === "boolean"
                  ) {
                    iValue = self.meta[keyname.value];
                  } else {
                    iValue = JSON.stringify(self.meta[keyname.value], null, 2);
                  }

                  this.$swal
                    .fire({
                      title: "Edit: " + keyname.value,
                      input: "textarea",
                      footer: `<small>Make sure to close all: {},[] and quotes</small>`,
                      confirmButtonColor: "#5C3069",
                      cancelButtonColor: "#006476",

                      customClass: "scale-in-center",
                      inputPlaceholder: self.meta[keyname.value],
                      inputValue: iValue,
                      inputAttributes: {
                        "aria-label": keyname.value,
                        rows: 15,
                      },
                      showCancelButton: true,
                      confirmButtonText: "Save",
                      inputValidator: (value) => {
                        return new Promise((resolve) => {
                          if (value === self.meta[keyname.value]) {
                            resolve("You haven't changed anything yet");
                          } else {
                            resolve();
                          }
                        });
                      },
                    })
                    .then((newdata) => {
                      if (newdata.value) {
                        if (
                          newdata.value[0] === "{" ||
                          newdata.value[0] === "["
                        ) {
                          self.meta[keyname.value] = JSON.parse(newdata.value);
                        } else {
                          self.meta[keyname.value] = newdata.value;
                        }

                        this.$swal.showLoading();
                        let parts = self.meta["@type"].split(":");
                        let namespace = parts[0];
                        let prefix = parts[0];
                        let className = parts[1];
                        // let url = '/api/dataset?schema='+namespace+'::'+prefix+':'+className;
                        let url =
                          self.apiUrl + "/api/dataset/" + self.meta["_id"];
                        // if (self.meta && self.meta['_meta']['guide']) {
                        //   url = url+"&guide="+self.meta['_meta']['guide']
                        // }
                        axios
                          .put(url, self.meta)
                          .then((res) => {
                            this.$swal.hideLoading();
                            if (res.data.success) {
                              new Notify({
                                status: 'success',
                                title: 'Success!',
                                text: 'Field Updated',
                                position: 'right'
                              })
                              this.$swal
                                .fire({
                                  title: "Make other changes?",
                                  confirmButtonColor: "#5C3069",
                                  cancelButtonColor: "#006476",

                                  showCancelButton: true,
                                  customClass: "scale-in-center",
                                  confirmButtonText: "Yes",
                                  cancelButtonText: "No",
                                })
                                .then((r) => {
                                  if (r.value) {
                                    self.edit(id);
                                  } else {
                                    location.reload(true);
                                  }
                                });
                            }
                          })
                          .catch((err) => {
                            // console.log('err',err.response.data)
                            let culprit =
                              "<h6>" + err.response.data.error + "</h6>";
                            if (err.response.data.hasOwnProperty("path")) {
                              if (err.response.data.path.length) {
                                culprit +=
                                  "<h5>Culprit --> <b class='text-danger'>" +
                                  err.response.data.path +
                                  "</b></h5>";
                              }
                            }
                            if (
                              err.response.data.parent &&
                              err.response.data.parent.path
                            ) {
                              if (true) {
                                culprit +=
                                  "<h5>Also check --> <b class='text-danger'>" +
                                  err.response.data.parent.path +
                                  "</b></h5>";
                              }
                              if (
                                err.response.data.parent &&
                                err.response.data.parent.reason
                              ) {
                                culprit +=
                                  "<div class='alert alert-warning'><small>" +
                                  err.response.data.parent.reason +
                                  "</small></div>";
                              }
                            }
                            if (
                              err.response.data.hasOwnProperty(
                                "validator_value"
                              ) &&
                              err.response.data.validator_value.length
                            ) {
                              culprit +=
                                "<div class='alert alert-info'><small> Hint: " +
                                err.response.data.validator_value +
                                "</small></div>";
                            }
                            this.$swal.fire({
                              type: "error",
                              position: "top center",
                              title: "Oh no! It failed because: ",
                              html: culprit,
                              footer: "<small>Validation Error</small>",
                            });
                            throw err;
                          });
                      }
                    });
                }
              });
          }
        })
        .catch((err) => {
          this.$swal.fire("Oh, no!", "Can't edit at this time", "error");
          throw err;
        });
    },
    updateSelected(type, namespace) {
      var self = this;

      let options = {
        "Refresh URL": "Refresh URL",
        "Change URL": "Change URL",
      };

      this.$swal
        .fire({
          title: "What would like to do?",
          html: "<p>Do you want to <b class='text-danger'>change the url</b> of the schema OR just <b class='text-danger'>refresh</b> the content?</p>",
          footer:
            "<small>Tip: If you wanna test that there is no breaking changes first, try visualizing it on the Schema Playground!</small>",
          input: "select",
          inputOptions: options,
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",

          customClass: "scale-in-center",
          confirmButtonText: "Go",
        })
        .then((result) => {
          let ns = namespace == "bioschemas" ? "?ns=bioschemas" : "";

          if (result.value == "Refresh URL") {
            // same url
            self.$store.commit("setLoading", { value: true });
            axios
              .put(self.apiUrl + "/api/registry/" + namespace + ns)
              .then((res) => {
                if (res.data.result == "updated") {
                  this.$swal.fire(
                    "Boom! Done!",
                    "schema: " + namespace + " updated!",
                    "success"
                  );
                  self.$store.commit("setLoading", { value: false });
                } else if (res.data.result == "noop") {
                  this.$swal.fire(
                    "Nothing new here",
                    "schema: " +
                      namespace +
                      " is already on its latest version",
                    "success"
                  );
                  self.$store.commit("setLoading", { value: false });
                } else {
                  this.$swal.fire("Done!", res.data.result, "info");
                  self.$store.commit("setLoading", { value: false });
                }
              })
              .catch((err) => {
                this.$swal.fire(
                  "Oh, no!",
                  "We had trouble updating: " + namespace,
                  "error"
                );
              });
          } else if (result.value == "Change URL") {
            // new url
            this.$swal
              .fire({
                title: "What's the new URL?",
                text: "Make sure it's the RAW data link! (if hosted on GitHub)",
                input: "text",
                inputAttributes: {
                  autocapitalize: "off",
                },
                showCancelButton: true,
                confirmButtonText: "Go",
                allowOutsideClick: () => !this.$swal.isLoading(),
              })
              .then((result) => {
                if (result.value) {
                  let newurl = encodeURI(result.value);

                  data = {
                    url: newurl,
                  };
                  self.$store.commit("setLoading", { value: true });
                  axios
                    .put(self.apiUrl + "/api/registry/" + namespace + ns, data)
                    .then((res) => {
                      if (res.data.result) {
                        this.$swal.fire(
                          "Ta-dah!",
                          "Status: " + res.data.result,
                          "success"
                        );
                        self.$store.commit("setLoading", { value: false });
                      }
                    })
                    .catch((err) => {
                      this.$swal.fire(
                        "Oh, no!",
                        "We had trouble updating: " + namespace,
                        "error"
                      );
                      self.$store.commit("setLoading", { value: false });
                    });
                }
              });
          }
        });
    },
    deleteSelected(type, identifier) {
      var self = this;
      let index = self.apiUrl + "/api/registry/";
      if (type === "metadata") {
        index = self.apiUrl + "/api/dataset/";
      }
      this.$swal
        .fire({
          title: "<h4>Are you sure you want to delete this item?</h4>",
          text: "You won't be able to revert this!",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",

          customClass: "scale-in-center",
          confirmButtonText: "Yes, delete it!",
        })
        .then((result) => {
          if (result.value) {
            axios
              .delete(index + identifier)
              .then((res) => {
                if (res.status) {
                  switch (res.status) {
                    case 200:
                      //reload with no cache
                      location.reload(true);
                      break;
                    case 401:
                      v;
                      self.getAll();
                      break;
                    case 403:
                      this.$swal.fire(
                        "Oh, no!",
                        "You do not have permission to delete this item",
                        "error"
                      );
                      self.getAll();
                      break;
                    case 404:
                      this.$swal.fire(
                        "Oh, no!",
                        "This item does not seem to exist",
                        "error"
                      );
                      self.getAll();
                      break;
                    default:
                      this.$swal.fire(
                        "Oh no!",
                        "something went wrong",
                        "error"
                      );
                  }
                }
              })
              .catch((err) => {
                this.$swal.fire("Oh no!", "something went wrong", "error");
                throw err;
              });
          }
        });
    },
    getAll() {
      this.dashboard = [];
      if (this.loggedIn) {
        this.getNamespaces();
        this.getDatasets();
      }
    },
    getNamespaces() {
      let self = this;
      self.$store.commit("setLoading", { value: true });
      var params = {
        params: {
          size: self.perPage_NS,
          from:
            self.page_NS == 1
              ? self.page_NS - 1
              : (self.page_NS - 1) * self.perPage_NS,
          meta: true,
          user: self.userInfo.login,
        },
      };
      //SCHEMA NAMESPACES
      self.$store.commit("setLoading", { value: true });
      axios
        .get(self.apiUrl + "/api/registry", params)
        .then((res) => {
          // console.log("SCHEMAS",res.data)
          self.dashboard = res.data.hits;
          self.total_NS = res.data.total;
          self.calculatePages_NS();
          self.$store.commit("setLoading", { value: false });
        })
        .catch((err) => {
          self.$store.commit("setLoading", { value: false });
          throw err;
        });
    },
    getDatasets() {
      let self = this;
      self.$store.commit("setLoading", { value: true });
      if (self.datasetQuery) {
        var params = {
          params: {
            size: self.perPage,
            from:
              self.page == 1 ? self.page - 1 : (self.page - 1) * self.perPage,
            meta: true,
          },
        };

        params.params.q = `q="${self.datasetQuery}" AND _meta.private:${self.privateOnly} AND _meta.username:${self.userInfo.login}`;

        axios
          .get(self.apiUrl + "/api/dataset/query", params)
          .then((res) => {
            self.datasets = res.data.hits;
            self.datasetsTotal = res.data.total;
            self.calculatePages();
            self.$store.commit("setLoading", { value: false });
          })
          .catch((err) => {
            self.$store.commit("setLoading", { value: false });
            throw err;
          });
      } else {
        var params = {
          params: {
            size: self.perPage,
            from:
              self.page == 1 ? self.page - 1 : (self.page - 1) * self.perPage,
            meta: true,
            user: self.userInfo.login,
            private: self.privateOnly,
          },
        };

        axios
          .get(self.apiUrl + "/api/dataset", params)
          .then((res) => {
            self.datasets = res.data.hits;
            self.datasetsTotal = res.data.total;
            self.calculatePages();
            self.$store.commit("setLoading", { value: false });
          })
          .catch((err) => {
            self.$store.commit("setLoading", { value: false });
            throw err;
          });
      }
    },
    handlePrivacy(item, privacyStatus) {
      var title = () =>
        privacyStatus === "private"
          ? "<h4>Make this item PUBLIC?</h4>"
          : "<h4>Make this item PRIVATE?</h4>";
      this.$swal
        .fire({
          title: title(),
          footer: "<small>You can change the privacy settings anytime.</small>",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",

          customClass: "scale-in-center",
          confirmButtonText: "Yes",
          cancelButtonText: "No",
        })
        .then((result) => {
          if (result.value) {
            let data = item;
            let parts = data["@type"].split(":");
            let namespace = parts[0];
            let prefix = parts[0];
            let className = parts[1];
            // let url = '/api/dataset?schema='+namespace+'::'+prefix+':'+className;
            let url = self.apiUrl + "/api/dataset/" + item["_id"];
            if (privacyStatus === "private") {
              item["_meta"]["private"] = false;
              // url = url+'&private=false'
            } else {
              // url = url+'&private=true'
              item["_meta"]["private"] = true;
            }
            axios
              .put(url, data)
              .then((res) => {
                //reload with no cache
                setTimeout(function () {
                  location.reload(true);
                }, 1000);
              })
              .catch((err) => {
                throw err;
              });
          }
        });
    },
    trunc(item) {
      if (item.length > 100) {
        return item.substring(0, 100) + "...";
      } else {
        return item;
      }
    },
    formatDate(meta) {
      let date = "";
      if (meta.hasOwnProperty("last_updated")) {
        date = meta["last_updated"];
        return "last updated " + moment(date).format("MMM Do YYYY, h:mm a");
      }
      return "No recent updates";
    },
    ...mapActions(["checkUser"]),
  },
  mounted: function () {
    const runtimeConfig = useRuntimeConfig()
    this.apiUrl = runtimeConfig.public.apiUrl;
    this.getAll();
    
  },
  created: function () {
    this.checkUser();
  },
};
</script>
