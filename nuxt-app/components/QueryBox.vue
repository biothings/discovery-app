<template>
  <div class="p-3 mb-2 alert alert-light shadow">
    <div v-if="q && q.name">
      <a class="d-inline text-primary" :href="'/ns/' + q.name.split(':')[0]">
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
            <span
              :class="[
                index !== path.length - 1
                  ? 'text-dark'
                  : 'text-dde-mid font-weight-bold',
              ]"
              class="pointer"
              @click="goTo(item)"
              v-text="item"
            ></span>
            <span v-if="index !== path.length - 1"
              >&nbsp;<font-awesome-icon
                icon="fas fa-caret-right"
                class="text-dde-mid"
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
      <div
        class="resultsTabFull mt-3 p-3 text-light text-left"
        :class="backColor"
      >
        <h5 class="d-inline">
          <b class="mr-2" v-text="q.label"></b>
          <span class="text-warning">
            (<small
              v-if="q && q.properties"
              v-text="q.properties.length + ' properties'"
            >
            </small
            >)
          </span>
        </h5>
        <button
          @click="hide = !hide"
          style="border: 2px solid white"
          class="btn btn-sm text-light ml-5 themeButton"
          v-text="!hide ? 'Hide All' : 'Show All'"
        ></button>
        <button
          class="btn btn-sm themeButton text-light float-right"
          @click="exportToCSV(q?.properties)"
        >
          Export to CSV
        </button>
      </div>
      <table
        v-show="!hide"
        class="table mb-2 table-sm"
        :class="!parent ? 'table-striped table-light' : 'table-striped-main'"
      >
        <thead class="thead-dark">
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Expected Type</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-if="q && q.properties"
            v-for="(item, i) in reorderByLabel(q.properties)"
          >
            <td>
              <a class="font-weight-bold" :href="'./' + item.label">
                <span v-html="item.label"></span>
              </a>
            </td>
            <td
              class="text-dark"
              v-html="item.description || 'No description provided'"
            ></td>
            <td>
              <template v-for="(type, i) in item.range">
                <a
                  v-for="link in getLink(type)"
                  :href="link"
                  :key="link"
                  v-text="type"
                >
                </a>
                <span v-if="i !== item.range.length - 1">, </span>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div
      v-if="!q.properties && !validationView && !q.domain"
      class="jumbotron alert-primary d-flex justify-content-center align-items-center"
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
    <div
      v-if="validationView && !q.validation && !q.domain"
      class="jumbotron alert-primary d-flex justify-content-center align-items-center"
    >
      <div>
        <p class="m-4">This class does not define any validation rules.</p>
      </div>
    </div>
  </div>
</template>

<script>
import ValidationBox from "./ValidationBox.vue";
import { mapGetters, mapActions } from "vuex";
import Papa from "papaparse";

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
      hide: false,
    };
  },
  props: ["q", "userSchema", "parent"],
  methods: {
    ...mapActions(["toggleShowAll"]),
    exportToCSV(data) {
      let csv = Papa.unparse(data);
      // Create a blob from the CSV string
      let blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

      // Create a temporary link element to trigger the download
      let link = document.createElement("a");
      if (link.download !== undefined) {
        // Check if download attribute is supported
        let url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", this.q.label + ".csv"); // Set the desired file name
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link); // Clean up by removing the link
      }
    },
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
      if (string.includes(":")) {
        res = `/ns/${string.split(":")[0]}/${string}`;
      } else {
        res = "/ns/" + string;
      }
      console.log("Going to ", res);
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
    reorderByLabel(objects) {
      return objects.sort((a, b) => {
        // Ensure that both objects have a 'label' property before comparing
        if (a.label && b.label) {
          return a.label.localeCompare(b.label);
        }
        return 0;
      });
    },
  },
  mounted: function () {
    if (this.parent) {
      this.textColor = "text-dde-mid";
      this.backColor = "bg-dde-mid";
    } else {
      this.textColor = "text-dde-dark";
      this.backColor = "bg-dde-dark";
    }
  },
  computed: {
    ...mapGetters(["validationView", "showAll"]),
  },
  watch: {
    parent: {
      handler: function (v) {
        if (!v) {
          this.hide = false;
        } else {
          this.hide = true;
        }
      },
      immediate: true,
    },
  },
};
</script>
