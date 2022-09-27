<template>
  <div id="registry" class="jumbotron bg-white" style="min-height: 80vh">
    <div class="container">
      <div>
        <h1 class="text-center logoText mb-1 mt-2">Schema Registry</h1>
        <ul class="nav nav-tabs" id="myTab" role="tablist">
          <li class="nav-item" role="presentation">
            <nuxt-link
              class="nav-link"
              :class="{ 'bg-dark text-light': choice == 'classes' }"
              to="/registry?search=classes"
              >Search By Class Name</nuxt-link
            >
          </li>
          <li class="nav-item" role="presentation" @click="getNameSpaces()">
            <nuxt-link
              class="nav-link"
              :class="{ 'bg-dark text-light': choice == 'namespaces' }"
              to="/registry?search=namespaces"
              >Browse By Namespace</nuxt-link
            >
          </li>
        </ul>
        <div class="tab-content p-0 m-0" id="myTabContent">
          <!-- 🌈  CLASS SEARCH 🌈 -->
          <div v-if="choice == 'classes'">
            <div class="p-2 alert-secondary">
              <div class="alert alert-light jumbotron">
                <h2 class="logoText">Classes</h2>
                <p>
                  Visualize (<font-awesome-icon
                    icon="fas fa-eye"
                    class="text-info"
                  />), extend (<font-awesome-icon
                    icon="fas fa-code-branch"
                    class="mainTextLight"
                  />) and compare (<font-awesome-icon
                    icon="fas fa-not-equal"
                    class="mainTextDark"
                  />) available schema classes.
                </p>
              </div>
              <div>
                <form @submit.prevent="search()">
                  <div class="row m-0 cBox actions bg-secondary rounded">
                    <div class="col-sm-9 p-2">
                      <div class="d-flex align-item-center">
                        <div
                          class="d-flex align-item-center justify-content-center"
                        >
                          <small
                            class="text-light px-2"
                            v-text="total + ' Results'"
                          ></small>
                        </div>
                        <input
                          class="form-control col-10"
                          id="search_query"
                          type="text"
                          v-model="query"
                          name="query"
                          placeholder="Search..."
                        />
                      </div>
                    </div>
                    <div
                      class="col-sm-3 p-2 bg-dark actions d-flex align-items-center justify-content-around"
                    >
                      <span
                        class="fa-stack fa-1x pointer unselectable tip"
                        data-tippy-content="Search"
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
                        class="fa-stack fa-1x pointer tip unselectable"
                        data-tippy-content="Reset"
                        @click.prevent="
                          query = '';
                          search();
                        "
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="text-danger fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-undo"
                          class="fa-stack-1x text-light"
                        />
                      </span>
                      <span
                        class="fa-stack fa-1x pointer unselectable tip"
                        data-tippy-content="Compare Schemas"
                        @click="openModal()"
                      >
                        <font-awesome-icon
                          icon="fas fa-circle"
                          class="mainTextDark fa-stack-2x"
                        />
                        <font-awesome-icon
                          icon="fas fa-not-equal"
                          class="fa-stack-1x text-light"
                        />
                      </span>
                    </div>
                  </div>
                </form>
              </div>
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
                  <option value="relevance">Relevance</option>
                  <option value="A-Z">Alphabetically A-Z</option>
                  <option value="Z-A">Alphabetically Z-A</option>
                </select>
              </div>
              <div
                class="d-flex align-item-center justify-content-between px-3 text-muted"
              >
                <small>Compare (Max 4)</small>
                <small
                  >Details |
                  <img src="@/assets/img/cube.svg" width="15" /> (validation
                  available)</small
                >
                <small>View/Extend</small>
              </div>
              <ul class="list-group context" id="regTippyParent">
                <template
                  v-if="registry.length"
                  v-for="item in registry"
                  :key="item._id"
                >
                  <SchemaRegistryItem :item="item"></SchemaRegistryItem>
                </template>
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
                  <div
                    class="page-item rounded-0"
                    :class="{ disabled: page <= 1 }"
                  >
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
                    <div
                      class="page-item rounded-0"
                      v-show="!startCapLimitReached"
                    >
                      <a
                        href="#"
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
                        href="#"
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
                    <div
                      class="page-item rounded-0"
                      v-show="!endCapLimitReached"
                    >
                      <a
                        href="#"
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
          <!-- 🌈  NAMESPACE 🌈 -->
          <div v-if="choice == 'namespaces'">
            <div class="p-2 alert-dark">
              <div class="alert alert-light jumbotron">
                <h2 class="logoText">Namespaces</h2>
                <p>
                  Browse registered namespaces and view their available schema
                  classes and properties.
                </p>
              </div>
              <ul
                class="pagination overflow-x-scroll mt-3"
                v-show="classesGroupByLetter.length > 5"
              >
                <li
                  class="page-link"
                  v-for="(item, i) in classesGroupByLetter"
                  :key="i + 'sm'"
                >
                  <a :href="'#' + item.group" v-text="item.group"></a>
                </li>
              </ul>
              <div style="overflow-y: scroll; max-height: 600px">
                <ul class="list-group mt-3" v-if="classesGroupByLetter">
                  <li
                    class="list-group-item list-group-item-action"
                    v-for="(item, i) in classesGroupByLetter"
                    :key="i + 'letter'"
                  >
                    <h3
                      :id="item.group"
                      class="text-dark"
                      v-text="item.group"
                      v-show="classesGroupByLetter.length > 5"
                    ></h3>
                    <ul style="list-style: none">
                      <li v-for="def in item.children">
                        <router-link :to="{ path: '/view/' + def }">
                          <span v-text="def"></span>
                          <font-awesome-icon icon="fas fa-chevron-right" />
                        </router-link>
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- compareResults -->
    <div id="compareResults" class="modal" style="z-index: 1000">
      <!-- Modal content -->
      <div class="modal-content">
        <div>
          <span id="closeBtn" class="close">&times;</span>
        </div>
        <div>
          <h5 class="text-center logoText">Compare Schemas</h5>
        </div>
        <div
          class="d-flex justify-content-center p-2"
          v-if="compareItems.length > 1"
        >
          <div class="w-50 border-right p-1 text-muted text-center">
            <h6 class="mainTextLight">
              Compare All Properties (Extended and Inherited)
            </h6>
            <small class="d-block"
              ><font-awesome-icon
                icon="fas fa-dot-circle"
                class="text-danger"
              />
              Inherited from Schema.org</small
            >
            <small class="d-block"
              ><font-awesome-icon icon="fas fa-circle" class="text-info" />
              Extended Definition</small
            >
            <button
              @click="compareAll()"
              class="btn mainBackLight text-light m-auto"
            >
              <font-awesome-icon icon="fas fa-list-ul" /> Compare All
            </button>
          </div>
          <div class="w-50 border-left p-1 text-muted text-center">
            <h6 class="mainTextDark">
              Compare Used Properties By Schema (If Specified)
            </h6>
            <small class="d-block"
              >Only properties used as specified in validation</small
            >
            <small v-if="!compareUsedAvailable" class="text-danger d-block"
              >Not available: One or more of these items do no specify used
              properties. ( <span class="badge badge-success">V</span> )</small
            >
            <small v-else class="d-block"
              >(embedded JSON-schema validation)</small
            >
            <button
              :disabled="!compareUsedAvailable"
              @click="compareUsed()"
              class="btn mainBackDark text-light m-auto"
            >
              <font-awesome-icon icon="fas fa-tasks" /> Compare Used
            </button>
          </div>
        </div>
        <p v-else class="text-center text-muted alert alert-light p-2 mt-2">
          <font-awesome-icon
            icon="fas fa-exclamation-circle"
            class="text-danger"
          />
          Please select at least 2 items to compare. <br />Select any items to
          compare ALL properties or items with validation available (
          <small class="badge badge-success">V</small> ) to compare USED
          properties only.
        </p>
        <div>
          <small class="text-muted">
            <b v-text="results.length"></b> properties were compared
          </small>
        </div>
        <div id="example-table"></div>
        <div
          v-if="compareItems.length > 1"
          class="p-1 alert-secondary text-center"
        >
          <a id="downloadCSV" href="#" class="text-muted">
            <small
              ><font-awesome-icon icon="fas fa-file-download" /> Download
              CSV</small
            >
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Mark from "mark.js";
import axios from "axios";
import { orderBy } from "lodash";
import { mapGetters } from "vuex";
import SchemaRegistryItem from "~~/components/SchemaRegistryItem.vue";

export default {
  name: "SchemaRegistry",
  components: {
    SchemaRegistryItem,
  },
  computed: {
    compareItems: function () {
      return this.$store.getters.getCompareItems;
    },
    results: function () {
      return this.$store.getters.getResults;
    },
    compareUsedAvailable: function () {
      return this.$store.getters.getCompareUsedAvailable;
    },
    ...mapGetters(["loading"]),
  },
  data: function () {
    return {
      choice: "",
      finalQ: "",
      alphabet: [
        "ALL",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
      ],
      input: "",
      data: null,
      user: {},
      testURL: "",
      registry: [],
      total: "0",
      sortChange: "relevance",
      query: "",
      highlighter: null,
      startingPoints: [
        {
          namespace: "schema",
          prefix: "schema",
          name: "Dataset",
          description:
            "A body of structured information describing some topic(s) of interest.",
        },
      ],
      shortcuts: [
        {
          name: "Schema.org",
          registered_namespace: "schema",
        },
        {
          name: "BioLink",
          registered_namespace: "bts",
        },
      ],
      classesGroupByLetter: [],
      perPage: 10,
      page: 1,
      pages: 1,
      startCap: 0,
      endCap: 20,
      groupPages: false,
      pageLimit: 20,
      startCapLimitReached: true,
      endCapLimitReached: false,
    };
  },
  watch: {
    "$route.query.search": {
      immediate: true,
      handler: function (v) {
        this.choice = v;
        if (!v) {
          this.choice = "classes";
        }
      },
    },
    "$route.query.q": {
      immediate: true,
      handler: function (v) {
        if (v) {
          this.query = v;
        }
      },
    },
    finalQ: function (v) {
      this.$router.push({
        name: "SchemaRegistry",
        query: { search: this.$route.query.search, q: v },
      });
    },
  },
  methods: {
    getNameSpaces() {
      var self = this;
      let res = [];
      // TODO:
      // change this to use https://discovery.biothings.io/api/registry?field=_id&size=20
      const runtimeConfig = useRuntimeConfig()
      axios
        .get(
          runtimeConfig.public.apiUrl + "/api/registry/query?facets=namespace&facet_size=100"
        )
        .then((res) => {
          res = res.data.facets.namespace.terms.map((r) => r.term);
          let data = res.reduce((r, e) => {
            let group = e[0];
            if (!r[group]) r[group] = { group, children: [e] };
            else r[group].children.push(e);
            return r;
          }, {});
          res = Object.values(data);
          self.classesGroupByLetter = orderBy(data, ["group"], ["asc"]);
        })
        .catch((err) => {
          throw err;
        });
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
    getQueryFilters: function () {
      var filters = [];
      var authorFilters = [];
      var finalFilters = {};
      this.tags.forEach(function (item) {
        if (item.active) filters.push(item.name);
      });
      if (filters.length > 0) {
        finalFilters["tags.name.raw"] = filters;
      }

      this.authors.forEach(function (item) {
        if (item.active) {
          authorFilters.push(item.name);
        }
      });
      if (authorFilters.length) {
        finalFilters["info.contact.name.raw"] = authorFilters;
      }

      return finalFilters;
    },
    search() {
      var self = this;

      let query = self.query || "__all__";
      if (query !== "__all__") {
        self.finalQ = query;
      }
      const runtimeConfig = useRuntimeConfig()

      let url = runtimeConfig.public.apiUrl + `/api/registry/query?q=${query}`;

      self.$store.commit("setLoading", { value: true });
      self.registry = [];
      self.highlighter.unmark();

      //query analytics
      if (query !== "__all__") {
        self.sendGAEvent("class_search", query);
      }

      // sorting
      switch (self.sortChange) {
        case "relevance":
          //default behavior
          break;
        case "A-Z":
          url += "&sort=label.raw";
          break;
        case "Z-A":
          url += "&sort=-label.raw";
          break;
        default:
          //no matching sort
          break;
      }

      var params = {
        params: {
          size: self.perPage,
          from: self.page == 1 ? self.page - 1 : (self.page - 1) * self.perPage,
        },
      };

      axios
        .get(url, params)
        .then(function (response) {
          self.registry = response.data.hits;
          self.total = response.data.total;
          self.calculatePages();
          console.log("%c Query executed", "color:violet");
          console.log(
            "%c " +
              JSON.stringify(
                {
                  q: query,
                  size: self.perPage,
                  from:
                    self.page == 1
                      ? self.page - 1
                      : (self.page - 1) * self.perPage,
                  sorting: self.sortChange,
                },
                null,
                2
              ),
            "color:orange"
          );
          console.log("%c hits: " + response.data.total, "color:limegreen");
          self.$store.commit("setLoading", { value: false });
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
    sortResults(e) {
      this.sort = e.target.value;
    },
    compareAll() {
      this.$store.commit("compareAll");
    },
    compareUsed() {
      this.$store.commit("compareUsed");
    },
    resetItems() {
      this.$.commit("resetItems");
    },
    openModal() {
      var self = this;
      var modal = document.getElementById("compareResults");
      modal.style.display = "block";
      var span = document.getElementById("closeBtn");
      span.onclick = function () {
        modal.style.display = "none";
      };
      if (self.compareItems.length > 1) {
        this.$store.commit("compareAll");
      }
    },
  },
  updated: function () {
    // Highlight matches in results
    this.mark(this.query);
  },
  mounted: function () {
    let self = this;
    this.highlighter = new Mark(document.querySelector(".context"));
    this.search();
    window.onpopstate = function () {
      self.search();
    };
  },
};
</script>
