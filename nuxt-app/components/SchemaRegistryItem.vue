<template>
  <li class="list-group-item p-0">
    <div class="d-flex flex-wrap">
      <div class="flex-grow-1 d-flex align-items-center">
        <div class="d-inline mr-1 ml-2">
          <template v-if="item.validation">
            <img
              src="@/assets/img/cube.svg"
              width="15"
              title="validation available"
              class="ml-1 tip"
              data-tippy-content="Validation available"
            />
          </template>
          <h6 class="m-1 mainTextDark d-inline">
            <small class="text-dde-dark">
              <NuxtLink :to="'/ns/' + item.namespace">{{
                item.namespace
              }}</NuxtLink
              >: </small
            ><b>{{ item.label }}</b>
          </h6>
        </div>
        <p v-if="propTotal" class="m-0 text-dde-dark d-none d-md-inline">
          <small class="text-info">
            <span :data-tippy-content="propNames">
              + <span v-text="propTotal"></span> Properties added</span
            >
          </small>
        </p>
        <small class="text-muted"
          >&nbsp; | Subclass of: {{ getSubclass(item.parent_classes) }}</small
        >
      </div>
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
    </div>
  </li>
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
