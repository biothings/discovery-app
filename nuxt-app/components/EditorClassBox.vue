<template>
  <div v-if="item.special" class="text-dde-dark">
    <h5>Your New Extended Class:</h5>
    <small> <i class="text-danger">Required</i></small> Here you can add new
    properties to include in your schema.
  </div>
  <div
    class="row m-1 cBox actions text-dde-dark shadow"
    :class="{
      'bg-dde-mid-muted mb-3': item.special,
      'alert-light': !item.special,
    }"
  >
    <div class="col-sm-9 p-2">
      <div>
        <details>
          <summary class="text-dde-dark">
            <b>{{ item?.name }}</b>
          </summary>
          <template v-for="tree in item?.parent_classes">
            <template v-for="(name, i) in getSubclass(tree)" :key="i + 'sc'">
              <span v-text="name"></span>
              <span
                ><font-awesome-icon
                  icon="fas fa-chevron-right"
                  class="mr-1"
                ></font-awesome-icon
              ></span>
            </template>
            <span class="text-dde-dark"
              ><b v-text="item.name"></b>
              <font-awesome-icon
                icon="fas fa-info-circle"
                class="text-info cTip pointer ml-1"
                :data-tippy-content="item.description"
              ></font-awesome-icon
            ></span>
          </template>
        </details>
        <!-- 🌈 prop totals 🌈 -->
        <div v-if="totals" class="col-sm-12 p-0">
          <table style="font-size: small">
            <tr>
              <td v-for="(val, name) in totals" class="px-1">
                <span v-if="val">
                  <template v-if="name == 'required'">
                    <font-awesome-icon
                      title="required"
                      icon="fas fa-asterisk"
                      class="text-danger"
                    ></font-awesome-icon>
                    required
                  </template>
                  <template v-else-if="name == 'selected'">
                    <font-awesome-icon
                      title="selected"
                      icon="fas fa-check-circle"
                      class="text-success"
                    ></font-awesome-icon>
                    selected
                  </template>
                  <template v-else-if="name == 'optional'">
                    <font-awesome-icon
                      title="optional"
                      icon="fas fa-square"
                      class="text-info"
                    ></font-awesome-icon>
                    optional
                  </template>
                  <template v-else-if="name == 'recommended'">
                    <font-awesome-icon
                      title="recommended"
                      icon="fas fa-circle"
                      class="text-warning"
                    ></font-awesome-icon>
                    recommended
                  </template>
                  <i v-else v-text="name"></i> :
                  <b
                    v-text="val"
                    :class="[val ? 'text-primary' : 'text-muted']"
                  ></b>
                </span>
              </td>
            </tr>
          </table>
        </div>
        <span
          style="clear: both"
          v-if="item.special && !item.properties"
          class="text-muted float-right"
          >Add properties here
          <font-awesome-icon
            icon="fas fa-arrow-right"
            class="text-danger"
          ></font-awesome-icon
        ></span>
        <template v-if="showDesc">
          <span
            class="d-block text-muted"
            v-html="item.description || 'No description provided'"
          ></span>
        </template>
      </div>

      <!-- 🌈 selected list 🌈 -->
      <div v-if="!item.special">
        <template
          v-if="item && item.properties"
          v-for="prop in item.properties"
        >
          <span v-if="prop.selected" class="badge text-dark border-success m-1">
            <font-awesome-icon
              v-if="prop && prop.isRequired"
              icon="fas fa-asterisk"
              class="text-danger mr-1"
            ></font-awesome-icon>
            <font-awesome-icon
              v-else-if="prop && prop.isRecommended"
              icon="fas fa-circle"
              class="text-warning mr-1"
            ></font-awesome-icon>
            <font-awesome-icon
              v-else-if="prop && prop.isOptional"
              icon="fas fa-square"
              class="text-info mr-1"
            ></font-awesome-icon>
            <strong>{{ prop.label }}</strong>
          </span>
        </template>
      </div>

      <div v-show="expand" class="mt-1">
        <div
          class="p-1 bg-secondary"
          v-if="!item.special && item.properties.length > perPage"
        >
          <!-- 🌈 filter by name 🌈 -->
          <div>
            <input
              type="text"
              class="form-control form-control-sm col-sm-6"
              placeholder="search properties"
              v-model="query"
            />
          </div>

          <!-- 🌈 filtered 🌈 -->
          <template v-for="prop in filtered">
            <div class="row m-1 alert-secondary pBox actions">
              <div class="col-sm-9">
                <span class="text-dark">
                  <span v-text="prop.label"></span>
                  <font-awesome-icon
                    icon="fas fa-info-circle"
                    class="cTip pointer text-info"
                    :data-tippy-content="prop.description"
                  ></font-awesome-icon>
                  <template v-if="showDesc">
                    <span
                      class="d-block text-muted"
                      v-html="prop.description || 'No description provided'"
                    ></span>
                  </template>
                </span>
              </div>
              <div
                class="col-sm-3 bg-dark actions d-flex align-items-center justify-content-around"
              >
                <font-awesome-icon
                  v-show="item.special"
                  icon="fas fa-minus-circle"
                  class="pointer text-muted unselectable"
                  data-tippy-content="Delete Property"
                  @click="removeProp(prop.label)"
                ></font-awesome-icon>
                <font-awesome-icon
                  icon="fas fa-check-circle"
                  class="pointer unselectable select"
                  @click="markSelected(prop.label)"
                  :class="{
                    'text-muted': !prop.selected,
                    'text-success': prop.selected,
                  }"
                ></font-awesome-icon>
                <font-awesome-icon
                  icon="fas fa-asterisk"
                  class="pointer unselectable"
                  data-tippy-content="Mark as required"
                  @click="markRequired(prop.label)"
                  :class="{
                    'text-muted': !prop.isRequired,
                    'text-danger': prop.isRequired,
                  }"
                ></font-awesome-icon>
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="pointer unselectable"
                  data-tippy-content="Mark as recommended"
                  @click="markRecommended(prop.label)"
                  :class="{
                    'text-muted': !prop.isRecommended,
                    'text-warning': prop.isRecommended,
                  }"
                ></font-awesome-icon>
                <font-awesome-icon
                  icon="fas fa-square"
                  class="pointer unselectable"
                  data-tippy-content="Mark as optional"
                  @click="markOptional(prop.label)"
                  :class="{
                    'text-muted': !prop.isOptional,
                    'text-info': prop.isOptional,
                  }"
                ></font-awesome-icon>
              </div>
            </div>
          </template>
        </div>

        <!-- 🌈 results 🌈 -->
        <template v-for="prop in paginatedResults">
          <div class="row m-1 alert-secondary pBox actions">
            <div class="col-sm-9">
              <span class="mainTextDark">
                <span v-text="prop.label"></span>
                <font-awesome-icon
                  icon="fas fa-info-circle"
                  class="cTip pointer text-info ml-1"
                  :data-tippy-content="prop.description"
                ></font-awesome-icon>
                <template v-if="showDesc">
                  <span
                    class="d-block text-muted"
                    v-html="prop.description || 'No description provided'"
                  ></span>
                </template>
              </span>
            </div>
            <div
              class="col-sm-3 bg-dark actions d-flex align-items-center justify-content-around"
            >
              <font-awesome-icon
                v-show="item.special"
                icon="fas fa-minus-circle"
                class="pointer text-muted unselectable tip"
                data-tippy-content="Delete"
                @click="removeProp(prop.label)"
              ></font-awesome-icon>
              <font-awesome-icon
                v-show="item.special"
                icon="fas fa-pen-square"
                class="pointer text-muted unselectable tip mr-3"
                data-tippy-content="Edit"
                @click="editCustomProp(prop)"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-check-circle"
                class="pointer unselectable"
                data-tippy-content="Select (Re-use) property"
                @click="markSelected(prop.label)"
                :class="{
                  'text-muted': !prop.selected,
                  'text-success': prop.selected,
                }"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-asterisk"
                class="pointer unselectable"
                data-tippy-content="Mark As Required (Select First)"
                @click="markRequired(prop.label)"
                :class="{
                  'text-muted': !prop.isRequired,
                  'text-danger': prop.isRequired,
                }"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-circle"
                class="recommended pointer unselectable"
                data-tippy-content="Mark As Recommended (Select First)"
                @click="markRecommended(prop.label)"
                :class="{
                  'text-muted': !prop.isRecommended,
                  'text-warning': prop.isRecommended,
                }"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-square"
                class="pointer unselectable"
                data-tippy-content="Mark As Optional (Select First)"
                @click="markOptional(prop.label)"
                :class="{
                  'text-muted': !prop.isOptional,
                  'text-info': prop.isOptional,
                }"
              ></font-awesome-icon>
            </div>
          </div>
        </template>

        <!-- 🌈 pagination 🌈 -->
        <template v-if="!item.special && item.properties.length > perPage">
          <div class="d-flex flex-wrap justify-content-center p-1 mt-2">
            <div class="page-item rounded-0" :class="{ disabled: page <= 1 }">
              <a class="page-link p-1" @click.prevent="prevPage()"
                ><font-awesome-icon
                  icon="fas fa-step-backward"
                ></font-awesome-icon
              ></a>
            </div>
            <template v-if="groupPages">
              <div class="page-item rounded-0" v-show="!startCapLimitReached">
                <a
                  href="#"
                  class="page-link p-1"
                  @click.prevent="previousGroup()"
                  >Previous 20</a
                >
              </div>
            </template>
            <template v-for="n in pages">
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
                  @click.prevent="page = n"
                  v-text="n"
                ></a>
              </div>
            </template>
            <template v-if="groupPages">
              <div class="page-item rounded-0" v-show="!endCapLimitReached">
                <a href="#" class="page-link p-1" @click.prevent="nextGroup()"
                  >Next 20</a
                >
              </div>
            </template>
            <div
              class="page-item rounded-0"
              :class="{ disabled: page >= pages }"
            >
              <a class="page-link p-1" @click.prevent="nextPage()"
                ><font-awesome-icon
                  icon="fas fa-step-forward"
                ></font-awesome-icon
              ></a>
            </div>
          </div>
        </template>
      </div>
    </div>

    <div
      class="col-sm-3 p-2 bg-dde-mid actions d-flex align-items-center justify-content-around"
    >
      <span
        v-if="item.special"
        class="fa-stack fa-1x pointer unselectable tip"
        data-tippy-content="Add New Property"
        @click="
          addPropMode = !addPropMode;
          (newPropDomain = item.label), populateInputOptions();
        "
      >
        <font-awesome-icon
          icon="fas fa-circle"
          class="fa-stack-2x"
          :class="[addPropMode ? 'text-success' : 'mainTextLight']"
        ></font-awesome-icon>
        <font-awesome-icon
          v-if="addPropMode"
          icon="fas fa-minus"
          class="text-light fa-stack-1x"
        ></font-awesome-icon>
        <font-awesome-icon
          v-else
          icon="fas fa-plus"
          class="text-light fa-stack-1x"
        ></font-awesome-icon>
      </span>
      <button
        v-if="item && item.properties"
        type="button"
        class="btn btn-sm themeButton text-light"
        @click="expand = !expand"
      >
        {{ expand ? "Hide" : "Show" }}
        <span class="text-warning">({{ item.properties.length }})</span>
      </button>
    </div>

    <div
      v-if="addPropMode"
      class="col-sm-12 p-2 bg-dde-dark d-flex align-items-center justify-content-center text-light"
    >
      <div class="col-sm-10 m-auto p-3 bg-light text-muted rounded">
        <h5>New Property</h5>
        <form>
          <div class="form-group">
            <label for="name"
              >Name
              <font-awesome-icon
                icon="fas fa-asterisk"
                class="text-danger"
              ></font-awesome-icon
            ></label>
            <input
              v-model="newPropName"
              type="text"
              class="form-control"
              id="name"
              placeholder="name of new property eg. myProperty"
            />
            <span class="d-block my-1 text-info"
              >Learn about naming conventions
              <a
                href="https://schema.org/docs/styleguide.html"
                target="_blank"
                rel="nonreferrer"
                >here</a
              ></span
            >
            <span v-if="propExists" class="text-danger"
              >A property with this name already exists, any changes will
              replace existing value unless the property name changes.</span
            >
          </div>
          <div class="form-group">
            <label for="desc"
              >Description
              <font-awesome-icon
                icon="fas fa-asterisk"
                class="text-danger"
              ></font-awesome-icon
            ></label>
            <input
              v-model="newPropDescription"
              type="text"
              class="form-control"
              id="desc"
              placeholder="description of new property"
            />
          </div>
          <div class="form-group">
            <label for="domain"
              >Domain
              <font-awesome-icon
                icon="fas fa-asterisk"
                class="text-danger"
              ></font-awesome-icon
            ></label>
            <input
              disabled
              v-model="newPropDomain"
              type="text"
              class="form-control alert-secondary text-success"
              id="domain"
            />
          </div>
          <div class="form-group">
            <label for="input"
              >Input Type(s)
              <font-awesome-icon
                icon="fas fa-asterisk"
                class="text-danger"
              ></font-awesome-icon
            ></label>
            <div
              class="border p-1 rounded border-secondary mb-2"
              v-if="newPropRange && newPropRange.length"
            >
              <span
                class="badge badge-success m-1"
                v-for="selection in newPropRange"
                @click="removeRangePill(selection)"
                ><b v-text="selection"></b> &times;</span
              >
            </div>
            <div class="input-group mb-1">
              <input
                v-model="range_query"
                type="text"
                class="form-control"
                id="input"
                list="myCustomList"
                placeholder="Look up range options"
              />
              <datalist id="myCustomList"></datalist>
              <div
                class="input-group-append"
                @click.prevent="handlePillSubmit()"
              >
                <button type="button" class="input-group-text btn btn-success">
                  ADD
                </button>
              </div>
            </div>
          </div>
          <div class="w-100 p-1">
            <button
              type="button"
              class="btn btn-lg w-50 btn-danger"
              @click.prevent="addPropMode = false"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-lg w-50 btn-success"
              @click.prevent="submitNewProp()"
            >
              {{ addNewPropReady && !propExists ? "Submit" : "Update" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div v-if="item.special" class="text-dde-dark">
    <h5>Inherited Classes and Properties:</h5>
    <small>
      <i class="text-danger">Required</i> Here you can view and select
      properties from parent classes to include in your schema. If you extended
      a class with validation rules, they will be auto populated here.
    </small>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

import Notify from "simple-notify";

export default {
  name: "EditorClassBox",
  props: ["item"],
  data: function () {
    return {
      expand: false,
      addPropMode: false,
      newPropName: "",
      propExists: false,
      newPropDescription: "",
      newPropDomain: "",
      newPropRange: [],
      rangeOptions: [],
      query: "",
      filtered: [],
      // pagination
      perPage: 20,
      page: 1,
      pages: 1,
      startCap: 0,
      endCap: 20,
      groupPages: false,
      pageLimit: 20,
      startCapLimitReached: true,
      endCapLimitReached: false,
      // prop totals
      totals: {},
      // add prop input
      range_options: [],
      range_query: "",
    };
  },
  computed: {
    ...mapGetters({
      showDesc: "getShowDesc",
    }),
    addNewPropReady: function () {
      return this.newPropName && this.newPropDescription
        ? this.newPropDomain && this.newPropRange.length
          ? true
          : false
        : false;
    },
    paginatedResults: function () {
      var start = (this.page - 1) * this.perPage,
        end = start + this.perPage;
      return this.item.properties && this.item.properties.slice(start, end);
    },
  },
  watch: {
    newPropName: function (v) {
      this.propExists = this.$store.getters.isDuplicateProp(v);
    },
    query: function (q) {
      if (q) {
        this.filtered = this.item.properties.filter((prop) =>
          prop["label"].toLocaleLowerCase().includes(q.toLocaleLowerCase())
        );
      } else {
        this.filtered = [];
      }
    },
    range_query: function (q) {
      var self = this;
      if (q && self.range_options.includes(q)) {
        self.handlePillSubmit();
      }
    },
  },
  methods: {
    editCustomProp(prop) {
      let self = this;
      self.getRangeOptions();
      self.populateInputOptions();

      self.addPropMode = true;
      self.newPropDescription = prop["description"] || "";
      self.newPropName = prop["label"] || "";
      self.newPropDomain = prop["domain"] || "";

      if (prop && prop["range"]) {
        if (prop["range"].constructor == Array) {
          prop["range"].forEach((value) => {
            self.range_query = value;
            self.handlePillSubmit();
          });
        } else {
          prop["range"].split(",").forEach((value) => {
            self.range_query = value;
            self.handlePillSubmit();
          });
        }
      }
      // let payload = {};
      // payload["label"] = prop["label"];
      // self.$store.commit("removeProperty", payload);
    },
    handlePillSubmit() {
      var self = this;
      if (!self.newPropRange.includes(self.range_query)) {
        self.newPropRange.push(self.range_query);
        self.range_query = "";
      }
    },
    removeRangePill(value) {
      var self = this;
      const index = self.newPropRange.indexOf(value);
      if (index > -1) {
        self.newPropRange.splice(index, 1);
      }
    },
    populateInputOptions() {
      var self = this;
      var options = "";
      options += '<option value="schema:Text" />';
      options += '<option value="schema:URL" />';
      options += '<option value="schema:Integer" />';
      options += '<option value="schema:Number" />';
      options += '<option value="schema:Date" />';
      options += '<option value="schema:Float" />';
      options += '<option value="schema:Boolean" />';
      options += '<option value="schema:DateTime" />';
      options += '<option value="schema:Time" />';
      const runtimeConfig = useRuntimeConfig();
      axios
        .get(runtimeConfig.public.apiUrl + "/api/registry/schema?field=name")
        .then((res) => {
          self.$swal.hideLoading();
          if (res.data.hits) {
            for (var i = 0; i < res.data.hits.length; i++) {
              options += '<option value="' + res.data.hits[i].name + '" />';
              self.range_options.push(res.data.hits[i].name);
            }
            document.getElementById("myCustomList").innerHTML = options;
          }
        })
        .catch((err) => {
          throw err;
        });
    },
    updateTotals() {
      let totals = {
        // properties: 0,
        selected: 0,
        required: 0,
        recommended: 0,
        optional: 0,
      };
      if (this.item.hasOwnProperty("properties")) {
        this.item.properties.forEach((prop) => {
          // totals.properties++;
          if (prop && prop.selected) {
            totals.selected++;
          }
          if (prop && prop.isRequired) {
            totals.required++;
          }
          if (prop && prop.isRecommended) {
            totals.recommended++;
          }
          if (prop && prop.isOptional) {
            totals.optional++;
          }
        });
      }
      this.totals = totals;
    },
    removeProp(propLabel) {
      let self = this;
      self.$swal
        .fire({
          title: "Are you sure you want to delete " + propLabel + "?",
          text: "You won't be able to revert this",
          showCancelButton: true,
          confirmButtonColor: "#43318d",
          cancelButtonColor: "#d83f87",
          animation: false,
          customClass: "scale-in-center",
          confirmButtonText: "Yes, Delete it!",
        })
        .then((res) => {
          if (res.value) {
            let payload = {};
            payload["label"] = propLabel;
            self.$store.commit("removeProperty", payload);
          }
        });
    },
    sortedList() {
      var self = this;
      try {
        return self.$_.orderBy(self.item.properties, ["label"], ["asc"]);
      } catch (e) {
        return self.item.properties;
      }
    },
    calculatePages: function () {
      var self = this;
      self.pages = Math.ceil(self.item.properties.length / self.perPage);
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
    getSubclass(item) {
      return item.split(", ");
    },
    markSelected(propLabel) {
      let self = this;
      var payload = {};
      payload["label"] = propLabel;
      self.$store.commit("selectProp", payload);
      this.updateTotals();
    },
    markRequired(propLabel) {
      var self = this;
      for (var i = 0; i < self.item.properties.length; i++) {
        if (
          self.item.properties[i].label === propLabel &&
          self.item.properties[i].selected
        ) {
          var payload = {};
          payload["label"] = propLabel;
          self.$store.commit("requireProp", payload);
        } else if (
          self.item.properties[i].label === propLabel &&
          !self.item.properties[i].selected
        ) {
          new Notify({
            status: "error",
            title: "Order Error",
            text: "You must mark as selected first",
            position: "right",
          });
        }
      }
      this.updateTotals();
    },
    markOptional(propLabel) {
      var self = this;
      for (var i = 0; i < self.item.properties.length; i++) {
        if (
          self.item.properties[i].label === propLabel &&
          self.item.properties[i].selected
        ) {
          var payload = {};
          payload["label"] = propLabel;
          self.$store.commit("optionalProp", payload);
        } else if (
          self.item.properties[i].label === propLabel &&
          !self.item.properties[i].selected
        ) {
          new Notify({
            status: "error",
            title: "Order Error",
            text: "You must mark as selected first",
            position: "right",
          });
        }
      }
      this.updateTotals();
    },
    markRecommended(propLabel) {
      var self = this;
      for (var i = 0; i < self.item.properties.length; i++) {
        if (
          self.item.properties[i].label === propLabel &&
          self.item.properties[i].selected
        ) {
          var payload = {};
          payload["label"] = propLabel;
          self.$store.commit("recommendProp", payload);
        } else if (
          self.item.properties[i].label === propLabel &&
          !self.item.properties[i].selected
        ) {
          new Notify({
            status: "error",
            title: "Order Error",
            text: "You must mark as selected first",
            position: "right",
          });
        }
      }
      this.updateTotals();
    },
    resetAddPropForm() {
      var self = this;
      new Notify({
        status: "success",
        title: "New Property",
        text: "Added: " + self.newPropName,
        position: "right",
        autoclose: true, // Enable auto close
        autotimeout: 3000, // Set timeout in milliseconds (3 seconds)
      });
      self.newPropName = "";
      self.newPropDescription = "";
      self.newPropRange = [];
    },
    getRangeOptions() {
      var self = this;
      let options = [];
      const runtimeConfig = useRuntimeConfig();
      axios
        .get(runtimeConfig.public.apiUrl + "/api/registry/schema?field=name")
        .then((res) => {
          if (res.data.hits) {
            for (var i = 0; i < res.data.hits.length; i++) {
              options.push(res.data.hits[i].name);
            }
          }
          self.rangeOptions = options;
        })
        .catch((err) => {
          throw err;
        });
    },
    submitNewProp() {
      var self = this;
      let payload = {};
      payload["name"] = self.newPropName;
      payload["range"] = self.newPropRange.toString();
      payload["description"] = self.newPropDescription;
      payload["domain"] = self.newPropDomain;
      if (self.item.special) {
        payload["special"] = true;
      } else {
        payload["special"] = false;
      }
      self.$store.commit("addProperty", payload);
      self.addPropMode = false;
      self.resetAddPropForm();
    },
    addInputType() {
      var self = this;
      self.$swal
        .fire({
          title: "What is this property's expected type(s)?",
          footer:
            "Start typing to check for existing classes. If none found specify it's context prefix and name. eg. prefix:Name (Multiple separated by commas)",
          html: '<datalist id="myCustomList"></datalist>',
          input: "text",
          confirmButtonColor: "#43318d",
          cancelButtonColor: "#d83f87",
          confirmButtonText: "Add",
          animation: false,
          customClass: "scale-in-center",
          inputAttributes: {
            list: "myCustomList",
          },
          onOpen: function () {
            self.$swal.isLoading();
            var options = "";
            options += '<option value="schema:Text" />';
            options += '<option value="schema:URL" />';
            options += '<option value="schema:Integer" />';
            options += '<option value="schema:Number" />';
            options += '<option value="schema:Date" />';
            options += '<option value="schema:Float" />';
            options += '<option value="schema:Boolean" />';
            options += '<option value="schema:DateTime" />';
            options += '<option value="schema:Time" />';
            if (self.rangeOptions && self.rangeOptions.length) {
              for (let i = 0; i < self.rangeOptions.length; i++) {
                let element = self.rangeOptions[i];
                options += '<option value="' + element + '" />';
              }
            }
            document.getElementById("myCustomList").innerHTML = options;
            self.$swal.hideLoading();
          },
        })
        .then((res) => {
          if (res.value) {
            self.newPropRange.push(res.value);
          }
        });
    },
    addProp(domain) {
      var self = this;
      self.$swal
        .mixin({
          input: "text",
          confirmButtonText: "Next &rarr;",
          showCancelButton: true,
          confirmButtonColor: "#43318d",
          cancelButtonColor: "#d83f87",
          animation: false,
          customClass: "scale-in-center",
          progressSteps: ["1", "2", "3"],
        })
        .queue([
          {
            title: "Choose a name for your property",
            html: 'input name must be camelCased <b class="text-danger">eg. myProperty </b>',
            inputValidator: (value) => {
              return new Promise((resolve) => {
                if (value.match(/^[a-z]+(?:[A-Z][a-z]+)*$/)) {
                  // DUPLICATE CHECK
                  if (self.$store.getters.isDuplicateProp(value)) {
                    resolve(
                      "Property already exists in parent classes. All properties should be unique or more specific."
                    );
                  } else {
                    resolve();
                  }
                } else {
                  resolve("property names must be camelCased");
                }
              });
            },
          },
          {
            title: "What is this property's expected type(s)?",
            footer:
              "Start typing to check for existing classes. If none found specify it's context prefix and name. eg. prefix:Name (Multiple separated by commas)",
            html: '<datalist id="myCustomList"></datalist>',
            input: "text",
            inputAttributes: {
              list: "myCustomList",
            },
            onOpen: function () {
              var options = "";
              options += '<option value="schema:Text" />';
              options += '<option value="schema:URL" />';
              options += '<option value="schema:Integer" />';
              options += '<option value="schema:Number" />';
              options += '<option value="schema:Date" />';
              options += '<option value="schema:Float" />';
              options += '<option value="schema:Boolean" />';
              options += '<option value="schema:DateTime" />';
              options += '<option value="schema:Time" />';
              self.$swal.isLoading();
              const runtimeConfig = useRuntimeConfig();
              axios
                .get(
                  runtimeConfig.public.apiUrl +
                    "/api/registry/schema?field=name"
                )
                .then((res) => {
                  self.$swal.hideLoading();
                  if (res.data.hits) {
                    for (var i = 0; i < res.data.hits.length; i++) {
                      options +=
                        '<option value="' + res.data.hits[i].name + '" />';
                    }
                    document.getElementById("myCustomList").innerHTML = options;
                  }
                })
                .catch((err) => {
                  self.$swal.hideLoading();
                  throw err;
                });
            },
            inputValidator: (value) => {
              return (
                value.length < 10 &&
                "Property should have at least 1 input type"
              );
            },
          },
          {
            title: "Write a comment about this class",
            html: "Write a short summary about this class",
            input: "textarea",
            inputValidator: (value) => {
              return (
                value.length < 10 &&
                "Description is too short! You should write something meaningful."
              );
            },
          },
        ])
        .then((result) => {
          if (result.value) {
            self.$swal
              .fire({
                title: "Add Property " + result.value[0] + "?",
                text: result.value[2],
                showCancelButton: true,
                confirmButtonColor: "#43318d",
                cancelButtonColor: "#d83f87",
                confirmButtonText: "Yes, Add It!",
                animation: false,
                customClass: "scale-in-center",
              })
              .then((res) => {
                if (res.value) {
                  new Notify({
                    status: "success",
                    title: "Success",
                    text: result.value[0] + " added",
                    position: "right",
                    autoclose: true, // Enable auto close
                    autotimeout: 3000, // Set timeout in milliseconds (3 seconds)
                  });
                  let payload = {};
                  payload["name"] = result.value[0];
                  payload["range"] = result.value[1];
                  payload["description"] = result.value[2];
                  payload["domain"] = domain;
                  if (self.item.special) {
                    payload["special"] = true;
                  } else {
                    payload["special"] = false;
                  }
                  self.$store.commit("addProperty", payload);
                  self.expand = true;
                }
              });
          }
        });
    },
  },
  mounted: function () {
    if (this.item.special) {
      this.getRangeOptions();
      this.expand = true;
    } else if (this.item && this.item.properties) {
      this.calculatePages();
    } else {
      this.item.properties = [];
    }
    this.updateTotals();
  },
};
</script>
