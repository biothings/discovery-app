<script setup>
import axios from "axios";
import { reactive, computed, ref } from "vue";
import { useStore } from "vuex";
import Notify from "simple-notify";

const { $swal } = useNuxtApp();
const store = useStore();
let schemaSelected = reactive({});
let metadataSelected = reactive({});
let optionSelected = reactive({});
const runtimeConfig = useRuntimeConfig();
let errors = ref(false);
let valid = ref(false);
let expanded = ref(false);
let expandedWide = ref(false);

let userInfo = computed(() => store.getters.userInfo);
let metaToValidate = computed(() => store.getters.getValidationMetadata);

useHead({
  title: "DDE | Metadata Validator",
  meta: [
    {
      property: "og:description",
      content: "An interactive metadata vs schema validator.",
    },
    {
      name: "description",
      content: "An interactive metadata vs schema validator.",
    },
    {
      name: "twitter:card",
      content: "An interactive metadata vs schema validator.",
    },
    {
      name: "og:url",
      content: "https://discovery.biothings.io/dataset/validator",
    },
    {
      name: "og:image",
      content: "https://i.postimg.cc/ZRm0nQ0h/dde-Validator.jpg",
    },
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/ZRm0nQ0h/dde-Validator.jpg",
    },
  ],
});

let schemas = store.getters.getValidationSchemaOptions;

function format() {
  //trigger a change, will be handled on JSONEditor
  metadataSelected.value = { ...metaToValidate.value };
}

function getSchema(e) {
  store.commit("setLoading", { value: true });
  optionSelected.value = schemas.find((opt) => opt.url == e.target.value);
  console.log(optionSelected.value);
  axios
    .get(runtimeConfig.public.apiUrl + optionSelected.value["url"])
    .then((res) => {
      store.commit("setLoading", { value: false });
      schemaSelected.value = res.data;
    })
    .catch((err) => {
      store.commit("setLoading", { value: false });
      $swal.fire("Oh no!", "There was an issue fetching this schema", "error");
      throw err;
    });
}

function validateMetadata() {
  if (
    !optionSelected.value?.["name"] ||
    !schemaSelected.value ||
    !metaToValidate
  ) {
    $swal.fire(
      "Error!",
      "Missing required data to perform validation",
      "error"
    );
  } else {
    store.commit("setLoading", { value: true });
    const headers = {
      "Content-Type": "application/json",
    };
    axios
      .post(
        runtimeConfig.public.apiUrl +
          "/api/schema/validate/" +
          optionSelected.value["name"].split(":")[0] +
          "/" +
          optionSelected.value["name"],
        metaToValidate.value,
        {
          headers: headers,
        }
      )
      .then((res) => {
        store.commit("setLoading", { value: false });
        if (Object.hasOwnProperty.call(res.data, "valid")) {
          if (res.data?.valid) {
            errors.value = false;
            valid.value = true;
          } else {
            errors.value = res.data?.details;
            valid.value = false;
            new Notify({
              status: "error",
              title: "Invalid metadata",
              text: errors.value.length + " issues found",
              effect: "fade",
              speed: 300,
              customClass: null,
              customIcon: null,
              showIcon: true,
              showCloseButton: true,
              autoclose: true,
              autotimeout: 3000,
              gap: 20,
              distance: 20,
              type: 1,
              position: "right top",
            });
          }
        } else {
          valid.value = false;
          $swal.fire("Oh no!", "Cannot validate this metadata", "error");
        }
      })
      .catch((err) => {
        valid.value = false;
        store.commit("setLoading", { value: false });
        $swal.fire("Oh no!", "Cannot validate this metadata", "error");
        throw err;
      });
  }
}

function reset() {
  schemaSelected.value = {};
  metadataSelected.value = {};
  errors.value = false;
  valid.value = false;
}

function loadRegistered() {
  store.commit("setLoading", { value: true });
  axios
    .get(runtimeConfig.public.apiUrl + "/api/dataset?&user=" + userInfo?.login)
    .then((publicResults) => {
      let list = publicResults.data.hits;
      store.commit("setLoading", { value: false });
      let options = {};
      for (var i = 0; i < list.length; i++) {
        options[list[i]["name"]] = list[i]["name"];
      }
      $swal
        .fire({
          title: "Select metadata to load",
          input: "select",
          inputOptions: options,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          customClass: "scale-in-center",
          customClass: "scale-in-center",
          inputPlaceholder: "Select an item",
          showCancelButton: true,
        })
        .then((result) => {
          if (result.value) {
            for (var i = 0; i < list.length; i++) {
              if (result.value === list[i]["name"]) {
                metadataSelected.value = list[i];
                new Notify({
                  status: "success",
                  title: "Loading success",
                  text: list[i]["name"],
                  effect: "fade",
                  speed: 300,
                  customClass: null,
                  customIcon: null,
                  showIcon: true,
                  showCloseButton: true,
                  autoclose: true,
                  autotimeout: 3000,
                  gap: 20,
                  distance: 20,
                  type: 1,
                  position: "right top",
                });
                break;
              }
            }
          }
        });
    })
    .catch((err) => {
      store.commit("setLoading", { value: false });
      new Notify({
        status: "error",
        title: "Failed to load public metadata",
        text: err.toString(),
        effect: "fade",
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 3000,
        gap: 20,
        distance: 20,
        type: 1,
        position: "right top",
      });
      throw err;
    });
}

// function getFromURL(){
//   $swal.fire({
//     title: 'Enter URL',
//     footer:"<small>Enter URL where metadata could be found, we will look for metadata imbedded in a script tag</small>",
//     input: 'text',
//     inputAttributes: {
//       autocapitalize: 'off'
//     },
//     showCancelButton: true,
//     confirmButtonText: 'Look up',
//     showLoaderOnConfirm: true,
//     preConfirm: (url) => {
//       return fetch(url)
//         .then(response => {
//           if (!response.ok) {
//             throw new Error(response.statusText)
//           }
//           return response.toString()
//         })
//         .catch(error => {
//           $swal.showValidationMessage(
//             `Request failed: ${error}`
//           )
//         })
//     },
//     allowOutsideClick: () => !$swal.isLoading(),
//     backdrop: true
//   }).then((result) => {
//     if (result.isConfirmed) {
//       console.log('RESULT URL', result.value)
//       var doc = new DOMParser().parseFromString(result.value, "text/html");
//       var links = doc.querySelectorAll("h1");
//       console.log('H!', links)
//       var els = document.createElement('div');
//       els.innerHTML = result.value;
//       let found = els.querySelectorAll('h1')
//       console.log('FOUND', found)
//     }
//   })
// }

async function getFile() {
  const { value: file } = await $swal.fire({
    title: "Open File",
    html: `<p>Select JSON file to start.</p>`,
    input: "file",
    confirmButtonColor: "#5C3069",
    cancelButtonColor: "#006476",
    customClass: "scale-in-center",
    inputAttributes: {
      accept: "json",
      "aria-label": "Upload your file",
    },
  });

  if (file) {
    try {
      const blob = new Blob([file], { type: "application/json" });
      const fr = new FileReader();

      fr.addEventListener("load", () => {
        metadataSelected.value = JSON.parse(fr.result);
      });
      fr.readAsText(blob);
    } catch (e) {
      $swal.fire({
        icon: "error",
        title: "Something is wrong..",
        text: e,
      });
    }
  }
}
</script>
<template>
  <div
    class="mt-5 p-0"
    :class="[!expandedWide ? 'container' : 'container-fluid px-3']"
  >
    <div class="jumbotron bg-light text-center p-2">
      <h1 class="logoText logoFont">Metadata Validator</h1>
    </div>
    <div class="row p-2 alert-secondary rounded mb-5">
      <div class="col-sm-12 alert-info p-0">
        <div
          class="bg-info p-1 d-flex justify-content-start align-items-center flex-wrap px-4 py-2"
        >
          <div class="numberCircle mainBackDark m-0 mr-2">1</div>
          <strong class="text-light mr-2">Schema:</strong>
          <select
            name="schema-selector"
            class="form-control form-control-sm col-sm-4"
            @change="getSchema($event)"
          >
            <option value="" disabled selected>Select Schema</option>
            <template v-for="schema in schemas" :key="schema.name">
              <option :value="schema.url">
                {{ schema.name }}
              </option>
            </template>
          </select>
          <font-awesome-icon
            icon="fas fa-info-circle"
            class="mx-2 text-warning"
            data-tippy-content="Load the json-schema validation from a registered class and use it to validate against some metadata. Changes will not have an effect on results."
          ></font-awesome-icon>
          <button
            class="btn btn-sm rounded btn-info mr-2"
            @click="expanded = !expanded"
          >
            <font-awesome-icon
              v-if="!expanded"
              icon="fas fa-chevron-down"
            ></font-awesome-icon>
            <font-awesome-icon
              v-if="expanded"
              icon="fas fa-chevron-up"
            ></font-awesome-icon>
          </button>
          <button
            type="button"
            class="btn btn-sm btn-info"
            @click="expandedWide = !expandedWide"
          >
            <template v-if="!expandedWide">
              <font-awesome-icon
                icon="fas fa-chevron-left"
                class="mr-1"
              ></font-awesome-icon>
              <font-awesome-icon
                icon="fas fa-chevron-right"
              ></font-awesome-icon>
            </template>
            <template v-if="expandedWide">
              <font-awesome-icon
                icon="fas fa-chevron-right"
                class="mr-1"
              ></font-awesome-icon>
              <font-awesome-icon icon="fas fa-chevron-left"></font-awesome-icon>
            </template>
          </button>
        </div>
        <JSONEditor
          v-if="expanded"
          name="validatorSchema"
          :content="schemaSelected"
        ></JSONEditor>
      </div>
      <div class="col-sm-12 col-md-7 alert-primary p-0">
        <div
          class="bg-primary p-1 d-flex justify-content-start align-items-center flex-wrap px-4 py-2"
        >
          <div class="numberCircle mainBackDark m-0 mr-2">2</div>
          <strong class="text-light mr-2">Metadata:</strong>
          <button
            data-tippy-content="Open local file"
            type="button"
            class="btn btn-sm btn-dark mr-2"
            @click="getFile()"
          >
            <font-awesome-icon
              icon="fas fa-file-download"
              class="mr-1 text-info"
            ></font-awesome-icon>
            Load File
          </button>
          <!-- <button
            data-tippy-content="GitHub or web page"
            type="button"
            class="btn btn-sm btn-primary mr-2"
            @click="getFromURL()"
          >
            Load from URL
          </button> -->
          <button
            data-tippy-content="Load metadata from your dashboard"
            type="button"
            class="btn btn-sm btn-dark mr-2"
            @click="loadRegistered()"
          >
            <font-awesome-icon
              icon="fas fa-registered"
              class="mr-1 text-info"
            ></font-awesome-icon>
            Load Registered
          </button>
          <button
            data-tippy-content="prettify JSON"
            type="button"
            class="btn btn-sm btn-primary mr-2"
            @click="format()"
          >
            <font-awesome-icon
              icon="fas fa-indent"
              class="mr-1"
            ></font-awesome-icon>
            Format
          </button>
          <font-awesome-icon
            icon="fas fa-info-circle"
            class="mx-2 text-warning"
            data-tippy-content="Load metadata in json format to validate against the selected schema validation above. Changes can be made and will have an effect on results."
          ></font-awesome-icon>
        </div>
        <JSONEditor
          name="validatorMetadata"
          :content="metadataSelected"
        ></JSONEditor>
      </div>
      <div class="col-sm-12 col-md-5 p-0 alert-light">
        <div
          class="p-1 d-flex justify-content-start align-items-center flex-wrap px-4 py-2"
          :class="[!errors.length ? 'bg-success' : 'bg-danger']"
        >
          <div class="numberCircle mainBackDark m-0 mr-2">3</div>
          <div>
            <button
              data-tippy-content="Validate Metadata against schema selected"
              type="button"
              class="btn btn-sm btn-dark mr-2"
              @click="validateMetadata()"
            >
              <font-awesome-icon
                icon="fas fa-check"
                class="mr-1 text-success"
              ></font-awesome-icon>
              Validate Metadata
            </button>
            <button
              data-tippy-content="Clear all fields"
              type="button"
              class="btn btn-sm btn-dark mr-2"
              @click="reset()"
            >
              <font-awesome-icon
                icon="fas fa-retweet"
                class="mr-1 text-danger"
              ></font-awesome-icon>
              Reset
            </button>
          </div>
        </div>
        <div class="m-2" v-if="errors">
          <p>Details:</p>
          <template v-for="(err, i) in errors" :key="i + '-error'">
            <div
              class="d-flex justify-items-start align-items-center text-danger"
            >
              <font-awesome-icon
                icon="fas fa-exclamation-circle"
                class="text-danger mr-1"
              ></font-awesome-icon>
              <code>{{ err }}</code>
            </div>
          </template>
        </div>
        <div class="m-2 text-success" v-if="valid">
          <h4><strong> Valid metadata!</strong></h4>
        </div>
      </div>
    </div>
  </div>
</template>
