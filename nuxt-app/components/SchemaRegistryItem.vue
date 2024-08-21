<template>
  <li class="list-group-item p-0">
    <div class="d-flex flex-wrap">
      <div class="p-4 d-none d-md-inline">
        <input
          v-model="picked"
          @change="handlePick"
          class="tip m-auto slider"
          :data-tippy-content="
            maxReached
              ? 'Max Comparison Items Reached'
              : 'Choose For Comparison'
          "
          type="checkbox"
        />
        <font-awesome-icon
          v-if="adding"
          icon="fas fa-spinner"
          class="fa-pulse text-info ml-2"
        />
      </div>
      <div class="flex-grow-1 d-flex align-items-center">
        <div class="d-inline mr-1">
          <div class="mr-1 d-none d-md-inline"></div>
          <h6 class="m-1 mainTextDark d-inline">
            {{ item.label }}
          </h6>
        </div>
        <p class="m-0 text-muted d-none d-md-inline">
          <small class="pointer" @click="expand = !expand">
            <span :class="[propTotal > 0 ? 'text-primary' : 'text-muted']"
              ><span v-text="propTotal"></span> Properties</span
            >
            <template v-show="propTotal">
              <font-awesome-icon
                v-if="!expand"
                icon="fas fa-plus-square"
                class="text-success"
              />
              <font-awesome-icon
                v-else
                icon="fas fa-minus-square"
                class="text-danger"
              />
            </template>
          </small>
          |
          <small><font-awesome-icon icon="fas fa-home" />: </small>
          <small class="text-muted">
            <a v-text="item.namespace" :href="'/view/' + item.namespace"></a>
          </small>
          |
          <small>Subclass of:</small>
          <small class="mb-1" v-text="getSubclass(item.parent_classes)"></small>
          <img
            v-if="item && item.validation"
            src="@/assets/img/cube.svg"
            width="15"
            title="validation available"
            class="ml-1 tip"
            data-tippy-content="Validation available"
          />
        </p>
      </div>
      <div
        class="p-1 bg-dde-dark d-flex align-items-center justify-content-around"
      >
        <div>
          <button
            class="btn btn-sm btn-info m-1"
            @click.prevent="saveDataAndRedirect(item)"
            data-tippy-content="Visualize class in detail"
          >
            View
          </button>
        </div>
        <div>
          <button
            class="btn btn-sm bg-dde-light text-light m-1"
            @click.prevent="saveDataAndRedirect(item, 'editor')"
            data-tippy-content="Extend using this class as a subclass"
          >
            Extend
          </button>
        </div>
      </div>
      <div
        class="col-sm-12 alert alert-info d-flex flex-wrap m-0"
        v-if="expand"
      >
        <template v-for="(prop, i) in item.properties" :key="prop.label">
          <small
            class="mr-1"
            v-text="
              i + 1 < item.properties.length ? prop.label + ', ' : prop.label
            "
          ></small>
        </template>
      </div>
    </div>
  </li>
</template>

<script>
import axios from "axios";
import Notify from "simple-notify";

export default {
  name: "SchemaRegistryItem",
  data: function () {
    return {
      options: false,
      expand: false,
      picked: false,
      adding: false,
      itemID: Math.floor(Math.random() * 90000) + 10000,
    };
  },
  props: ["item"],
  methods: {
    saveDataAndRedirect(item, goesToEditor) {
      console.log(item, goesToEditor);
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
    getRandomColor() {
      var letters = "0123456789ABCDEF";
      var color = "#";
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    getFullInfo(item) {
      //add param v for verbose definition including all parents
      var self = this;
      self.adding = true;
      const runtimeConfig = useRuntimeConfig();
      axios
        .get(
          runtimeConfig.public.apiUrl +
            "/api/registry/" +
            item.namespace +
            "/" +
            item.name +
            "?v"
        )
        .then((res) => {
          let allProps = [];
          for (var i = 0; i < res.data["hits"].length; i++) {
            // keep item form but combine all props from parents and add
            let current = res.data["hits"][i];
            if (current.hasOwnProperty("properties")) {
              allProps = allProps.concat(current["properties"]);
            }
          }
          // console.log('All props for '+item.label+" are "+allProps.length)
          let sorted = self.$_.sortBy(allProps, [
            function (o) {
              return o.label;
            },
          ]);
          item["properties"] = sorted;
          item["color"] = self.getRandomColor();
          let payload = {};
          payload["item"] = item;
          self.$store.commit("addItem", payload);

          self.adding = false;
        })
        .catch((err) => {
          self.adding = false;
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
          });
          throw err;
        });
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
    maxReached() {
      return this.$store.getters.getMaxReached;
    },
  },
  watch: {
    picked: function (picked) {
      let self = this;
      let payload = {};
      payload["item"] = self.item;
      if (picked) {
        self.getFullInfo(self.item);
      } else {
        this.$store.commit("removeItem", payload);
      }
    },
  },
};
</script>
