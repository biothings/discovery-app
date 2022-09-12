<template>
  <div class="d-block w-100">
    <div class="row m-0 p-relative">
      <div class="col-sm-12 w-100">
        <div class="d-flex justify-content-center align-items-stretch">
          <!-- 🍏 TABS 🍏-->
          <template v-for="(value, name) in parsed_options">
            <div
              class="pointer m-1 text-center text-light rounded"
              @click="select(name)"
              :class="[
                type_selected == name
                  ? 'mainBackLight arrow-bottom'
                  : 'mainBackDark',
                isChild ? 'p-1' : 'p-2',
              ]"
            >
              <h6 class="m-0" v-if="!isChild">
                <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
                <span v-text="name"></span>
              </h6>
              <h6 class="m-0" v-else>
                <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
                <span v-text="name"></span>
              </h6>
            </div>
          </template>
        </div>
      </div>
      <!-- 🍏 Animation 🍏-->
      <div style="perspective: 800px; z-index: 999">
        <div :id="'over-' + main_name"></div>
      </div>
      <!-- 🍏 TAB SECTIONS 🍏-->
      <div class="col-sm-12 w-100 text-dark">
        <form
          class="w-100 fade-in"
          v-for="(value, name) in parsed_options"
          @submit.prevent="handleSubmit(name, value)"
        >
          <template v-if="type_selected == name">
            <div class="col-sm-12 py-2">
              <template v-if="!isChild">
                <small class="text-muted m-2"
                  ><font-awesome-icon
                    icon="fas fa-circle"
                    class="text-danger"
                  ></font-awesome-icon>
                  = required</small
                >
                <small class="text-muted"
                  ><font-awesome-icon
                    icon="fas fa-circle"
                    class="text-info"
                  ></font-awesome-icon>
                  = recommended</small
                >
              </template>
            </div>

            <!-- 🤩 CLASS TYPE  IF NOT ENUM OR VOCAB🤩-->
            <div
              class="col-sm-12 mainBackLight text-light p-1 text-center classTab"
              v-if="value && !value.vocabulary && !value.enum"
            >
              <h5 class="m-0" v-text="name"></h5>
            </div>

            <!-- 🐸 VOCABULARY TOP LEVEL 🐸-->
            <div
              v-if="value && value.vocabulary"
              class="bg-light p-4 text-light d-flex justify-content-start align-items-center"
              :class="[isChild ? 'col-sm-12' : 'col-sm-12']"
            >
              <Vocabulary :main_name="main_name" :info="info"></Vocabulary>
            </div>

            <!-- 🍒 ENUMERATION TOP LEVEL 🍒-->
            <div
              v-else-if="value && value.enum"
              class="bg-light p-4 text-light d-flex justify-content-start align-items-center"
              :class="[isChild ? 'col-sm-12' : 'col-sm-12']"
            >
              <button
                class="btn btn-danger m-auto"
                @click.prevent="handleEnum(main_name, value)"
              >
                <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
                <span v-text="main_name"></span>
              </button>
            </div>

            <!-- 🎃 ARRAY KEYWORDS 🎃-->
            <div
              v-else-if="value && value.keywords && !value.enum"
              class="bg-light p-4 text-light align-items-center"
              :class="[isChild ? 'col-sm-12' : 'col-sm-12']"
            >
              <div class="w-100">
                <form
                  id="keywords_form"
                  class="w-100 d-flex justify-content-center"
                  @submit.prevent="addKeyword"
                >
                  <input
                    class="form-control"
                    type="text"
                    v-model="keyword_input"
                  />
                  <button
                    type="button"
                    class="btn btn-sm btn-primary form-label"
                    @click="addKeyword"
                  >
                    Add Keyword
                  </button>
                </form>
              </div>
              <div class="alert alert-success m-3 w-100" v-show="keywords.size">
                <span
                  v-for="(text, i) in [...keywords]"
                  class="badge badge-sm badge-success pointer"
                >
                  <small v-html="text"></small>
                </span>
              </div>
            </div>

            <!-- 🌈🌈🌈 FOR EACH PROP 🌈🌈🌈-->

            <div
              v-for="(propInfo, propName) in value.properties"
              class="row m-0"
            >
              <!-- 🤩 INPUT DESCRIPTION 🤩-->
              <div
                class="col-sm-12 p-1"
                v-if="propInfo && propInfo.description && propName !== '@type'"
              >
                <small v-html="propInfo.description"></small>
              </div>
              <!-- 🤩 INPUT NAME 🤩-->
              <div
                class="bg-dark p-1 text-light d-flex justify-content-start align-items-center border-bottom"
                :class="[isChild ? 'col-sm-12' : 'col-sm-12 col-md-4']"
                v-if="propName !== '@type'"
              >
                <small>
                  <b v-if="value && value.required">
                    <font-awesome-icon
                      icon="fas fa-circle"
                      class="text-info"
                      :class="[
                        isRequired(value.required, propName)
                          ? 'text-danger'
                          : 'text-info',
                      ]"
                    ></font-awesome-icon>
                    <span v-text="propName"></span>
                  </b>
                  <b v-else class="text-info" v-text="propName"></b>
                </small>
              </div>
              <!-- 🎃 INPUT TYPES 🎃-->
              <div
                class="p-1 text-dark border-bottom"
                :class="[
                  isChild
                    ? 'col-sm-12 alert-secondary'
                    : 'col-sm-12 col-md-8 bg-light',
                ]"
                v-if="propName !== '@type'"
              >
                <!-- 🥶 WITH TYPE 🥶-->
                <template v-if="propInfo && propInfo.type">
                  <!-- 🥶 STRING TYPES 🥶-->
                  <template v-if="propInfo.type == 'string'">
                    <!-- 🐸 VOCABULARY UNDER PROPERTIES 🐸-->
                    <template v-if="propInfo && propInfo.vocabulary">
                      <button
                        class="btn btn-danger m-auto"
                        @click.prevent="handleVocab(main_name, value)"
                      >
                        <font-awesome-icon
                          icon="fas fa-plus"
                        ></font-awesome-icon>
                        <span v-text="main_name + '(s)'"></span>
                      </button>
                    </template>
                    <!-- 🥶 WITH FORMAT 🥶-->
                    <template v-else-if="propInfo && propInfo.format == 'uri'">
                      <!-- 🥶 STRING URL 🥶-->
                      <div class="input-group">
                        <div class="input-group-prepend">
                          <span class="input-group-text" id="basic-addon1"
                            ><font-awesome-icon
                              icon="fas fa-link"
                            ></font-awesome-icon
                          ></span>
                        </div>
                        <input
                          class="form-control"
                          type="url"
                          @input="updateObject(propName, $event)"
                          :placeholder="'enter ' + propName"
                        />
                      </div>
                    </template>
                    <template v-else-if="propInfo && propInfo.format == 'date'">
                      <!-- 🥶 STRING DATE 🥶-->
                      <div class="input-group">
                        <div class="input-group-prepend">
                          <span class="input-group-text" id="basic-addon1"
                            ><font-awesome-icon
                              icon="fas fa-calendar-alt"
                            ></font-awesome-icon
                          ></span>
                        </div>
                        <input
                          class="form-control"
                          type="date"
                          @input="updateObject(propName, $event)"
                        />
                      </div>
                    </template>
                    <!-- 🥶 REGULAR STRING 🥶-->
                    <input
                      v-else
                      class="form-control"
                      type="text"
                      @input="updateObject(propName, $event)"
                      :placeholder="'enter ' + propName"
                    />
                  </template>
                  <!-- 🧤  INTEGER 🧤 -->
                  <template v-else-if="propInfo && propInfo.type == 'integer'">
                    <div class="input-group">
                      <div class="input-group-prepend">
                        <span class="input-group-text" id="basic-addon1"
                          ><font-awesome-icon
                            icon="fas fa-hashtag"
                          ></font-awesome-icon
                        ></span>
                      </div>
                      <input
                        class="form-control"
                        type="number"
                        @input="updateObject(propName, $event)"
                      />
                    </div>
                  </template>
                  <!-- 🌼   BOOLEAN 🌼  -->
                  <template v-else-if="propInfo && propInfo.type == 'boolean'">
                    <small>Oops, this hasn't been handled yet..</small>
                  </template>
                  <!-- 🩳  TYPE OBJECT 🩳 -->
                  <template v-else-if="propInfo && propInfo.type == 'object'">
                    <div class="alert-secondary">
                      <pre v-text="getNestedValue(propName)"></pre>
                    </div>
                    <type-selector
                      :info="propInfo"
                      :main_name="main_name"
                      :childName="propName"
                      :isChild="true"
                      @update="updateParent"
                    ></type-selector>
                  </template>

                  <!-- 🥶🥶🥶 LAST RESORT STRING 🥶🥶🥶-->
                  <input
                    v-else
                    class="form-control"
                    type="text"
                    @input="updateObject(propName, $event)"
                    :placeholder="'enter ' + propName"
                  />
                </template>
                <!-- 👹  NO TYPE ON TOP LEVEL 👹 -->
                <template v-else>
                  <template v-if="propInfo && propInfo.anyOf">
                    <!-- 🦷  ANY OF 🦷 -->
                    <div class="w-100">
                      <div class="border rounded p-1">
                        <pre v-text="getNestedValue(propName)"></pre>
                      </div>
                      <type-selector
                        :info="propInfo"
                        :main_name="main_name"
                        :childName="propName"
                        :isChild="true"
                        @update="updateParent"
                      ></type-selector>
                    </div>
                  </template>
                  <template v-if="propInfo && propInfo.oneOf">
                    <!-- 👿  ONE OF 👿 -->
                    <div class="w-100">
                      <div class="alert-secondary">
                        <pre v-text="getNestedValue(propName)"></pre>
                      </div>
                      <type-selector
                        :info="propInfo"
                        :main_name="main_name"
                        :childName="propName"
                        :isChild="true"
                        @update="updateParent"
                      ></type-selector>
                    </div>
                  </template>
                  <!-- 👹  CONSTANT 👹 -->
                  <template v-else-if="propInfo && propInfo.const">
                    <div class="text-muted">
                      <small v-text="propInfo.const"></small>
                    </div>
                  </template>
                  <!-- 🥶🥶🥶 LAST RESORT NO TYPE 🥶🥶🥶-->
                  <template v-else>
                    <small v-text="propInfo"></small>
                  </template>
                </template>
              </div>
            </div>
            <!-- 🍏 SUBMIT IF NOT ENUM OR VOCAB🍏-->
            <div
              class="col-sm-12 p-0 mt-2"
              v-if="value && !value.vocabulary && !value.enum & !value.keywords"
            >
              <button
                type="submit"
                class="btn w-100"
                :class="[
                  isChild ? 'btn-info btn-sm' : 'btn-success btn-lg',
                  pulse && isChild ? 'jello' : '',
                ]"
              >
                Add <span v-text="isChild ? childName : name"></span>
              </button>
            </div>
          </template>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";
import Vocabulary from "./Vocabulary.vue";

export default {
  name: "TypeSelector",
  data: function () {
    return {
      options: [],
      parsed_options: {},
      type_selected: "",
      userObject: {},
      pulse: false,
      keywords: new Set(),
      keyword_input: "",
    };
  },
  props: ["info", "main_name", "isChild", "childName"],
  components: {
    Vocabulary,
  },
  methods: {
    parseOptions() {
      var self = this;
      // get options from oneOf or anyOf
      self.info && self.info.oneOf
        ? (self.options = self.info.oneOf)
        : self.info && self.info.anyOf
        ? (self.options = self.info.anyOf)
        : console.warn(`No oneOf/anyOf in ${self.main_name}`);
      // narrow options don't include array of existing options
      if (self.options.length) {
        // ANY OF AND ONE OF TYPE FIELDS
        for (let i = 0; i < self.options.length; i++) {
          const option = self.options[i];
          if (option && option["@type"]) {
            self.parsed_options[option["@type"]] = option;
          } else if (option && option["items"] && option["items"]["@type"]) {
            if (!self.parsed_options.hasOwnProperty(option["items"]["@type"])) {
              self.parsed_options[option["items"]["@type"]] = option;
            }
          } else if (option && option["enum"]) {
            // use main prop name and replace underscore with space
            let name = self.main_name.split("_").join(" ");
            if (!self.parsed_options.hasOwnProperty(name)) {
              self.parsed_options[name] = option;
            }
          } else if (option && option["type"] == "array") {
            let name = self.main_name.split("_").join(" ");
            if (!self.parsed_options.hasOwnProperty(name)) {
              option["keywords"] = true;
              self.parsed_options[name] = option;
            }
          }
        }
      } else if (
        self.info.hasOwnProperty("properties") &&
        self.info.hasOwnProperty("@type") &&
        self.info.hasOwnProperty("type") &&
        self.info.type == "object"
      ) {
        // OBJECT TYPE FIELD
        self.parsed_options[self.info["@type"]] = self.info;
      }
      // console.log(self.main_name, self.parsed_options)
      // self.checkAutoSelect();
    },
    isRequired(requiredList, name) {
      return requiredList.includes(name) ? true : false;
    },
    updateObject(prop, event) {
      var self = this;
      self.userObject[prop] = event.target.value;
    },
    updateParent(childValue) {
      var self = this;
      if (self.userObject && self.userObject[childValue.subfield]) {
        let existing_val = [self.userObject[childValue.subfield]];
        existing_val.push(childValue.value);
        self.userObject[childValue.subfield] = existing_val;
      } else {
        self.userObject[childValue.subfield] = childValue.value;
      }
    },
    select(name) {
      var self = this;
      self.type_selected == name
        ? (self.type_selected = "")
        : (self.type_selected = name);
    },
    getNestedValue(childName) {
      var self = this;
      return self.userObject.hasOwnProperty(childName)
        ? JSON.stringify(self.userObject[childName], null, 2)
        : "";
    },
    checkAutoSelect() {
      var self = this;
      Object.keys(self.parsed_options).length == 1
        ? (self.type_selected = Object.keys(self.parsed_options)[0])
        : console.log("multiple options");
    },
    handleVocab(propName, propInfo) {
      let self = this;

      self.$swal
        .fire({
          title: propName,
          text: "Search for an existing term here:",
          input: "text",
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
          animation: false,
          customClass: "scale-in-center",
          inputAttributes: {
            autocapitalize: "off",
          },
          showCancelButton: true,
          confirmButtonText: "Look up",
          showLoaderOnConfirm: true,
          focusConfirm: false,
          preConfirm: (query) => {
            let ontologies = propInfo["vocabulary"]["ontology"].toString();
            let children = propInfo["vocabulary"]["children_of"].toString();
            let url =
              `https://www.ebi.ac.uk/ols/api/search?q=${query}` +
              "&ontology=" +
              ontologies +
              "&childrenOf=" +
              children +
              "&type=class&fieldList=id,iri,label,description,obo_id,short_form,ontology_prefix" +
              "&queryFields=label" +
              "&rows=100";

            return fetch(url)
              .then((response) => {
                if (!response.ok) {
                  throw new Error(response.statusText);
                }
                return response.json();
              })
              .catch((error) => {
                self.$swal.showValidationMessage(`Request failed: ${error}`);
              });
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
        })
        .then((result) => {
          if (result.value) {
            let html =
              "<div id='ontology' style='max-height: 500px;overflow: scroll;' class='p-1 text-left'>";
            let docs = result.value.response.docs;
            html += self.getVocabCheckboxHTML(html, docs);
            if (propInfo && !propInfo.strict) {
              html += `<div class="alert alert-info mt-1">
                          <h6>Didn't find what you are looking for? Enter value here:</h6>
                          <input class="form-control" type="text" id="qTerm">
                      </div>`;
            }
            html += "</div>";

            self.$swal
              .fire({
                title: propName + "(s):",
                html: html,
                confirmButtonColor: "{{color_main}}",
                cancelButtonColor: "{{color_sec}}",
                animation: false,
                customClass: "scale-in-center",
                preConfirm: () => {
                  let checked = [];

                  for (var i = 0; i < 100; i++) {
                    let x = document.getElementById("cb" + i);
                    if (x && x.checked) {
                      checked.push(x.value);
                    }
                  }
                  let y = document.getElementById("qTerm");
                  if (y.value) {
                    checked.push(y.value);
                  }
                  return checked;
                },
              })
              .then((result) => {
                if (result.value) {
                  for (var i = 0; i < result.value.length; i++) {
                    let res = result.value[i];
                    // let data = {value:res, subfield: self.main_name};
                    // console.log('term lookup res', data)
                    // self.updateParent(data)
                    var payload = {};
                    payload["item"] = res;
                    payload["from"] = self.main_name;
                    this.$store.commit("addToArrayFrom", payload);
                    this.$store.dispatch("saveProgress");
                  }
                }
              });
          }
        });
    },
    getVocabCheckboxHTML(html, docs) {
      for (var i = 0; i < docs.length; i++) {
        tippy("#cb" + i, {
          content: docs[i],
        });

        let label = docs[i]["label"];
        if (label && label.length > 37) {
          label = label.substring(0, 37) + "...";
        }
        html +=
          `<div class="form-check">
                      <input class="form-check-input mr-2 slider" type="checkbox" value="` +
          docs[i]["iri"] +
          `" id="cb` +
          i +
          `">
                      <label class="form-check-label" for="cb` +
          i +
          `" title="` +
          docs[i]["label"] +
          `">
                          ` +
          label +
          `
                          <i class="modaltip" data-tippy-info='` +
          JSON.stringify(docs[i]) +
          `'>ℹ️</i>
                      </label>
                  </div>`;
      }
      return html;
    },
    regularSubmit(ClassType, fieldInfo) {
      var self = this;
      let inputIsObject =
        fieldInfo.hasOwnProperty("type") && fieldInfo.type == "object"
          ? true
          : false;
      if (ClassType && inputIsObject) {
        self.userObject = Object.assign(
          { "@type": ClassType },
          self.userObject
        );
      }
      let data = Object.assign({}, self.userObject);
      // console.log('submit data', JSON.stringify(data, null, 2))
      if (self.isChild) {
        // CHILD
        self.$emit("update", { value: data, subfield: self.childName });
        self.type_selected = "";
      } else {
        // PARENT
        var payload = {};
        payload["item"] = data;
        payload["from"] = self.main_name;
        this.$store.commit("addToArrayFrom", payload);
        this.$store.dispatch("saveProgress");
        //reset
        self.userObject = {};
        self.type_selected = "";
      }
    },
    animatedSubmit(ClassType, fieldInfo) {
      let self = this;
      const over = document.querySelector("#over-" + self.main_name);
      // hide lower part
      self.type_selected = "";

      over.classList = "bg-success text-center p-5 slit-out-horizontal";
      over.innerHTML = `<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
            <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
            <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
          </svg>`;
      setTimeout(() => {
        self.regularSubmit(ClassType, fieldInfo);
        over.classList = "";
        over.innerHTML = "";
      }, 1900);
    },
    handleSubmit(ClassType, fieldInfo) {
      let self = this;
      if (self.requirementsFulfilled(fieldInfo)) {
        if (!self.isChild) {
          self.animatedSubmit(ClassType, fieldInfo);
        } else {
          self.regularSubmit(ClassType, fieldInfo);
        }
      } else {
        self.$swal.fire({
          type: "error",
          toast: true,
          title: `${ClassType} missing requirements`,
          showConfirmButton: false,
          timer: 2000,
        });
      }
    },
    requirementsFulfilled(req) {
      let self = this;
      let req_list = req.hasOwnProperty("required") ? req.required : false;
      if (!req_list) return true;
      let check = true;
      req_list.forEach((r) => {
        if (!self.userObject.hasOwnProperty(r)) check = false;
      });
      return check;
    },
    handleEnum(propName, propInfo) {
      let self = this;
      let e = propInfo["enum"];
      let html = "";

      for (var eIndex = 0; eIndex < e.length; eIndex++) {
        let name = e[eIndex];
        html +=
          '<div><label><input type="checkbox" class="mr-1 zoom-2" id="cb' +
          eIndex +
          '" value="' +
          name +
          '"/>' +
          name +
          "</label></div>";
      }

      html =
        `<div class="text-left">
                  <form id=#cbForm">` +
        html +
        `</form>
                </div>`;

      self
        .$swal({
          title: propName,
          inputAttributes: {
            id: "hideThis",
          },
          animation: false,
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
          customClass: "scale-in-center",
          html: html,
          onOpen: () => {
            document.getElementById("hideThis").classList.add("d-none");
          },
          preConfirm: () => {
            let checked = [];

            for (var i = 0; i < e.length; i++) {
              let x = document.getElementById("cb" + i);
              if (x && x.checked) {
                checked.push(x.value);
              }
            }
            console.log(checked);
            return checked;
          },
        })
        .then((result) => {
          if (result.value) {
            for (var i = 0; i < result.value.length; i++) {
              var payload = {};
              payload["item"] = result.value[i];
              payload["from"] = propName;
              this.$store.commit("addToArrayFrom", payload);

              this.$store.dispatch("saveProgress");
            }
          }
        });
    },
    addKeyword() {
      var payload = {};
      payload["item"] = this.keyword_input;
      payload["from"] = this.main_name;
      this.$store.commit("addToArrayFrom", payload);
      this.$store.dispatch("saveProgress");
      this.keyword_input = "";
    },
  },
  watch: {
    userObject: {
      handler(val) {
        let keys = Object.keys(val).length;
        keys >= 1 ? (this.pulse = true) : (this.pulse = false);
      },
      deep: true,
    },
  },
  mounted: function () {
    this.parseOptions();
  },
};
</script>
