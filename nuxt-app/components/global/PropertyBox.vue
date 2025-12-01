<template>
  <div class="border-bottom row m-0">
    <div
      class="col-sm-12 col-md-3 bg-dark bold d-flex justify-content-start align-items-center"
    >
      <span class="m-0">
        <font-awesome-icon
          v-if="FAClass && !isPotentialRequirement"
          :icon="'fas ' + FAClass"
          :class="getColorClass(name)"
          class="mr-1"
        />
        <font-awesome-layers v-else class="mr-1">
          <font-awesome-icon icon="fas fa-circle" class="text-primary" />
          <font-awesome-icon icon="fas fa-asterisk" class="text-light" />
        </font-awesome-layers>
        <span
          class="text-light font-weight-bold"
          v-text="name"
          :data-tippy-content="JSON.stringify(fullInfo, null, 2)"
        ></span>
      </span>
    </div>
    <div class="col-sm-12 col-md-9 text-dark bg-light">
      <!-- Validation view descriptions -->
      <MarkdownParser :description="fullInfo?.description"></MarkdownParser>
      <div class="rounded-0">
        <div class="p-1 rounded-0 d-flex">
          <!-- HAS TYPE -->
          <div
            v-if="fullInfo && fullInfo.type"
            class="d-flex justify-content-center align-items-center"
          >
            <div class="badge badge-pill alert-info m-1">
              type: <b>{{ fullInfo["type"] }}</b>
            </div>
          </div>

          <!-- ARRAY -->
          <div
            v-if="fullInfo && fullInfo.items"
            class="d-flex justify-content-center align-items-center"
          >
            <div class="badge badge-pill badge-secondary m-1">
              <span v-text="fullInfo.items.type"></span>
            </div>
          </div>

          <template v-if="fullInfo.enum">
            <select
              multiple
              class="form-control"
              id="exampleFormControlSelect2"
            >
              <template v-for="option in fullInfo.enum">
                <option :value="option" v-text="option"></option>
              </template>
            </select>
          </template>

          <template v-if="fullInfo['const']">
            <div class="pillType d-inline">
              <span style="background: #17a2b8" v-text="'const'"></span>
              <span v-text="fullInfo['const']"></span>
            </div>
          </template>

          <!-- OBJECT -->
          <div
            v-if="fullInfo && fullInfo.properties"
            class="d-flex justify-content-center align-items-center"
          >
            <small>fields</small>
            <font-awesome-icon
              icon="fas fa-chevron-right"
              class="text-muted mr-1"
            />
          </div>
          <div
            v-if="fullInfo && fullInfo.properties"
            class="d-flex justify-content-center align-items-center"
          >
            <div class="border-left border-info pl-3">
              <template
                v-for="(value, name) in fullInfo['properties']"
                :key="name"
              >
                <div
                  class="my-2 pl-2 d-flex align-items-center justify-content-center"
                >
                  <span class="mainTextDark">
                    <font-awesome-icon
                      icon="fas fa-asterisk"
                      class="text-danger mr-1"
                      v-if="isPropRequired(name)" />
                    <b v-text="name"></b
                  ></span>

                  <font-awesome-icon
                    icon="fas fa-caret-right"
                    class="text-muted m-1"
                  />

                  <div
                    class="badge badge-pill alert-primary"
                    v-if="value?.oneOf"
                    :data-tippy-content="JSON.stringify(value, null, 2)"
                  >
                    more info <font-awesome-icon icon="fas fa-info-circle" />
                  </div>

                  <small
                    class="badge badge-pill alert-dark"
                    v-text="fullInfo['properties'][name]['type']"
                  ></small>
                  <small
                    class="badge badge-pill alert-light"
                    v-text="fullInfo['properties'][name]['format']"
                  ></small>
                </div>
              </template>
            </div>
          </div>

          <!-- ONE OF -->
          <div v-if="fullInfo && fullInfo.oneOf" class="row m-0 w-100 p-0">
            <div class="col-sm-12 text-center bold mainTextDark alert-dark">
              <small> ONE OF </small>
            </div>
            <div
              class="col-sm-12 d-flex justify-content-center align-items-start flex-wrap"
            >
              <template v-for="option in fullInfo['oneOf']" :key="option">
                <OneOf :name="name" :option="option"></OneOf>
              </template>
            </div>
          </div>

          <!-- ANY OF -->
          <div v-if="fullInfo && fullInfo.anyOf" class="row m-0 p-0 w-100">
            <div class="col-sm-12 text-center bold mainTextLight alert-dark">
              <small> ANY OF </small>
            </div>
            <div
              class="col-sm-12 d-flex justify-content-center align-items-start flex-wrap"
            >
              <template v-for="option in fullInfo['anyOf']" :key="option">
                <AnyOf :name="name" :option="option"></AnyOf>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MarkdownParser from "../MarkdownParser.vue";

export default {
  name: "PropertyBox",
  data: function () {
    return {
      userSchema: [],
      textColor: "",
      backColor: "",
      itemID: Math.floor(Math.random() * 90000) + 10000,
      isPotentialRequirement: false,
    };
  },
  props: [
    "name",
    "fullInfo",
    "required",
    "recommended",
    "optional",
    "potential",
  ],
  methods: {
    getText(ref) {
      let arr = ref.split("/");
      return arr[arr.length - 1];
    },
    isPropRequired(name) {
      var self = this;
      if (
        self.fullInfo.hasOwnProperty("required") &&
        self.fullInfo["required"].includes(name)
      ) {
        return true;
      }
      return false;
    },
    getColorClass(propname) {
      if (this.required && this.required.includes(propname)) {
        return "text-danger";
      } else if (this.recommended && this.recommended.includes(propname)) {
        return "text-warning";
      } else if (this.optional && this.optional.includes(propname)) {
        return "text-info";
      } else if (this.potential && this.potential.includes(propname)) {
        this.isPotentialRequirement = true;
      } else {
        return "text-light";
      }
    },
  },
  computed: {
    FAClass() {
      if (this.required && this.required.includes(this.name)) {
        return "fa-asterisk";
      } else if (this.recommended && this.recommended.includes(this.name)) {
        return "fa-circle";
      } else if (this.optional && this.optional.includes(this.name)) {
        return "fa-square";
      } else if (this.potential && this.potential.includes(this.name)) {
        this.isPotentialRequirement = true;
      } else {
        return false;
      }
    },
  },
  mounted: function () {
    if (this.parent) {
      this.textColor = "mainTextLight";
      this.backColor = "mainBackLight";
    } else {
      this.textColor = "mainTextDark";
      this.backColor = "mainBackDark";
    }
  },
};
</script>
