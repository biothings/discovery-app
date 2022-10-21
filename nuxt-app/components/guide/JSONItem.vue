<template>
  <tr>
    <td>
      <b class="text-info" v-text="number + ': '"></b>
      <small v-text="item.name"></small>
      <small class="ml-1 pointer text-primary" @click="getPreview()"
        >Inspect Metadata</small
      >
    </td>
    <td class="align-middle">
      <small v-if="loading" class="text-muted">Please wait...</small>
      <details v-if="errMSG" class="text-left text-danger">
        <summary>View Issues</summary>
        <small v-html="errMSG"></small>
      </details>
      <details v-if="exists" class="text-left text-success">
        <template v-if="canOverwrite">
          <summary>🛎️ You've already registered this metadata.</summary>
          <small
            >Here's a link to
            <router-link target="_blank" :to="'/dataset/' + exists"
              >that record</router-link
            >. If you choose to update this record it will replace the
            previously registered metadata completely.
          </small>
        </template>
        <template v-else>
          <summary>🚨 Already registered by someone else.</summary>
          <small
            >The identifier provided has already been used to register
            <a target="_blank" :href="'/dataset/' + exists">this record</a>.
            Looks like you won't be able to make any changes to this item.
          </small>
        </template>
      </details>
      <details
        v-if="missingRequired.length && !exists"
        class="text-left text-danger"
      >
        <summary
          v-text="'(' + missingRequired.length + ') Missing Required Fields'"
        ></summary>
        <small v-text="missingRequired.join(', ')"></small>
      </details>
      <details
        v-if="missingFields.length && !exists"
        class="text-left text-info"
      >
        <summary
          v-text="'(' + missingFields.length + ') Missing Optional Fields'"
        ></summary>
        <small v-text="missingFields.join(', ')"></small>
      </details>
      <details
        v-if="nullValueWarnings.length && !exists"
        class="text-left text-danger"
      >
        <summary
          class="mainTextDark"
          v-text="
            '(' + nullValueWarnings.length + ') Null values found and removed'
          "
        ></summary>
        <small v-text="nullValueWarnings.join(', ')"></small>
      </details>
    </td>
    <td v-if="errMSG" class="align-middle">
      <button
        role="button"
        @click="editItem(item)"
        class="btn btn-sm mainBackDark text-light m-1"
      >
        Edit Metadata
      </button>
      <button
        role="button"
        @click="register()"
        class="btn btn-sm mainBackLight text-light m-1"
      >
        Retry Registration
      </button>
    </td>
    <td v-else>
      <div v-if="canOverwrite">
        <button
          role="button"
          @click="editItem(item)"
          class="btn btn-sm mainBackDark text-light m-1"
        >
          Edit Metadata
        </button>
        <button
          role="button"
          @click="updateJSONItem()"
          class="btn btn-sm btn-info text-light m-1"
        >
          Update Registration
        </button>
      </div>
    </td>
    <td
      class="align-middle"
      :class="{
        'badge-danger': errMSG,
        'badge-success': successMSG,
        'badge-info': successMSGUpdate,
      }"
    >
      <span class="d-block text-light">
        <font-awesome-icon
          v-if="loading"
          icon="fas fa-spinner"
          class="fa-pulse mainTextDark"
        ></font-awesome-icon>
        <small v-if="errMSG">FAILED <i class="fas fa-poo"></i></small>
        <small v-if="successMSG"
          >REGISTERED
          <font-awesome-icon icon="fas fa-registered"></font-awesome-icon
        ></small>
        <small v-if="successMSGUpdate"
          >UPDATED <font-awesome-icon icon="fas fa-check"></font-awesome-icon
        ></small>

        <small
          v-if="successMSG && !exists"
          v-html="successMSG"
          class="d-block"
        ></small>
        <small
          v-if="successMSGUpdate"
          v-html="successMSGUpdate"
          class="d-block"
        ></small>
        <small v-if="help" v-html="help" class="d-block"></small>
      </span>
    </td>
  </tr>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  name: "JSONItem",
  data: function () {
    return {
      errMSG: "",
      successMSG: "",
      successMSGUpdate: "",
      loading: false,
      editor: null,
      beforeCloseVal: null,
      missingRequired: [],
      missingFields: [],
      nullValueWarnings: [],
      exists: null,
      canOverwrite: false,
      help: false,
    };
  },
  props: ["item", "number", "username"],
  methods: {
    checkAlreadyExists() {
      let self = this;
      if (Object.hasOwnProperty.call(this.item, "identifier")) {
        let id = this.item.identifier.replace("&", "%26");
        const runtimeConfig = useRuntimeConfig();
        axios
          .get(
            runtimeConfig.public.apiUrl +
              `/api/dataset/query?q=(identifier:"${id}")`
          )
          .then((res) => {
            if (res.data.total == 1) {
              self.exists = res.data.hits[0]["_id"];
              store.commit("addBulkReport", {
                field: "Exists",
                value: self.exists,
              });
              if (self.username == res.data.hits[0]["_meta"]["username"]) {
                self.canOverwrite = true;
              } else {
                self.canOverwrite = false;
              }
            } else {
              self.registerJSONItem();
            }
          })
          .catch((err) => {
            throw err;
          });
      }
    },
    checkRequirements() {
      let self = this;
      //rest first
      self.missingFields = [];
      self.missingRequired = [];

      let itemFields = Object.keys(self.item);
      let validationFields = Object.keys(self.validation.properties);
      let requiredFields = self.validation.required;
      requiredFields.forEach((field) => {
        if (!itemFields.includes(field)) {
          self.missingRequired.push(field);
        }
      });
      validationFields.forEach((field) => {
        if (!itemFields.includes(field) && !requiredFields.includes(field)) {
          self.missingFields.push(field);
        }
      });
    },
    clean(object) {
      let self = this;
      Object.entries(object).forEach(([k, v]) => {
        if (v && typeof v === "object") self.clean(v);
        if (
          (v && typeof v === "object" && !Object.keys(v).length) ||
          v === null ||
          v === undefined ||
          v.length === 0
        ) {
          if (Array.isArray(object)) object.splice(k, 1);
          else if (!(v instanceof Date)) {
            self.nullValueWarnings.push(k);
            delete object[k];
          }
        }
      });
      return object;
    },
    register() {
      this.item = this.clean(this.item);
      this.checkRequirements();
      this.checkAlreadyExists();
    },
    SaveDefinition() {
      let value = this.beforeCloseVal;
      this.$swal.fire({
        type: "success",
        toast: true,
        title: "Metadata Updated",
        showConfirmButton: false,
        timer: 1000,
      });
      try {
        this.item = JSON.parse(value);
      } catch (error) {
        this.$swal.fire({
          type: "error",
          toast: true,
          title: "Invalid JSON",
          showConfirmButton: false,
          timer: 1000,
        });
      }
    },
    getPreview() {
      this.$swal.fire({
        position: "center",
        confirmButtonColor: "#5C3069",
        cancelButtonColor: "#006476",
        animation: false,
        customClass: "scale-in-center",
        html:
          `<h6 class="text-center mainTextDark">Preview</h6><div class="text-left p-1 previewBox"><small><pre>` +
          JSON.stringify(this.item, null, 2) +
          `</pre></small></div>`,
      });
    },
    registerJSONItem() {
      var self = this;

      let schema = store.getters.getSchema;
      self.loading = true;
      let config = {
        headers: {
          "content-type": "application/json",
        },
      };
      const runtimeConfig = useRuntimeConfig();

      axios
        .post(
          runtimeConfig.public.apiUrl +
            "/api/dataset?schema=" +
            schema["namespace"] +
            "::" +
            schema["prefix"] +
            ":" +
            schema["label"] +
            "&guide=" +
            self.startingPoint["guide"],
          self.item,
          config
        )
        .then((res) => {
          self.loading = false;
          if (res.data.success) {
            self.successMSG =
              `<a class="btn btn-sm alert-success" href="/dataset/` +
              res.data.id +
              `" target="_blank" rel="nonreferrer"> 
              View Registration</a>`;
            self.errMSG = "";
            store.commit("addBulkReport", {
              field: "Registered",
              value: self.item.identifier,
            });
          }
        })
        .catch((err) => {
          self.loading = false;
          store.commit("addBulkReport", {
            field: "Failed",
            value: self.item.identifier,
          });
          self.errMSG = `<ul class='text-danger mb-0 text-left'>
            <li>Reason: <b>${err.response.data.reason || "N/A"}</b></li>
            <li>Required: ${
              err.response.data.validator ? "🟢 Yes" : "🔴 No"
            }</li>
            <li>Failing at field: <b>${err.response.data.path || "N/A"}</b></li>
            <li>Additional Details: <b>${
              (err.response.data.parent && err.response.data.parent.reason) ||
              "N/A"
            }</b></li>
            </ul>`;
          self.help = `<a class="btn btn-sm alert-danger"
              href="https://github.com/biothings/discovery-app/issues/new?assignees=marcodarko&labels=bug&template=bulk-registration-issue.md&title=Issue+registering+some+metadata"
              target="_blank"  rel="nonreferrer"> Get help!</a>`;
        });
    },
    updateJSONItem() {
      var self = this;
      self.loading = true;
      let config = {
        headers: {
          "content-type": "application/json",
        },
      };
      const runtimeConfig = useRuntimeConfig();

      axios
        .put(
          runtimeConfig.public.apiUrl + "/api/dataset/" + self.exists,
          self.item,
          config
        )
        .then((res) => {
          self.loading = false;
          if (res.data.success) {
            store.commit("addBulkReport", {
              field: "Updated",
              value: self.exists,
            });
            self.successMSGUpdate =
              `<a class="btn btn-sm alert-info" href="/dataset/` +
              self.exists +
              `" target="_blank" rel="nonreferrer">
               View Update</a>`;
            self.errMSG = "";
          }
        })
        .catch((err) => {
          self.loading = false;
          store.commit("addBulkReport", {
            field: "Failed",
            value: self.exists,
          });
          self.errMSG = `<ul class='text-danger mb-0 text-left'>
            <li>Reason: <b>${err.response.data.reason || "N/A"}</b></li>
            <li>Required: ${
              err.response.data.validator ? "🟢 Yes" : "🔴 No"
            }</li>
            <li>Failing at field: <b>${err.response.data.path || "N/A"}</b></li>
            <li>Additional Details: <b>${
              (err.response.data.parent && err.response.data.parent.reason) ||
              "N/A"
            }</b></li>
            </ul>`;
          self.help = `<a class="btn btn-sm alert-danger"
              href="https://github.com/biothings/discovery-app/issues/new?assignees=marcodarko&labels=bug&template=bulk-registration-issue.md&title=Issue+registering+some+metadata"
              target="_blank"  rel="nonreferrer">Get help!</a>`;
        });
    },
    editItem(item) {
      let self = this;
      this.$swal
        .fire({
          title: "Edit Metadata",
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          animation: false,
          customClass: "scale-in-center swal-wide",
          html: '<textarea id="editContent"></textarea>',
          showCancelButton: true,
          confirmButtonText: "Save Changes",
          onOpen: function () {
            self.editor = CodeMirror.fromTextArea(
              document.getElementById("editContent"),
              {
                mode: "json",
                // lineNumbers: true,
                autorefresh: true,
                lineWrapping: true,
                spellcheck: true,
                autofocus: true,
              }
            );
            self.editor.setValue(JSON.stringify(item, null, 2));
            self.editor.on("change", (editor) => {
              self.beforeCloseVal = editor.getValue();
            });
          },
          preConfirm: () => {
            self.SaveDefinition();
          },
        })
        .then((dataChange) => {
          if (dataChange.value) {
            self.SaveDefinition();
          }
        });
    },
  },
  computed: {
    ...mapGetters({
      startingPoint: "getStartingPoint",
      validation: "getValidation",
      beginBulkRegistration: "beginBulkRegistration",
    }),
  },
  watch: {
    beginBulkRegistration: function (v) {
      if (v) {
        this.register();
      }
    },
  },
};
</script>
