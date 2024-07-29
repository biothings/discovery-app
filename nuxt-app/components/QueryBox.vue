<template>
  <div class="p-3 mb-2 alert alert-light">
    <div v-if="q && q.name">
      <a class="d-inline text-info" :href="'/ns/' + q.name.split(':')[0]">
        <h3
          class="bold d-inline"
          :id="q.name"
          v-text="q.name.split(':')[0] + ':'"
        ></h3>
      </a>
      <h3
        class="bold d-inline"
        :class="textColor"
        :id="q.name"
        v-text="q.name.split(':')[1]"
      ></h3>
    </div>
    <div v-else-if="q && q.label">
      <h3
        class="bold d-inline"
        :class="textColor"
        :id="q.label"
        v-text="q.label.split(':')[0]"
      ></h3>
    </div>
    <template v-if="q && q.domain">
      <small class="text-dark">is a property of: </small>
      <template v-for="(item, index) in q.domain">
        <template v-for="link in getLink(item)">
          <RouterLink
            class="d-inline bold mr-1"
            :to="link"
            :class="[index !== q.domain.length - 1 ? 'text-dark' : textColor]"
          >
            <small>
              <span v-html="item"></span>
            </small>
          </RouterLink>
        </template>
      </template>
    </template>
    <template v-if="q.label && q.parent_classes">
      <ul style="list-style: none">
        <li v-for="path in getPaths(q)">
          <span v-for="(item, index) in path">
            <!-- <a
              :class="[index !== path.length - 1 ? 'text-dark' : textColor]"
              class="font-weight-bold"
              :href="getBreadcrumbLink(item)"
              v-text="item"
            ></a> -->
            <span
              :class="[index !== path.length - 1 ? 'text-dark' : textColor]"
              class="font-weight-bold pointer"
              @click="goTo(item)"
              v-text="item"
            ></span>
            <span v-if="index !== path.length - 1"
              >&nbsp;<font-awesome-icon
                icon="fas fa-caret-right"
                :class="textColor"
              />&nbsp;</span
            >
          </span>
        </li>
      </ul>
    </template>
    <p
      v-html="q['description'] || 'No Description Provided'"
      class="p-2 description"
      :class="textColor"
    ></p>
    <template v-if="q && q.range">
      <small class="text-dark"
        >Values expected to be one of these types:
      </small>
      <template v-for="(item, index) in q.range">
        <template v-for="link in getLink(item)">
          <RouterLink
            class="d-inline bold"
            :to="link"
            :class="[index !== q.domain.length - 1 ? 'text-dark' : textColor]"
          >
            <small>
              <span v-html="item"></span>
            </small>
            <font-awesome-icon
              icon="fas fa-external-link-alt"
              v-if="link[0] !== '.'"
            />
          </RouterLink>
        </template>
      </template>
    </template>
    <div v-if="q.properties && !validationView">
      <div class="resultsTabFull mt-3 p-3 text-light" :class="backColor">
        <h5 class="d-inline">
          <span v-text="q.label + ' has '"></span>
          <span class="badge badge-light" :class="textColor">
            <span
              v-if="q && q.properties"
              v-text="q.properties.length + ' properties'"
            >
            </span>
            <span v-else> </span>
          </span>
        </h5>
        <button
          v-if="q && q.properties.length"
          @click="toggleShowAll()"
          style="border: 2px solid white"
          class="btn text-light ml-5"
          :class="backColor"
          v-text="showAll ? 'Hide All' : 'Show All'"
        ></button>
      </div>
      <table
        v-show="showAll"
        class="table mb-2"
        :class="!parent ? 'table-striped-sec' : 'table-striped-main'"
      >
        <tbody>
          <tr v-if="q && q.properties" v-for="(item, i) in q.properties">
            <td>
              <a class="font-weight-bold" :href="'./' + item.label">
                <span v-html="item.label"></span>
              </a>
              <p>
                <span
                  class="text-dark"
                  v-html="item.description || 'No description provided'"
                ></span>
              </p>
            </td>
            <td>
              <small class="mainTextDark bold">Expected Type: </small>
              <template v-for="(type, i) in item.range">
                <a v-for="link in getLink(type)" :href="link" :key="link">
                  <small>
                    <span v-html="type"></span>
                  </small>
                </a>
                <span v-if="i !== item.range.length - 1">, </span>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div
      v-if="!q.properties && !validationView"
      class="jumbotron d-flex justify-content-center align-items-center"
    >
      <div>
        <p class="m-4">
          This class does not define any new properties, instead all of its
          properties are directly inherited from it's subclasses.
        </p>
      </div>
    </div>
    <div v-if="validationView && q.validation">
      <ValidationBox :validation="q.validation"></ValidationBox>
    </div>
  </div>
</template>

<script>
import ValidationBox from "./ValidationBox.vue";
import { mapGetters, mapActions } from "vuex";
import Notify from "simple-notify";

export default {
  name: "QueryBox",
  components: {
    ValidationBox,
  },
  data: function () {
    return {
      textColor: "",
      backColor: "",
      properties: [],
    };
  },
  props: ["q", "userSchema", "parent"],
  methods: {
    ...mapActions(["toggleShowAll"]),
    getPaths(classInfo) {
      // console.log('getting all possible paths...')
      let res = [];
      for (var i = 0; i < classInfo["parent_classes"].length; i++) {
        if (classInfo["parent_classes"][i]) {
          let parents = classInfo["parent_classes"][i].split(", ");
          parents.push(classInfo.name);
          res.push(parents);
        }
      }
      return res;
    },
    getPropertiesFor(classInfo) {
      // console.log('getting props for ', classInfo.name);
      if (
        classInfo.hasOwnProperty("properties") &&
        classInfo["properties"].length > 0
      ) {
        return classInfo["properties"];
        // console.log('returning ', classInfo['properties']);
      } else {
        return ["This class has no properties of its own"];
      }
    },
    getType: function (data) {
      let types = [];
      if (data.hasOwnProperty("schema:rangeIncludes")) {
        if (this.$_.isString(data["schema:rangeIncludes"])) {
          let type = data["schema:rangeIncludes"].split(":");
          type = type[type.length - 1];
          types.push(type);
        } else if (this.$_.isArray(data["schema:rangeIncludes"])) {
          for (var i = 0; i < data["schema:rangeIncludes"].length; i++) {
            let type = data["schema:rangeIncludes"][i]["@id"].split(":");
            type = type[type.length - 1];
            types.push(type);
          }
        } else if (this.$_.isObject(data["schema:rangeIncludes"])) {
          let type = data["schema:rangeIncludes"]["@id"].split(":");
          type = type[type.length - 1];
          types.push(type);
        }
      }
      return types;
    },
    getName(string) {
      let res = "";
      if (string.includes("http")) {
        let arr = string.split("/");
        res = arr[arr.length - 1];
      } else if (string.includes(":")) {
        let arr = string.split(":");
        res = arr[arr.length - 1];
      } else {
        res = string;
      }
      return res;
    },
    getBreadcrumbLink(string) {
      let res = "";
      let arr = [];
      if (string.includes(":")) {
        arr = string.split(":");
        let name = arr[arr.length - 1];
        arr["0"] == "schema"
          ? (res += "/ns/schema/" + name)
          : (res += "./" + name);
      } else {
        res = string;
      }
      return res;
    },
    goTo(string) {
      let res = "";
      let arr = [];
      if (string.includes(":")) {
        arr = string.split(":");
        if (arr[0] == "schema") {
          new Notify({
            status: "warning",
            title: "Navigation Unavailable",
            text: "This class cannot be navigated to directly. Taking you to its homepage.",
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
          this.$router.push("/ns/schema");
          return;
        }
        res = `/ns/${arr[0]}/${arr[arr.length - 1]}`;
      } else {
        res = string;
      }
      this.$router.push(res);
    },
    getLink(qName) {
      // console.log('getLink', qName)
      try {
        let link = [store.getters.handleLink(qName)];
        return link;
      } catch (e) {
        if (qName.includes(":")) {
          return ["/ns/" + qName.split(":")[0] + "/" + qName];
        } else {
          return false;
        }
      }
    },
  },
  mounted: function () {
    if (this.parent) {
      this.textColor = "mainTextLight";
      this.backColor = "mainBackLight";
    } else {
      this.textColor = "mainTextDark";
      this.backColor = "mainBackDark";
    }
  },
  computed: {
    ...mapGetters(["validationView", "showAll"]),
  },
};
</script>
