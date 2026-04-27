<template>
  <div class="jumbotron p-4 pb-0 bg-dde-mid text-dark m-0">
    <div class="jumbotron bg-light m-0">
      <h3>Compare Classes</h3>
      <p>View a quick side-by-side comparison of classes registered here.</p>
      <div class="content">
        <form
          @submit.prevent="getFullInfo"
          class="col-sm-12 col-lg-4 d-flex p-0"
        >
          <input
            type="text"
            list="input_ac"
            placeholder="Search"
            v-model="searchTerm"
            class="form-control form-control-sm d-inline"
          />
          <datalist
            id="input_ac"
            v-if="schema_namespaces.length && searchTerm.length > 0"
          >
            <option v-for="item in schema_namespaces" :key="item" :value="item">
              {{ item }}
            </option>
          </datalist>
          <button type="submit" class="btn btn-sm themeButton text-light ml-1">
            Add
          </button>
        </form>
      </div>
      <div class="p-1">
        <p v-if="compared_items.length">
          (Min 2 / Max 4) Selected {{ compared_items.length }} items:
        </p>
        <div class="row">
          <template v-for="item in compared_items" :key="item.label">
            <div
              class="alert-secondary border border-secondary col-sm-3 rounded shadow p-2"
            >
              {{ item.name }}
              <font-awesome-icon
                icon="fas fa-times"
                class="ml-1 text-danger pointer float-right"
                data-tippy-content="Remove item"
                @click="removeItem(item)"
              ></font-awesome-icon>
              <CompareItemDetails :cls="item"></CompareItemDetails>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useStore } from "vuex";
import { onMounted, ref, computed, watch } from "vue";
import Notify from "simple-notify";
import CompareItemDetails from "./CompareItemDetails.vue";

const store = useStore();
let schema_namespaces = computed(() => store.getters.validationSchemaOptions);
let compared_items = computed(() => store.getters.getCompareItems);
let searchTerm = ref("");

onMounted(() => {
  store.dispatch("getValidationOptions");
});

watch(
  compared_items,
  (newVal) => {
    console.log("Compared items changed:", newVal);
  },
  { deep: true }
);

function removeItem(item) {
  store.commit("removeItem", { item: item });
}

function getFullInfo() {
  let item = searchTerm.value;
  console.log("Getting full info for " + item);
  if (!item || item.includes(":") === false) {
    return;
  }
  const runtimeConfig = useRuntimeConfig();

  axios
    .get(
      runtimeConfig.public.apiUrl +
        "/api/registry/" +
        item.split(":")[0] +
        "/" +
        item +
        "?v"
    )
    .then((res) => {
      let payload = {
        item: res.data.hits[0],
      };

      // combine all props from parents and add to item
      let allProps = [];
      for (var i = 0; i < res.data["hits"].length; i++) {
        let current = res.data["hits"][i];
        if (current.hasOwnProperty("properties")) {
          allProps = allProps.concat(current["properties"]);
        }
      }
      // sort props by label
      let sorted = allProps.sort((a, b) => a.label.localeCompare(b.label));
      payload.item.properties = sorted;
      store.commit("addItem", payload);
      searchTerm.value = "";
    })
    .catch((err) => {
      new Notify({
        status: "error",
        title: "Registry Error",
        text: "Could not add item " + item.name,
        effect: "fade",
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 2000,
        gap: 20,
        distance: 20,
        type: 1,
        position: "right top",
        autoclose: true, // Enable auto close
        autotimeout: 3000, // Set timeout in milliseconds (3 seconds)
      });
      throw err;
    });
}
</script>
