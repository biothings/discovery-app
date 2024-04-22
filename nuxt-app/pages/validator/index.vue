<script setup>
import axios from "axios";
import { reactive, ref, onMounted } from "vue";
import { useAuthStore } from "../../stores/auth";
import { useValidatorStore } from "../../stores/validator";
import Notify from "simple-notify";
import { useRouter, useRoute } from "vue-router";
import { useMainStore } from '../../stores/index'

const { $swal } = useNuxtApp();
const authStore = useAuthStore();
const store = useMainStore();
const validatorStore = useValidatorStore();
let classValidationJSON = reactive({});
let metadataSelected = reactive({});
const runtimeConfig = useRuntimeConfig();
let errors = ref(false);
let valid = ref(false);
let expanded = ref(false);
let expandedWide = ref(false);
let router = useRouter();
let route = useRoute();

let searchTerm = ref("");

function handleSubmit() {
  router.push({
    name: route.name,
    query: { schema_class: searchTerm.value },
  });
  getClassValidation(searchTerm.value);
}

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

function format() {
  //trigger a change, will be handled on JSONEditor
  metadataSelected.value = { ...validatorStore.getValidationMetadata };
}

function getClassValidation(v) {
  store.loadingON();
  axios
    .get(runtimeConfig.public.apiUrl + "/api/schema/" + v + "/validation")
    .then((res) => {
      store.loadingOFF();
      classValidationJSON.value = res.data;
      $swal.fire({
        icon: "success",
        toast: true,
        title: v + "Schema Class Validation Loaded",
        showConfirmButton: false,
        timer: 3000,
        position: "top-right",
        iconColor: "white",
        customClass: {
          popup: "bg-success text-white",
        },
      });
    })
    .catch((err) => {
      store.loadingOFF();
      $swal.fire({
        title: "Oh no!",
        html: `<b>"${v}"</b> is not a class with validation, make another selection.`,
        footer: err?.message,
      });
      throw err;
    });
}

function validateMetadata() {
  if (
    !searchTerm.value ||
    !classValidationJSON.value ||
    !validatorStore.getValidationMetadata
  ) {
    $swal.fire(
      "Error!",
      "Missing required data to perform validation",
      "error"
    );
  } else {
    store.loadingON();
    const headers = {
      "Content-Type": "application/json",
    };
    axios
      .post(
        runtimeConfig.public.apiUrl +
          "/api/schema/validate/" +
          searchTerm.value.split(":")[0] +
          "/" +
          searchTerm.value,
        validatorStore.getValidationMetadata,
        {
          headers: headers,
        }
      )
      .then((res) => {
        store.loadingOFF();
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
        store.loadingOFF();
        $swal.fire("Oh no!", "Cannot validate this metadata", "error");
        throw err;
      });
  }
}

function reset() {
  classValidationJSON.value = {};
  metadataSelected.value = {};
  errors.value = false;
  valid.value = false;
}

function loadRegistered() {
  store.loadingON();
  axios
    .get(
      runtimeConfig.public.apiUrl +
        "/api/dataset?&user=" +
        authStore.userInfo?.login
    )
    .then((publicResults) => {
      let list = publicResults.data.hits;
      store.loadingOFF();
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
      store.loadingOFF();
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

onMounted(() => {
  validatorStore.getValidationOptions();
  if (route.query.schema_class) {
    searchTerm.value = route.query.schema_class;
  }
  if (searchTerm.value) {
    getClassValidation(searchTerm.value);
  }
});
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
          <strong class="text-light mr-2">Schema Class Validation:</strong>
          <div class="col-sm-4">
            <form @submit.prevent="handleSubmit()" class="d-flex">
              <input
                type="text"
                list="input_ac"
                placeholder="Type here..."
                v-model="searchTerm"
                class="form-control form-control-sm"
              />
              <datalist
                id="input_ac"
                v-if="validatorStore.validationSchemaOptions.length"
              >
                <option
                  v-for="item in validatorStore.validationSchemaOptions"
                  :key="item"
                  :value="item"
                >
                  {{ item }}
                </option>
              </datalist>
              <button
                v-if="searchTerm"
                type="submit"
                class="btn btn-sm bg-dark text-light"
              >
                Load
              </button>
            </form>
          </div>
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
          :content="classValidationJSON"
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
