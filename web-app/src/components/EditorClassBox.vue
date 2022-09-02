<template>
  <div
    class="row m-1 cBox actions"
    :class="{
      'alert-warning mb-3': item.special,
      'alert-primary': !item.special,
    }"
  >
    <div class="col-sm-10 p-2">
      <div>
        <i v-if="item.special" class="fas fa-star text-warning"></i>
        <i v-else class="fas fa-circle text-primary"></i>
        <template
          v-if="item && item.parent_classes.length"
          v-for="tree in item.parent_classes"
        >
          <template v-for="(name, i) in getSubclass(tree)">
            <small v-text="name"></small>
            <small><i class="fas fa-chevron-right"></i></small>
          </template>
        </template>
        <small class="bold"
          ><span v-text="item.label"></span>
          <i
            class="fas fa-info-circle text-info cTip pointer"
            :data-tippy-description="item.description"
            :data-tippy-label="item.label"
          ></i
        ></small>
        <!-- 🌈 prop totals 🌈 -->
        <div v-if="totals" class="col-sm-12">
          <table>
            <tr>
              <td v-for="(val, name) in totals" class="px-1">
                <small>
                  <template v-if="name == 'required'">
                    <i title="required" class="fas fa-asterisk text-danger"></i>
                    req
                  </template>
                  <template v-else-if="name == 'selected'">
                    <i
                      title="selected"
                      class="fas fa-check-circle text-success"
                    ></i>
                    sel
                  </template>
                  <template v-else-if="name == 'optional'">
                    <i title="optional" class="fas fa-square text-info"></i> opt
                  </template>
                  <template v-else-if="name == 'recommended'">
                    <i
                      title="recommended"
                      class="fas fa-circle text-warning"
                    ></i>
                    rec
                  </template>
                  <i v-else v-text="name"></i> :
                  <b
                    v-text="val"
                    :class="[val ? 'text-primary' : 'text-muted']"
                  ></b>
                </small>
              </td>
            </tr>
          </table>
        </div>
        <small
          style="clear: both"
          v-if="item.special && !item.properties"
          class="text-muted float-right"
          >Add properties here <i class="fas fa-arrow-right text-danger"></i
        ></small>
        <template v-if="showDesc">
          <small
            class="d-block text-muted"
            v-html="item.description || 'No description provided'"
          ></small>
        </template>
      </div>

      <!-- 🌈 selected list 🌈 -->
      <div v-if="!item.special" class="">
        <template
          v-if="item && item.properties"
          v-for="prop in item.properties"
        >
          <small v-if="prop.selected" class="badge badge-success m-1">
            <i
              v-if="prop && prop.isRequired"
              class="fas fa-asterisk text-danger"
            ></i>
            <i
              v-else-if="prop && prop.isRecommended"
              class="fas fa-circle text-warning"
            ></i>
            <i
              v-else-if="prop && prop.isOptional"
              class="fas fa-square text-info"
            ></i>
            <span v-text="prop.label"></span>
          </small>
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
                <small class="text-dark">
                  <span v-text="prop.label"></span>
                  <i
                    class="fas fa-info-circle cTip pointer text-info"
                    :data-tippy-description="prop.description"
                    :data-tippy-label="prop.label"
                  ></i>
                  <template v-if="showDesc">
                    <small
                      class="d-block text-muted"
                      v-html="prop.description || 'No description provided'"
                    ></small>
                  </template>
                </small>
              </div>
              <div
                class="col-sm-3 bg-dark actions d-flex align-items-center justify-content-around"
              >
                <i
                  v-show="item.special"
                  class="fas fa-minus-circle pointer text-muted unselectable remove"
                  @click="removeProp(prop.label)"
                ></i>
                <i
                  class="fas fa-check-circle pointer unselectable select"
                  @click="markSelected(prop.label)"
                  :class="{
                    'text-muted': !prop.selected,
                    'text-success': prop.selected,
                  }"
                ></i>
                <i
                  class="fas fa-asterisk required pointer unselectable"
                  @click="markRequired(prop.label)"
                  :class="{
                    'text-muted': !prop.isRequired,
                    'text-danger': prop.isRequired,
                  }"
                ></i>
                <i
                  class="fas fa-circle recommended pointer unselectable"
                  @click="markRecommended(prop.label)"
                  :class="{
                    'text-muted': !prop.isRecommended,
                    'text-warning': prop.isRecommended,
                  }"
                ></i>
                <i
                  class="fas fa-square optional pointer unselectable"
                  @click="markOptional(prop.label)"
                  :class="{
                    'text-muted': !prop.isOptional,
                    'text-info': prop.isOptional,
                  }"
                ></i>
              </div>
            </div>
          </template>
        </div>

        <!-- 🌈 results 🌈 -->
        <template v-for="prop in paginatedResults">
          <div class="row m-1 alert-light pBox actions">
            <div class="col-sm-9">
              <small class="mainTextDark">
                <span v-text="prop.label"></span>
                <i
                  class="fas fa-info-circle cTip pointer text-info"
                  :data-tippy-description="prop.description"
                  :data-tippy-label="prop.label"
                ></i>
                <template v-if="showDesc">
                  <small
                    class="d-block text-muted"
                    v-html="prop.description || 'No description provided'"
                  ></small>
                </template>
              </small>
            </div>
            <div
              class="col-sm-3 bg-dark actions d-flex align-items-center justify-content-around"
            >
              <i
                v-show="item.special"
                class="fas fa-minus-circle pointer text-muted unselectable tip"
                data-tippy-info="Delete"
                @click="removeProp(prop.label)"
              ></i>
              <i
                v-show="item.special"
                class="fas fa-pen-square pointer text-muted unselectable tip mr-3"
                data-tippy-info="Edit"
                @click="editCustomProp(prop)"
              ></i>
              <i
                class="fas fa-check-circle pointer unselectable select"
                @click="markSelected(prop.label)"
                :class="{
                  'text-muted': !prop.selected,
                  'text-success': prop.selected,
                }"
              ></i>
              <i
                class="fas fa-asterisk required pointer unselectable"
                @click="markRequired(prop.label)"
                :class="{
                  'text-muted': !prop.isRequired,
                  'text-danger': prop.isRequired,
                }"
              ></i>
              <i
                class="fas fa-circle recommended pointer unselectable"
                @click="markRecommended(prop.label)"
                :class="{
                  'text-muted': !prop.isRecommended,
                  'text-warning': prop.isRecommended,
                }"
              ></i>
              <i
                class="fas fa-square optional pointer unselectable"
                @click="markOptional(prop.label)"
                :class="{
                  'text-muted': !prop.isOptional,
                  'text-info': prop.isOptional,
                }"
              ></i>
            </div>
          </div>
        </template>

        <!-- 🌈 pagination 🌈 -->
        <template v-if="!item.special && item.properties.length > perPage">
          <div class="d-flex flex-wrap justify-content-center p-1 mt-2">
            <div class="page-item rounded-0" :class="{ disabled: page <= 1 }">
              <a class="page-link p-1" @click.prevent="prevPage()"
                ><i class="fas fa-step-backward"></i
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
                ><i class="fas fa-step-forward"></i
              ></a>
            </div>
          </div>
        </template>
      </div>
    </div>

    <div
      class="col-sm-2 p-2 bg-dark actions d-flex align-items-center justify-content-around"
    >
      <span
        v-if="item.special"
        class="fa-stack fa-1x pointer addprop unselectable tip"
        @click="
          addPropMode = !addPropMode;
          (newPropDomain = item.label), populateInputOptions();
        "
      >
        <i
          class="fas fa-circle fa-stack-2x"
          :class="[addPropMode ? 'text-success' : 'mainTextLight']"
        ></i>
        <i
          class="fas fa-stack-1x text-light"
          :class="[addPropMode ? 'fa-minus' : 'fa-plus']"
        ></i>
      </span>
      <span
        class="fa-stack fa-1x pointer expand unselectable"
        @click="expand = !expand"
        v-if="item && item.properties"
      >
        <i
          class="fas fa-circle fa-stack-2x"
          :class="{ 'text-muted': !expand, 'text-success': expand }"
        ></i>
        <i
          class="fas fa-stack-1x text-light"
          :class="[expand ? 'fa-list-ul' : 'fa-ellipsis-h']"
        ></i>
      </span>
    </div>

    <div
      v-if="addPropMode"
      class="col-sm-12 p-2 bg-dark d-flex align-items-center justify-content-center text-light"
    >
      <div class="col-sm-10 m-auto p-3 bg-light text-muted rounded">
        <h5>New Property</h5>
        <form>
          <div class="form-group">
            <label for="name"
              >Name <i class="fas fa-asterisk text-danger"></i
            ></label>
            <input
              v-model="newPropName"
              type="text"
              class="form-control"
              id="name"
              placeholder="name of new property eg. myProperty"
            />
            <small class="d-block my-1 text-info"
              >Learn about naming conventions
              <a
                href="https://schema.org/docs/styleguide.html"
                target="_blank"
                rel="nonreferrer"
                >here</a
              ></small
            >
            <small v-if="propExists" class="text-danger"
              >A property with this name already exists</small
            >
          </div>
          <div class="form-group">
            <label for="desc"
              >Description <i class="fas fa-asterisk text-danger"></i
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
              >Domain <i class="fas fa-asterisk text-danger"></i
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
              >Input Type(s) <i class="fas fa-asterisk text-danger"></i
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
              :disabled="!addNewPropReady && !propExists"
              :class="[
                addNewPropReady && !propExists
                  ? 'btn-success'
                  : 'btn-secondary',
              ]"
              type="submit"
              class="btn btn-lg w-100"
              @click.prevent="submitNewProp()"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";
import axios from "axios";
import { mapGetters } from "vuex";
import { orderBy } from "lodash";

import "@/assets/js/notify.min.js";

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
      this.propExists = self.$store.getters.isDuplicateProp(v);
    },
    query: function (q) {
      if (q) {
        this.filtered = this.item.properties.filter((prop) =>
          prop["label"].includes(q)
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
      let payload = {};
      payload["label"] = prop["label"];
      self.$store.commit("removeProperty", payload);
    },
    handlePillSubmit() {
      var self = this;
      if (!self.newPropRange.includes(self.range_query)) {
        self.newPropRange.push(self.range_query);
        self.range_query = "";
      } else {
        self.$swal.fire({
          type: "error",
          toast: true,
          title: "Option already added",
          showConfirmButton: false,
          timer: 2000,
        });
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
      axios
        .get(self.$apiUrl + "/api/registry/schema?field=name")
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
        properties: 0,
        selected: 0,
        required: 0,
        recommended: 0,
        optional: 0,
      };
      if (this.item.hasOwnProperty("properties")) {
        this.item.properties.forEach((prop) => {
          totals.properties++;
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
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
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
        return orderBy(self.item.properties, ["label"], ["asc"]);
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
          $.notify("You must mark as selected first", {
            globalPosition: "right",
            style: "danger",
            showDuration: 40,
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
          $.notify("You must mark as selected first", {
            globalPosition: "right",
            style: "danger",
            showDuration: 40,
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
          $.notify("You must mark as selected first", {
            globalPosition: "right",
            style: "danger",
            showDuration: 40,
          });
        }
      }
      this.updateTotals();
    },
    resetAddPropForm() {
      var self = this;
      $.notify("New property added: " + self.newPropName, {
        globalPosition: "right",
        style: "success",
        showDuration: 200,
      });
      self.newPropName = "";
      self.newPropDescription = "";
      self.newPropRange = [];
    },
    getRangeOptions() {
      var self = this;
      let options = [];
      axios
        .get(self.$apiUrl + "/api/registry/schema?field=name")
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

      // if (!self.newPropName.match(/^[a-z]+(?:[A-Z][a-z]+)*$/)) {
      //   $.notify("name does not follow naming conventions",{ globalPosition: 'right',style:'warning', showDuration: 200, });
      // }
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
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
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
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
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
              axios
                .get(self.$apiUrl + "/api/registry/schema?field=name")
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
                confirmButtonColor: "{{color_main}}",
                cancelButtonColor: "{{color_sec}}",
                confirmButtonText: "Yes, Add It!",
                animation: false,
                customClass: "scale-in-center",
              })
              .then((res) => {
                if (res.value) {
                  $.notify(result.value[0] + " added", {
                    globalPosition: "right",
                    style: "success",
                    showDuration: 200,
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

    tippy(".cTip", {
      interactive: "true",
      placement: "right",
      animation: "fade",
      trigger: "click",
      theme: "light",
      onShow(instance) {
        let desc = instance.reference.dataset.tippyDescription;
        instance.setContent(
          "<div class='text-muted m-0 text-left wraptext'>" + desc + "</div>"
        );
      },
    });

    tippy(".expand", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-muted m-0" style="border-radius:none">Show/Hide Properties</div>',
      animation: "fade",
      theme: "light",
    });

    tippy(".addprop", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-muted m-0" style="border-radius:none">Add New Property</div>',
      animation: "fade",
      theme: "light",
    });

    tippy(".required", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-danger m-0" style="border-radius:none">Mark As Required</div>',
      animation: "fade",
      theme: "light",
    });

    tippy(".recommended", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-warning m-0" style="border-radius:none">Mark As Recommended</div>',
      animation: "fade",
      theme: "light",
    });

    tippy(".optional", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-info m-0" style="border-radius:none">Mark As Optional</div>',
      animation: "fade",
      theme: "light",
    });

    tippy(".select", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-success m-0" style="border-radius:none">Select (Re-Use) This Property</div>',
      animation: "fade",
      theme: "light",
    });

    tippy(".remove", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-danger m-0" style="border-radius:none">Delete Property</div>',
      animation: "fade",
      theme: "light",
    });
  },
};
</script>
