<script setup>
import axios from "axios";
import { reactive, computed, ref } from "vue";
import { useStore } from "vuex";
import Notify from "simple-notify";

const { $swal } = useNuxtApp();
const store = useStore();
let schemaSelected = reactive({});
let metadataSelected = reactive({});
const runtimeConfig = useRuntimeConfig();
let schemaLoaded = ref("");
let validationAvailable = ref(false);

let userInfo = computed(() => store.getters.userInfo);

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
      content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
    },
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
    },
  ],
});

let schemas = [
  {
    name: "n3c:Dataset",
    url: "/api/registry/n3c",
  },
  {
    name: "niaid:Dataset",
    url: "/api/registry/niaid",
  },
  {
    name: "niaid:ComputationalTool",
    url: "/api/registry/niaid",
  },
  {
    name: "outbreak:Dataset",
    url: "/api/registry/outbreak",
  },
];

function getSchema(e) {
  store.commit("setLoading", { value: true });
  axios
    .get(runtimeConfig.public.apiUrl + e.target.value)
    .then((res) => {
      store.commit("setLoading", { value: false });
      if (Object.hasOwnProperty.call(res.data, "source")) {
        schemaSelected.value = res.data.source["@graph"].find(
          (cls) => cls["rdfs:label"] == "Dataset"
        );
        if (
          typeof schemaSelected.value === "object" &&
          schemaSelected.value !== null
        ) {
          schemaLoaded.value = schemaSelected.value["@id"];
        } else {
          schemaLoaded.value = "";
        }
        if (Object.hasOwnProperty.call(schemaSelected.value, "$validation")) {
          validationAvailable.value = true;
        } else {
          validationAvailable.value = false;
        }
      } else {
        $swal.fire("Oh no!", "No schema found", "error");
      }
    })
    .catch((err) => {
      store.commit("setLoading", { value: false });
      $swal.fire("Oh no!", "There was an issue fetching this schema", "error");
      throw err;
    });
}

function reset() {
  schemaSelected.value = {};
  metadataSelected.value = {};
  schemaLoaded.value = false;
  validationAvailable.value = false;
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
          title: "Select Metadata To Load",
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

async function getFile(type) {
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

      fr.addEventListener("load", (e) => {
        var payload = {};
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
  <div class="container mt-5 p-0">
    <div class="jumbotron bg-light text-center p-2">
      <h1 class="logoText logoFont">Metadata Validator</h1>
    </div>
    <div class="row p-2 alert-secondary rounded mb-5">
      <div class="col-sm-12 col-md-6 alert-info p-0">
        <div
          class="bg-info p-1 d-flex justify-content-start align-items-center flex-wrap px-4 py-2"
        >
          <select
            name="schema-selector"
            class="form-control form-control-sm alert-info"
            @change="getSchema($event)"
          >
            <option value="" disabled selected>Select Schema</option>
            <template v-for="schema in schemas" :key="schema.name">
              <option :value="schema.url">
                {{ schema.name }}
              </option>
            </template>
          </select>
        </div>
        <h5 class="m-1">
          Schema:
          <small
            class="text-success btn btn-sm alert-info"
            data-tippy-content="Schema loaded"
            v-if="schemaLoaded"
          >
            <font-awesome-icon
              icon="fas fa-file-download"
              class="text-primary"
            />
            {{ schemaLoaded }}
          </small>
          <small
            class="text-muted btn btn-sm alert-secondary"
            data-tippy-content="No schema selected"
            v-else
          >
            <font-awesome-icon
              icon="fas fa-file-download"
              class="text-primary"
            />
            NO
          </small>
          <small
            class="text-success btn btn-sm mr-1 alert-info"
            data-tippy-content="Schema validation available"
            v-if="validationAvailable"
          >
            <img
              src="@/assets/img/cube.svg"
              width="15"
              title="validation available"
            />
            OK
          </small>
          <small
            class="text-muted btn btn-sm mr-1 alert-secondary"
            data-tippy-content="No validation available"
            v-else
          >
            <img
              src="@/assets/img/cube.svg"
              width="15"
              title="validation available"
            />
            NO
          </small>
        </h5>
        <JSONEditor
          name="validatorSchema"
          :content="schemaSelected"
        ></JSONEditor>
      </div>
      <div class="col-sm-12 col-md-6 alert-primary p-0">
        <div
          class="bg-primary p-1 d-flex justify-content-start align-items-center flex-wrap px-4 py-2"
        >
          <button
            data-tippy-content="Open local file"
            type="button"
            class="btn btn-sm btn-primary mr-2"
            @click="getFile()"
          >
            Load File
          </button>
          <button
            data-tippy-content="GitHub or web page"
            type="button"
            class="btn btn-sm btn-primary mr-2"
          >
            Load from URL
          </button>
          <button
            data-tippy-content="Load metadata from your dashboard"
            type="button"
            class="btn btn-sm btn-primary mr-2"
            @click="loadRegistered()"
          >
            Load Registered
          </button>
          <button
            data-tippy-content="Clear all fields"
            type="button"
            class="btn btn-sm btn-danger mr-2"
            @click="reset()"
          >
            Reset
          </button>
        </div>
        <h5 class="m-1">Metadata:</h5>
        <JSONEditor
          name="validatorMetadata"
          :content="metadataSelected"
        ></JSONEditor>
      </div>
    </div>
  </div>
</template>
