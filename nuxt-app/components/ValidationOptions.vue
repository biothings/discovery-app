<script setup>
import { watch, computed, onMounted } from "vue";
import { useStore } from "vuex";

let store = useStore();
const { $swal, $_ } = useNuxtApp();
let search_query = ref("");
let filter_selected = ref("by_name");
let search_active = ref(false);
let filter_options = ref([]);
let valSelect = ref("default");
let ordered_options = ref([]);

let editItem = computed(() => store.getters.getEditItem);
let editDefintionItem = computed(() => store.getters.getEditDefinitionItem);
let valOps = computed(() => store.getters.getValidationOptions);
let defOps = computed(() => store.getters.getDefinitionOptions);
let bioschemasMostUsed = computed(() => store.getters.getBioschemasMostUsed);
let recentlyUsed = computed(() => store.getters.getRecentlyUsed);

function filterBioSchemasMostUsed() {
  filter_options.value = valOps.value.filter((item) =>
    bioschemasMostUsed.value.includes(item.title)
  );
}

function filterAllOptions(filter) {
  if (filter == "bioschemas") {
    filter_options.value = valOps.value.filter(
      (item) => item.belongs_to == "bioschemas"
    );
    filterBioSchemasMostUsed();
  } else {
    filter_options.value = valOps.value.filter(
      (item) => item.belongs_to == "default"
    );
  }
}

function filterChange(filter) {
  filter_selected.value = filter;
}

function filterByName(q) {
  filter_options.value = filter_options.value.filter((op) =>
    op.title.includes(q.toLocaleLowerCase())
  );
}

function filterByValue(q) {
  filter_options.value = filter_options.value.filter((op) =>
    JSON.stringify(op.validation).includes(q.toLocaleLowerCase())
  );
}

function filterByCardinality(cardinality) {
  if (cardinality == "many") {
    filter_options.value = filter_options.value.filter((op) =>
      JSON.stringify(op.validation).includes("array")
    );
  } else {
    filter_options.value = filter_options.value.filter(
      (op) => !JSON.stringify(op.validation).includes("array")
    );
  }
}

function handleSubmit() {
  // console.log(search_query.value, filter_selected.value)
  if (filter_selected.value.includes("cardinality")) {
    //reset all options first
    filter_options.value = valOps.value;
    switch (filter_selected.value) {
      case "cardinality_one":
        filterByCardinality("one");
        break;
      case "cardinality_many":
        filterByCardinality("many");
        break;
      default:
        alert("You must select a filter first");
        break;
    }
  } else {
    if (!search_query.value) {
      filter_options.value = valOps.value;
      filterBioSchemasMostUsed();
    } else {
      //reset all options first
      filter_options.value = valOps.value;
      switch (filter_selected.value) {
        case "by_name":
          filterByName(search_query.value);
          break;
        case "by_value":
          filterByValue(search_query.value);
          break;
        default:
          alert("You must select a filter first");
          break;
      }
    }
  }
}

watch(search_query, function (v) {
  handleSubmit();
});

watch(valSelect, function (v) {
  filterAllOptions(v);
});

watch(search_active, function (v) {
  if (!v) {
    reset();
  }
});

watch(filter_options, function (v) {
  orderAlphabetically(v);
});

function orderAlphabetically(items) {
  let res = [];
  if (items.length < 25) {
    ordered_options.value = [
      { group: "⭐ Recently used", children: recentlyUsed },
      {
        group: "All",
        children: items,
      },
    ];
  } else {
    let data = items.reduce((r, e) => {
      let group = e["title"][0].toLocaleLowerCase();
      if (!r[group]) r[group] = { group, children: [e] };
      else r[group].children.push(e);
      return r;
    }, {});
    res = Object.values(data);
    ordered_options.value = $_.orderBy(res, ["group"], ["asc"]);
    // console.log(ordered_options.value)
    // add frequently used to beginning
    if (recentlyUsed.value?.length) {
      ordered_options.value.unshift({
        group: "⭐ Recently used",
        children: recentlyUsed,
      });
    }
  }
}

function reset() {
  search_query.value = "";
  filter_selected.value = "by_name";
  filter_options.value = valOps.value;
  filterAllOptions(valSelect.value);
}

function makeid(length) {
  var result = "";
  var characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function getRandomColor() {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

async function addValidationOption() {
  const { value: name } = await $swal.fire({
    title: "Name of new validation option",
    input: "text",
    inputPlaceholder: "Name this option",
    customClass: {
      popup: "scale-in-center",
    },
  });

  if (name) {
    let payload = {
      validation: {
        _id: makeid(4),
        title: name,
        color: getRandomColor(),
        list: 2,
        validation: { type: "EDIT to define" },
        can_delete: true,
        belongs_to: "both",
      },
    };
    store.commit("addValidationOption", payload);
    checkCustomValidation();
    checkCustomDefinitions();
    filter_options.value = valOps.value;
  }
}

async function addDefinitionOption() {
  const { value: name } = await $swal.fire({
    title: "Name of new definition (must be unique)",
    input: "text",
    inputPlaceholder: "Name this option",
    customClass: {
      popup: "scale-in-center",
    },
  });

  if (name) {
    let payload = {
      definition: {
        _id: makeid(6),
        title: name,
        color: getRandomColor(),
        list: 2,
        validation: { type: "EDIT to define" },
        can_delete: true,
        belongs_to: "both",
      },
    };
    store.commit("addDefinitionOption", payload);
    checkCustomValidation();
    checkCustomDefinitions();
    filter_options.value = valOps.value;
  }
}

function checkCustomValidation() {
  let v = localStorage.getItem("custom_validation");
  if (v) {
    store.commit("updateValidationOptions", {
      validation: JSON.parse(v),
    });
  }
}

function checkCustomDefinitions() {
  let v = localStorage.getItem("custom_definitions");
  if (v) {
    store.commit("updateDefinitionOptions", {
      definitions: JSON.parse(v),
    });
  }
}

function checkFrequentlyUsed() {
  store.commit("checkIfFrequentlyUsed");
}

onMounted(() => {
  store.dispatch("checkVersion");
});
onMounted(() => checkCustomDefinitions());
onMounted(() => checkCustomValidation());
onMounted(() => checkFrequentlyUsed());
onMounted(() => filterAllOptions(valSelect.value));
</script>

<template>
  <div class="rounded bg-dde-mid-muted p-1 text-dde-dark">
    <div class="row m-0">
      <div class="col-sm-8 d-flex justify-content-start align-items-center">
        <h6 class="m-0 font-weight-bold">Validation Options</h6>
      </div>
      <div class="col-sm-4 d-flex justify-content-start align-items-center">
        <span
          data-tippy-content="Search and filter validation"
          class="pointer text-primary"
          @click="search_active = !search_active"
        >
          <font-awesome-icon icon="fas fa-search"></font-awesome-icon> Search
        </span>
      </div>
      <div
        class="col-sm-12 d-flex justify-content-center align-items-center border-top border-light pt-1"
      >
        <span class="my-0 mr-2 text-muted">Load presets:</span>
        <select
          v-model="valSelect"
          id="valSelect"
          class="form-control form-control-sm w-50"
        >
          <option value="default" selected>Default</option>
          <option value="bioschemas">Bioschemas</option>
        </select>
        <font-awesome-icon
          icon="fas fa-rotate"
          data-tippy-content="refresh"
          class="pointer text-primary ml-2"
          @click="reset()"
        ></font-awesome-icon>
      </div>
    </div>
    <div v-if="search_active" class="fade-in">
      <form
        class="form my-1 alert-primary p-1 d-flex flex-wrap"
        @submit.prevent="handleSubmit()"
      >
        <div
          class="input-group col-sm-6 d-flex justify-content-center align-items-center"
        >
          <input
            autocomplete="off"
            v-model="search_query"
            type="text"
            class="form-control col-sm-12 form-control-sm"
            id="inlineFormInputGroup"
            placeholder="Enter your search term here"
          />
        </div>
        <div class="fade-in border-info form-group row m-0 col-sm-6">
          <div class="form-check col-sm-12">
            <input
              class="form-check-input"
              type="radio"
              id="name"
              name="flist"
              value="name"
              @click="filterChange('by_name')"
              checked
            />
            <label for="name">property name</label>
          </div>
          <div class="form-check col-sm-12">
            <input
              class="form-check-input"
              type="radio"
              id="value"
              name="flist"
              value="value"
              @click="filterChange('by_value')"
            />
            <label for="value">expected type</label>
          </div>
        </div>
        <div class="col-sm-12 px-4 row m-0 border-top border-dark pt-3">
          <div class="form-check col-sm-6">
            <input
              class="form-check-input"
              type="radio"
              id="c-one"
              name="flist"
              value="c-one"
              @click="
                filterChange('cardinality_one');
                handleSubmit();
              "
            />
            <label for="c-one">cardinality: one</label>
          </div>
          <div class="form-check col-sm-6">
            <input
              class="form-check-input"
              type="radio"
              id="c-many"
              name="flist"
              value="c-many"
              @click="
                filterChange('cardinality_many');
                handleSubmit();
              "
            />
            <label for="c-many">cardinality: many</label>
          </div>
        </div>
      </form>
    </div>
    <div class="border rounded p-2 bg-light mb-2">
      <small class="text-dark text-left d-block"
        >Drag & drop common validation options to merge into each
        property.</small
      >
      <div class="val-options-container">
        <div v-for="g in ordered_options" :key="g.group">
          <details open>
            <summary
              class="m-0 font-weight-bold text-dark border-bottom border-dark"
            >
              {{ g.group.toUpperCase() }}
              <small class="text-muted">({{ g.children.length }})</small>
            </summary>
            <template v-for="item in g.children" :key="item._id">
              <DraggableBadge :item="item"></DraggableBadge>
            </template>
          </details>
        </div>
      </div>
      <div
        @click="addValidationOption()"
        data-tippy-content="ADD NEW"
        data-tippy-placement="bottom"
        data-tippy-theme="light"
        class="badge m-1 badge-secondary text-light pointer"
      >
        <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
      </div>
      <template v-if="editItem">
        <CodeEditor></CodeEditor>
      </template>
    </div>
    <div>
      <h6 class="text-left m-0 pt-2">Definitions</h6>
      <small class="text-dark text-left d-block"
        >Create reusable validation definitions to use in your schema. New
        definitions will appear as validation options above.</small
      >
      <div class="border rounded p-2 alert-info mb-2">
        <template v-for="item in defOps" :key="item.title">
          <DefinitionBadge :item="item"></DefinitionBadge>
        </template>
        <div
          @click="addDefinitionOption()"
          data-tippy-content="ADD NEW DEFINITION"
          data-tippy-placement="bottom"
          data-tippy-theme="light"
          class="badge m-1 badge-secondary text-light pointer"
        >
          <font-awesome-icon icon="fas fa-plus"></font-awesome-icon>
        </div>
        <template v-if="editDefintionItem">
          <DefinitionEditor></DefinitionEditor>
        </template>
      </div>
    </div>
  </div>
</template>
