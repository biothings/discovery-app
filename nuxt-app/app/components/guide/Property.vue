<template>
  <div>
    <div class="row m-0">
      <div
        class="col-sm-12 grad d-flex justify-content-around align-items-center p-1"
      >
        <h3
          class="badge d-inline m-0"
          v-text="type"
          :class="type === 'REQUIRED' ? 'badge-danger' : 'badge-info'"
        ></h3>
        <button
          class="btn btn-sm btn-outline-secondary text-light"
          @click="viewSettings = !viewSettings"
        >
          <small
            ><font-awesome-icon icon="fas fa-cog"></font-awesome-icon> Display
            Settings</small
          >
        </button>
        <div v-show="viewSettings">
          <input
            class="form-check-input slider mr-2"
            type="checkbox"
            :checked="allMode"
            id="customControlInline2"
            @click="allMode = !allMode"
          />
          <label class="form-check-label text-light" for="customControlInline2">
            <small>Change Form Style</small>
          </label>
        </div>
      </div>
      <div class="col-sm-12 col-md-9 p-0">
        <template v-if="allMode && validation">
          <!-- 🌈  ALL MODE 🌈 -->
          <div class="p-0">
            <template
              v-if="$router.currentRoute?.value?.path == '/guide/n3c/dataset'"
            >
              <div class="mainTextDark row m-0">
                <div class="col-sm-10 p-1 text-left p-2">
                  <h6>
                    To request an external dataset accessible in the N3C Enclave
                  </h6>
                  <h6>please fill this out:</h6>
                </div>
                <div class="col-sm-2 alert-dark"></div>
              </div>
            </template>
            <template v-if="type === 'REQUIRED'">
              <template
                v-for="(prop, index) in validation.properties"
                :key="index"
              >
                <InputBox
                  v-if="isRequired(index)"
                  :name="index"
                  :info="prop"
                ></InputBox>
              </template>
            </template>
            <template v-if="type === 'RECOMMENDED'">
              <template
                v-for="(prop, index) in validation.properties"
                :key="index"
              >
                <InputBox
                  v-if="!isRequired(index)"
                  :name="index"
                  :info="prop"
                ></InputBox>
              </template>
            </template>
          </div>
        </template>

        <template v-if="!allMode && validation">
          <!-- 🌈  1 BY 1 MODE 🌈 -->
          <!-- 🌈  TODO 🌈 -->
          <div class="p-1 bg-dark text-left mb-0">
            <span class="badge m-1 badge-dark text-warning">
              TO-DO
              <font-awesome-icon
                icon="fas fa-chevron-right"
              ></font-awesome-icon>
            </span>
            <template v-if="type === 'REQUIRED'">
              <template v-for="(prop, index) in validation.properties">
                <template v-if="isRequired(index)">
                  <span
                    class="badge badge-dark m-1 pointer badgeDesc font-weight-normal slit-in-vertical"
                    @click="selectProp(index)"
                    v-if="prop && !prop.value && prop.value !== false"
                    :class="{ highlight: prop.highlighted }"
                  >
                    <span v-text="index"></span>
                    <font-awesome-icon
                      icon="fas fa-asterisk"
                      class="text-danger required pointer unselectable"
                      v-if="isRequired(index)"
                    ></font-awesome-icon>
                  </span>
                </template>
              </template>
            </template>
            <template v-if="type === 'RECOMMENDED'">
              <template
                v-for="(prop, index) in validation.properties"
                v-if="!isRequired(index)"
              >
                <span
                  class="badge badge-dark m-1 pointer badgeDesc font-weight-normal slit-in-vertical"
                  @click="selectProp(index)"
                  v-if="prop && !prop.value && prop.value !== false"
                  :class="{ highlight: prop.highlighted }"
                >
                  <span v-text="index"></span>
                </span>
              </template>
            </template>
          </div>
          <!-- 🌈  DONE 🌈 -->
          <div class="p-1 alert-success text-left mb-0">
            <span class="badge m-1 badge-light text-success">
              DONE
              <font-awesome-icon
                icon="fas fa-chevron-right"
              ></font-awesome-icon>
            </span>
            <template v-if="type === 'REQUIRED'">
              <template v-for="(prop, index) in validation.properties">
                <template v-if="isRequired(index)">
                  <small
                    class="m-1 text-success pointer desc"
                    @click="selectProp(index)"
                    v-if="(prop && prop.value) || prop.value === false"
                    :class="{ highlight: prop.highlighted }"
                    data-tippy-content="Edit"
                  >
                    <font-awesome-icon
                      icon="fas fa-check-circle"
                      class="text-success"
                    ></font-awesome-icon>
                    <span v-text="index"></span>
                    <font-awesome-icon
                      icon="fas fa-asterisk"
                      class="text-danger required pointer unselectable"
                      v-if="isRequired(index)"
                    ></font-awesome-icon>
                  </small>
                </template>
              </template>
            </template>
            <template v-if="type === 'RECOMMENDED'">
              <template
                v-for="(prop, index) in validation.properties"
                v-if="!isRequired(index)"
              >
                <small
                  class="m-1 text-success pointer desc"
                  @click="selectProp(index)"
                  v-if="(prop && prop.value) || prop.value === false"
                  :class="{ highlight: prop.highlighted }"
                  data-tippy-content="Edit"
                >
                  <font-awesome-icon
                    icon="fas fa-check-circle"
                    class="text-success"
                  ></font-awesome-icon>
                  <span v-text="index"></span>
                </small>
              </template>
            </template>
          </div>
          <div class="p-1">
            <template
              v-if="validation.properties"
              v-for="(prop, index) in validation.properties"
            >
              <InputBox
                class="border border-dark"
                v-if="prop && prop.selected"
                :name="index"
                :info="prop"
                :key="index"
              ></InputBox>
            </template>
          </div>
        </template>
      </div>
      <!-- 🌈  PROGRESS TRACKER 🌈 -->
      <div class="col-sm-12 col-md-3 p-0 grad-dark">
        <div
          class="w-100 text-light d-flex justify-content-around align-items-center p-1"
        >
          <h6>Progress Tracker</h6>
        </div>
        <template v-if="categoryTotals && showCategories">
          <template v-for="(subcats, cat, i) in categoryTotals" :key="cat + i">
            <Category class="fade-in" :cat="cat" :subcats="subcats"></Category>
          </template>
        </template>
      </div>
      <div
        class="col-sm-12 text-right m-0 rounded-0 p-1"
        :class="{ 'alert-success': isComplete, 'alert-danger': !isComplete }"
      >
        <div class="bg-none p-2 rounded">
          <template v-if="type === 'REQUIRED' && isComplete">
            <small class="text-success bold">Ready to proceed!</small>
            <button
              class="btn themeButton text-light"
              @click="nextStep()"
              :class="{ heartbeat: isComplete }"
              :disabled="!isComplete"
            >
              NEXT
            </button>
          </template>
          <template v-if="type === 'REQUIRED' && !isComplete">
            <small class="text-danger bold"
              >Complete ALL requirements to proceed!</small
            >
            <button
              class="btn themeButton text-light"
              @click="nextStep()"
              :class="{ heartbeat: isComplete, notallowed: !isComplete }"
              :disabled="!isComplete"
            >
              NEXT
            </button>
          </template>

          <template v-if="type === 'RECOMMENDED'">
            <small v-show="fieldsLeft !== 0" class="text-info"
              >Complete as many recommended fields as possible
              <b class="text-danger"
                >ONLY <span v-text="fieldsLeft"></span> LEFT!</b
              ></small
            >
            <small v-show="fieldsLeft === 0" class="text-success bold"
              >Great job! Ready to proceed!</small
            >
            <button
              class="btn btn-danger text-light mr-3 ml-3"
              @click="goToStep(step - 1)"
            >
              <font-awesome-icon icon="fas fa-chevron-left"></font-awesome-icon>
              BACK
            </button>
            <button class="btn themeButton text-light" @click="nextStep()">
              NEXT
              <font-awesome-icon
                icon="fas fa-chevron-right"
              ></font-awesome-icon>
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Category from "./Category.vue";
import InputBox from "./InputBox.vue";
import Notify from "simple-notify";

export default {
  name: "Property",
  data: function () {
    return {
      settings: { "form-mode": 1 },
      allMode: Boolean,
      viewSettings: false,
    };
  },
  components: {
    Category,
    InputBox,
  },
  props: {
    type: {
      type: String,
      default: "",
    },
    showCategories: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    isRequired(propname) {
      let req = this.$store.getters.getValidation["required"];
      if (req.includes(propname)) {
        return true;
      } else {
        return false;
      }
    },
    nextStep() {
      var self = this;
      if (self.type === "REQUIRED") {
        let payload = {};
        payload["step"] = 4;
        this.$store.commit("changeStep", payload);
      } else {
        if (self.isComplete) {
          let payload = {};
          payload["step"] = 5;
          this.$store.commit("changeStep", payload);
        } else {
          new Notify({
            status: "error",
            title: "Error",
            text: "Incomplete",
            effect: "fade",
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: false,
            autotimeout: 3000,
            gap: 20,
            distance: 20,
            type: 1,
            position: "right top",
          });
        }
      }
    },
    selectProp(propname) {
      var payload = {};
      payload["select"] = propname;
      this.$store.commit("markSelected", payload);
    },
    checkSettings() {
      var self = this;
      if (self.settings && self.settings.hasOwnProperty("form-mode")) {
        self.allMode = self.settings["form-mode"];
      } else {
        self.allMode = false;
      }
    },
    goToStep(s) {
      var self = this;
      let payload = {};
      payload["step"] = s;
      this.$store.commit("changeStep", payload);
    },
    toggleDesc() {
      this.$store.commit("toggleDesc");
    },
  },
  mounted: function () {
    this.checkSettings();
  },
  computed: {
    ...mapGetters({
      validation: "getValidation",
      isComplete: "isComplete",
      categoryTotals: "getCategoryTotals",
      totals: "getTotals",
      step: "getStep",
      showDesc: "showDesc",
      fieldsLeft: "fieldsLeft",
    }),
  },
};
</script>
