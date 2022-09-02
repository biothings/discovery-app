<template>
  <div class="border-bottom row m-0">
    <div
      class="col-sm-12 col-md-3 bg-dark bold d-flex justify-content-start align-items-center"
    >
      <small class="m-0">
        <font-awesome-icon
          v-if="FAClass"
          :icon="'fas ' + FAClass"
          :class="getColorClass(name)"
          class="mr-1"
        />
        <span
          class="text-light font-weight-bold"
          v-text="name"
          :data-tippy-content="JSON.stringify(fullInfo, null, 2)"
          :id="'tipped' + itemID"
        ></span>
      </small>
    </div>
    <div class="col-sm-12 col-md-9 text-muted bg-light">
      <small v-text="fullInfo['description']"></small>
      <div class="rounded-0">
        <div class="p-1 rounded-0 d-flex">
          <!-- HAS TYPE -->
          <div
            v-if="fullInfo && fullInfo.type"
            class="d-flex justify-content-center align-items-center"
          >
            <div class="badge badge-pill badge-dark m-1">
              <span class="text-warning" v-text="fullInfo['type']"></span>
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
            <font-awesome-icon icon="fas fa-chevron-right" class="text-muted" />
          </div>
          <div
            v-if="fullInfo && fullInfo.properties"
            class="d-flex justify-content-center align-items-center"
          >
            <div class="border-left border-info pl-3">
              <template
                v-for="(value, name) in fullInfo['properties']"
                :key="option"
              >
                <div class="border-left border-primary my-4 pl-2">
                  <small class="mainTextDark"
                    ><font-awesome-icon icon="fas fa-circle" />
                    <b v-text="name"></b
                  ></small>
                  <span
                    v-if="isPropRequired(name)"
                    class="text-danger caps"
                    style="zoom: 0.5"
                    >is required</span
                  >

                  <font-awesome-icon
                    icon="fas fa-caret-right"
                    class="text-dark m-1"
                  />

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
import tippy from "tippy.js";

export default {
  name: "PropertyBox",
  data: function () {
    return {
      userSchema: [],
      textColor: "",
      backColor: "",
      itemID: Math.floor(Math.random() * 90000) + 10000,
    };
  },
  props: ["name", "fullInfo", "required", "recommended", "optional"],
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
      } else {
        return false;
      }
    },
  },
  mounted: function () {
    var self = this;
    tippy("#tipped" + this.itemID, {
      theme: "light",
    });
    if (self.parent) {
      self.textColor = "mainTextLight";
      self.backColor = "mainBackLight";
    } else {
      self.textColor = "mainTextDark";
      self.backColor = "mainBackDark";
    }
  },
};
</script>
