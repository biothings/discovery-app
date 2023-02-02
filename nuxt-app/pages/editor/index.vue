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
            <font-awesome-icon
              icon="fas fa-user-check"
              class="text-light"
            ></font-awesome-icon>
          </span>
          <a
            class="nav-link active text-primary mr-2"
            :href="'/login?next=' + $route.currentPath"
            v-if="userInfo && !userInfo.login"
          >
            <span
              class="badge bg-info text-light pointer tip"
              data-tippy-content="Click to sign in"
            >
              <font-awesome-icon
                icon="fas fa-sign-in-alt"
                class="text-light"
              ></font-awesome-icon>
              Sign In
            </span>
          </a>
          <template v-if="newClassAdded">
            <span
              class="badge mainBackDark text-light pointer tip mr-2"
              data-tippy-content="Preview"
              @click="getPreview()"
            >
              <font-awesome-icon
                icon="fas fa-code"
                class="text-light"
              ></font-awesome-icon>
              Preview
            </span>
            <span
              class="badge btn-success text-light pointer tip mr-2"
              data-tippy-content="Download your schema"
              @click="downloadSchema()"
            >
              <font-awesome-icon
                icon="fas fa-file-download"
                class="text-light"
              ></font-awesome-icon>
              Download
            </span>
            <span
              class="badge btn-primary text-light pointer tip mr-2"
              data-tippy-content="Requires GitHub Login"
              @click.prevent="githubOptions()"
            >
              <font-awesome-icon
                icon="fab fa-github"
                class="text-light"
              ></font-awesome-icon>
              Save to GitHub*
            </span>
            <span
              class="badge btn-secondary text-light pointer tip mr-2"
              data-tippy-content="Learn about this editor"
              @click.prevent="showHelp()"
            >
              <font-awesome-icon
                icon="fas fa-question-circle"
                class="text-light"
              ></font-awesome-icon>
              Help
            </span>
          </template>
          <span
            v-if="userInfo && userInfo.login"
            class="badge btn-primary text-light pointer tip mr-2"
            data-tippy-content="Save Progress Locally"
            @click.prevent="handleProgress()"
          >
            Save/Load Progress
          </span>
          <small class="text-light"
            >Extending
            <font-awesome-icon
              icon="fas fa-chevron-right"
              class="mr-1"
            ></font-awesome-icon>
            <b v-text="startingPoint"></b
          ></small>
          <nuxt-link
            class="mx-2 text-warning"
            data-tippy-content="Click here to go to the schema registry and select a starting point or choose a new one."
            to="/registry"
            >change starting point</nuxt-link
          >
        </div>
        <div
          v-if="newClassAdded && !removeValidation"
          class="actions p-2 rounded d-flex align-items-center justify-content-center rounded-0"
          :class="[
            validationView ? 'bg-info text-light' : 'alert-info text-dark',
          ]"
        >
          <div
            class="col-sm-5 mr-1 d-flex align-items-center justify-content-center"
          >
            <div class="mr-2">
              <small
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
                  ><font-awesome-icon
                    icon="fas fa-info-circle"
                    class="text-light"
                  ></font-awesome-icon>
                  Define how the input for each property should be validated,
                  drag and drop common rules or create your own.</small
                >
              </p>
            </div>
            <div
              class="col-sm-12 col-md-6 bg-secondary border-right"
              style="max-height: 800px; overflow-y: scroll"
            >
              <h4 class="text-light text-center m-0 pt-2">
                Your Validation
              </h4>
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
            <div class="col-sm-12 col-md-6 bg-dark border-left pb-2">
              <h4 class="text-light text-left m-0 pt-2">Options</h4>
              <!-- CARDINALITY -->
              <div
                class="my-1 alert alert-primary"
              >
                <h6 class="text-left font-weight-bold">Cardinality</h6>
                <small class="text-dark text-left d-block"
                  >Refers to the number of elements in a set or other grouping, as
                  a property of that grouping.</small
                >
                <div class="py-1">
                  <label class="text-muted m-0" for="ac"
                    >Enable Cardinality</label
                  >
                  <input
                    v-model="addCardinality"
                    id="ac"
                    class="slider ml-2"
                    @click="toggleCardinality()"
                    type="checkbox"
                  />
                </div>
              </div>
              <ValidationOptions></ValidationOptions>
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
                ><font-awesome-icon
                  icon="fas fa-chevron-right"
                ></font-awesome-icon>
                Choose a namespace</small
              >
            </p>
            <h4 class="text-info text-center">
              Choose a short name used to identify new definitions
            </h4>
            <p class="text-center text-muted">
              <small class="text-muted"
                ><font-awesome-icon
                  icon="fas fa-info-circle"
                  class="text-info"
                ></font-awesome-icon>
                For example: <b>myname</b>:ClassName
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
                ><font-awesome-icon
                  icon="fas fa-chevron-right"
                ></font-awesome-icon>
                namespace: <span class="text-info" v-text="prefix"></span
              ></small>
              <small class="text-muted bold"
                ><font-awesome-icon
                  icon="fas fa-chevron-right"
                ></font-awesome-icon>
                Create a new class</small
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
                  <font-awesome-icon
                    icon="fas fa-info-circle"
                    class="text-info"
                  ></font-awesome-icon>
                  You are extending
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
                  <font-awesome-icon
                    icon="fas fa-asterisk"
                    class="text-danger"
                  ></font-awesome-icon>
                  Name of the new extended class:
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
                  <font-awesome-icon
                    icon="fas fa-asterisk"
                    class="text-danger"
                  ></font-awesome-icon>
                  Brief description about this class:
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
                    >1.
                    <font-awesome-icon
                      icon="fas fa-circle"
                      class="text-primary"
                    ></font-awesome-icon>
                    Reuse properties from parents
                    <i class="text-danger">Required</i></small
                  >
                  <small class="text-muted d-block"
                    >2.
                    <font-awesome-icon
                      icon="fas fa-star"
                      class="text-warning"
                    ></font-awesome-icon>
                    Add new properties
                    <i class="text-danger">Required</i></small
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
                    >4.
                    <font-awesome-icon
                      icon="fab fa-github"
                      class="text-success"
                    ></font-awesome-icon>
                    Save/Download schema</small
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
                  ><font-awesome-icon
                    icon="fas fa-times"
                    class="text-danger mr-1"
                  ></font-awesome-icon
                  >Remove Validation</label
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
        <font-awesome-icon
          icon="fas fa-arrow-right"
          class="text-success"
        ></font-awesome-icon>
        Click <b>Download</b>
        <font-awesome-icon
          icon="fas fa-arrow-right"
          class="text-success"
        ></font-awesome-icon>
        Host your schema file<span class="text-danger">*</span>. Eg. on
        <a target="_blank" rel="noreferrer" href="https://github.com/"
          >GitHub</a
        >
      </p>
      <p class="m-0">
        Done with that too?
        <font-awesome-icon
          icon="fas fa-arrow-right"
          class="text-success"
        ></font-awesome-icon>
        Visualize, Register and share your schema here:
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
import { mapGetters, mapState } from "vuex";
import axios from "axios";
import moment from "moment";
import Notify from "simple-notify";

import editorImg from "@/assets/img/editor.png";
import dropSound from "@/assets/img/tinybutton.wav";

import NGXGraph from "~~/components/NGXGraph.vue";
import ValidationDropzone from "~~/components/ValidationDropzone.vue";
import GitHubSaver from "~~/components/GitHubSaver.vue";
import EditorClassBox from "~~/components/EditorClassBox.vue";

export default {
  name: "SchemaEditor",
  head() {
    return {
      title: "DDE | Schema Editor",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/rssJ788J/editor.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/rssJ788J/editor.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/editor",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/editor",
        },
        {
          property: "og:description",
          content: "Extend an existing schema to create your own.",
        },
        {
          name: "description",
          content: "Extend an existing schema to create your own.",
        },
        {
          name: "twitter:card",
          content: "Extend an existing schema to create your own.",
        },
      ],
    };
  },
  components: {
    NGXGraph,
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
      dropSound: dropSound,
    };
  },
  computed: {
    ...mapGetters({
      userInfo: "userInfo",
      validation_props: "getValidationProps",
      startingPoint: "getStartingPoint",
      prefix: "getPrefix",
      classesAvailable: "getSchema",
      loading: "loading",
      addCardinality: "addCardinality",
    }),
    removeValidation: {
      get() {
        return this.$store.getters.removeValidation;
      },
      set(v) {
        this.$store.commit("setRemoveValidation", { value: v });
      },
    },
    ...mapState({
      newClassAdded: (state) => {
        if (state?.editor?.schema?.length) {
          for (var i = 0; i < state.editor.schema.length; i++) {
            if (state.editor.schema[i].special) {
              return true;
            }
          }
          return false;
        } else {
          return false;
        }
      },
    }),
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
          new Notify({
            status: "error",
            title: "Oh no!",
            text: "[" + value + "] cannot contain non-alphanumeric values",
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
          self.availableNamespace = false;
        } else {
          const runtimeConfig = useRuntimeConfig();
          let url = runtimeConfig.public.apiUrl + "/api/registry/" + value;
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
    toggleCardinality() {
      this.$store.commit("toggleCardinality");
    },
    toggleVOptions() {
      this.$store.commit("toggleValOptions");
    },
    editValidation() {
      let self = this;
      self.validationView = !self.validationView;
      this.$store.commit("formPreview");
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

          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
          confirmButtonText: "Next",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
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
      let self = this;
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

            confirmButtonColor: "#63296b",
            cancelButtonColor: "#4a7d8f",
            customClass: "scale-in-center",
            confirmButtonText: "Next",
            showLoaderOnConfirm: true,
            preConfirm: (method) => {
              return method;
            },
            allowOutsideClick: () => !self.$swal.isLoading(),
            backdrop: true,
          })
          .then((result) => {
            if (result.value) {
              switch (result.value) {
                case "all":
                  localStorage.removeItem("EditorProgress");
                  new Notify({
                    status: "success",
                    title: "Done!",
                    text: "All gone!",
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
                    new Notify({
                      status: "success",
                      title: "Done!",
                      text: "All gone!",
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
                  } else {
                    new Notify({
                      status: "error",
                      title: "Oh no!",
                      text: "Not found, nothing happened...",
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
                  break;
              }
            }
          });
      } else {
        new Notify({
          status: "warning",
          title: "Hmmm",
          text: "Nothing to delete",
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

            confirmButtonColor: "#63296b",
            cancelButtonColor: "#4a7d8f",
            customClass: "scale-in-center",
            confirmButtonText: "Next",
            showLoaderOnConfirm: true,
            preConfirm: (method) => {
              return method;
            },
            allowOutsideClick: () => !self.$swal.isLoading(),
            backdrop: true,
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
              schema: this.$store.state["editor"],
              // 'startingPoint': this.$store.getters.getStartingPoint,
              // 'parentInfo': this.$store.getters.getSchema.find(cls => cls.name == this.$store.getters.getStartingPoint)
            };
          } else {
            return entry;
          }
        });
        localStorage.setItem("EditorProgress", JSON.stringify(newEntries));
        new Notify({
          status: "success",
          title: "Done!",
          text: "Save complete!",
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
      } else {
        new Notify({
          status: "warning",
          title: "Done!",
          text: "Not found, saving as NEW!",
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
        this.saveNewEntry(schema);
      }
    },
    async saveNewEntry(schema) {
      let self = this;
      var progress = localStorage.getItem("EditorProgress");
      if (progress) {
        progress = JSON.parse(progress);
        const { value: desc } = await self.$swal.fire({
          title:
            "Enter a short description to help you remember this save file.",
          input: "text",
          inputLabel: "Enter description",
          inputPlaceholder: "Type here",

          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
        });

        if (desc) {
          let item = {
            description: desc,
            date: moment().format("MM-DD-YYYY, h:mm:ss A"),
            schema: this.$store.state["editor"],
            // 'startingPoint': this.$store.getters.getStartingPoint,
            // 'parentInfo': this.$store.getters.getSchema.find(cls => cls.name == this.$store.getters.getStartingPoint)
          };
          progress.push(item);
          localStorage.setItem("EditorProgress", JSON.stringify(progress));
          new Notify({
            status: "success",
            title: "Done!",
            text: desc + " SAVED!",
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
            schema: this.$store.state["editor"],
            // 'startingPoint': this.$store.getters.getStartingPoint,
            // 'parentInfo': this.$store.getters.getSchema.find(cls => cls.name == this.$store.getters.getStartingPoint)
          };
          localStorage.setItem("EditorProgress", JSON.stringify([item]));
          new Notify({
            status: "success",
            title: "Done!",
            text: desc + " SAVED!",
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

          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
          confirmButtonText: "Next",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (result.value) {
            let found = progress.find((entry) => entry.date == result.value);
            if (found) {
              self.loadDataIntoEditor(found);
              new Notify({
                status: "success",
                title: "Done!",
                text: "Loading: " + found.date,
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
            } else {
              new Notify({
                status: "error",
                title: "Oh no!",
                text: "Oh no! We can't find this item...",
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
        new Notify({
          status: "warning",
          title: "Oops!",
          text: "Class name should be PascalCased",
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
            icon: "error",
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

          customClass: "scale-in-center",
          html: `<h6 class="text-center mainTextDark">Preview</h6><div class="text-left p-1 previewBox bg-dark"><pre id="previewJSON"></pre></div>`,
          didOpen: function () {
            renderjson.set_show_to_level(5);
            document
              .getElementById("previewJSON")
              .appendChild(renderjson(self.$store.getters.getFinalSchema));
          },
        });
      }
    },
    checkForData() {
      let self = this;
      var schema = localStorage.getItem("EditorData");
      var startingPoint = localStorage.getItem("EditorStartingPoint");

      if (schema && startingPoint) {
        var payload = {};
        payload["schema"] = JSON.parse(schema);
        payload["start"] = startingPoint;
        this.$store.commit("saveSchemaForEditor", payload);
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

            customClass: "scale-in-center",
            inputAttributes: {
              autocapitalize: "off",
            },
            showCancelButton: true,
            confirmButtonText: "Download JSON-LD",
            allowOutsideClick: () => !self.$swal.isLoading(),
            backdrop: true,
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
      this.$swal.fire({
        title: "Editor",

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
          progressSteps: ["A", "B"],
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
            const runtimeConfig = useRuntimeConfig();

            return axios
              .post(runtimeConfig.public.apiUrl + "/api/gh", data, config)
              .then((res) => {
                if (res.data.success) {
                  return "https://github.com/" + res.data.msg;
                } else {
                  self.$swal.fire({
                    icon: "error",
                    title: "Unsuccesful...",
                    text: JSON.stringify(res.data, null, 2),
                  });
                }
              })
              .catch((err) => {
                self.$swal.fire({
                  icon: "error",
                  title: "Oops...Something went wrong!",
                  text: err,
                });
                throw err;
              });
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (!result.dismiss) {
            self.$swal.fire({
              icon: "success",
              title: "Success!",
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
  },
  mounted: function () {
    this.checkForData();
  },
  updated: function () {
    this.$store.dispatch("setUpTips");
  },
};
</script>
