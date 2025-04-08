<template>
  <div class="m-0 inputbox fade-in" :id="name" v-if="!isInputHidden">
    <div class="row m-0">
      <div
        class="col-sm-10 p-1 text-left d-flex align-items-center justify-content-center"
        :class="[userInput || userInput === false ? '' : 'alert-light']"
      >
        <div class="d-flex w-100 justify-content-center">
          <div class="w-100 p-2">
            <div class="pb-3">
              <div class="col-sm-12 p-0 d-flex justify-content-start">
                <small v-if="isRequired && !userInput && userInput !== false"
                  ><font-awesome-icon
                    icon="fas fa-asterisk"
                    class="fa-xs text-danger required pointer unselectable mr-1"
                  ></font-awesome-icon
                ></small>
                <h6
                  class="m-0"
                  :class="[
                    userInput || userInput === false
                      ? 'text-success'
                      : 'text-dark',
                  ]"
                >
                  <span
                    v-html="info.description || 'No description provided'"
                  ></span>
                  <small class="mainTextLight">
                    (<span v-text="name"></span>)
                  </small>
                  <br>
                  <small class="text-dark" v-if="name === 'identifier'">
                    Note: Identifier is a unique identifier for the resource. If multiple are provided, all will be saved but only the first will be used as the canonical identifier.
                  </small>
                </h6>
              </div>
              <h6 v-show="loading" class="text-primary">
                Loading
                <font-awesome-icon
                  icon="fas fa-spinner fa-pulse"
                ></font-awesome-icon>
              </h6>
              <div class="ml-3">
                <!--🌈🌈🌈 INPUT 🌈 🌈🌈 TYPES 🌈🌈🌈-->

                <!-- 🌈 BOOLEAN 🌈 -->
                <template v-if="info && info?.type === 'boolean'">
                  <BooleanInput :name="name" :info="info"></BooleanInput>
                </template>
                <template v-if="info && info?.type === 'string'">
                  <!-- 🌈 STRING 🌈 -->
                  <template v-if="info && !info.format">
                    <!-- 🌈 STRING VOCABULARY🌈 -->
                    <template v-if="info && info.vocabulary">
                      <small
                        >Input
                        <b
                          v-text="
                            info.vocabulary && !info.vocabulary.strict
                              ? 'CAN'
                              : 'MUST'
                          "
                        ></b>
                        be from existing ontology terms.</small
                      >
                      <div class="input-group">
                        <div class="input-group-prepend">
                          <div class="input-group-text bg-secondary text-light">
                            <font-awesome-icon
                              icon="fas fa-search"
                            ></font-awesome-icon>
                          </div>
                        </div>
                        <input
                          :required="isRequired"
                          type="text"
                          v-model="vocabTerm"
                          class="form-control form-control-sm"
                          :placeholder="
                            userInput ? userInput : 'Type to begin search'
                          "
                          id="stringInput"
                          list="suggestionlist"
                        />
                      </div>
                      <datalist id="suggestionlist">
                        <template v-for="item in vocabSuggestions">
                          <option
                            :value="item.autosuggest"
                            @click="
                              vocabTerm = item.autosuggest;
                              vocabSuggestions = [];
                            "
                          ></option
                        ></template>
                      </datalist>
                      <div
                        v-show="vocabTerm"
                        class="alert alert-light optionBox"
                      >
                        <small
                          ><b
                            class="text-primary"
                            v-text="'(' + vocab.length + ')'"
                          ></b>
                          Existing results related to: <i v-text="vocabTerm"></i
                        ></small>
                        <template
                          v-if="vocab.length"
                          v-for="(item, i) in vocab"
                        >
                          <div class="form-check">
                            <input
                              class="form-check-input"
                              type="radio"
                              name="exampleRadios"
                              :id="i"
                              :value="item.iri"
                              @click="
                                userInput = item.iri;
                                vocabDetails = item;
                              "
                              v-model="userInput"
                            />
                            <label class="form-check-label" :for="i">
                              <span v-text="item.label"></span>
                              <font-awesome-icon
                                v-if="userInput && userInput === item.iri"
                                icon="fas fa-check"
                                class="text-success"
                              ></font-awesome-icon>
                            </label>
                          </div>
                        </template>
                        <template
                          v-if="info.vocabulary && !info.vocabulary.strict"
                        >
                          <div class="alert alert-warning">
                            <h6>Didn't find what you are looking for?</h6>
                            <p class="text-muted">
                              Just use
                              <b
                                class="pointer text-success"
                                v-text="vocabTerm"
                                @click="
                                  userInput = vocabTerm;
                                  vocabDetails = {};
                                "
                              ></b>
                            </p>
                          </div>
                        </template>
                      </div>
                    </template>
                    <!-- 🌈 ENUM 🌈 -->
                    <template
                      v-else-if="info && info.enum"
                      v-for="(item, i) in info.enum"
                    >
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="radio"
                          name="exampleRadios"
                          :id="i"
                          :value="item"
                          @click="userInput = item"
                          v-model="userInput"
                        />
                        <label
                          :class="{ 'text-success': userInput === item }"
                          class="form-check-label"
                          :for="i"
                          v-text="item"
                        ></label>
                      </div>
                    </template>
                    <!-- 🌈 STRING NORMAL🌈 -->
                    <template v-else>
                      <small class="text-info" v-if="name === 'description'">
                        This field is recommended to be between 50 and 5000
                        characters long (
                        <b v-text="(userInput && userInput.length) || '0'"></b>
                        characters).
                        <a
                          href="https://developers.google.com/search/docs/data-types/dataset#dataset"
                          target="_blank"
                          >Learn more</a
                        >.
                      </small>
                      <!-- 🌈 NAME FIELD🌈 -->
                      <template v-if="name == 'name'">
                        <NameSpecial :info="info" :name="name"></NameSpecial>
                      </template>
                      <!-- 🌈 IDENTIFIER FIELD🌈 -->
                      <template v-else-if="name == 'identifier'">
                        <IdentifierSpecial
                          :info="info"
                          :name="name"
                        ></IdentifierSpecial>
                      </template>
                      <!-- 🌈 TEXTAREA 🌈 -->
                      <textarea
                        v-else
                        :rows="name === 'description' ? 5 : 2"
                        type="text"
                        v-model="userInput"
                        class="form-control form-control-sm"
                        placeholder="enter text here"
                      ></textarea>
                    </template>
                    <!-- 🌈 VOCAB PREVIEW🌈 -->
                    <template
                      v-if="
                        vocabDetails &&
                        vocab.length &&
                        vocabDetails.ontology_prefix
                      "
                    >
                      <div class="alert alert-info optionBox">
                        <h6>
                          <span v-text="vocabDetails.label" class="bold"></span>
                          <template
                            v-if="vocabDetails && vocabDetails.short_form"
                          >
                            (<small v-text="vocabDetails.short_form"></small>)
                          </template>
                        </h6>
                        <table>
                          <tbody>
                            <tr>
                              <td>
                                <div class="pillType d-block m-1">
                                  <span
                                    class="mainBackDark"
                                    style="font-size: 1em"
                                    >Ontology</span
                                  >
                                  <span style="font-size: 1em">
                                    <a
                                      :href="vocabDetails.iri"
                                      v-text="vocabDetails.ontology_prefix"
                                      rel="nonreferrer"
                                      target="_blank"
                                    ></a>
                                  </span>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td>
                                <div class="pillType d-block m-1">
                                  <span
                                    class="mainBackLight"
                                    style="font-size: 1em"
                                    >ID</span
                                  >
                                  <span style="font-size: 1em">
                                    <a
                                      :href="vocabDetails.iri"
                                      v-text="vocabDetails.obo_id"
                                      rel="nonreferrer"
                                      target="_blank"
                                    ></a>
                                  </span>
                                </div>
                              </td>
                            </tr>
                            <tr v-if="vocabDetails && vocabDetails.description">
                              <td>
                                <small
                                  v-html="vocabDetails.description[0]"
                                ></small>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </template>
                  </template>
                  <!-- 🌈 URL 🌈 -->
                  <template v-if="info && info.format === 'uri'">
                    <input
                      type="url"
                      v-model="userInput"
                      class="form-control form-control-sm"
                      placeholder="enter url here"
                    />
                  </template>
                  <!-- 🌈 EMAIL 🌈 -->
                  <template v-if="info && info.format === 'email'">
                    <input
                      type="email"
                      v-model="userInput"
                      class="form-control form-control-sm"
                      placeholder="enter e-mail here"
                    />
                  </template>
                  <!-- 🌈 STRING FORMAT DATE 🌈 -->
                  <template v-if="info && info.format === 'date'">
                    <input
                      type="date"
                      v-model="userInput"
                      class="form-control form-control-sm"
                    />
                  </template>
                </template>

                <!-- 🌈 LICENSE 🌈 -->
                <template v-if="info?.type === 'object' && name === 'license'">
                  <form id="licenseForm" class="p-1" v-if="!userInput">
                    <small class="text-muted"
                      >Allow commercial uses of your work?</small
                    >
                    <select
                      @change="getLicense()"
                      ref="license1"
                      class="form-control form-control-sm"
                      id="ControlSelect1"
                    >
                      <option selected>Choose...</option>
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                      <option value="Yes, as long as others share alike">
                        Yes, as long as others share alike
                      </option>
                    </select>
                    <small class="text-muted"
                      >Allow commercial uses of your work?</small
                    >
                    <select
                      @change="getLicense()"
                      ref="license2"
                      class="form-control form-control-sm"
                      id="ControlSelect2"
                      required=""
                    >
                      <option selected>Choose...</option>
                      <option value="Yes">Yes</option>
                      <option value="No">No</option>
                    </select>
                    <div v-show="licenseThirdQuestion">
                      <small class="text-muted"
                        >Impose legal requirement for attribution?</small
                      >
                      <select
                        @change="getLicense()"
                        ref="license3"
                        class="form-control form-control-sm"
                        id="ControlSelect3"
                        required=""
                      >
                        <option selected>Choose...</option>
                        <option value="Yes">Yes</option>
                        <option value="No">No</option>
                      </select>
                    </div>
                  </form>
                  <template v-if="userLicense.text && !userInput">
                    <div class="alert alert-success text-center mt-3">
                      <h6 v-text="userLicense.text"></h6>
                      <p>
                        <small v-text="userLicense.description"></small>
                      </p>
                      <small>
                        <a
                          :href="userLicense.url"
                          target="_blank"
                          v-text="'Learn More About ' + userLicense.text"
                        ></a>
                      </small>
                    </div>
                  </template>
                  <template v-if="userInput && userInput.text">
                    <div class="alert alert-success text-center mt-3">
                      <small><b>License Chosen:</b> </small>
                      <h6 v-text="userInput.text"></h6>
                      <p>
                        <small v-text="userInput.description"></small>
                      </p>
                      <small>
                        <a
                          :href="userInput.url"
                          target="_blank"
                          v-text="'Learn More About ' + userInput.text"
                        ></a>
                      </small>
                      <hr />
                    </div>
                  </template>
                  <div
                    class="text-center p-1"
                    v-if="userLicense.text && !userInput"
                  >
                    <button
                      class="btn btn-success"
                      @click="userInput = userLicense"
                    >
                      Use This License
                    </button>
                  </div>
                </template>

                <!-- 🌈  KEYWORDS 🌈 -->
                <template v-if="info?.type === 'array' && name === 'keywords'">
                  <div class="form-group p-2 row">
                    <div class="col-sm-12 mb-2">
                      <form @submit.prevent="addKeyword">
                        <small class="text-muted"
                          >Enter single or multiple keywords separated by
                          commas</small
                        >
                        <input
                          ref="keywordInput"
                          autocomplete="off"
                          type="text"
                          class="form-control form-control-sm"
                          placeholder="Enter text here"
                        />
                      </form>
                    </div>
                    <div class="col-sm-12 m-auto">
                      <template v-for="text in userInput">
                        <span
                          title="Delete"
                          class="badge kwbadge badge-success mr-1 pointer slit-in-vertical"
                        >
                          <span v-html="text"></span>
                          <span
                            style="opacity: 0"
                            class="d-inline"
                            @click.prevent="removeItem($event, text)"
                          >
                            <font-awesome-icon
                              icon="fas fa-times"
                            ></font-awesome-icon
                          ></span>
                        </span>
                      </template>
                    </div>
                    <div
                      class="alert alert-success m-3 w-75"
                      v-show="userInput"
                    >
                      <small><b>Saved Keywords:</b> </small>
                      <template v-for="(text, i) in userInput">
                        <small v-html="text"></small>
                        <small v-if="i !== userInput.length - 1">, </small>
                      </template>
                    </div>
                  </div>
                </template>

                <!-- 🌈  CONSTANT DATA CATALOG 🌈 -->
                <template v-if="info?.type === 'object' && name === ''">
                  <!--<div class="text-center">
                      <div class="text-center bold text-info" v-if="constFound">
                        <small class="bold m-auto">Fixed Value, No Action Needed</small>
                      </div>
                      <div class='alert alert-success m-auto w-75'>
                      <p v-for="(item,index) in userInput" class="m-0">
                        <small class="bold" v-text='index'></small>:<small v-text='item'></small>
                      </p>
                      </div>
                    </div>-->
                </template>
                <!-- 🌈  OBJECT 🌈 -->
                <template v-if="info?.type === 'object' && name !== 'license'">
                  <div class="form-group p-2 row">
                    <TypeSelector
                      :info="info"
                      :main_name="name"
                      :isChild="false"
                    ></TypeSelector>
                  </div>
                  <div class="col-sm-12 m-auto">
                    <!-- 🌈  input preview for object or array🌈 -->
                    <InputPreview
                      :name="name"
                      :userInput="userInput"
                      :removeItem="removeItem"
                    ></InputPreview>
                    <!-- 🌈  input preview for string🌈 -->
                    <template v-if="typeof userInput === 'string'">
                      <span
                        style="overflow: hidden; max-width: 100%"
                        class="badge badge-success text-light"
                        v-text="userInput"
                      ></span>
                    </template>
                  </div>
                </template>
                <!-- 🌈  ONE OF  OR ANY OF🌈 -->
                <template v-if="info.oneOf || info.anyOf">
                  <!-- 🌈  ONE OF ANYTHING🌈 -->
                  <template
                    v-if="name !== 'datePublished' && name !== 'dateModified'"
                  >
                    <div class="form-group p-2 row">
                      <TypeSelector
                        :info="info"
                        :main_name="name"
                        :isChild="false"
                      ></TypeSelector>
                    </div>
                    <div class="col-sm-12 m-auto">
                      <!-- 🌈  input preview for object or array🌈 -->
                      <InputPreview
                        :name="name"
                        :userInput="userInput"
                        :removeItem="removeItem"
                      ></InputPreview>
                      <!-- 🌈  input preview for string🌈 -->
                      <template v-if="typeof userInput === 'string'">
                        <span
                          style="overflow: hidden; max-width: 100%"
                          class="badge badge-success text-light"
                          v-text="userInput"
                        ></span>
                      </template>
                    </div>
                  </template>

                  <!-- 🌈  ONE OF  VOCABULARY🌈
                    <template v-if="info.oneOf && info.oneOf[0].vocabulary">
                      <input-box :name="name" :info="info.oneOf[0]"></input-box>
                    </template> -->

                  <!-- 🌈  ONE OF  DATES🌈 -->
                  <template
                    v-if="name === 'datePublished' || name === 'dateModified'"
                  >
                    <div v-if="datePreset && !userInput" class="p-2">
                      <small>Dates used:</small>
                      <small
                        class="badge badge-info pointer m-1"
                        v-text="'Click to use ' + datePreset"
                        @click="userInput = datePreset"
                      ></small>
                    </div>
                    <template v-for="(item, i) in info.oneOf">
                      <div>
                        <template v-if="item.format === 'date'">
                          <input
                            type="date"
                            v-model="userInput"
                            class="form-control form-control-sm"
                            :placeholder="'enter ' + item.format"
                          />
                        </template>
                        <template
                          v-if="item?.type === 'string' && !item.format"
                        >
                          <input
                            type="text"
                            v-model="userInput"
                            class="form-control form-control-sm"
                            :placeholder="'enter ' + item?.type"
                          />
                        </template>
                      </div>
                    </template>
                  </template>
                </template>
              </div>
              <small v-if="showDesc && info.categories.length > 1">
                <small class="text-muted bold">Part of</small>
                <template
                  v-if="info && info.categories"
                  v-for="category in info.categories"
                >
                  <small
                    v-text="category.category"
                    class="tip pointer mr-2"
                    :data-tippy-content="[
                      category.subcategory === 'Required'
                        ? 'Required'
                        : 'Recommended',
                    ]"
                    :class="[
                      category.subcategory === 'Required'
                        ? 'text-danger'
                        : 'text-info',
                    ]"
                  ></small>
                </template>
              </small>
              <!-- 🌈  ISSUE 🌈 -->
              <template
                v-if="info && info.hasIssue"
                v-for="(issue, i) in info.hasIssue"
                :key="i"
              >
                <small class="ml-3 d-block" style="color: salmon">
                  <font-awesome-icon
                    icon="fas fa-exclamation-circle"
                  ></font-awesome-icon>
                  <span v-text="issue"></span>
                </small>
              </template>
            </div>
          </div>
        </div>
      </div>
      <div
        class="col-sm-2 p-2 actions d-flex align-items-center justify-content-around"
        :class="{
          'alert-success': userInput,
          'alert-dark': !userInput,
          'alert-warning': hasErrors,
        }"
      >
        <span
          class="fa-stack fa-1x pointer tip"
          :data-tippy-content="
            hasErrors ? 'Invalid Input. See Issues Above' : 'Perfect!'
          "
          @click="markCompleted(name)"
          v-show="userInput || userInput === false"
        >
          <font-awesome-icon
            icon="fas fa-circle"
            class="back fa-stack-2x"
            :class="[hasErrors ? 'text-warning' : 'text-success']"
          ></font-awesome-icon>
          <font-awesome-icon
            v-if="!hasErrors"
            icon="fas fa-check"
            class="fa-stack-1x text-light"
          ></font-awesome-icon>
          <font-awesome-icon
            v-else
            icon="fas fa-exclamation-circle"
            class="fa-stack-1x text-danger heartbeat"
          ></font-awesome-icon>
        </span>
        <span
          class="fa-stack fa-1x pointer tip"
          data-tippy-content="Clear"
          @click="clearFieldFor(name)"
          v-show="(info && info.value) || (info && info.value === false)"
        >
          <font-awesome-icon
            icon="fas fa-circle"
            class="text-muted fa-stack-2x"
          ></font-awesome-icon>
          <font-awesome-icon
            icon="fas fa-times"
            class="fa-stack-1x text-light"
          ></font-awesome-icon>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
import tippy from "tippy.js";
import moment from "moment";

import BooleanInput from "./BooleanInput.vue";
import IdentifierSpecial from "./IdentifierSpecial.vue";
import InputPreview from "./InputPreview.vue";
import NameSpecial from "./NameSpecial.vue";

export default {
  name: "InputBox",
  data: function () {
    return {
      constFound: false,
      constObj: {},
      licenseThirdQuestion: false,
      vocabTerm: "",
      vocab: Array,
      userLicense: {
        text: "",
        url: "",
        description: "",
      },
      canAcceptMultiple: false,
      vocabDetails: Object,
      vocabSuggestions: [],
      loading: false,
    };
  },
  components: {
    BooleanInput,
    IdentifierSpecial,
    InputPreview,
    NameSpecial,
  },
  props: ["name", "info"],
  methods: {
    markCompleted(propname) {
      var self = this;

      var payload = {};
      payload["completed"] = { name: propname, value: self.userInput };
      self.$store.commit("markCompleted", payload);
      //unselect after complete
      var payload2 = {};
      payload2["select"] = "";
      self.$store.commit("markSelected", payload2);
      self.$store.dispatch("saveProgress");
    },
    clearFieldFor: function (propname) {
      var self = this;
      var payload = {};
      payload["clear"] = propname;
      self.$store.commit("clearValueOfProp", payload);
      self.$store.dispatch("saveProgress");
    },
    addKeyword() {
      let self = this;
      let value = self.$refs.keywordInput.value;

      if (value.includes(",")) {
        let arr = value.split(",");
        for (var i = 0; i < arr.length; i++) {
          let val = arr[i].trim();
          var payload = {};
          payload["item"] = val;
          payload["from"] = self.name;
          self.$store.commit("addToArrayFrom", payload);
          self.$refs.keywordInput.value = "";
        }
      } else {
        var payload = {};
        payload["item"] = value;
        payload["from"] = self.name;
        self.$store.commit("addToArrayFrom", payload);
        self.$refs.keywordInput.value = "";
      }
    },
    removeItem(e, name) {
      console.log(e);
      let self = this;

      var x = e.pageX - 130;
      var y = e.pageY - 20;
      var el = document.querySelector("#puff");
      el.classList.add("d-inline");
      let audio = document.getElementById("pop-sound");
      audio.play();
      el.style.position = "absolute";
      el.style.left = x;
      el.style.top = y;
      setTimeout(() => {
        el.classList.remove("d-inline");
      }, 500);

      var payload = {};
      payload["item"] = name;
      payload["from"] = self.name;
      self.$store.commit("removeArrayItemFrom", payload);
    },
    handleOneOf(parentProp, childProp, childPropInfo) {
      var self = this;
      setTimeout(function () {
        self.addItem(parentProp, childPropInfo);
      }, 500);
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
              `https://www.ebi.ac.uk/ols4/api/search?q=${query}` +
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
          backdrop: true,
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
                    var payload = {};
                    payload["item"] = result.value[i];
                    payload["from"] = propName;
                    self.$store.commit("addToArrayFrom", payload);
                    self.$store.dispatch("saveProgress");
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
                          <i class="modaltip" data-tippy-content='` +
          JSON.stringify(docs[i]) +
          `'>ℹ️</i>
                      </label>
                  </div>`;
      }
      return html;
    },
    oneOfEnum(propName, propInfo) {
      var self = this;

      for (var oF_i = 0; oF_i < propInfo["oneOf"].length; oF_i++) {
        if (propInfo["oneOf"][oF_i].hasOwnProperty("enum")) {
          let e = propInfo["oneOf"][oF_i]["enum"];
          let optionsenum = {};

          for (var eIndex = 0; eIndex < e.length; eIndex++) {
            optionsenum[e[eIndex]] = e[eIndex];
          }
          self.$swal.fire({
            title: propName,
            input: "select",
            inputOptions: optionsenum,
            inputPlaceholder: "Select one",
            showCancelButton: true,
            inputValidator: (value) => {
              if (value) {
                var payload = {};
                payload["item"] = value;
                payload["from"] = propName;
                self.$store.commit("addToArrayFrom", payload);

                self.$store.dispatch("saveProgress");
              }
            },
          });
        }
        if (
          propInfo["oneOf"][oF_i].hasOwnProperty("type") &&
          propInfo["oneOf"][oF_i]["type"] == "array"
        ) {
          self.canAcceptMultiple = true;
        }
      }
    },
    checkBoxModal(propName, propInfo) {
      var self = this;

      let html = "";

      for (var oF_i = 0; oF_i < propInfo["oneOf"].length; oF_i++) {
        if (propInfo["oneOf"][oF_i].hasOwnProperty("enum")) {
          let e = propInfo["oneOf"][oF_i]["enum"];

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

          self.$swal
            .fire({
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
                  if (
                    self.info?.oneOf?.length == 1 &&
                    self.info?.oneOf?.[0]?.type == "array"
                  ) {
                    payload["forceArray"] = true;
                  }
                  self.$store.commit("addToArrayFrom", payload);

                  self.$store.dispatch("saveProgress");
                }
              }
            });
        }
      }
    },
    addItem(propName, propInfo) {
      var self = this;
      let progressSteps = [];
      let questions = [];

      let props = {};

      console.log("addItem", propInfo);

      if (propInfo.hasOwnProperty("vocabulary")) {
        self.handleVocab(propName, propInfo);
      }

      if (propInfo.hasOwnProperty("oneOf")) {
        // console.log("ONE OF")

        path = "";

        for (var oF_i = 0; oF_i < propInfo["oneOf"].length; oF_i++) {
          if (propInfo["oneOf"][oF_i].hasOwnProperty("enum")) {
            path = "enum";
          }
          if (
            propInfo["oneOf"][oF_i].hasOwnProperty("type") &&
            propInfo["oneOf"][oF_i]["type"] == "string"
          ) {
            if (propInfo["oneOf"][oF_i].hasOwnProperty("enum")) {
              path = "enum";
            } else {
              path = "string";
            }
          }
          if (propInfo["oneOf"][oF_i].hasOwnProperty("@type")) {
            path = "types";
          }
          if (
            propInfo["oneOf"][oF_i].hasOwnProperty("type") &&
            propInfo["oneOf"][oF_i]["type"] == "array"
          ) {
            self.canAcceptMultiple = true;
          }
        }
        // console.log('path',path)
        switch (path) {
          case "string":
            self.$swal.fire({
              title: propName,
              input: "text",
              inputPlaceholder: "Enter text here",
              footer:
                propName == "keywords"
                  ? "Multiple keywords can be entered separated by commas."
                  : " ",
              inputValidator: (value) => {
                if (value) {
                  if (propName == "keywords") {
                    slist = value.split(",");
                    for (var sIndex = 0; sIndex < slist.length; sIndex++) {
                      var payload = {};
                      payload["item"] = slist[sIndex];
                      payload["from"] = propName;
                      if (
                        self.info?.oneOf?.length == 1 &&
                        self.info?.oneOf?.[0]?.type == "array"
                      ) {
                        payload["forceArray"] = true;
                      }
                      self.$store.commit("addToArrayFrom", payload);

                      self.$store.dispatch("saveProgress");
                    }
                  } else {
                    var payload = {};
                    payload["item"] = value;
                    payload["from"] = propName;
                    if (
                      self.info?.oneOf?.length == 1 &&
                      self.info?.oneOf?.[0]?.type == "array"
                    ) {
                      payload["forceArray"] = true;
                    }
                    self.$store.commit("addToArrayFrom", payload);

                    self.$store.dispatch("saveProgress");
                  }
                }
              },
            });
            break;
          case "enum":
            if (self.canAcceptMultiple) {
              self.checkBoxModal(propName, propInfo);
            } else {
              self.oneOfEnum(propName, propInfo);
            }
            break;
          case "types":
            options = {};
            for (var oF_i = 0; oF_i < propInfo["oneOf"].length; oF_i++) {
              if (propInfo["oneOf"][oF_i].hasOwnProperty("@type")) {
                // value : user text
                options[oF_i] = propInfo["oneOf"][oF_i]["@type"];
              }
              if (
                propInfo["oneOf"][oF_i].hasOwnProperty("type") &&
                propInfo["oneOf"][oF_i]["type"] == "array"
              ) {
                self.canAcceptMultiple = true;
              }
            }

            if (Object.keys(options).length == 1) {
              // if only one option auto start
              self.handleOneOf(
                propName,
                propInfo["oneOf"][0]["@type"],
                propInfo["oneOf"][0]
              );
            } else {
              // if options, user chooses type
              self.$swal.fire({
                title: "Select type of " + propName,
                input: "select",
                inputOptions: options,
                inputPlaceholder: "Select one",
                animation: false,
                confirmButtonColor: "{{color_main}}",
                cancelButtonColor: "{{color_sec}}",
                customClass: "scale-in-center",
                showCancelButton: true,
                inputValidator: (value) => {
                  if (value) {
                    self.handleOneOf(
                      propName,
                      propInfo["oneOf"][value]["@type"],
                      propInfo["oneOf"][value]
                    );
                  }
                },
              });
            }
            break;
          default:
            console.warn("PATH NOT HANDLED", path);
        }
      }

      if (propInfo.hasOwnProperty("anyOf")) {
        options = {};
        for (var oF_i = 0; oF_i < propInfo["anyOf"].length; oF_i++) {
          if (propInfo["anyOf"][oF_i].hasOwnProperty("@type")) {
            // value : user text
            options[oF_i] = propInfo["anyOf"][oF_i]["@type"];
          }
          if (
            propInfo["anyOf"][oF_i].hasOwnProperty("type") &&
            propInfo["anyOf"][oF_i]["type"] == "array"
          ) {
            self.canAcceptMultiple = true;
          }
        }

        if (Object.keys(options).length == 1) {
          // if only one option auto start
          self.handleOneOf(
            propName,
            propInfo["anyOf"][0]["@type"],
            propInfo["anyOf"][0]
          );
        } else {
          // if options, user chooses type
          self.$swal.fire({
            title: "Select type of " + propName,
            input: "select",
            inputOptions: options,
            inputPlaceholder: "Select one",
            animation: false,
            confirmButtonColor: "{{color_main}}",
            cancelButtonColor: "{{color_sec}}",
            customClass: "scale-in-center",
            showCancelButton: true,
            inputValidator: (value) => {
              if (value) {
                self.handleOneOf(
                  propName,
                  propInfo["anyOf"][value]["@type"],
                  propInfo["anyOf"][value]
                );
              }
            },
          });
        }
      } else if (propInfo.hasOwnProperty("properties")) {
        props = propInfo.properties;
        // console.log('props for questions', props)
        // Create questions
        for (key in props) {
          if (key == "@type" && props[key].hasOwnProperty("const")) {
            // TODO: Handle constants found in @type if any.
          } else {
            progressSteps.push(key);

            let description = "";
            if (props[key].hasOwnProperty("description")) {
              description =
                "<small class='text-muted'>" +
                props[key].description +
                "</small>";
            }
            let title =
              "<b>" +
              propName +
              "</b>" +
              "." +
              "<b class='text-info'>" +
              key +
              "</b>";
            if (propInfo && propInfo.required) {
              if (propInfo.required.includes(key)) {
                title = title + " 🔴";
              }
            }

            switch (props[key]["type"]) {
              case "string":
                if (props[key].hasOwnProperty("format")) {
                  switch (props[key]["format"]) {
                    case "uri":
                      questions.push({
                        title: title,
                        footer: description,
                        inputValidator: (value) => {
                          return new Promise((resolve) => {
                            function validURL(str) {
                              str = str
                                .replace(/\(/g, "%28")
                                .replace(/\)/g, "%29");
                              var pattern = new RegExp(
                                "^(https?:\\/\\/)?" + // protocol
                                  "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
                                  "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
                                  "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
                                  "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
                                  "(\\#[-a-z\\d_]*)?$",
                                "i"
                              ); // fragment locator
                              // var pattern = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
                              return !!pattern.test(str);
                            }

                            if (
                              propInfo &&
                              propInfo.hasOwnProperty("required")
                            ) {
                              let currentField =
                                document.getElementById(
                                  "swal2-title"
                                ).textContent;
                              if (propInfo["required"].includes(currentField)) {
                                // is required needs to be validated
                                if (value) {
                                  if (validURL(value)) {
                                    resolve();
                                  } else {
                                    resolve("Input must be a valid URL");
                                  }
                                } else {
                                  resolve(currentField + " is required");
                                }
                              } else {
                                // not required user can skip
                                resolve();
                              }
                            }
                            if (propInfo && propInfo.hasOwnProperty("oneOf")) {
                              for (
                                var i = 0;
                                i < propInfo["oneOf"].length;
                                i++
                              ) {
                                if (
                                  propInfo["oneOf"][i] &&
                                  propInfo["oneOf"][i].hasOwnProperty(
                                    "required"
                                  )
                                ) {
                                  let currentField =
                                    document.getElementById(
                                      "swal2-title"
                                    ).textContent;
                                  if (
                                    propInfo["oneOf"][i]["required"].includes(
                                      currentField
                                    )
                                  ) {
                                    // is required needs to be validated
                                    if (value) {
                                      if (validURL(value)) {
                                        resolve();
                                      } else {
                                        resolve("Input must be a valid URL");
                                      }
                                    } else {
                                      resolve(currentField + " is required");
                                    }
                                  } else {
                                    // not required user can skip
                                    resolve();
                                  }
                                }
                              }
                            }

                            // if not required or anthything else just resolve()
                            resolve();
                          });
                        },
                      });
                      break;
                    case "date":
                      questions.push({
                        title: title,
                        footer: description,
                        inputAttributes: {
                          id: "hideThis",
                        },
                        html: '<input type="date" id="datePicked"/>',
                        onOpen: () => {
                          document
                            .getElementById("hideThis")
                            .classList.add("d-none");
                        },
                        preConfirm: () => {
                          return moment(
                            document.getElementById("datePicked").value
                          ).format("YYYY-MM-DD");
                        },
                      });
                      break;
                    default:
                      console.warning(
                        "Property not handled by guide: " + props[key]
                      );
                  }
                } else {
                  // any string value
                  questions.push({
                    title: title,
                    footer: description,
                    inputValidator: (value) => {
                      return new Promise((resolve) => {
                        if (propInfo && propInfo.hasOwnProperty("required")) {
                          let currentField =
                            document.getElementById("swal2-title").textContent;
                          if (propInfo["required"].includes(currentField)) {
                            // is required needs to be validated
                            if (value) {
                              resolve();
                            } else {
                              resolve(currentField + " is required");
                            }
                          } else {
                            // not required user can skip
                            resolve();
                          }
                        }
                        if (propInfo && propInfo.hasOwnProperty("oneOf")) {
                          for (var i = 0; i < propInfo["oneOf"].length; i++) {
                            if (
                              propInfo["oneOf"][i] &&
                              propInfo["oneOf"][i].hasOwnProperty("required")
                            ) {
                              let currentField =
                                document.getElementById(
                                  "swal2-title"
                                ).textContent;
                              if (
                                propInfo["oneOf"][i]["required"].includes(
                                  currentField
                                )
                              ) {
                                // is required needs to be validated
                                if (value) {
                                  resolve();
                                } else {
                                  resolve(currentField + " is required");
                                }
                              } else {
                                // not required user can skip
                                resolve();
                              }
                            }
                          }
                        }
                        // if not required just resolve value
                        resolve();
                      });
                    },
                  });
                  break;
                }
                break;
              case "integer":
                questions.push({
                  title: title,
                  input: "number",
                  footer: description,
                  inputValidator: (value) => {
                    return new Promise((resolve) => {
                      if (!value) {
                        return "You should write something meanignful";
                      } else {
                        return new Promise((resolve) => {
                          function validInteger(str) {
                            var pattern = new RegExp("^[0-9]*$");
                            return !!pattern.test(str);
                          }
                          if (validInteger(value)) {
                            resolve();
                          } else {
                            resolve("Input must be an integer");
                          }
                        });
                      }
                    });
                  },
                });
                break;
              case "array":
                html = "";
                if (props[key].hasOwnProperty("oneOf")) {
                  for (var ix = 0; ix < props[key]["oneOf"].length; ix++) {
                    if (props[key]["oneOf"][ix]["type"] == "object") {
                      let obj = props[key]["oneOf"][ix]["properties"];
                      for (var obj_key in obj) {
                        switch (obj[obj_key]["type"]) {
                          case "string":
                            html +=
                              '<div class="form-group"><input type="text" class="form-control"  name="' +
                              obj_key +
                              '" placeholder="' +
                              obj_key +
                              '"/></div>';
                            break;
                          case "url":
                            html +=
                              '<div class="form-group"><input type="url" class="form-control" name="' +
                              obj_key +
                              '" placeholder="' +
                              obj_key +
                              '"/></div>';
                            break;
                          case "date":
                            html +=
                              '<div class="form-group"><input class="form-control" name="' +
                              obj_key +
                              '" type="date"/></div>';
                            break;
                          default:
                            html +=
                              '<div class="form-group"><input class="form-control" type="text" name="' +
                              obj_key +
                              '" placeholder="' +
                              obj_key +
                              '"/></div>';
                            break;
                        }
                      }
                    }
                  }

                  html =
                    `<div class="alert-light p-1">
                              <form id="arrayForm">` +
                    html +
                    `</form>
                            </div>`;
                  questions.push({
                    title: title,
                    footer: description,
                    inputAttributes: {
                      id: "hideThis",
                    },
                    html: html,
                    onOpen: () => {
                      document
                        .getElementById("hideThis")
                        .classList.add("d-none");
                    },
                    preConfirm: () => {
                      let formArray = $("#arrayForm").serializeArray();
                      var returnArray = {};
                      for (var i = 0; i < formArray.length; i++) {
                        if (formArray[i]["name"].includes("date")) {
                          returnArray[formArray[i]["name"]] = moment(
                            formArray[i]["value"]
                          ).format("YYYY-MM-DD");
                        } else {
                          returnArray[formArray[i]["name"]] =
                            formArray[i]["value"];
                        }
                      }
                      return returnArray;
                    },
                  });
                }
                break;
              case "object":
                html = "";
                let obj = props[key]["properties"];
                for (var obj_key in obj) {
                  switch (obj[obj_key]["type"]) {
                    case "string":
                      html +=
                        '<div class="form-group"><input type="text" class="form-control"  name="' +
                        obj_key +
                        '" placeholder="' +
                        obj_key +
                        '"/></div>';
                      break;
                    case "url":
                      html +=
                        '<div class="form-group"><input type="url" class="form-control" name="' +
                        obj_key +
                        '" placeholder="' +
                        obj_key +
                        '"/></div>';
                      break;
                    case "date":
                      html +=
                        '<div class="form-group"><input class="form-control" name="' +
                        obj_key +
                        '" type="date"/></div>';
                      break;
                    default:
                      html +=
                        '<div class="form-group"><input class="form-control" type="text" name="' +
                        obj_key +
                        '" placeholder="' +
                        obj_key +
                        '"/></div>';
                      break;
                  }
                }

                html =
                  `<div class="alert-light p-1">
                            <form id="arrayForm">` +
                  html +
                  `</form>
                          </div>`;
                questions.push({
                  title: title,
                  footer: description,
                  inputAttributes: {
                    id: "hideThis",
                  },
                  html: html,
                  onOpen: () => {
                    document.getElementById("hideThis").classList.add("d-none");
                  },
                  preConfirm: () => {
                    let formArray = $("#arrayForm").serializeArray();
                    var returnArray = {};
                    for (var i = 0; i < formArray.length; i++) {
                      if (formArray[i]["name"].includes("date")) {
                        returnArray[formArray[i]["name"]] = moment(
                          formArray[i]["value"]
                        ).format("YYYY-MM-DD");
                      } else {
                        returnArray[formArray[i]["name"]] =
                          formArray[i]["value"];
                      }
                    }
                    return returnArray;
                  },
                });

                break;
              default:
                // ONE OF
                html = "";
                if (props[key].hasOwnProperty("oneOf")) {
                  for (var ix = 0; ix < props[key]["oneOf"].length; ix++) {
                    if (props[key]["oneOf"][ix]["type"] == "object") {
                      let obj = props[key]["oneOf"][ix]["properties"];
                      for (var obj_key in obj) {
                        switch (obj[obj_key]["type"]) {
                          case "string":
                            html +=
                              '<div class="form-group"><input type="text" class="form-control"  name="' +
                              obj_key +
                              '" placeholder="' +
                              obj_key +
                              '"/></div>';
                            break;
                          case "url":
                            html +=
                              '<div class="form-group"><input type="url" class="form-control" name="' +
                              obj_key +
                              '" placeholder="' +
                              obj_key +
                              '"/></div>';
                            break;
                          case "date":
                            html +=
                              '<div class="form-group"><input class="form-control" name="' +
                              obj_key +
                              '" type="date"/></div>';
                            break;
                          default:
                            html +=
                              '<div class="form-group"><input class="form-control" type="text" name="' +
                              obj_key +
                              '" placeholder="' +
                              obj_key +
                              '"/></div>';
                            break;
                        }
                      }
                    }
                  }

                  html =
                    `<div class="alert-light p-1">
                              <form id="arrayForm">` +
                    html +
                    `</form>
                            </div>`;
                  questions.push({
                    title: title,
                    footer: description,
                    inputAttributes: {
                      id: "hideThis",
                    },
                    html: html,
                    onOpen: () => {
                      document
                        .getElementById("hideThis")
                        .classList.add("d-none");
                    },
                    preConfirm: () => {
                      let formArray = $("#arrayForm").serializeArray();
                      var returnArray = {};
                      for (var i = 0; i < formArray.length; i++) {
                        if (formArray[i]["name"].includes("date")) {
                          returnArray[formArray[i]["name"]] = moment(
                            formArray[i]["value"]
                          ).format("YYYY-MM-DD");
                        } else {
                          returnArray[formArray[i]["name"]] =
                            formArray[i]["value"];
                        }
                      }
                      return returnArray;
                    },
                  });
                }
            }
          }
        }

        let arr = []; //modal header steps
        for (var i = 0; i < progressSteps.length; i++) {
          arr.push(i + 1);
        }
        self.$swal
          .mixin({
            input: "text",
            confirmButtonText: "Next &rarr;",
            showCancelButton: true,
            confirmButtonColor: "{{color_main}}",
            cancelButtonColor: "{{color_sec}}",
            animation: false,
            customClass: "scale-in-center",
            progressSteps: arr,
          })
          .queue(questions)
          .then((result) => {
            if (result.value) {
              let obj = {};

              //check for const @type or @type of input
              if ("@type" in propInfo) {
                console.log("has @type ", propInfo);
                obj["@type"] = propInfo["@type"];
              } else if (
                "properties" in propInfo &&
                "@type" in propInfo["properties"]
              ) {
                if ("const" in propInfo["properties"]["@type"]) {
                  console.log("@type COST", propInfo);
                  obj["@type"] = propInfo["properties"]["@type"]["cost"];
                }
              }

              // console.log('obj',obj)

              for (var i = 0; i < progressSteps.length; i++) {
                // check if value is empty if so skip
                if (result && result.value[i]) {
                  if (result.value[i] == "keywords") {
                    try {
                      let val = result.value[i].split(",");
                      obj[progressSteps[i]] = val;
                    } catch (e) {
                      let val = result.value[i];
                      obj[progressSteps[i]] = val;
                    }
                  } else {
                    if (
                      props[progressSteps[i]].hasOwnProperty("type") &&
                      props[progressSteps[i]]["type"] === "integer"
                    ) {
                      let val = parseInt(result.value[i]);
                      obj[progressSteps[i]] = val;
                    } else {
                      let val = result.value[i];
                      obj[progressSteps[i]] = val;
                    }
                  }
                }
              }

              if (
                propInfo &&
                propInfo.hasOwnProperty("oneOf") &&
                propInfo["oneOf"][0].hasOwnProperty("vocabulary")
              ) {
                //if its a vocab enum field do nothing. separate modal will launch
              } else {
                if (
                  Object.keys(obj).length !== 0 &&
                  obj.constructor === Object
                ) {
                  var payload = {};
                  payload["item"] = obj;
                  payload["from"] = propName;
                  if (
                    self.info?.oneOf?.length == 1 &&
                    self.info?.oneOf?.[0]?.type == "array"
                  ) {
                    payload["forceArray"] = true;
                  }
                  self.$store.commit("addToArrayFrom", payload);

                  self.$store.dispatch("saveProgress");
                }
              }
            }
          });
      }
    },
    checkForConstantKey(obj, keyname, parentkey) {
      var self = this;

      _.mapKeys(obj, function (value, key) {
        if (key === keyname) {
          self.constFound = true;
        }
        if (typeof value === "object") {
          self.checkForConstantKey(value, keyname, key);
        }
      });
    },
    getLicense(specialCase) {
      let self = this;
      let question1 = this.$refs.license1.value;
      let question2 = this.$refs.license2.value;

      if (specialCase) {
        switch (specialCase) {
          case "No":
            self.userLicense.description = "No Rights Reserved";
            self.userLicense.url =
              "https://creativecommons.org/share-your-work/public-domain/cc0/";
            self.userLicense.text = "CC0";
            break;
          case "Yes":
            self.userLicense.description = "Attribution 4.0 International";
            self.userLicense.url =
              "http://creativecommons.org/licenses/by/4.0/";
            self.userLicense.text = "CC BY 4.0";
            break;
          default:
            self.userLicense.description =
              "We had trouble with your input, please try this link:";
            self.userLicense.text = "";
            self.userLicense.url = "https://creativecommons.org/choose/";
            self.thirdQuestion = false;
            break;
        }
      } else {
        switch (question1 + "|" + question2) {
          case "Yes|Yes":
            // Special Case
            self.licenseThirdQuestion = true;
            let question3 = this.$refs["license3"].value;
            self.getLicense(question3);
            break;
          case "No|Yes":
            self.userLicense.description =
              "Attribution-NoDerivatives 4.0 International";
            self.userLicense.url =
              "http://creativecommons.org/licenses/by-nd/4.0/";
            self.userLicense.text = "CC BY-ND 4.0";
            self.licenseThirdQuestion = false;
            break;
          case "Yes, as long as others share alike|Yes":
            self.userLicense.description =
              "Attribution-ShareAlike 4.0 International";
            self.userLicense.url =
              "http://creativecommons.org/licenses/by-sa/4.0/";
            self.userLicense.text = "CC BY-SA 4.0";
            self.licenseThirdQuestion = false;
            break;
          case "Yes|No":
            self.userLicense.description =
              "Attribution-NonCommercial 4.0 International";
            self.userLicense.url =
              "http://creativecommons.org/licenses/by-nc/4.0/";
            self.userLicense.text = "CC BY-NC 4.0";
            self.licenseThirdQuestion = false;
            break;
          case "No|No":
            self.userLicense.description =
              "Attribution-NonCommercial-NoDerivatives 4.0 International";
            self.userLicense.text = "CC BY-NC-ND 4.0";
            self.userLicense.url =
              "http://creativecommons.org/licenses/by-nc-nd/4.0/";
            self.licenseThirdQuestion = false;
            break;
          case "Yes, as long as others share alike|No":
            self.userLicense.description =
              "Attribution-NonCommercial-ShareAlike 4.0 International";
            self.userLicense.text = "CC BY-NC-SA 4.0";
            self.userLicense.url =
              "http://creativecommons.org/licenses/by-nc-nd/4.0/";
            self.licenseThirdQuestion = false;
            break;
          default:
            self.userLicense.description =
              "We had trouble with your input, please try this link:";
            self.userLicense.text = "";
            self.userLicense.url = "https://creativecommons.org/choose/";
            self.licenseThirdQuestion = false;
            break;
        }
      }
    },
    getVocabulary() {
      var self = this;
      let obj = self.info;

      if (obj.hasOwnProperty("vocabulary")) {
        try {
          let query = self.vocabTerm;
          let ontologies = obj["vocabulary"]["ontology"].toString();
          let children = obj["vocabulary"]["children_of"].toString();

          // AUTOSUGGEST

          // self.loading = true;
          //
          // axios.get("http://www.ebi.ac.uk/ols4/api/suggest?q="+query+"&ontology="+ontologies+"&rows=5").then(res=>{
          //   self.vocabSuggestions = res.data.response.docs;
          //   self.loading = false;
          // }).catch(err=>{
          //   throw err;
          // });

          let url =
            "https://www.ebi.ac.uk/ols4/api/search?q=" +
            query +
            "&ontology=" +
            ontologies +
            "&childrenOf=" +
            children +
            "&type=class&fieldList=id,iri,label,description,obo_id,short_form,ontology_prefix" +
            "&queryFields=label" +
            "&rows=100";

          self.loading = true;

          axios
            .get(url)
            .then((res) => {
              if (
                res.data.response.hasOwnProperty("docs") &&
                res.data.response.docs.length >= 1
              ) {
                self.vocab = res.data.response.docs;
                self.loading = false;
              } else {
                self.vocab = [];
              }
            })
            .catch((err) => {
              self.vocab = [];
              throw err;
            });
        } catch (e) {
          throw e;
        }
      }
    },
  },
  watch: {
    constObj: {
      handler(obj) {
        var payload = {};
        payload["completed"] = { name: this.name, value: obj };
        self.$store.commit("markCompleted", payload);
      },
      deep: true,
    },
    vocabTerm(term) {
      this.getVocabulary();
    },
  },
  mounted: function () {
    var self = this;
    // console.log('%c MOUNTING ' + self.name, "color:green")
    if (self.info.hasOwnProperty("oneOf")) {
      if (
        (self.info["oneOf"].hasOwnProperty("type") &&
          self.info["oneOf"][0]?.type == "array") ||
        self.info["oneOf"][1]?.type == "array"
      ) {
        self.canAcceptMultiple = true;
      }
    }
    if (self.info.hasOwnProperty("anyOf")) {
      if (
        (self.info["anyOf"].hasOwnProperty("type") &&
          self.info["anyOf"][0]["type"] == "array") ||
        self.info["anyOf"][1]["type"] == "array"
      ) {
        self.canAcceptMultiple = true;
      }
    }
    // self.checkForConstantKey(self.info,'const')
  },
  computed: {
    ...mapGetters({
      showDesc: "showDesc",
      errors: "getErrors",
    }),
    isRequired: function () {
      return this.$store.getters.isRequired(this.name);
    },
    isInputHidden: function () {
      return this.$store.getters.isInputHidden(this.name);
    },
    userInput: {
      get() {
        return this.$store.getters.getValidationValue(this.name);
      },
      set(newValue) {
        var payload = {};
        let self = this;
        if (this.timer) {
          clearTimeout(this.timer);
          this.timer = null;
        }
        this.timer = setTimeout(() => {
          if (name.includes("date")) {
            let v = moment(newValue).format("YYYY-MM-DD");
            payload["completed"] = { name: self.name, value: v };
          } else {
            payload["completed"] = { name: self.name, value: newValue };
          }
          self.$store.commit("markCompleted", payload);
          self.$store.dispatch("saveProgress");
        }, 800);
      },
    },
    datePreset: function () {
      let schema = this.$store.getters.schema;
      if (
        schema.validation.properties.hasOwnProperty("datePublished") &&
        schema.validation.properties["datePublished"].value
      ) {
        return schema.validation.properties["datePublished"].value;
      } else if (
        schema.validation.properties.hasOwnProperty("dateModified") &&
        schema.validation.properties["dateModified"].value
      ) {
        return schema.validation.properties["dateModified"].value;
      } else {
        return false;
      }
    },
    hasErrors: function () {
      let self = this;
      if (this.errors && this.errors.length) {
        let found = this.errors.some((val) =>
          val.instancePath.includes(self.name)
        );
        if (found) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
  },
};
</script>
