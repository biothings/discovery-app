<template>
  <tr>
    <td class="text-dark">
      <b class="text-info" v-text="number + 1 + ': '"></b>
      <b
        :data-tippy-content="item.name"
        v-text="
          item.name.length > 30
            ? item.name?.substring(0, 30) + '...'
            : item.name
        "
      ></b>
      <font-awesome-icon
        icon="fas fa-magnifying-glass"
        class="ml-1 pointer text-primary"
        data-tippy-content="Inspect Metadata"
        @click="getPreview(item)"
      ></font-awesome-icon>
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
            <router-link target="_blank" :to="'/resource/' + exists"
              >that record</router-link
            >. If you choose to update this record it will replace the
            previously registered metadata completely.
          </small>
        </template>
        <template v-else>
          <summary>🚨 Already registered by someone else.</summary>
          <small
            >The identifier provided has already been used to register
            <a target="_blank" :href="'/resource/' + exists">this record</a>.
            Looks like you won't be able to make any changes to this item.
          </small>
        </template>
      </details>
      <small
        data-tippy-content="This metadata cannot be registered until all requirements are met"
        class="badge badge-warning"
        v-if="missingRequired.length"
        >Attention Required</small
      >
      <details
        v-if="missingRequired.length && !exists"
        class="text-left text-danger"
      >
        <summary
          v-text="'(' + missingRequired.length + ') Missing Required Fields'"
        ></summary>
        <b v-text="missingRequired.sort().join(', ')"></b>
      </details>
      <details
        v-if="missingFields.length && !exists"
        class="text-left text-primary"
      >
        <summary
          v-text="'(' + missingFields.length + ') Missing Optional Fields'"
        ></summary>
        <b class="text-dark" v-text="missingFields.sort().join(', ')"></b>
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
    <td class="align-middle">
      <div>
        <button
          class="btn btn-sm m-1 btn-block"
          data-tippy-content="Edit Metadata"
          @click="editMode = !editMode"
          :class="[editMode ? 'btn-warning' : 'btn-primary']"
        >
          <font-awesome-icon
            icon="fas fa-pen-square"
            class="ml-1 pointer"
          ></font-awesome-icon>
          Edit Metadata
        </button>
        <button
          class="btn btn-sm m-1 btn-primary btn-block"
          data-tippy-content="Perform a full validation check locally against the schema in question"
          @click="validate()"
        >
          <font-awesome-icon
            icon="fas fa-check"
            class="ml-1 pointer"
          ></font-awesome-icon>
          Validate vs Schema
        </button>
        <button
          class="btn btn-sm m-1 btn-primary btn-block"
          data-tippy-content="Test validity for registration without registering this metadata"
          @click="validateAPI()"
        >
          <font-awesome-icon
            icon="fas fa-registered"
            class="ml-1 pointer"
          ></font-awesome-icon>
          Dry Run Registration
        </button>
      </div>
      <template v-if="errMSG">
        <div>
          <button
            role="button"
            @click="register()"
            class="btn btn-sm btn-block mainBackLight text-light m-1"
            title="Try to registered your metadata again with latest changes"
          >
            Retry Registration
          </button>
        </div>
      </template>
      <template v-else>
        <div v-if="canOverwrite">
          <button
            role="button"
            @click="updateJSONItem()"
            class="btn btn-sm btn-info btn-block text-light m-1"
            title="Update registered metadata with new changes made here"
          >
            Update Registration
          </button>
        </div>
      </template>
    </td>
    <td
      class="align-middle"
      :class="{
        'badge-danger': errMSG,
        'badge-success': successMSG,
        'badge-info': successMSGUpdate,
      }"
    >
      <span class="d-block text-light text-center">
        <font-awesome-icon
          v-if="loading"
          icon="fas fa-spinner"
          class="fa-pulse mainTextDark"
        ></font-awesome-icon>
        <small v-if="errMSG">FAILED</small>
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
  <tr v-if="editMode">
    <td colspan="4" class="m-0 alert alert-secondary">
      <button
        type="button"
        @click="closeAndSave()"
        class="btn btn-success btn-sm m-1"
      >
        Save & Close
      </button>
      <div :id="itemID" style="width: 800px"></div>
      <button
        type="button"
        @click="closeAndSave()"
        class="btn btn-success btn-sm m-1"
      >
        Save & Close
      </button>
    </td>
  </tr>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
import { basicSetup, EditorView } from "codemirror";
import { EditorState, Compartment } from "@codemirror/state";
import { json } from "@codemirror/lang-json";
import { autocompletion } from "@codemirror/autocomplete";
import {
  defaultHighlightStyle,
  syntaxHighlighting,
} from "@codemirror/language";
import { history } from "@codemirror/commands";
import Ajv from "ajv";
import addFormats from "ajv-formats";

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
      editMode: false,
      editor: null,
      itemID: Math.floor(Math.random() * 90000) + 10000,
      editedItem: {},
    };
  },
  props: ["item", "number", "username"],
  methods: {
    checkAlreadyExists(item) {
      let self = this;
      if (Object.hasOwnProperty.call(item, "identifier")) {
        let id = item.identifier.replace("&", "%26");
        const runtimeConfig = useRuntimeConfig();
        axios
          .get(
            runtimeConfig.public.apiUrl +
              `/api/dataset/query?q=(identifier:("${id}"))`
          )
          .then((res) => {
            if (res.data.total == 1) {
              self.exists = res.data.hits[0]["_id"];
              self.$store.commit("addBulkReport", {
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
    checkRequirements(item) {
      let self = this;
      //rest first
      self.missingFields = [];
      self.missingRequired = [];

      let itemFields = Object.keys(item);
      let validationFields = Object.keys(self.validation.properties);
      let requiredFields = self.validation.required;
      // ensure all items have @type and @context
      requiredFields.push("@type");
      requiredFields.push("@context");
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
      //add @context if missing from original file
      if (!item?.["@context"]) {
        let schemaContext = this.$store.getters.getOutput?.["@context"];
        if (schemaContext) {
          this.item["@context"] = schemaContext;
          self.missingFields.push("(ADDED) @context");
        }
      }
      const ordered = Object.keys(item)
        .sort()
        .reduce((obj, key) => {
          obj[key] = item[key];
          return obj;
        }, {});
      this.$store.commit("saveEditedItem", {
        value: ordered,
        index: this.number,
        notify: false,
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
      let item = this.clean(Object.assign({}, this.item));
      this.checkRequirements(item);
      this.checkAlreadyExists(item);
    },
    SaveDefinition() {
      let value = this.beforeCloseVal;
      console.log("value", value);
      this.$swal.fire({
        icon: "success",
        toast: true,
        title: "Metadata Updated",
        showConfirmButton: false,
        timer: 1000,
      });
      try {
        this.item = JSON.parse(value);
      } catch (error) {
        this.$swal.fire({
          icon: "error",
          toast: true,
          title: "Invalid JSON",
          showConfirmButton: false,
          timer: 1000,
        });
      }
    },
    getPreview(item) {
      this.$swal.fire({
        position: "center",
        confirmButtonColor: "#43318d",
        cancelButtonColor: "#d83f87",
        customClass: "scale-in-center",
        html: `<div class="text-left p-1 previewBox bg-dark"><pre id="previewJSON"></pre></div>`,
        didOpen: function () {
          renderjson.set_show_to_level(5);
          document.getElementById("previewJSON").appendChild(renderjson(item));
        },
      });
    },
    registerJSONItem() {
      var self = this;

      let schema = self.$store.getters.schema;
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
              `<a class="btn btn-sm alert-success" href="/resource/` +
              res.data.id +
              `" target="_blank" rel="nonreferrer"> 
              View Registration</a>`;
            self.errMSG = "";
            self.$store.commit("addBulkReport", {
              field: "Registered",
              value: self.item.identifier,
            });
          }
        })
        .catch((err) => {
          self.loading = false;
          self.$store.commit("addBulkReport", {
            field: "Failed",
            value: self.item.identifier,
          });
          self.errMSG =
            err.response?.data?.error == "Conflict"
              ? "Registration already exists"
              : JSON.stringify(err.response?.data, null, 2);
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
            self.$store.commit("addBulkReport", {
              field: "Updated",
              value: self.exists,
            });
            self.successMSGUpdate =
              `<a class="btn btn-sm alert-info" href="/resource/` +
              self.exists +
              `" target="_blank" rel="nonreferrer">
               View Update</a>`;
            self.errMSG = "";
          }
        })
        .catch((err) => {
          self.loading = false;
          self.$store.commit("addBulkReport", {
            field: "Failed",
            value: self.exists,
          });
          self.errMSG =
            err.response?.data?.error == "Conflict"
              ? "Registration already exists"
              : JSON.stringify(err.response?.data, null, 2);
        });
    },
    // editItemOLD(item) {
    //   let self = this;
    //   this.$swal
    //     .fire({
    //       title: "Edit Metadata",
    //       confirmButtonColor: "#5C3069",
    //       cancelButtonColor: "#006476",
    //       customClass: "scale-in-center swal-wide",
    //       html: '<textarea id="editContent"></textarea>',
    //       showCancelButton: true,
    //       confirmButtonText: "Save Changes",
    //       didOpen: function () {
    //         // self.editor = CodeMirror.fromTextArea(
    //         //   document.getElementById("editContent"),
    //         //   {
    //         //     mode: "json",
    //         //     // lineNumbers: true,
    //         //     autorefresh: true,
    //         //     lineWrapping: true,
    //         //     spellcheck: true,
    //         //     autofocus: true,
    //         //   }
    //         // );
    //         // self.editor.setValue(JSON.stringify(item, null, 2));
    //         // self.editor.on("change", (editor) => {
    //         //   self.beforeCloseVal = editor.getValue();
    //         // });
    //       },
    //       preConfirm: () => {
    //         self.SaveDefinition();
    //       },
    //     })
    //     .then((dataChange) => {
    //       if (dataChange.value) {
    //         self.SaveDefinition();
    //       }
    //     });
    // },
    closeAndSave() {
      let self = this;
      try {
        let editorData = this.editor.state.doc.toString();
        if (editorData) {
          let newVal = JSON.parse(editorData);
          this.$store.commit("saveEditedItem", {
            value: newVal,
            index: this.number,
            notify: true,
          });
          this.editor = null;
          this.editMode = false;
          setTimeout(() => {
            self.checkRequirements(self.item);
          }, 1000);
        } else {
          console.log("No editor data", editorData);
        }
      } catch (error) {
        console.log("INVALID JSON", error.toString());
      }
    },
    loadContent() {
      let self = this;
      let language = new Compartment(),
        tabSize = new Compartment();

      let state = EditorState.create({
        doc: JSON.stringify(this.item, null, 2),
        extensions: [
          basicSetup,
          history(),
          autocompletion(),
          language.of(json()),
          tabSize.of(EditorState.tabSize.of(8)),
          syntaxHighlighting(defaultHighlightStyle),
          // watch for changes
          // EditorView.updateListener.of(function (e) {
          //     console.log('change', e.state.doc.toString())
          //     try {
          //       //valid JSON
          //       let newVal = JSON.parse(e.state.doc.toString());
          //       this.editedItem = newVal;
          //     } catch (error) {
          //       // not yet valid JSON
          //     }
          // })
        ],
      });

      setTimeout(() => {
        // give UI time to render container needed for editor
        self.editor = new EditorView({
          state,
          parent: document.getElementById(self.itemID),
        });
      }, 500);
      // let value = editor.state.doc;
      // console.log(value);
    },
    validate() {
      var ajv = new Ajv({ allErrors: true, strict: false });
      addFormats(ajv);
      var schema = this.validation;
      var data = this.item;
      const isValid = ajv.validate(schema, data);
      if (!isValid && ajv?.errors) {
        this.getPreview(ajv.errors);
      } else {
        this.getPreview({ result: "ALL GOOD!" });
      }
    },
    validateAPI() {
      var self = this;

      let schema = self.$store.getters.schema;
      self.loading = true;
      let config = {
        headers: {
          "content-type": "application/json",
        },
      };
      // ./api/schema/validate/namespace/curie
      const runtimeConfig = useRuntimeConfig();

      axios
        .post(
          runtimeConfig.public.apiUrl +
            "/api/schema/validate/" +
            schema["namespace"] +
            "/" +
            schema["prefix"] +
            ":" +
            schema["label"],
          self.item,
          config
        )
        .then((res) => {
          self.loading = false;
          self.getPreview(res.data);
        })
        .catch((err) => {
          self.loading = false;
          self.getPreview(err);
        });
    },
  },
  computed: {
    ...mapGetters({
      startingPoint: "startingPoint",
      validation: "getValidation",
      beginBulkRegistration: "beginBulkRegistration",
    }),
  },
  mounted: function () {
    this.checkRequirements(this.item);
  },
  watch: {
    beginBulkRegistration: function () {
      this.register();
    },
    editMode: function (v) {
      if (v) {
        this.loadContent();
      }
    },
  },
};
</script>

<style>
#editContent {
  width: 700px;
  height: 400px;
}
</style>
