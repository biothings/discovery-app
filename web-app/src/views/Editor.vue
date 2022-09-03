<template>
  <section
    id="editor"
    class="container-fluid m-auto col-sm-12 col-md-10 col-lg-10 col-xl-8"
    style="min-height: 80vh; padding-top: 60px"
    v-cloak
  >
    <audio id="dropsound" :src="dropSound"></audio>
    <div>
      <div class="jumbotron bg-light text-center m-1 p-2">
        <h1 class="logoText">Schema Editor</h1>
        <small class="text-muted"
          >Extend an existing schema to create your own.</small
        >
      </div>
      <div id="widget">
        <div
          class="actions bg-dark p-2 rounded d-flex align-items-center justify-content-start rounded-0"
        >
          <span
            class="badge bg-success text-light tip mr-2"
            :data-tippy-content="'Logged in as ' + userInfo.login"
            v-if="userInfo && userInfo.login"
          >
            <font-awesome-icon icon="fas fa-user-check" class="text-light"></font-awesome-icon>
          </span>
          <a
            class="nav-link active text-primary mr-2"
            :href="'/login?next=' + window.location.pathname"
            v-if="userInfo && !userInfo.login"
          >
            <span
              class="badge bg-info text-light pointer tip"
              data-tippy-content="Click to sign in"
            >
              <font-awesome-icon icon="fas fa-sign-in-alt" class="text-light"></font-awesome-icon> Sign In
            </span>
          </a>
          <template v-if="newClassAdded">
            <span
              class="badge mainBackDark text-light pointer tip mr-2"
              data-tippy-content="Preview"
              @click="getPreview()"
            >
              <font-awesome-icon icon="fas fa-code" class="text-light"></font-awesome-icon> Preview
            </span>
            <span
              class="badge bg-success text-light pointer tip mr-2"
              data-tippy-content="Download your schema"
              @click="downloadSchema()"
            >
              <font-awesome-icon icon="fas fa-file-download" class="text-light"></font-awesome-icon> Download
            </span>
            <span
              class="badge bg-primary text-light pointer tip mr-2"
              data-tippy-content="Requires GitHub Login"
              @click.prevent="githubOptions()"
            >
              <font-awesome-icon icon="fab fa-github" class="text-light"></font-awesome-icon> Save to GitHub*
            </span>
            <span
              class="badge bg-secondary text-light pointer tip mr-2"
              data-tippy-content="Learn about this editor"
              @click.prevent="showHelp()"
            >
              <font-awesome-icon icon="fas fa-question-circle" class="text-light"></font-awesome-icon> Help
            </span>
          </template>
          <span
            v-if="userInfo && userInfo.login"
            class="badge bg-primary text-light pointer tip mr-2"
            data-tippy-content="Save Progress Locally"
            @click.prevent="handleProgress()"
          >
            Save/Load Progress
          </span>
          <small class="text-light"
            >Extending <font-awesome-icon icon="fas fa-chevron-right"></font-awesome-icon>
            <b v-text="startingPoint"></b
          ></small>
        </div>
        <div
          v-if="newClassAdded && !removeValidation"
          class="actions bg-info p-2 rounded d-flex align-items-center justify-content-center rounded-0"
        >
          <div
            class="col-sm-5 mr-1 d-flex align-items-center justify-content-center"
          >
            <div class="mr-2">
              <small class="text-light"
                ><img src="@/assets/img/cube.svg" width="30px" /> Validation
                Editor</small
              >
            </div>
            <div>
              <input
                class="form-control slider m-auto tip"
                @click="editValidation()"
                data-tippy-content="Edit Schema Validation"
                type="checkbox"
              />
            </div>
          </div>
        </div>
        <!-- Validation -->
        <div
          v-if="validationView && !removeValidation"
          class="v-container p-0 bg-dark justify-content-center d-flex align-items-center"
        >
          <div class="w-100 row m-0">
            <div class="bg-info p-1 col-sm-12">
              <p class="text-center text-light m-0">
                <small class="text-light"
                  ><font-awesome-icon icon="fas fa-info-circle" class="text-light"></font-awesome-icon> Define how the
                  input for each property should be validated, drag and drop
                  common rules or create your own.</small
                >
              </p>
            </div>
            <div
              class="col-sm-12 col-md-6 bg-secondary border-right"
              style="max-height: 800px; overflow-y: scroll"
            >
              <h5 class="text-light text-center m-0 text-dark pt-2">
                Your Validation
              </h5>
              <template
                v-for="(val, propname) in validation_props"
                :key="propname"
              >
                <ValidationDropzone
                  :propname="propname"
                  :val="val"
                ></ValidationDropzone>
              </template>
            </div>
            <div class="col-sm-12 col-md-6 bg-dark border-left">
              <h5 class="text-light text-center m-0 text-muted pt-2">
                Common Validation Options
              </h5>
              <small class="text-info text-center d-block"
                >Drag & drop to merge validation</small
              >
              <div class="border rounded p-2 bg-light mb-2">
                <template v-for="item in validation_options" :key="item.title">
                  <div
                    class="badge drag-el m-1"
                    :data-tippy-content="JSON.stringify(item.validation, null, 2)"
                    :style="{ 'background-color': item.color }"
                    draggable
                    @dragstart="startDrag($event, item)"
                  >
                    <span v-text="item.title"></span>
                    <span
                      data-tippy-content="EDIT"
                      class="badge badge-light pointer"
                      @click="editValidationOption(item)"
                      ><font-awesome-icon icon="fas fa-pen-square"></font-awesome-icon></span>
                    <span
                      v-if="item && item.can_delete"
                      data-tippy-content="DELETE"
                      class="badge badge-danger pointer"
                      @click="deleteValidationOption(item)"
                      ><font-awesome-icon icon="fas fa-times"></font-awesome-icon></span>
                  </div>
                </template>
                <div
                  @click="addValidationOption()"
                  data-tippy="ADD NEW"
                  class="badge m-1 badge-secondary text-light pointer"
                >
                  <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
                </div>
              </div>
              <div class="bg-dark p-1" v-if="item">
                <CodeEditor></CodeEditor>
              </div>
              <h5 class="text-light text-center m-0 text-muted pt-2">
                Definitions
              </h5>
              <small class="text-info text-center d-block"
                >Create reusable validation definitions</small
              >
              <div class="border rounded p-2 alert-info mb-2">
                <template v-for="item in definition_options" :key="item.title">
                  <div
                    class="badge m-1 text-light"
                    :data-tippy-content="JSON.stringify(item.validation, null, 2)"
                    :style="{ 'background-color': item.color }"
                  >
                    <span v-text="item.title"></span>
                    <span
                      data-tippy-content="EDIT"
                      class="badge badge-light pointer"
                      @click="editDefinitionOption(item)"
                      ><font-awesome-icon icon="fas fa-pen-square"></font-awesome-icon></span>
                    <span
                      v-if="item && item.can_delete"
                      data-tippy-content="DELETE"
                      class="badge badge-danger pointer"
                      @click="deleteDefinitionOption(item)"
                      ><font-awesome-icon icon="fas fa-times"></font-awesome-icon
                    ></span>
                  </div>
                </template>
                <div
                  @click="addDefinitionOption()"
                  data-tippy="ADD NEW"
                  class="badge m-1 badge-secondary text-light pointer"
                >
                  <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
                </div>
              </div>
              <div class="bg-dark p-1" v-if="definition_item">
                <DefinitionEditor></DefinitionEditor>
              </div>
            </div>
          </div>
        </div>
        <!-- LOGGED IN DASHBOARD -->
        <template v-if="userInfo && userInfo.login">
          <!-- NAMESPACE -->
          <div class="jumbotron alert-secondary" v-if="!prefix">
            <p class="text-center text-muted">
              <small
                >Extending:
                <span class="text-dark" v-text="startingPoint"></span
              ></small>
              <small
                class="bold"
                :class="{
                  'text-success': availableNamespace,
                  'text-danger': !availableNamespace,
                }"
                ><font-awesome-icon icon="fas fa-chevron-right"></font-awesome-icon> Choose a namespace</small
              >
            </p>
            <h4 class="text-info text-center">
              Choose a short name used to identify new definitions
            </h4>
            <p class="text-center text-muted">
              <small class="text-muted"
                ><font-awesome-icon icon="fas fa-info-circle" class="text-info"></font-awesome-icon> For example:
                <b>myname</b>:ClassName
              </small>
            </p>
            <div
              class="d-flex justify-content-center align-items-center flex-wrap"
            >
              <form @submit.prevent="savePrefix" class="text-center">
                <div class="input-group">
                  <input
                    type="text"
                    v-model="inputNamespace"
                    class="form-control m-auto text-center"
                    :class="{
                      'text-success': availableNamespace,
                      'text-danger': !availableNamespace,
                    }"
                    placeholder=""
                  />
                  <div>
                    <button
                      :disabled="!availableNamespace"
                      class="btn text-light"
                      :class="{
                        'btn-success': availableNamespace,
                        'btn-danger': !availableNamespace,
                      }"
                      type="submit"
                    >
                      Continue
                    </button>
                  </div>
                </div>
                <small class="text-muted"
                  >Choose a short namespace (a-z) 3 chars minimum
                  recommended.</small
                >
              </form>
            </div>
          </div>

          <!-- Custom Class -->
          <div
            class="jumbotron alert-secondary p-2 text-center text-muted"
            v-if="prefix && !newClassAdded"
          >
            <p class="text-center text-muted">
              <small
                >Extending schema:
                <span class="text-info" v-text="startingPoint"></span
              ></small>
              <small class="text-muted"
                ><font-awesome-icon icon="fas fa-chevron-right"></font-awesome-icon> namespace:
                <span class="text-info" v-text="prefix"></span
              ></small>
              <small class="text-muted bold"
                ><font-awesome-icon icon="fas fa-chevron-right"></font-awesome-icon> Create a new class</small
              >
            </p>
            <hr />
            <form
              class="m-auto col-sm-12 col-md-9 py-2 bg-light rounded fade-in text-left"
              @submit.prevent="addClass()"
            >
              <h4 class="text-info">Create a new class</h4>
              <small>
                <p>
                  <font-awesome-icon icon="fas fa-info-circle" class="text-info"></font-awesome-icon> You are extending
                  <span class="text-info" v-text="startingPoint"></span>,
                  consider naming your class something more specific or relevant
                  to the class' hierarchy.
                </p>
                <p>
                  Description can be a short paragraph about how this class is
                  more specific from the class you are extending, need to extend
                  this hierarchy, or use case.
                </p>
              </small>
              <div class="form-group">
                <h5 for="exampleInputEmail1" class="text-dark">
                  <font-awesome-icon icon="fas fa-asterisk" class="text-danger"></font-awesome-icon> Name of the new
                  extended class:
                </h5>
                <small class="d-block my-1 text-info"
                  >Learn about naming conventions
                  <a
                    href="https://schema.org/docs/styleguide.html"
                    target="_blank"
                    rel="nonreferrer"
                    >here</a
                  ></small
                >
                <input
                  type="text"
                  ref="clsName"
                  class="form-control"
                  id="exampleInputEmail1"
                  placeholder="Name should be PascalCased eg. MyClass"
                />
              </div>
              <div class="form-group">
                <h5 for="exampleInputPassword1" class="text-dark">
                  <font-awesome-icon icon="fas fa-asterisk" class="text-danger"></font-awesome-icon> Brief description
                  about this class:
                </h5>
                <textarea
                  type="password"
                  minlength="20"
                  rows="6"
                  ref="clsDesc"
                  class="form-control"
                  placeholder="Enter your Class description here"
                ></textarea>
              </div>
              <div>
                <button type="submit" class="btn btn-success">Continue</button>
              </div>
            </form>
          </div>

          <!-- PARENT CLASSES -->
          <div
            class="jumbotron alert-secondary p-2"
            v-if="newClassAdded && !validationView"
            id="editorTippy"
          >
            <div class="row m-0">
              <div class="col-sm-12">
                <h6 class="text-info text-left">
                  Select and create properties for your schema
                </h6>
                <p class="text-left">
                  <small class="text-muted d-block"
                    >1. <font-awesome-icon icon="fas fa-circle" class="text-primary"></font-awesome-icon> Reuse
                    properties from parents
                    <i class="text-danger">Required</i></small
                  >
                  <small class="text-muted d-block"
                    >2. <font-awesome-icon icon="fas fa-star" class="text-warning"></font-awesome-icon> Add new
                    properties <i class="text-danger">Required</i></small
                  >
                  <small class="text-muted d-block"
                    >3. (<img src="@/assets/img/cube.svg" width="15px" />
                    Complete Validation Editor) <b>OR</b> (<i
                      class="fas fa-times text-danger mr-1"
                    ></i>
                    Remove Validation)
                    <i class="text-danger">Required</i></small
                  >
                  <small class="text-muted d-block"
                    >4. <font-awesome-icon icon="fab fa-github" class="text-success"></font-awesome-icon> Save/Download
                    schema</small
                  >
                </p>
              </div>
            </div>

            <!-- REMOVE VALIDATION -->
            <div
              class="col-sm-12 d-flex align-items-center justify-content-around"
            >
              <div class="mt-2">
                <input
                  v-model="removeValidation"
                  id="rv"
                  class="slider mr-2 tip"
                  @click="toggleRemoveValidation()"
                  data-tippy-content="Remove Validation"
                  type="checkbox"
                />
                <label class="text-muted" for="rv"
                  ><font-awesome-icon icon="fas fa-times" class="text-danger mr-1"></font-awesome-icon>Remove
                  Validation</label
                >
              </div>
              <div class="mt-2">
                <input
                  type="checkbox"
                  class="slider mr-2"
                  id="customControlInline"
                  @click="toggleDesc()"
                />
                <label for="customControlInline" class="text-muted"
                  >Show Descriptions</label
                >
              </div>
            </div>
            <template v-for="(item, index) in classesAvailable" :key="index">
              <EditorClassBox :item="item"></EditorClassBox>
            </template>
            <div class="w-100 p-1">
              <NGXGraph></NGXGraph>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="alert alert-light text-danger text-center p-5">
            <h5>You must be logged in to proceed</h5>
          </div>
        </template>
      </div>
    </div>
    <div class="alert alert-secondary" v-if="newClassAdded">
      <p class="m-0">
        Done editing? Easy!
        <font-awesome-icon icon="fas fa-arrow-right" class="text-success"></font-awesome-icon> Click <b>Download</b>
        <font-awesome-icon icon="fas fa-arrow-right" class="text-success"></font-awesome-icon> Host your schema
        file<span class="text-danger">*</span>. Eg. on
        <a target="_blank" rel="noreferrer" href="https://github.com/"
          >GitHub</a
        >
      </p>
      <p class="m-0">
        Done with that too?
        <font-awesome-icon icon="fas fa-arrow-right" class="text-success"></font-awesome-icon> Visualize, Register and
        share your schema here:
        <a href="/schema-playground">Schema Playground</a>
      </p>
    </div>
    <div id="ghOptions" class="modal" style="z-index: 1000">
      <!-- Modal content -->
      <div class="modal-content bg-light">
        <div>
          <span id="closeBtn" class="close">&times;</span>
        </div>
        <GitHubSaver></GitHubSaver>
      </div>
    </div>
  </section>
</template>

<script>
import tippy from "tippy.js";
import { mapGetters, mapState } from "vuex";
import axios from "axios";
import moment from "moment";
import renderjson from 'renderjson'


import cubeImg from "@/assets/img/cubeplus.svg";
import editorImg from "@/assets/img/editor.png";
import dropSound from "@/assets/img/tinybutton.wav"

import NGXGraph from "../components/NGXGraph.vue";
import DefinitionEditor from "../components/DefinitionEditor.vue";
import CodeEditor from "../components/CodeEditor.vue";
import ValidationDropzone from "../components/ValidationDropzone.vue";
import GitHubSaver from "../components/GitHubSaver.vue";
import EditorClassBox from "../components/EditorClassBox.vue";

export default {
  name: "SchemaEditor",
  components: {
    NGXGraph,
    DefinitionEditor,
    CodeEditor,
    ValidationDropzone,
    GitHubSaver,
    EditorClassBox,
  },
  data: function () {
    return {
      inputNamespace: "",
      availableNamespace: false,
      validationView: false,
      loadingMode: false,
      loadingSchema: null,
      dropSound: dropSound
    };
  },
  computed: {
    ...mapGetters({
        userInfo: 'userInfo',
        removeValidation: 'removeValidation',
        definition_options: 'getDefinitionOptions',
        validation_props: 'getValidationProps',
        validation_options: 'getValidationOptions',
        startingPoint: 'getStartingPoint',
        prefix: 'getPrefix',
        classesAvailable: 'getSchema',
        item: 'getEditItem',
        definition_item: 'getEditDefinitionItem',
        loading: 'loading',

    }),
    ...mapState({
        newClassAdded: state => {
            console.log('STATE', state)
            for (var i = 0; i < state.editor.schema.length; i++) {
                if (state.editor.schema[i].special) {
                return true;
                }
            }
            return false;
        }
    })
  },
  watch: {
    prefix: function (prefix) {
      if (prefix && !this.loadingMode) {
        this.$store.dispatch("getParents");
        setTimeout(() => {
          this.$store.dispatch("SelectExistingProps");
        }, 1000);
        setTimeout(() => {
          this.$store.dispatch("applyExistingValidationRules");
        }, 2000);
      }
    },
    inputNamespace: function (value, oldvalue) {
      let self = this;
      var re = /^[a-z0-9]+$/i;
      if (value.length < 3) {
        self.availableNamespace = false;
      } else {
        if (!re.test(value)) {
          $.notify("[" + value + "] cannot contain non-alphanumeric values", {
            globalPosition: "right",
            style: "error",
            showDuration: 100,
          });
          self.availableNamespace = false;
        } else {
          let url = self.$apiUrl +  "/api/registry/" + value;
          self.$store.commit("setLoading", { value: true });
          axios
            .head(url)
            .then(function (res) {
              self.availableNamespace = false;
              console.log(
                '%c Namespace "' + value + '" is NOT available',
                "color:coral"
              );
              self.$store.commit("setLoading", { value: false });
            })
            .catch((err) => {
              //last check for reserved names
              self.$store.commit("setLoading", { value: false });
              if (value === "metadata" || value === "dataset") {
                self.availableNamespace = false;
              } else {
                self.availableNamespace = true;
              }
              console.log(
                '%c Namespace "' + value + '" is available',
                "color:limegreen"
              );
              // throw err;
            });
        }
      }
    },
  },
  methods: {
    editValidation() {
      let self = this;
      self.validationView = !self.validationView;
      this.$store.commit("formPreview");
    },
    getRandomColor() {
      let self = this;
      var letters = "0123456789ABCDEF";
      var color = "#";
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    editValidationOption(item) {
      let copy = Object.assign({}, item);
      this.$store.commit("editThis", { item: copy });
    },
    editDefinitionOption(item) {
      let copy = Object.assign({}, item);
      this.$store.commit("editThisDefinition", { item: copy });
    },
    makeid(length) {
      var result = "";
      var characters =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      var charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    },
    async addValidationOption() {
      let self = this;
      const { value: name } = await self.$swal.fire({
        title: "Name of new validation option",
        input: "text",
        inputPlaceholder: "Name this option",
      });

      if (name) {
        let payload = {
          validation: {
            _id: self.makeid(4),
            title: name,
            color: self.getRandomColor(),
            list: 2,
            validation: { type: "EDIT to define" },
            can_delete: true,
          },
        };
        this.$store.commit("addValidationOption", payload);
      }
    },
    async addDefinitionOption() {
      let self = this;
      const { value: name } = await self.$swal.fire({
        title: "Name of new definition (must be unique)",
        input: "text",
        inputPlaceholder: "Name this option",
      });

      if (name) {
        let payload = {
          definition: {
            _id: self.makeid(6),
            title: name,
            color: self.getRandomColor(),
            list: 2,
            validation: { type: "EDIT to define" },
            can_delete: true,
          },
        };
        this.$store.commit("addDefinitionOption", payload);
      }
    },
    startDrag: (evt, item) => {
      let img = new Image();
      img.src = cubeImg;
      evt.dataTransfer.setDragImage(img, 10, 10);

      evt.dataTransfer.dropEffect = "move";
      evt.dataTransfer.effectAllowed = "move";
      evt.dataTransfer.setData("itemID", item._id);
    },
    githubOptions() {
      // show modal
      this.$store.commit("formPreview");
      var modal = document.getElementById("ghOptions");
      modal.style.display = "block";
      var span = document.getElementById("closeBtn");
      span.onclick = function () {
        modal.style.display = "none";
      };
    },
    handleProgress() {
      var self = this;
      self.$swal
        .fire({
          title: "Save/Load Progress",
          text: "What would you like to do?",
          input: "select",
          inputOptions: {
            save: "💾 Save my work",
            load: "⏬ Load something",
            delete: "🗑️ Delete some stuff",
          },
          footer:
            "<small>Note: This feature will use your <a href='https://www.w3schools.com/html/html5_webstorage.asp' target='_blank'>browser's local storage</a>, <b>clearing it will delete all your progress records</b>. To manage your local storage: <code>right click > inspect > click on the Application tab > Storage > Local Storage</code></small>",
          inputPlaceholder: "Select Action",
          showCancelButton: true,
          animation: false,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
          confirmButtonText: "Next",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
        })
        .then((result) => {
          if (result.value) {
            switch (result.value) {
              case "save":
                self.saveProgress();
                break;
              case "load":
                self.loadProgress();
                break;
              case "delete":
                self.deleteProgress();
                break;
              default:
                return false;
            }
          }
        });
    },
    deleteProgress() {
      var progress = localStorage.getItem("EditorProgress");
      if (progress) {
        progress = JSON.parse(progress);
        let options = {
          all: "🗑️ Get rid of it all! 🗑️",
        };
        progress.forEach((entry) => {
          options[
            entry.date
          ] = `🗑️ Delete : "${entry.description} (${entry.date})"`;
        });
        self.$swal
          .fire({
            title: "🗑️ Delete some stuff",
            text: "What would you like to do?",
            input: "select",
            inputOptions: options,
            footer: "Note: There is no way to recover anything once trashed.",
            inputPlaceholder: "Select Option",
            showCancelButton: true,
            animation: false,
            confirmButtonColor: "#63296b",
            cancelButtonColor: "#4a7d8f",
            customClass: "scale-in-center",
            confirmButtonText: "Next",
            showLoaderOnConfirm: true,
            preConfirm: (method) => {
              return method;
            },
            allowOutsideClick: () => !self.$swal.isLoading(),
          })
          .then((result) => {
            if (result.value) {
              switch (result.value) {
                case "all":
                  localStorage.removeItem("EditorProgress");
                  $.notify("Done! All gone", {
                    globalPosition: "right",
                    style: "info",
                    showDuration: 200,
                  });
                  break;
                default:
                  let found = progress.find(
                    (entry) => entry.date == result.value
                  );
                  if (found) {
                    let newEntries = progress.filter(
                      (entry) => entry.date !== result.value
                    );
                    localStorage.setItem(
                      "EditorProgress",
                      JSON.stringify(newEntries)
                    );
                    $.notify("Gone!", {
                      globalPosition: "right",
                      style: "success",
                      showDuration: 200,
                    });
                  } else {
                    $.notify("Not Found, nothing happened", {
                      globalPosition: "right",
                      style: "danger",
                      showDuration: 200,
                    });
                  }
                  break;
              }
            }
          });
      } else {
        $.notify("Nothing to delete", {
          globalPosition: "right",
          style: "info",
          showDuration: 200,
        });
      }
    },
    saveProgress() {
      let self = this;

      this.$store.commit("formPreview");
      let schema = this.$store.getters.getFinalSchema;

      var progress = localStorage.getItem("EditorProgress");
      if (progress) {
        progress = JSON.parse(progress);
        let options = {
          new: "💾 Save as new entry 💾",
        };
        progress.forEach((entry) => {
          options[
            entry.date
          ] = `💟 Save over : "${entry.description} (${entry.date})"`;
        });
        self.$swal
          .fire({
            title: "💾 Save Progress",
            text: "What would you like to do?",
            input: "select",
            inputOptions: options,
            footer:
              "Note: There is no way to recover old saves once saved over.",
            inputPlaceholder: "Select Option",
            showCancelButton: true,
            animation: false,
            confirmButtonColor: "#63296b",
            cancelButtonColor: "#4a7d8f",
            customClass: "scale-in-center",
            confirmButtonText: "Next",
            showLoaderOnConfirm: true,
            preConfirm: (method) => {
              return method;
            },
            allowOutsideClick: () => !self.$swal.isLoading(),
          })
          .then((result) => {
            if (result.value) {
              switch (result.value) {
                case "new":
                  self.saveNewEntry(schema);
                  break;
                default:
                  self.saveOver(progress, result.value, schema);
                  break;
              }
            }
          });
      } else {
        // new progress
        self.saveNewEntry(schema);
      }
    },
    saveOver(entries, date, schema) {
      let found = entries.find((entry) => entry.date == date);
      if (found) {
        let newEntries = entries.map((entry) => {
          if (entry.date == date) {
            return {
              description: found.description,
              date: moment().format("MM-DD-YYYY, h:mm:ss A"),
              schema: this.$store.state,
              // 'startingPoint': this.$store.getters.getStartingPoint,
              // 'parentInfo': this.$store.getters.getSchema.find(cls => cls.name == this.$store.getters.getStartingPoint)
            };
          } else {
            return entry;
          }
        });
        localStorage.setItem("EditorProgress", JSON.stringify(newEntries));
        $.notify("Save Complete!", {
          globalPosition: "right",
          style: "success",
          showDuration: 200,
        });
      } else {
        $.notify("Not Found, saving as new", {
          globalPosition: "right",
          style: "danger",
          showDuration: 200,
        });
        this.saveNewEntry(schema);
      }
    },
    async saveNewEntry(schema) {
      var progress = localStorage.getItem("EditorProgress");
      if (progress) {
        progress = JSON.parse(progress);
        const { value: desc } = await self.$swal.fire({
          title:
            "Enter a short description to help you remember this save file.",
          input: "text",
          inputLabel: "Enter description",
          inputPlaceholder: "Type here",
          animation: false,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
        });

        if (desc) {
          let item = {
            description: desc,
            date: moment().format("MM-DD-YYYY, h:mm:ss A"),
            schema: this.$store.state,
            // 'startingPoint': this.$store.getters.getStartingPoint,
            // 'parentInfo': this.$store.getters.getSchema.find(cls => cls.name == this.$store.getters.getStartingPoint)
          };
          progress.push(item);
          localStorage.setItem("EditorProgress", JSON.stringify(progress));
          $.notify(desc + " SAVED", {
            globalPosition: "right",
            style: "success",
            showDuration: 200,
          });
        }
      } else {
        const { value: desc } = await self.$swal.fire({
          title:
            "Enter a short description to help you remember this save file.",
          input: "text",
          inputLabel: "Enter description",
          inputPlaceholder: "Type here",
        });

        if (desc) {
          let item = {
            description: desc,
            date: moment().format("MM-DD-YYYY, h:mm:ss A"),
            schema: this.$store.state,
            // 'startingPoint': this.$store.getters.getStartingPoint,
            // 'parentInfo': this.$store.getters.getSchema.find(cls => cls.name == this.$store.getters.getStartingPoint)
          };
          localStorage.setItem("EditorProgress", JSON.stringify([item]));
          $.notify(desc + " SAVED", {
            globalPosition: "right",
            style: "success",
            showDuration: 200,
          });
        }
      }
    },
    loadProgress() {
      let self = this;
      var progress = localStorage.getItem("EditorProgress");
      progress = JSON.parse(progress);
      let options = {};
      progress.forEach((entry) => {
        options[entry.date] = entry.description + ` (${entry.date})`;
      });
      self.$swal
        .fire({
          title: "⏬ Load Progress",
          text: "Choose progress to load",
          input: "select",
          inputOptions: options,
          inputPlaceholder: "Select item",
          showCancelButton: true,
          animation: false,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
          confirmButtonText: "Next",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
        })
        .then((result) => {
          if (result.value) {
            let found = progress.find((entry) => entry.date == result.value);
            if (found) {
              self.loadDataIntoEditor(found);
              $.notify("PLEASE WAIT...", {
                globalPosition: "right",
                style: "info",
                showDuration: 200,
              });
              $.notify("Loading: " + found.date, {
                globalPosition: "right",
                style: "success",
                showDuration: 200,
              });
            } else {
              $.notify("Oh no! We can't find this item!", {
                globalPosition: "right",
                style: "danger",
                showDuration: 200,
              });
            }
          }
        });
    },
    loadDataIntoEditor(data) {
      this.loadingMode = true;
      console.log("✅ Loading Mode: ", this.loadingMode);
      this.$store.commit("restoreStore", { schema: data.schema });
    },
    toggleDesc() {
      this.$store.commit("toggleDesc");
    },
    toggleRemoveValidation() {
      this.$store.commit("toggleRemoveValidation");
    },
    addClass() {
      let self = this;
      let name = this.$refs.clsName.value;
      let desc = this.$refs.clsDesc.value;

      if (!name.match(/^(?=.*[a-z])[A-Z]+[a-z]*(?:\d*(?:[A-Z]+[a-z]*)?)*$/)) {
        $.notify("Class name should be PascalCased", {
          globalPosition: "right",
          style: "danger",
          showDuration: 200,
        });
      } else {
        if (name && desc) {
          // DUPLICATE CHECK
          // this.$store.getters.isDuplicateClass(name)
          let payload = {
            name: name,
            description: desc,
          };
          this.$store.commit("addClass", payload);
        } else {
          self.$swal.fire({
            type: "error",
            toast: true,
            title: "You forgot something!",
            showConfirmButton: false,
            timer: 1000,
          });
        }
      }
    },
    getPreview() {
      let self = this;
      if (self.prefix) {
        this.$store.commit("formPreview");
        self.$swal.fire({
          position: "center",
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          animation: false,
          customClass: "scale-in-center",
          html: `<h6 class="text-center mainTextDark">Preview</h6><div class="text-left p-1 previewBox"><pre id="previewJSON"></pre></div>`,
          onOpen: function () {
            renderjson.set_show_to_level(5);
            document
              .getElementById("previewJSON")
              .appendChild(renderjson(this.$store.getters.getFinalSchema));
          },
        });
      }
    },
    checkForData() {
      var schema = localStorage.getItem("EditorData");
      var startingPoint = localStorage.getItem("EditorStartingPoint");

      if (schema && startingPoint) {
        var payload = {};
        payload["schema"] = JSON.parse(schema);
        payload["start"] = startingPoint;
        this.$store.commit("saveSchema", payload);
      } else {
        self.$swal({
          title: "No Schema Selected",
          imageAlt: "Warning",
          html:
            "<p>You have not selected a schema to start with.</p> " +
            '<p>Search the <a href="/registry">Registry</a> for a schema to start from.</p>',
          showCancelButton: false,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
        });
      }
    },
    savePrefix() {
      if (this.availableNamespace) {
        var payload = {};
        payload["prefix"] = this.inputNamespace;
        this.$store.commit("savePrefix", payload);
      }
    },
    downloadSchema() {
      var self = this;
      if (self.prefix) {
        this.$store.commit("formPreview");
        self.$swal
          .fire({
            title: "Name your file",
            input: "text",
            animation: false,
            customClass: "scale-in-center",
            inputAttributes: {
              autocapitalize: "off",
            },
            showCancelButton: true,
            confirmButtonText: "Download JSON-LD",
            allowOutsideClick: () => !self.$swal.isLoading(),
          })
          .then((result) => {
            if (result.value) {
              self.download(
                JSON.stringify(this.$store.getters.getFinalSchema, null, 2),
                result.value + ".jsonld",
                "text/plain"
              );
            }
          });
      }
    },
    download(content, fileName, contentType) {
      var a = document.createElement("a");
      var file = new Blob([content], { type: contentType });
      a.href = URL.createObjectURL(file);
      a.download = fileName;
      a.click();
    },
    showHelp() {
      self.$swal.fire({
        title: "Editor",
        animation: false,
        customClass: "scale-in-center",
        html: `<p>
                    After choosing a namespace and creating your class you will be able to edit the schema you decided to extend. It's really easy and fast! Here's a quick introduction to the layout:
                  </p>
                  <small>
                    <ol class="text-left">
                      <li>
                        Log-in status.
                      </li>
                      <li>
                        Preview your work.
                      </li>
                      <li>
                        Download your work.
                      </li>
                      <li>
                        Save to GitHub directly* Requires GitHub login and permission.
                      </li>
                      <li>
                        Edit validation rules for each property you have chosen.
                      </li>
                      <li>
                        Add a new property to your class.
                      </li>
                      <li>
                        The extended Class you created.
                      </li>
                      <li>
                        Parent properties available to choose from.
                      </li>
                    </ol>
                  </small>`,
        footer: "",
        width: "52em",
        confirmButtonColor: "#63296b",
        cancelButtonColor: "#4a7d8f",
        confirmButtonText: "Ready!",
        imageUrl: editorImg,
        imageAlt: "Metadata Editor",
      });
    },
    CreateRepo() {
      var self = this;
      self.$swal
        .mixin({
          input: "text",
          confirmButtonText: "Next &rarr;",
          showCancelButton: true,
          footer: `<small class="text-danger">Important: You need to have logged in using GitHub and given us permission to access your repositories.</small>`,
          progressSteps: [
            'A',
            'B',
          ],
        })
        .queue([
          {
            title: "Name your repository",
            text: "We will create a public repository with this name",
          },
          {
            title: "Name your schema file (without extension)",
            text: "We will create a JSON-LD file with this name",
          },
        ])
        .then((result) => {
          if (result.value) {
            const answers = result.value;
            self.handleGHRequest(answers[0], answers[1] + ".jsonld");
          }
        });
    },
    handleGHRequest(repo, file) {
      var self = this;
      self.$swal
        .fire({
          title:
            "<h4>Do you give us permission to create a repository and file with these names?</h4>",
          text: repo + "/" + file,
          showCancelButton: true,
          confirmButtonText: `Go Ahead`,
          cancelButtonText: `Never Mind`,
          showLoaderOnConfirm: true,
          preConfirm: () => {
            data = {
              name: repo,
              file: file,
              data: this.$store.getters.getFinalSchema,
            };

            console.log(typeof this.$store.getters.getFinalSchema);
            console.log(data);

            let config = {
              headers: {
                "content-type": "application/json",
              },
            };

            return axios
              .post(self.$apiUrl + "/api/gh", data, config)
              .then((res) => {
                if (res.data.success) {
                  return "https://github.com/" + res.data.msg;
                } else {
                  self.$swal.fire({
                    type: "error",
                    title: "Unsuccesful...",
                    text: JSON.stringify(res.data, null, 2),
                  });
                }
              })
              .catch((err) => {
                self.$swal.fire({
                  type: "error",
                  title: "Oops...Something went wrong!",
                  text: err,
                });
                throw err;
              });
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
        })
        .then((result) => {
          if (!result.dismiss) {
            self.$swal.fire({
              type: "success",
              title: "Sucess!",
              html:
                `<h2>Repository created!</h2>
                <p>
                  Click here to see it: <a href="` +
                result.value +
                `" target="_blank" rel="nonreferrer">` +
                result.value +
                `</a>
                </p>`,
            });
          }
        });
    },
    checkCustomValidation() {
      let v = localStorage.getItem("custom_validation");
      if (v) {
        this.$store.commit("updateValidationOptions", {
          validation: JSON.parse(v),
        });
      }
    },
    checkCustomDefinitions() {
      let v = localStorage.getItem("custom_definitions");
      if (v) {
        this.$store.commit("updateDefinitionOptions", {
          definitions: JSON.parse(v),
        });
      }
    },
    deleteValidationOption(item) {
      self.$swal
        .fire({
          title: "Are you sure?",
          text: `You are deleting "${item.title}" permanently.`,
          showCancelButton: true,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          animation: false,
          customClass: "scale-in-center",
          confirmButtonText: "Delete",
        })
        .then((res) => {
          if (res.value) {
            this.$store.commit("deleteValidationOption", { id: item._id });
          }
        });
    },
    deleteDefinitionOption(item) {
      let self = this;
      self.$swal
        .fire({
          title: "Are you sure?",
          html: `<b>Warning</b>: deleting this definition will remove it from your library entirely. <br>Definitions that are not referenced will not appear in your json schema validation. Continue?`,
          showCancelButton: true,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          animation: false,
          customClass: "scale-in-center",
          confirmButtonText: "Yes, Delete",
        })
        .then((res) => {
          if (res.value) {
            this.$store.commit("deleteDefinitionOption", { id: item._id });
          }
        });
    },
  },
  mounted: function () {
    this.checkForData();
    this.checkCustomValidation();
    this.checkCustomDefinitions();

    tippy(".tip", {
      animation: "fade",
      theme: "light bg-light",
    });

    $.notify.addStyle("success", {
      html: "<div><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#28a745",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("danger", {
      html: "<div class='bg-danger text-light p-1'><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#dc3545",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("warning", {
      html: "<div class='bg-danger text-light p-1'><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#ffc107",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("info", {
      html: "<div class='bg-danger text-light p-1'><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#17a2b8",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("trophy", {
      html: `<div class="bg-dark p-1 text-light"> <span data-notify-text/>
      </div>`,
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#343a40",
          padding: "5px",
          color: "white",
          "border-radius": "5px",
        },
      },
    });
  },
};
</script>
