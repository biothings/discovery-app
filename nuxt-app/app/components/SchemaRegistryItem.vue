<template>
  <!-- display status (deprecated, validation), name, properties added, parent class and extend/view actions -->
  <tr>
    <td class="text-center" colspan="1" style="width: 3%">
      <font-awesome-icon v-if="item?.deprecated" icon="fas fa-circle" class="text-danger" data-tippy-content="This class is deprecated and should not be used"></font-awesome-icon>
      <font-awesome-icon v-else icon="fas fa-circle" class="text-success" data-tippy-content="This class is current"></font-awesome-icon>
    </td>
    <td>
      <img
          v-if="item.validation"
          src="@/assets/img/cube.svg"
          width="15"
          title="validation available"
          class="ml-1 tip"
          data-tippy-content="Validation available"
        />
      <h6 class="m-1 mainTextDark d-inline">
        <small class="text-dde-dark" 
        :class="{ 'strikethrough-text': item?.superseded_by }">
          <NuxtLink :to="'/ns/' + item.namespace">{{
            item.namespace
          }}</NuxtLink
          >: </small
        ><b :class="{ 'strikethrough-text': item?.superseded_by, 'text-danger': item?.deprecated }">{{ item.label }}</b>
      </h6>
      <template v-if="item?.superseded_by">
        <small class="float-right">
          <font-awesome-icon icon="fas fa-arrow-right"> </font-awesome-icon> Use instead:
          <strong v-for="superseded in item.superseded_by" :key="superseded"
            class="mainTextDark ml-1">
            <!-- search the registry for the replacing class; searched by label
                 since a "prefix:label" query is parsed as field:value syntax -->
            <NuxtLink
              :to="{
                path: '/registry',
                query: { query: superseded.split(':').pop() },
              }"
              v-text="superseded"
            ></NuxtLink>
          </strong>
        </small>
      </template>
    </td>
    <td>
      <template v-if="propTotal">
        <span>+ {{ propTotal }}
          <font-awesome-icon icon="fas fa-info-circle" class="text-info" :data-tippy-content="propNames"> </font-awesome-icon>
        </span>
      </template>
    </td>
    <td>
      {{ getSubclass(item.parent_classes)}}
    </td>
    <td>
      <div
        class="p-1 bg-dde-mid d-flex align-items-center justify-content-around"
      >
        <div>
          <button
            class="btn btn-sm themeButton text-light m-1"
            @click.prevent="saveDataAndRedirect(item)"
            data-tippy-content="Visualize class in detail"
          >
            View
          </button>
        </div>
        <div>
          <ExtendClassBtn
            :ns="item.namespace"
            :curie="item.prefix + ':' + item.label"
          ></ExtendClassBtn>
        </div>
      </div>
    </td>
  </tr>
</template>

<script>
import ExtendClassBtn from "./ExtendClassBtn.vue";

export default {
  name: "SchemaRegistryItem",
  data: function () {
    return {
      options: false,
      itemID: Math.floor(Math.random() * 90000) + 10000,
    };
  },
  props: ["item"],
  methods: {
    saveDataAndRedirect(item, goesToEditor) {
      if (goesToEditor) {
        // Extend and send analytics
        if (item && item.namespace && item.label && item.prefix) {
          let obj = JSON.stringify(item);
          localStorage.setItem("EditorData", obj);
          localStorage.setItem(
            "EditorStartingPoint",
            item.prefix + ":" + item.label
          );
          this.$router.push({ path: "/editor" });
        } else {
          this.$swal.fire("Oops!", "Action not available for this item");
        }
      } else {
        // View and send analytics
        if (item && item.namespace && item.name) {
          this.$router.push("/ns/" + item.namespace + "/" + item.name);
        } else {
          this.$swal.fire("Oops!", "Action not available for this item");
        }
      }
    },
    getSubclass(parents) {
      if (parents) {
        let sub = parents[0].split(", ");
        return sub[sub.length - 1];
      } else {
        return "This class has no subclass";
      }
    },
  },
  computed: {
    imgLink: function () {
      switch (this.item["namespace"]) {
        case "schema":
          return "schema.png";
        case "niaid":
          return "niaid/icon.svg";
        case "outbreak":
          return "outbreak.png";
        case "bts":
          return "biothings-logo-xs.png";
        case "google":
          return "google.png";
        case "ctsa":
          return "dde-logo-o.svg";
        case "n3c":
          return "N3Co.png";
        default:
          return "dde-logo-o.svg";
      }
    },
    propTotal() {
      if (this.item.hasOwnProperty("properties")) {
        return this.item.properties.length;
      } else {
        return 0;
      }
    },
    propNames() {
      if (this.item.hasOwnProperty("properties")) {
        return this.item.properties.map((prop) => prop.label).join(", ");
      } else {
        return false;
      }
    },
  },
};
</script>

<style lang="css" module>
td {
  padding: 0 5px !important;
  vertical-align: middle !important;
}
</style>
