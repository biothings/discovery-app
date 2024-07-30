<template>
  <li class="list-group-item">
    <h6 class="font-weight-bold mainTextDark">
      <i
        class="fas fa-tiny fa-code text-dark float-right"
        :data-tippy-content="JSON.stringify(propinfo, null, 2)"
      ></i>
      <span v-text="propname"></span>
      <span v-if="isRequired" class="text-danger caps ml-2" style="zoom: 0.5"
        >is required</span
      >
    </h6>
    <small class="text-dark" v-text="propinfo['description']"></small>
    <div class="d-flex rounded-0">
      <div
        class="text-dark px-5 py-3 d-flex justify-content-center align-items-center"
      >
        <small>
          TAKES <i class="fas fa-chevron-right"></i>
          <i class="fas fa-chevron-right"></i>
        </small>
      </div>
      <div class="p-1 rounded-0 d-flex">
        <!-- HAS TYPE -->
        <div
          v-if="propinfo && propinfo.type"
          class="d-flex justify-content-center align-items-center"
        >
          <div
            class="circle m-1"
            v-if="propinfo['type'] == 'array'"
            data-tippy-content="Array"
          >
            [ ]
          </div>
          <div
            class="badge badge-pill badge-dark m-1"
            v-if="propinfo['type'] == 'string'"
            data-tippy-content="String"
          >
            A String
          </div>
          <div
            class="badge badge-pill badge-dark m-1"
            v-if="propinfo['type'] == 'object'"
            data-tippy-content="Object"
          >
            An Object
          </div>
          <div
            class="badge badge-pill badge-dark m-1"
            v-if="propinfo['type'] == 'number'"
            data-tippy-content="Number"
          >
            A Number
          </div>
          <div
            class="badge badge-pill badge-dark m-1"
            v-if="propinfo['type'] == 'boolean'"
            data-tippy-content="Boolean"
          >
            A Boolean T/F
          </div>
        </div>

        <!-- HAS TYPE -->
        <div
          v-if="propinfo && propinfo.properties"
          class="d-flex justify-content-center align-items-center"
        >
          <i class="fas fa-chevron-right m-1 text-dark"></i>
        </div>
        <div
          v-if="propinfo && propinfo.properties"
          class="d-flex justify-content-center align-items-center"
        >
          <div class="border-left border-info pl-3">
            <template
              v-for="(value, name) in propinfo['properties']"
              :key="name"
            >
              <div class="border-left border-primary my-4 pl-2">
                <small class="mainTextDark"
                  ><i class="fas fa-circle"></i> <b v-text="name"></b
                ></small>
                <span
                  v-if="isPropRequired(name)"
                  class="text-danger caps"
                  style="zoom: 0.5"
                  >is required</span
                >

                <i class="fas fa-caret-right m-1 text-dark"></i>

                <small
                  class="badge badge-pill alert-dark"
                  v-text="propinfo['properties'][name]['type']"
                ></small>
                <small
                  class="badge badge-pill alert-light"
                  v-text="propinfo['properties'][name]['format']"
                ></small>
              </div>
            </template>
          </div>
        </div>

        <!-- ONE OF -->
        <div
          v-if="propinfo && propinfo.oneOf"
          class="d-flex justify-content-center align-items-center"
        >
          <div class="d-flex justify-content-center align-items-center">
            <small class="text-dark">ONE OF</small>
          </div>
          <div class="d-flex justify-content-center align-items-center">
            <i class="fas fa-chevron-right m-1 text-dark"></i>
          </div>
          <div class="d-flex justify-content-center align-items-center">
            <div class="border-left border-info pl-3">
              <template v-for="option in propinfo['oneOf']" :key="option">
                <div class="border-left border-primary my-4 pl-2">
                  <a
                    data-tippy-content="To Definition"
                    v-if="option && option['$ref']"
                    :href="'#' + getText(option['$ref'])"
                    ><i class="fas fa-info-circle fa-xs"></i>
                    <i v-text="getText(option['$ref'])"></i
                  ></a>
                  <div v-if="option && option['items']" class="d-flex">
                    <div
                      class="d-flex justify-content-center align-items-center"
                    >
                      <div
                        class="badge badge-pill badge-dark m-1"
                        v-if="option['type'] == 'array'"
                        data-tippy-content="Array"
                      >
                        A List Of
                      </div>
                    </div>
                    <div
                      class="d-flex justify-content-center align-items-center"
                    >
                      <i class="fas fa-caret-right m-1 mainTextLight"></i>
                    </div>
                    <div
                      class="d-flex justify-content-center align-items-center"
                    >
                      <template
                        v-for="(val, key) in option['items']"
                        :key="key"
                      >
                        <a
                          data-tippy-content="To Definition"
                          v-if="key == '$ref'"
                          :href="'#' + getText(val)"
                          ><i class="fas fa-info-circle fa-xs"></i>
                          <i v-text="getText(val)"></i
                        ></a>
                        <small v-else v-text="val"></small>
                      </template>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: "JS_PropertyBox",
  data: function () {
    return {
      userSchema: [],
      textColor: "",
      backColor: "",
    };
  },
  props: ["propname", "propinfo"],
  methods: {
    getText(ref) {
      let arr = ref.split("/");
      return arr[arr.length - 1];
    },
    isPropRequired(name) {
      var self = this;
      if (
        self.propinfo.hasOwnProperty("required") &&
        self.propinfo["required"].includes(name)
      ) {
        return true;
      }
      return false;
    },
  },
  mounted: function () {
    var self = this;
    if (self.parent) {
      self.textColor = "mainTextLight";
      self.backColor = "mainBackLight";
    } else {
      self.textColor = "mainTextDark";
      self.backColor = "mainBackDark";
    }
  },
  computed: {
    isRequired: function () {
      return this.$store.getters.isPropRequired(this.propname);
    },
  },
};
</script>
