<template>
  <div id="registry" class="jumbotron" style="min-height: 80vh">
    <div class="col-md-10 col-sm-12 m-auto p-0">
      <div class="">
        <h1 class="text-center logoText mb-1 mt-2">
          <span v-if="N3CView">N3C</span> Resource Registry
        </h1>
        <p class="text-center text-muted" v-if="N3CView">
          For more general information about PPRL datasets, such as what this
          data is, and how to participate, please visit our
          <router-link to="/faq/n3c">PPRL FAQ</router-link>
        </p>
        <div>
          <form @submit.prevent="search(query)">
            <div class="row m-0 cBox actions bg-secondary">
              <div class="col-sm-10 p-2">
                <div class="">
                  <input
                    class="form-control col-12"
                    id="search_query"
                    type="text"
                    v-model="query"
                    name="query"
                    placeholder="Search..."
                  />
                </div>
              </div>
              <div
                class="col-sm-2 p-2 bg-dark actions d-flex align-items-center justify-content-around"
              >
                <span
                  data-tippy-content="search"
                  class="fa-stack fa-1x pointer unselectable tip"
                  @click.prevent="search()"
                >
                  <font-awesome-icon
                    icon="fas fa-circle"
                    class="text-muted fa-stack-2x"
                  />
                  <font-awesome-icon
                    icon="fas fa-search"
                    class="fa-stack-1x text-light"
                  />
                </span>
                <span
                  data-tippy-content="reset"
                  class="fa-stack fa-1x pointer unselectable tip"
                  @click.prevent="
                    query = '';
                    search();
                  "
                >
                  <font-awesome-icon
                    icon="fas fa-circle"
                    class="text-muted fa-stack-2x"
                  />
                  <font-awesome-icon
                    icon="fas fa-undo"
                    class="fa-stack-1x text-light"
                  />
                </span>
              </div>
            </div>
          </form>
        </div>
        <div class="alert-dark m-0 p-1" v-if="!N3CView">
          <div style="width: 120px" class="text-muted d-inline-block">
            <small>Portals</small>
          </div>
          <template
            v-for="filter in all_filters['_meta.guide']"
            :key="filter.name"
          >
            <span
              class="badge pointer m-1 fade-in"
              @click="toggleFilter(filter)"
              :class="[filter.active ? 'btn-info' : 'btn-secondary']"
            >
              <DynamicImage
                :imagePath="filter.icon"
                :id="filter.name"
                :alt="filter.name"
                width="20"
                class="mr-2"
              ></DynamicImage>
              <span v-text="filter.name" class="gaText"></span>
            </span>
          </template>
        </div>
        <!-- ONLY VISIBLE FOR N3C -->
        <template v-if="N3CView">
          <div class="alert-dark m-0 p-1">
            <div style="width: 120px" class="text-muted d-inline-block">
              <small>Submission Status</small>
            </div>
            <template
              v-for="filter in all_filters['_n3c.status']"
              :key="filter.term"
            >
              <span
                class="badge pointer m-1 fade-in"
                @click="toggleFilter(filter)"
                :class="[filter.active ? 'btn-info' : 'btn-secondary']"
              >
                <font-awesome-icon
                  icon="fas fa-circle"
                  :class="filter.color"
                  class="mr-1"
                />
                <span v-text="filter.name"></span> (<span
                  v-text="filter.count"
                ></span
                >)
              </span>
            </template>
          </div>
          <div class="alert-dark m-0 p-1">
            <div style="width: 120px" class="text-muted d-inline-block">
              <small>Dataset Type</small>
            </div>
            <template v-for="filter in all_filters['name']" :key="filter.name">
              <span
                class="badge pointer m-1 fade-in"
                @click="toggleFilter(filter)"
                :class="[filter.active ? 'btn-info' : 'btn-secondary']"
                :title="filter.tip"
              >
                <a
                  v-if="filter && filter.link"
                  class="ml-1"
                  :href="filter.link"
                  target="_blank"
                  title="Learn more"
                >
                  <font-awesome-icon
                    icon="fas fa-circle"
                    class="text-primary"
                  />
                </a>
                <font-awesome-icon
                  v-else
                  icon="fas fa-circle"
                  :class="filter.color"
                />
                <span v-text="filter.name" class="gaText ml-3 mr-3"></span>
              </span>
            </template>
          </div>
        </template>
        <div class="text-right d-none d-md-block">
          <label class="text-muted mr-2" for="exampleFormControlSelect1"
            ><small>Order</small></label
          >
          <select
            class="form-control form-control-sm w-25 float-right"
            id="exampleFormControlSelect1"
            @change="search()"
            v-model="sortChange"
          >
            <option>Choose one</option>
            <option value="A-Z">Alphabetically A-Z</option>
            <option value="Z-A">Alphabetically Z-A</option>
            <option value="recent">Recently Updated</option>
          </select>
        </div>
        <div class="d-flex justify-content-start align-items-center">
          <!-- Download -->
          <input
            type="checkbox"
            class="form-control slider mr-2"
            id="download_metadata"
            name="download_metadata"
            v-model="downloadMode"
            @click="toggleDownloadMode"
          />
          <label
            for="download_metadata"
            class="m-0 tip"
            data-tippy-content="Select registry items for download"
            >Download Mode
            <b
              :class="{ 'text-success': downloadMode }"
              v-text="downloadMode ? 'ON' : ''"
            ></b
          ></label>
          <small v-if="downloadMode" class="bold text-secondary ml-2"
            >Select items to download/ Toggle off to clear</small
          >
          <button
            @click="handleDownload()"
            class="btn ml-3 btn-sm btn-success text-light"
            v-if="downloadList.length"
            v-text="'Download (' + downloadList.length + ') items'"
          ></button>
        </div>
        <div
          v-if="total"
          class="mt-0 p-1 bg-secondary text-light text-center col-sm-12 col-md-3"
          v-text="total + ' Results'"
        ></div>
        <ul
          class="list-group context"
          style="border-top: solid 3px var(--main)"
          id="regTippyParent"
        >
          <li
            class="list-group-item d-flex justify-content-center align-items-center text-muted p-1"
            style="background: #d0d0d0"
          >
            <small v-if="hits.length && query" v-text="'results for ' + query">
            </small>
          </li>
          <template v-if="hits.length" v-for="item in hits" :key="item._id">
            <ResourceRegistryItem :item="item"></ResourceRegistryItem>
          </template>
          <li
            v-if="!hits.length"
            class="text-center text-muted list-group-item"
          >
            <div class="jumbotron">
              <h4>Search for existing datasets</h4>
            </div>
          </li>
        </ul>
        <div>
          <select
            class="form-control form-control-sm m-auto w-25"
            v-model="perPage"
            @change="
              calculatePages();
              search();
            "
            id="perPage"
          >
            <option value="" disabled selected>Shown Per Page</option>
            <option value="10">10 per page</option>
            <option value="25">25 per page</option>
            <option value="100">100 per page</option>
          </select>
          <div class="d-flex flex-wrap justify-content-center p-1 mt-2">
            <div class="page-item rounded-0" :class="{ disabled: page <= 1 }">
              <a
                class="page-link p-1"
                @click.prevent="
                  prevPage();
                  search();
                "
                ><font-awesome-icon icon="fas fa-step-backward"
              /></a>
            </div>
            <template v-if="groupPages">
              <div class="page-item rounded-0" v-show="!startCapLimitReached">
                <a
                  href="javascript:void(0)"
                  class="page-link p-1"
                  @click.prevent="
                    previousGroup();
                    search();
                  "
                  >Previous 20</a
                >
              </div>
            </template>
            <template v-for="n in pages">
              <div
                v-if="n >= startCap && n <= endCap"
                class="page-item rounded-0"
                :class="{
                  active: page == n,
                  'bg-primary': page == n,
                  'white-text': page == n,
                }"
              >
                <a
                  href="javascript:void(0)"
                  class="page-link p-1"
                  @click.prevent="
                    page = n;
                    search();
                  "
                  v-text="n"
                ></a>
              </div>
            </template>
            <template v-if="groupPages">
              <div class="page-item rounded-0" v-show="!endCapLimitReached">
                <a
                  href="javascript:void(0)"
                  class="page-link p-1"
                  @click.prevent="
                    nextGroup();
                    search();
                  "
                  >Next 20</a
                >
              </div>
            </template>
            <div
              class="page-item rounded-0"
              :class="{ disabled: page >= pages }"
            >
              <a
                class="page-link p-1"
                @click.prevent="
                  nextPage();
                  search();
                "
                ><font-awesome-icon icon="fas fa-step-forward"
              /></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Mark from "mark.js";
import Papa from "papaparse";

import { mapGetters } from "vuex";

import ResourceRegistryItem from "~~/components/ResourceRegistryItem.vue";
import DynamicImage from "~~/components/DynamicImage.vue";

export default {
  name: "ResourceRegistry",
  data: function () {
    return {
      perPage: 10,
      finalQ: "",
      page: 1,
      pages: 1,
      startCap: 0,
      endCap: 20,
      groupPages: false,
      pageLimit: 20,
      startCapLimitReached: true,
      endCapLimitReached: false,
      total: Number,
      apiUrl: '',
      registry_api_url: "/api/dataset/query?",
      hits: [],
      query: "",
      sortChange: "recent",
      highlighter: null,
      // key is the direct field to be filtered by
      //value is the final val set to ES
      all_filters: {
        "_meta.guide": [
          {
            name: "N3C:Dataset",
            value: "/guide/n3c/dataset",
            active: false,
            icon: "N3Co.png",
            type: "_meta.guide",
          },
          {
            name: "Outbreak:Dataset",
            value: "/guide/outbreak/dataset",
            active: false,
            icon: "icon-01.svg",
            type: "_meta.guide",
          },
          {
            name: "NIAID:Dataset",
            value: "/guide/niaid",
            active: false,
            icon: "niaid/icon.svg",
            type: "_meta.guide",
          },
          {
            name: "NIAID:ComputationalTool",
            value: "/guide/niaid/ComputationalTool",
            active: false,
            icon: "niaid/icon.svg",
            type: "_meta.guide",
          },
          {
            name: "CD2H:Dataset",
            value: "/guide",
            active: false,
            icon: "dde-logo-o.svg",
            type: "_meta.guide",
          },
        ],
        name: [
          {
            name: "IRB Required",
            value: "PPRL",
            active: false,
            icon: "N3Co.png",
            type: "name",
            tip: "Institutional Review Board Required",
            link: "https://covid.cd2h.org/PPRL",
          },
        ],
      },
      N3CView: false,
    };
  },
  components: {
    ResourceRegistryItem,
    DynamicImage,
  },
  methods: {
    toggleDownloadMode() {
      this.$store.commit("toggleDownloadMode");
    },
    handleDownload() {
      var self = this;
      self.$swal
        .fire({
          title: "Download Metadata",
          text: "Select the desired output of the metadata selected",
          input: "select",
          inputOptions: {
            json: "JSON",
            csv: "CSV",
          },
          footer: "Note: Documents will be flattened for CSV file.",
          inputPlaceholder: "Select Output",
          showCancelButton: true,
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          customClass: "scale-in-center",
          confirmButtonText: "Next",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (result.value) {
            switch (result.value) {
              case "json":
                self.downloadJSON();
                break;
              case "csv":
                self.downloadCSV();
                break;
              default:
                return false;
            }
          }
        });
    },
    flatten(target, opts) {
      function isBuffer(obj) {
        return (
          obj &&
          obj.constructor &&
          typeof obj.constructor.isBuffer === "function" &&
          obj.constructor.isBuffer(obj)
        );
      }

      function keyIdentity(key) {
        return key;
      }
      opts = opts || {};

      const delimiter = opts.delimiter || ".";
      const maxDepth = opts.maxDepth;
      const transformKey = opts.transformKey || keyIdentity;
      const output = {};

      function step(object, prev, currentDepth) {
        currentDepth = currentDepth || 1;
        Object.keys(object).forEach(function (key) {
          const value = object[key];
          const isarray = opts.safe && Array.isArray(value);
          const type = Object.prototype.toString.call(value);
          const isbuffer = isBuffer(value);
          const isobject =
            type === "[object Object]" || type === "[object Array]";

          const newKey = prev
            ? prev + delimiter + transformKey(key)
            : transformKey(key);

          if (
            !isarray &&
            !isbuffer &&
            isobject &&
            Object.keys(value).length &&
            (!opts.maxDepth || currentDepth < maxDepth)
          ) {
            return step(value, newKey, currentDepth + 1);
          }

          output[newKey] = value;
        });
      }

      step(target);

      return output;
    },
    downloadCSV() {
      let self = this;
      self.$swal
        .fire({
          title: "Name your file",
          input: "text",
          customClass: "scale-in-center",
          footer: "Note: First row is column names.",
          inputAttributes: {
            autocapitalize: "off",
          },
          showCancelButton: true,
          confirmButtonText: "Download CSV",
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (result.value) {
            let docs = [];
            let string = "";
            string = self.downloadList
              .map((id) => {
                return (string += `(_id:"${id}")`);
              })
              .join(" OR ");

            axios
              .get(self.apiUrl + "/api/dataset/query?q=" + string)
              .then(function (response) {
                docs = response.data.hits;
                docs = docs.map((doc) => {
                  delete doc._meta;
                  delete doc._ts;
                  delete doc._score;
                  return doc;
                });
                docs = docs.map(self.flatten);
                console.log(docs);
                let csv = Papa.unparse(docs, {
                  header: true,
                  delimiter: ",",
                });
                self.download(csv, result.value + ".csv", "text/plain");
              })
              .catch((err) => {
                $.notify("Failed to download items", {
                  globalPosition: "right",
                  style: "danger",
                  showDuration: 40,
                });
                throw err;
              });
          }
        });
    },
    downloadJSON() {
      let self = this;
      self.$swal
        .fire({
          title: "Name your file",
          input: "text",
          customClass: "scale-in-center",
          inputAttributes: {
            autocapitalize: "off",
          },
          showCancelButton: true,
          confirmButtonText: "Download JSON",
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
        })
        .then((result) => {
          if (result.value) {
            let docs = [];
            let string = "";
            string = self.downloadList
              .map((id) => {
                return (string += `(_id:"${id}")`);
              })
              .join(" OR ");

            axios
              .get(self.apiUrl + "/api/dataset/query?q=" + string)
              .then(function (response) {
                docs = response.data.hits;
                docs = docs.map((doc) => {
                  delete doc._meta;
                  delete doc._ts;
                  delete doc._score;
                  return doc;
                });
                self.download(
                  JSON.stringify(docs, null, 2),
                  result.value + ".json",
                  "text/plain"
                );
              })
              .catch((err) => {
                $.notify("Failed to download items", {
                  globalPosition: "right",
                  style: "danger",
                  showDuration: 40,
                });
                throw err;
              });
          }
        });
    },
    download(content, fileName, contentType) {
      var a = document.createElement("a");
      var file = new Blob([content], { type: contentType });
      a.href = URL.createObjectURL(file);
      a.download = fileName;
      a.click();
    },
    mark: function (keyword) {
      this.highlighter.unmark();
      this.highlighter.mark(keyword);
    },
    sendGAEvent(type, query) {
      this.$gtag.event("click", {
        event_category: type,
        event_label: query,
        event_value: 1,
      });
    },
    getStatusTextColor(s) {
      switch (s) {
        case "Available":
          return "text-success";
        case "Denied":
          return "text-danger";
        case "Approved for Import":
          return "text-purple";
        case "Pending Review":
          return "text-info";
        default:
          return "text-dark";
      }
    },
    aggregate(field) {
      let self = this;
      axios
        .get(self.apiUrl + `/api/dataset/query?aggs=${field}`)
        .then((response) => {
          //a.term and a.count
          let res = response.data?.facets?.[field]?.terms || [];
          let complete = res.map((item) => {
            item.active = false;
            item.value = item.term;
            item.name = item.term;
            item.color = self.getStatusTextColor(item.name);
            item.type = field;
            return item;
          });
          self.all_filters[field] = complete;
          // console.log('%c AGGS', 'color:limegreen')
          // console.log('AGGS', self.all_filters)
        })
        .catch((err) => {
          throw err;
        });
    },
    toggleFilter(item) {
      let self = this;
      self.all_filters[item.type].forEach((gf) => {
        if (gf.value == item.value) {
          gf.active = !gf.active;
          console.log(gf);
          if (gf.name.includes("N3C") && gf.active == true) {
            self.N3CView = true;
          }
        }
        if (gf.active) {
          self.sendGAEvent("dataset_portal_filter", item.value);
        }
      });
      this.buildURL();
      this.search();
    },
    buildURL() {
      // match url to search filters
      let url = new URL(window.location.href);
      let active_list = [];
      let pprl_active = [];

      url.searchParams.delete("guide");
      url.searchParams.delete("dataset_type");

      this.all_filters["_meta.guide"].forEach((item) => {
        if (item.active) {
          active_list.push(item.value);
        }
      });

      this.all_filters["name"].forEach((item) => {
        if (item.active) {
          pprl_active.push(item.value);
        }
      });

      if (active_list.length) {
        url = url + "?guide=" + active_list.toString();
      }
      if (pprl_active.length) {
        if (active_list.length) {
          url = url + "&dataset_type=" + pprl_active.toString();
        } else {
          url = url + "?dataset_type=" + pprl_active.toString();
        }
      }
      window.history.pushState({ html: "content", pageTitle: "DDE" }, "", url);
    },
    getFilters() {
      let self = this;
      let filters = {};

      for (const key in self.all_filters) {
        filters[key] = [];
        self.all_filters[key].forEach((item) => {
          if (item.active) {
            filters[key].push('"' + item.value + '"');
          }
        });
      }
      return filters;
    },
    search() {
      let self = this;
      let url = self.apiUrl + self.registry_api_url;
      self.$store.commit("setLoading", { value: true });
      self.hits = [];
      self.total = 0;

      self.highlighter.unmark();
      //query analytics
      if (self.query !== "__all__") {
        self.sendGAEvent("dataset_search", self.query);
        self.finalQ = self.query;
      }
      //look for existing active filters and
      let filters = self.getFilters();
      //prep active filters found to be added
      let f_list = [];
      Object.keys(filters).forEach((field) => {
        //if multiple possible values add OR
        let val = filters[field].toString().includes(",")
          ? "(" + filters[field].join(" OR ") + ")"
          : filters[field];
        filters[field] && filters[field].length
          ? f_list.push(field + ":" + val)
          : false;
      });
      //add AND condition if multiple filters
      let field_query = f_list.join(" AND ");

      //pagination
      var config = {
        params: {
          size: self.perPage,
          from: self.page == 1 ? self.page - 1 : (self.page - 1) * self.perPage,
        },
      };
      if (self.query) {
        url += "q=" + self.query;
      } else {
        url += "q=" + "__all__";
      }

      if (field_query) {
        url += " AND " + field_query;
        //remove __all__ as it makes fielded query fail
        if (url.includes("__all__")) {
          url = url.replace("__all__ AND ", "");
        }
      }
      // sorting
      switch (self.sortChange) {
        case "relevance":
          //default behavior
          break;
        case "A-Z":
          config.params.sort = "name.raw";
          break;
        case "Z-A":
          config.params.sort = "-name.raw";
          break;
        case "recent":
          config.params.sort = "-_ts.last_updated";
          break;
        default:
          //no matching sort
          break;
      }

      axios
        .get(url, config)
        .then(function (response) {
          self.hits = response.data.hits;
          console.log("%c Query executed", "color:hotpink");
          console.log("%c " + JSON.stringify(config, null, 2), "color:blue");
          console.log("%c hits: " + response.data.total, "color:limegreen");
          self.$store.commit("setLoading", { value: false });
          self.total = response.data.total;
          self.calculatePages();
        })
        .catch((err) => {
          self.$store.commit("setLoading", { value: false });
          throw err;
        });
    },
    calculatePages: function () {
      var self = this;
      self.pages = Math.ceil(this.total / self.perPage);

      if (self.pages > self.pageLimit) {
        self.groupPages = true;
      }
    },
    previousGroup: function () {
      var self = this;

      if (!self.startCapLimitReached) {
        if (self.startCap - 20 > 0) {
          self.page = self.startCap - 20;
          self.startCap = self.startCap - 20;
          self.endCap = self.endCap - 20;
          self.endCapLimitReached = false;
        } else {
          self.page = 1;
          self.startCap = 0;
          self.endCap = 20;
          self.startCapLimitReached = true;
          self.endCapLimitReached = false;
        }
      }
    },
    nextGroup: function () {
      var self = this;

      if (!self.endCapLimitReached) {
        if (self.endCap + 20 < self.pages) {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.endCap + 20;
          self.startCapLimitReached = false;
        } else {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.pages;
          self.endCapLimitReached = true;
          self.startCapLimitReached = false;
        }
      }
    },
    prevPage: function () {
      var self = this;
      if (self.page > 1) self.page -= 1;
    },
    nextPage: function () {
      var self = this;
      if (self.page < self.pages) self.page += 1;
    },
    checkURLQuery() {
      let url_string = window.location.href;
      let url = new URL(url_string);

      let q = url.searchParams.get("q");
      if (q) {
        this.query = q;
      }
      this.searchForFilterAndToggle(url, "guide", "_meta.guide");
      this.searchForFilterAndToggle(url, "dataset_type", "name");
    },
    searchForFilterAndToggle(url, param, filter_name) {
      let self = this;
      let items = url.searchParams.get(param);
      let item_paths = [];

      if (items) {
        if (items.includes(",")) {
          items = items.split(",");
        } else {
          items = [items];
        }
        // console.log('items found',items)
        for (var i = 0; i < items.length; i++) {
          let item_url = items[i];
          item_paths.push(item_url);
        }
        if (item_paths.length) {
          item_paths.forEach((item) => {
            let obj = {};
            obj.type = filter_name;
            obj.value = item;
            self.toggleFilter(obj);
          });
        }
      }
    },
  },
  watch: {
    downloadMode: function (v) {
      if (!v) {
        this.$store.commit("clearDownloadList");
      }
    },
    finalQ: function (v) {
      this.$router.push({ name: "ResourceRegistry", query: { q: v } });
    },
  },
  computed: {
    ...mapGetters(["loading", "downloadList"]),
    downloadMode: {
      get() {
        return this.$store.getters.downloadMode;
      },
      set(v) {
        this.$store.commit("setDownloadMode", { value: v });
      },
    },
  },
  mounted: function () {
    console.log('registry mounted')
    const runtimeConfig = useRuntimeConfig()
    this.apiUrl = runtimeConfig.public.apiUrl;
    this.highlighter = new Mark(document.querySelector(".context"));
    this.checkURLQuery();
    this.search();
    this.aggregate("_n3c.status");
    window.onpopstate = () => {
      this.search();
    };
  },
  updated: function () {
    // Highlight matches in results
    this.mark(this.query);
  },
};
</script>
