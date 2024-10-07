<script setup>
import axios from "axios";
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import Notify from "simple-notify";
import { useRouter, useRoute } from "vue-router";

import CodeEditorWithProp from "../../components/CodeEditorWithProp";
import InputBox from "../../components/guide/InputBox";

const { $swal } = useNuxtApp();
const runtimeConfig = useRuntimeConfig();
const store = useStore();
let router = useRouter();
let route = useRoute();

let schema_namespaces = computed(() => store.getters.validationSchemaOptions);
let validation = computed(() => store.getters.getValidation);
let expandedWide = computed(() => store.getters.expandUI);
let json = ref({});
let searchTerm = ref("");

function updateEditor() {
  store.commit("setUsePrefilled", false);
  store.commit("formPreviewForGuide");
  json.value = store.getters.getPreview;
}

function toggleUI() {
  store.commit("toggleExpandUI");
}

useHead({
  title: "DDE | Markup Generator",
  meta: [
    {
      property: "og:description",
      content:
        "Generate JSON based on a particular schema class specification and validation rules.",
    },
    {
      name: "description",
      content:
        "Generate JSON based on a particular schema class specification and validation rules.",
    },
    {
      name: "twitter:card",
      content:
        "Generate JSON based on a particular schema class specification and validation rules.",
    },
    {
      name: "og:url",
      content: "https://discovery.biothings.io/dataset/validator",
    },
    {
      name: "og:image",
      content: "https://i.postimg.cc/X7C7cYPZ/generator.jpg",
    },
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/X7C7cYPZ/generator.jpg",
    },
  ],
});

function reset() {
  router.push({
    name: route.name,
  });
  searchTerm.value = "";
  json.value = {};
  store.commit("reset");
}

function handleSubmit() {
  if (searchTerm.value) {
    router.push({
      name: route.name,
      query: { schema_class: searchTerm.value },
    });
    getClassValidation(searchTerm.value);
  } else {
    reset();
  }
}

function getClassValidation(curie) {
  store.commit("setLoading", { value: true });
  axios
    .get(runtimeConfig.apiUrl + `/api/registry/${curie.split(":")[0]}/${curie}`)
    .then((res) => {
      store.commit("setStartingPoint", {
        namespace: "n3c",
        prefix: "n3c",
        name: "Dataset",
      });
      store.commit("changeStep", { step: 3 });
      store.commit("saveSchemaName", { name: "n3c:Dataset" });
      store.commit("saveSchema", { schema: res.data });
      store.commit("setLoading", { value: false });
      new Notify({
        status: "success",
        title: "Ready",
        text: curie + " loaded successfully",
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
    })
    .catch((err) => {
      store.commit("setLoading", { value: false });
      try {
        $swal.fire({
          type: "error",
          position: "center",
          title: "Failed because: ",
          text: err,
        });
      } catch (e) {
        throw e;
      }
      throw err;
    });
}

onMounted(() => {
  store.dispatch("getValidationOptions");
  if (route.query.schema_class) {
    searchTerm.value = route.query.schema_class;
    getClassValidation(searchTerm.value);
  }
});
</script>
<template>
  <div class="bg-light min-100 mb-5">
    <div
      class="text-left bg-light"
      :class="[!expandedWide ? 'container' : 'container-fluid px-3']"
    >
      <Title :title="searchTerm || 'Markup Generator'"></Title>
      <div class="m-0 row p-1 bg-dde-mid">
        <div class="col-sm-12 bg-dde-dark p-2 d-flex">
          <form @submit.prevent="handleSubmit()" class="d-flex col-sm-5">
            <input
              type="text"
              list="input_ac"
              placeholder="Select Class"
              v-model="searchTerm"
              class="form-control form-control-sm"
            />
            <datalist id="input_ac" v-if="schema_namespaces.length">
              <option
                v-for="item in schema_namespaces"
                :key="item"
                :value="item"
              >
                {{ item }}
              </option>
            </datalist>
            <button
              v-if="searchTerm"
              type="submit"
              class="btn btn-sm bg-success text-light ml-1"
            >
              Load
            </button>
            <button
              v-if="searchTerm"
              type="button"
              @click="reset()"
              class="btn btn-sm bg-danger text-light ml-1"
            >
              Clear
            </button>
          </form>
          <button
            type="button"
            data-tippy-content="Stretch/Shrink UI Horizontally"
            class="btn btn-sm btn-info"
            @click="toggleUI()"
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
        <div
          class="col-sm-12 col-md-7 p-0"
          :class="[validation?.properties ? 'alert-success' : 'alert-dark']"
        >
          <div
            v-if="!searchTerm"
            class="row d-flex justify-content-center align-items-center"
          >
            <div class="col-sm-8 alert bg-dde-muted mt-5">
              <h5>Instructions</h5>
              <ol>
                <li>
                  Select a class to start with from the list and hit the
                  <b>load</b> button.
                </li>
                <li>
                  We'll display this class' validation as an easy-to-use form.
                </li>
                <li>Fill out whatever fields you want.</li>
                <li>Hit the <b>Generate JSON</b> to see your output.</li>
              </ol>
            </div>
          </div>
          <div class="text-danger alert-dark m-0 p-1">
            <h5 v-if="validation?.properties" class="m-0">Required</h5>
          </div>
          <template v-for="(prop, index) in validation.properties" :key="index">
            <InputBox
              v-if="store.getters.isRequired(index)"
              :name="index"
              :info="prop"
            ></InputBox>
          </template>
          <div class="text-info alert-dark m-0 p-1">
            <h5 v-if="validation?.properties" class="m-0">Recommended</h5>
          </div>
          <template v-for="(prop, index) in validation.properties" :key="index">
            <InputBox
              v-if="!store.getters.isRequired(index)"
              :name="index"
              :info="prop"
            ></InputBox>
          </template>
        </div>
        <div class="col-sm-12 col-md-5 p-0 bg-dde-mid">
          <div
            v-if="searchTerm"
            class="d-flex justify-content-center align-items-start grad-light"
          >
            <button class="btn btn-success m-1" @click="updateEditor">
              Generate JSON
            </button>
          </div>
          <CodeEditorWithProp
            class="alert-secondary"
            :item="json"
          ></CodeEditorWithProp>
          <div class="alert-warning p-1 m-0">
            <small>
              Note: Changes you type here won't have any effect on the form on
              the left side.
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
