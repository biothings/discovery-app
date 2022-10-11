<template>
  <div id="viewer" v-cloak>
    <!-- HOMEPAGE MODE -->
    <div class="bg-light" v-if="!query">
      <div
        class="grad d-flex justify-content-center align-items-center flex-wrap pt-5"
      >
        <div>
          <template v-if="namespaceRegistered">
            <div class="text-center p-5">
              <h1
                style="font-size: 3em"
                class="text-light"
                v-if="namespace === 'schema'"
              >
                Schema.org
              </h1>
              <h1
                style="font-size: 3em"
                class="text-light"
                v-else-if="namespace === 'bts'"
              >
                BioLink Schema
              </h1>
              <h1
                style="font-size: 3em"
                class="text-light"
                v-else-if="namespace === 'ctsa'"
              >
                CTSA
              </h1>
              <h1
                style="font-size: 3em"
                class="text-light"
                v-else
                v-text="namespace"
              ></h1>
              <p class="text-light" v-if="namespace === 'schema'">
                Schema.org is a collaborative, community activity with a mission
                to create, maintain, and promote schemas for structured data on
                the Internet. In addition to people from the founding companies
                (Google, Microsoft, Yahoo and Yandex), there is substantial
                participation by the larger Web community, through public
                mailing lists such as
                <a
                  target="_blank"
                  href="https://lists.w3.org/Archives/Public/public-vocabs/"
                  >public-vocabs@w3.org</a
                >
                and through
                <a target="_blank" href="http://github.com/schemaorg/schemaorg"
                  >GitHub</a
                >. <a target="_blank" href="https://schema.org/">Learn More.</a>
              </p>
              <p class="text-light" v-if="namespace === 'bts'">
                A high level datamodel of biological entities (genes, diseases,
                phenotypes, pathways, individuals, substances, etc) and their
                associations. Maintained by
                <a
                  target="_blank"
                  rel="noreferrer"
                  href="https://github.com/biolink"
                  >biolink</a
                >.
              </p>
            </div>
          </template>
          <template v-else>
            <div class="text-center p-5">
              <h1
                style="font-size: 3em"
                class="text-light"
                v-text="namespace"
              ></h1>
              <small class="text-info">(Temporary Namespace)</small>
            </div>
          </template>
          <div class="row" v-show="!namespaceRegistered">
            <div class="col-sm-12 text-center p-3">
              <button
                role="button"
                class="btn btn-sm btn-success"
                @click="openRegistration()"
              >
                <font-awesome-icon icon="fas fa-registered" /> Register This
                Schema
              </button>
            </div>
          </div>
        </div>

        <div class="input-group input-group-sm mb-2 col-sm-12 col-md-4">
          <div class="input-group-prepend">
            <div class="input-group-text bg-secondary text-light">
              <font-awesome-icon icon="fas fa-search" />
            </div>
          </div>
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            id="inlineFormInputGroup"
            placeholder="Search..."
          />
        </div>
      </div>

      <div
        class="row w-100 alert alert-secondary m-0"
        v-if="searchResults.length || searchResultsProps.length"
      >
        <div class="col-sm-12 col-md-6 p-4">
          <ul>
            <li
              v-if="searchResults.length"
              class="mainTextDark bold"
              style="list-style: none"
            >
              Classes
            </li>
            <li v-for="item in searchResults">
              <nuxt-link :to="'/' + item['label']"
                ><small v-text="item['label']"></small
              ></nuxt-link>
            </li>
          </ul>
        </div>
        <div class="col-sm-12 col-md-6 p-4">
          <ul>
            <li
              v-if="searchResultsProps.length"
              class="mainTextLight bold"
              style="list-style: none"
            >
              Properties
            </li>
            <li v-for="item in searchResultsProps">
              <nuxt-link :to="'/' + item['label']"
                ><small v-text="item['label']"></small
              ></nuxt-link>
            </li>
          </ul>
        </div>
      </div>

      <div class="flipcard container my-5">
        <div class="face front">
          <!-- alphabetical view -->
          <div
            id="alphabetical-order"
            class="text-left p-4 bg-light overflow-x-scroll"
          >
            <h3 class="text-muted d-inline mr-2 logoText">Definitions</h3>
            <a
              role="button"
              class="btn btn-sm btn-info pointer ml-2"
              @click="flipView()"
              >Change View <font-awesome-icon icon="fas fa-retweet"
            /></a>
            <div v-if="userSchemaURL" class="w-100 text-right">
              <a
                class="mr-2 text-primary"
                :href="userSchemaURL"
                target="_blank"
                rel="noreferrer"
              >
                <small
                  >View Source
                  <font-awesome-icon icon="fas fa-external-link-alt"
                /></small>
              </a>
            </div>
            <div v-show="developerMode" id="canvasTest"></div>
            <ul
              class="pagination overflow-x-scroll mt-3"
              v-show="classesGroupByLetter.length > 5"
            >
              <li
                class="page-link"
                v-for="(item, i) in classesGroupByLetter"
                :key="i"
              >
                <a :href="'#' + item.group" v-text="item.group"></a>
              </li>
            </ul>
            <ul class="list-group mt-3">
              <li
                class="list-group-item list-group-item-action"
                v-for="(item, i) in classesGroupByLetter"
                :key="i + 'l'"
              >
                <h3
                  :id="item.group"
                  class="text-dark"
                  v-text="item.group"
                  v-show="classesGroupByLetter.length > 5"
                ></h3>
                <ul style="list-style: none" class="stripedList">
                  <li
                    v-for="def in item.children"
                    class="d-flex justify-content-between align-item-center p-1"
                  >
                    <nuxt-link :to="{ path: '/ns/' + namespace + '/' + def }">
                      <span v-text="def.split(':')[1]"></span>
                      <font-awesome-icon icon="fas fa-chevron-right" />
                    </nuxt-link>
                    <font-awesome-icon
                      icon="fas fa-code-branch"
                      class="pointer tip text-light btn btn-info p-1"
                      @click.prevent="saveDataAndRedirect(def)"
                      :data-tippy-content="'Extend ' + def"
                    />
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
        <div class="face back">
          <!--hierarchical view -->
          <div
            id="hierarchical"
            class="text-left p-4 bg-light overflow-x-scroll"
          >
            <h3 class="text-muted d-inline mr-2 logoText">
              Definition Hierarchy
            </h3>
            <a
              role="button"
              class="btn btn-sm btn-info pointer ml-2"
              @click="flipView()"
              >Change View <font-awesome-icon icon="fas fa-retweet"
            /></a>
            <div class="alert alert-warning" v-if="treeBuildErr">
              <small
                >Hierarchical view not available. Tree could not be built due to
                endless cycles found on schema definition.</small
              >
            </div>
            <ul class="pagination mt-2" v-if="!treeBuildErr">
              <li
                v-for="n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
                class="d-inline hierarchicalSwatch"
                :class="'bg-' + n"
              ></li>
            </ul>
            <ul class="tree" v-if="!treeBuildErr">
              <li>
                <nuxt-link
                  class="text-0"
                  :to="'/ns/' + namespace + '/' + rootNode"
                  v-text="rootNode"
                ></nuxt-link>
                <ul>
                  <li v-for="item in getNeighbors(rootNode)">
                    <nuxt-link
                      class="text-1"
                      :to="'/ns/' + namespace + '/' + item"
                      v-text="item"
                    ></nuxt-link>
                    <ul>
                      <li v-for="item2 in getNeighbors(item)">
                        <nuxt-link
                          class="text-2"
                          :to="'/ns/' + namespace + '/' + item2"
                          v-text="item2"
                        ></nuxt-link>
                        <ul>
                          <li v-for="item3 in getNeighbors(item2)">
                            <nuxt-link
                              class="text-3"
                              :to="'/ns/' + namespace + '/' + item3"
                              v-text="item3"
                            ></nuxt-link>
                            <ul>
                              <li v-for="item4 in getNeighbors(item3)">
                                <nuxt-link
                                  class="text-4"
                                  :to="'/ns/' + namespace + '/' + item4"
                                  v-text="item4"
                                ></nuxt-link>
                                <ul>
                                  <li v-for="item5 in getNeighbors(item4)">
                                    <nuxt-link
                                      class="text-5"
                                      :to="'/ns/' + namespace + '/' + item5"
                                      v-text="item5"
                                    ></nuxt-link>
                                    <ul>
                                      <li v-for="item6 in getNeighbors(item5)">
                                        <nuxt-link
                                          class="text-6"
                                          :to="'/ns/' + namespace + '/' + item6"
                                          v-text="item6"
                                        ></nuxt-link>
                                        <ul>
                                          <li
                                            v-for="item7 in getNeighbors(item6)"
                                          >
                                            <nuxt-link
                                              class="text-7"
                                              :to="
                                                '/ns/' + namespace + '/' + item7
                                              "
                                              v-text="item7"
                                            ></nuxt-link>
                                            <ul>
                                              <li
                                                v-for="item8 in getNeighbors(
                                                  item7
                                                )"
                                              >
                                                <nuxt-link
                                                  class="text-8"
                                                  :to="
                                                    '/ns/' +
                                                    namespace +
                                                    '/' +
                                                    item8
                                                  "
                                                  v-text="item8"
                                                ></nuxt-link>
                                                <ul>
                                                  <li
                                                    v-for="item9 in getNeighbors(
                                                      item8
                                                    )"
                                                  >
                                                    <nuxt-link
                                                      class="text-9"
                                                      :to="
                                                        '/ns/' +
                                                        namespace +
                                                        '/' +
                                                        item9
                                                      "
                                                      v-text="item9"
                                                    ></nuxt-link>
                                                    <ul>
                                                      <li
                                                        v-for="item10 in getNeighbors(
                                                          item9
                                                        )"
                                                      >
                                                        <nuxt-link
                                                          class="text-10"
                                                          :to="
                                                            '/ns/' +
                                                            namespace +
                                                            '/' +
                                                            item10
                                                          "
                                                          v-text="item10"
                                                        ></nuxt-link>
                                                      </li>
                                                    </ul>
                                                  </li>
                                                </ul>
                                              </li>
                                            </ul>
                                          </li>
                                        </ul>
                                      </li>
                                    </ul>
                                  </li>
                                </ul>
                              </li>
                            </ul>
                          </li>
                        </ul>
                      </li>
                    </ul>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <!-- QUERY MODE -->
    <div id="mainCont">
      <div class="container mt-5" v-if="query">
        <div
          class="w-100 p-2 bg-dark d-flex align-items-center justify-content-around p-3"
        >
          <span
            class="fa-stack fa-1x pointer unselectable tip"
            data-tippy-content="Back to namespace home"
            @click.prevent="$router.push('/ns/' + namespace)"
          >
            <font-awesome-icon
              icon="fas fa-circle"
              class="fa-stack-2x text-muted"
            />
            <font-awesome-icon
              icon="fas fa-chevron-left"
              class="text-light fa-stack-1x"
            />
          </span>
          <div>
            <template v-if="!validationView">
              <small class="text-center text-light mb-1"
                >Expand Properties</small
              >
              <input
                id="toggle"
                class="form-control slider text-light m-auto tip"
                @change="showAll()"
                data-tippy-content="Expand or contract all property lists"
                type="checkbox"
                checked
              />
            </template>
          </div>
          <div>
            <small class="text-center text-light mb-1"
              ><img src="@/assets/img/cube.svg" width="15" /> Validation
              View</small
            >
            <input
              id="showButton"
              class="form-control slider m-auto"
              @change="changeView()"
              title="Show this class only and any validation included"
              type="checkbox"
              v-model="validationView"
            />
          </div>
          <div v-if="userSchemaURL">
            <a
              class="text-center text-light mb-1"
              :href="userSchemaURL"
              target="_blank"
              rel="noreferrer"
            >
              <small
                >View Source <font-awesome-icon icon="fas fa-external-link-alt"
              /></small>
            </a>
          </div>
        </div>

        <!-- CLASSES FOR QUERY -->
        <div class="context">
          <!-- Main Class -->
          <QueryBox
            v-if="queryContent"
            :parent="false"
            :q="queryContent"
            :userSchema="userSchema"
          ></QueryBox>
          <!-- Parent Classes -->
          <template
            v-if="queryContent && userSchemaParents"
            v-for="parent in userSchemaParents"
          >
            <QueryBox
              v-show="!validationView"
              :parent="true"
              :q="parent"
              :userSchema="userSchema"
            ></QueryBox>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";
import { mapGetters } from "vuex";
import { filter, sortBy, orderBy, find } from "lodash";
import axios from "axios";
import Notify from "simple-notify";
import QueryBox from "~~/components/QueryBox.vue";

import "@/assets/js/networkx.js";

export default {
  name: "SchemaViewer",
  head() {
    return {
      title: "DDE | Namespace Viewer",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/xdfr4zzV/schemav.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/xdfr4zzV/schemav.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/ns",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/ns",
        },
        {
          property: "og:description",
          content:
            "Visualize and share your schema definition with the biomedical research community",
        },
        {
          name: "description",
          content:
            "Visualize and share your schema definition with the biomedical research community",
        },
        {
          name: "twitter:card",
          content:
            "Visualize and share your schema definition with the biomedical research community",
        },
      ],
    };
  },
  //namespace argument and query argument
  components: {
    QueryBox,
  },
  data: function () {
    return {
      namespace: null,
      query: null,
      //show network x graph
      developerMode: true,
      //NEW VIEWER DATA
      userSchema: [],
      userSchemaURL: "",
      userSchemaAllProps: [],
      userSchemaAllClasses: [],
      parentList: [],
      userSchemaParents: [],
      //   query: "",
      //   namespace: "",
      namespaceRegistered: false,
      classesGroupByLetter: [],
      nxG: null,
      rootNode: null,
      edgeGraph: [],
      searchQuery: "",
      searchResults: [],
      searchResultsProps: [],
      filterLetters: [],
      topProp: {},
      filter: "",
      queryContentParents: [],
      checkbox: null,
      treeBuildErr: false,
      apiUrl: "",
    };
  },
  computed: {
    ...mapGetters(["loading", "userInfo", "queryContent"]),
    validationView: {
      get() {
        return this.$store.getters.validationView;
      },
      set(v) {
        this.$store.commit("setValidationView", { value: v });
      },
    },
    schemaFilters() {
      let letters = [];
      let self = this;
      if (self.userSchema) {
        for (var i = 0; i < self.userSchema["hits"].length; i++) {
          let q = self.userSchema["hits"][i]["label"][0];
          if (!letters.includes(q)) {
            letters.push(q);
          }
        }
      }
      return letters.sort();
    },
  },
  watch: {
    searchQuery: function (newQ) {
      if (newQ.length) {
        let result = filter(this.userSchema.hits, function (o) {
          if (o["label"].toLowerCase().includes(newQ.toLowerCase())) {
            return o;
          }
        });
        let resultProps = filter(this.userSchemaAllProps, function (o) {
          if (o["label"].toLowerCase().includes(newQ.toLowerCase())) {
            return o;
          }
        });

        this.searchResults = result;
        this.searchResultsProps = resultProps;
      } else {
        this.searchResults = [];
        this.searchResultsProps = [];
      }
    },
    queryContent: {
      handler: function (klass) {
        var self = this;
        let res = [];
        if (klass.hasOwnProperty("parent_classes")) {
          for (var i = 0; i < klass["parent_classes"].length; i++) {
            if (klass["parent_classes"][i]) {
              let parents = klass["parent_classes"][i].split(", ");
              for (var x = 0; x < parents.length; x++) {
                let name = self.getName(parents[x]);
                res.push(name);
              }
            }
          }
          if (res.length) {
            self.queryContentParents = res;
          } else {
            self.queryContentParents = [];
          }
        }
      },
      deep: true,
    },
  },
  methods: {
    saveDataAndRedirect(item) {
      var self = this;
      let found = find(self.userSchema.hits, (o) => o.name == item);
      if (found) {
        let data = JSON.stringify(found);
        localStorage.setItem("EditorData", data);
        localStorage.setItem("EditorStartingPoint", item);
        self.$router.push({ path: "/editor" });
      } else {
        self.$swal.fire("Hmmm", "Cannot find Class: " + item);
      }
    },
    checkIfNamespaceIsRegistered(namespace) {
      let self = this;
      self.$store.commit("setLoading", { value: true });
      axios
        .get(self.apiUrl + `/api/registry/` + namespace)
        .then(function (res) {
          self.$store.commit("setLoading", { value: false });
          if (res.data) {
            let url = res.data.url;
            if (url || res.data) {
              self.namespaceRegistered = true;
              self.loadSchema(namespace, url);
            } else {
              self.$swal.fire(
                "This namespace is registered but..",
                "No URL was found",
                "error"
              );
            }
          }
        })
        .catch((err) => {
          self.$store.commit("setLoading", { value: false });
          self.loadSchema();
          throw err;
        });
    },
    loadSchema(namespace, url) {
      let self = this;
      if (namespace && self.namespaceRegistered) {
        self.$store.commit("setLoading", { value: true });
        axios
          .get(self.apiUrl + "/api/registry/" + namespace)
          .then((res) => {
            self.data = res.data;
            self.$store.commit("setLoading", { value: false });
            self.userSchema = res.data;
            self.userSchemaURL = url;
            var payload = {};
            payload["schema"] = res.data;
            self.$store.commit("saveSchemaForViewer", payload);
            self.orderAlphabetically();
            if (self.query) {
              self.handleQuery();
            }
          })
          .catch((err) => {
            self.$store.commit("setLoading", { value: false });
            throw err;
          });
      } else if (!namespace) {
        this.userSchema = JSON.parse(
          localStorage.getItem("user-schema-classes")
        );
        this.userSchemaURL = localStorage.getItem("user-schema-url");

        var payload = {};
        payload["schema"] = JSON.parse(
          localStorage.getItem("user-schema-classes")
        );

        // CHECK IF LS ITEM EXISTS AT ALL
        if (localStorage.getItem("user-schema-classes") !== null) {
          // console.log('LS loaded')
          self.$store.commit("saveSchemaForViewer", payload);
          this.orderAlphabetically();

          if (self.query) {
            self.handleQuery();
          }
        } else {
          // IF NO SCHEMA AT ALL
          if (sessionStorage.getItem(self.namespace)) {
            // Last VIEWED DAT MATCHES url
            localStorage.setItem(
              "user-schema-classes",
              sessionStorage.getItem(self.namespace)
            );
            localStorage.setItem(
              "user-schema-url",
              sessionStorage.getItem(self.namespace + "-url")
            );
            self.loadSchema();
          } else {
            // DATA DOES NOT EXIST AT All
            let timerInterval;
            self.$swal.fire({
              icon: "error",
              title: "Page Does Not Exist",
              html: "Taking you to the Schema Playground in <b></b> seconds...",

              timer: 3000,
              didClose: () => {
                self.$router.push({ path: "/schema-playground" });
              },
              didOpen: () => {
                self.$swal.showLoading();
                const b = self.$swal.getHtmlContainer().querySelector("b");
                timerInterval = setInterval(() => {
                  b.textContent = Math.ceil(self.$swal.getTimerLeft() / 1000);
                }, 100);
              },
              willClose: () => {
                clearInterval(timerInterval);
              },
            });
          }
        }
      }
    },
    orderAlphabetically() {
      var self = this;
      let res = [];
      for (var i = 0; i < self.userSchema["hits"].length; i++) {
        //only order classes not referenced
        if (!self.userSchema["hits"][i]["ref"]) {
          res.push(self.userSchema["hits"][i]["name"]);
        }
      }

      let data = res.reduce((r, e) => {
        let group = e.split(":")[1][0];
        if (!r[group]) r[group] = { group, children: [e] };
        else r[group].children.push(e);
        return r;
      }, {});

      res = Object.values(data);
      self.classesGroupByLetter = orderBy(res, ["group"], ["asc"]);
      self.makeHierarchyTree();
      self.getAllProps();
    },
    flipView() {
      if ($(".flipcard").hasClass("flipped")) {
        $(".flipcard").removeClass("flipped");
      } else {
        $(".flipcard").addClass("flipped");
      }
    },
    makeHierarchyTree() {
      var self = this;
      // if (!self.query) {
      self.nxG = new jsnx.DiGraph();
      if (self.userSchema["hits"].length > 1) {
        for (var i = 0; i < self.userSchema["hits"].length; i++) {
          // console.log('CLASS: ',i,self.userSchema['hits'][i]["label"])
          let topLevel = self.userSchema["hits"][i]["name"];
          self.addNode(topLevel);
          // console.log("add node",self.userSchema['hits'][i]["name"])
          if (self.userSchema["hits"][i].hasOwnProperty("parent_classes")) {
            let parents = self.userSchema["hits"][i]["parent_classes"][0];
            if (parents) {
              let parentList = parents.split(", ");
              parentList.push(topLevel);
              for (
                var currentParent = 0;
                currentParent < parentList.length;
                currentParent++
              ) {
                if (
                  parentList[currentParent] &&
                  parentList[currentParent - 1]
                ) {
                  self.addNode(parentList[currentParent]);
                  self.addEdge(
                    parentList[currentParent - 1],
                    parentList[currentParent]
                  );
                }
              }
            }
          }
        }
      }

      try {
        let topoRes = jsnx.topologicalSort(self.nxG);
        // console.log('ROOT NODE IS...', topoRes[0])
        let rootNode = "";
        rootNode = topoRes[0];

        self.rootNode = rootNode;
      } catch (e) {
        console.log("Oh no...", e);
        self.treeBuildErr = true;
      } finally {
      }
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
    addEdge(class1, class2) {
      this.nxG.addEdge(class1, class2);
      let node = [class2, class1];
      this.edgeGraph.push(node);
    },
    addNode(className) {
      this.nxG.addNode(className, { label: className });
    },
    getNeighbors(node) {
      if (node) {
        let neighbors = this.nxG.neighbors(node);
        return neighbors;
      }
    },
    getAllProps() {
      let res = [];
      let self = this;
      for (var i = 0; i < self.userSchema["hits"].length; i++) {
        if (
          self.userSchema["hits"][i].hasOwnProperty("properties") &&
          self.userSchema["hits"][i]["properties"].length > 0
        ) {
          res = res.concat(self.userSchema["hits"][i]["properties"]);
        }
      }
      self.userSchemaAllProps = res;

      var payload = {};
      payload["props"] = res;
      self.$store.commit("saveProps", payload);
    },
    handleQuery() {
      var self = this;
      // Attempt to find Class first
      let q = self.findClass(self.query);
      if (q) {
        // self.queryContent = q;
        self.getParentsOf(q);
        var payload = {};
        payload["queryContent"] = q;
        self.$store.commit("checkIFValidationView", payload);
      } else if (self.findProp(self.query)) {
        let prop = self.findProp(self.query);
        var payload = {};
        payload["queryContent"] = prop;
        self.$store.commit("checkIFValidationView", payload);
      } else {
        new Notify({
          status: "error",
          title: "Visualization Error",
          text: "No match found",
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
      }
    },
    findClass(query) {
      let self = this;
      if (self.namespace === "schema") {
        console.log("SCHEMA.org case");
        axios(
          self.apiUrl +
            "/api/registry/" +
            self.namespace +
            "/" +
            "schema:" +
            self.query +
            "?v"
        )
          .then((res) => {
            var payload = {};
            payload["schema"] = res.data;
            self.$store.commit("saveSchemaForViewer", payload);
            this.userSchema = res.data;
            for (var i = 0; i < self.userSchema["hits"].length; i++) {
              if (self.userSchema["hits"][i]["label"] === query) {
                // console.log("MATCH",self.userSchema['hits'][i])
                let q = self.userSchema["hits"][i];
                self.getParentsOf(q);
                var payload = {};
                payload["queryContent"] = q;
                self.$store.commit("checkIFValidationView", payload);
              }
            }
            return false;
          })
          .catch((err) => {
            throw err;
          });
      } else {
        for (var i = 0; i < self.userSchema["hits"].length; i++) {
          if (
            self.userSchema["hits"][i]["name"] === query ||
            self.userSchema["hits"][i]["label"] == query
          ) {
            let found = self.userSchema["hits"][i];
            return found;
          }
        }
        return false;
      }
    },
    findProp(query) {
      let self = this;
      // console.log('Looking in schema for PROP: ',query)
      for (var i = 0; i < self.userSchemaAllProps.length; i++) {
        if (self.userSchemaAllProps[i]["label"] === query) {
          return self.userSchemaAllProps[i];
        }
      }
      return false;
    },
    handleFilter(e) {
      if (e.target.value !== "Choose...") {
        self.$router.push({ path: "/" + e.target.value });
      }
    },
    handleChange(e) {
      let target = e.target.value;
      this.filter = e.target.value;
      let fullList = this.userSchema;
      let results = [];
      switch (target) {
        case "ALL":
          this.filterResults = fullList;
          break;
        default:
          results = fullList;
          results = fullList.filter(
            (word) => word["name"].split(":")[1][0] === target
          );
          this.filterResults = sortBy(
            results,
            [(q) => q["name"].split(":")[1]],
            ["asc"]
          );
      }
    },
    getUniqueContent(paths) {
      var finalArr = [];
      let mergedpaths = [];
      for (var i = 0; i < paths.length; i++) {
        mergedpaths = mergedpaths.concat(paths[i]);
      }

      function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
      }

      finalArr = mergedpaths.filter(onlyUnique);
      // console.log('Unique Arr Elements ',finalArr)
      return finalArr;
    },
    getParentsOf(classInfo) {
      // console.log("Getting parents of ",classInfo)
      var self = this;
      let res = [];
      if (classInfo.hasOwnProperty("parent_classes")) {
        for (var i = 0; i < classInfo["parent_classes"].length; i++) {
          if (classInfo["parent_classes"][i]) {
            let parents = classInfo["parent_classes"][i].split(", ");
            res.push(parents);
          }
        }
        // console.log('ALL PATHS',res)
        self.queryContentParents = self.getUniqueContent(res).reverse();
        // console.log('TOP CLASS PARENTS...',self.queryContentParents)
        self.getParentsInfo(self.queryContentParents);
      }
      return res;
    },
    getParentsInfo(list) {
      var self = this;
      let res = [];
      for (var i = 0; i < list.length; i++) {
        for (var x = 0; x < self.userSchema["hits"].length; x++) {
          let parentName = list[i];
          // compare name not label as there might be duplicates
          if (self.userSchema["hits"][x].name === parentName) {
            // console.log("GOT PARENT FULL INFO...",self.userSchema['hits'][x].label,parentName)
            res.push(self.userSchema["hits"][x]);
          }
        }
      }
      self.userSchemaParents = res;
      //   console.log('ALL PARENTS INFO', self.userSchemaParents)
    },
    changeView() {
      console.log("changing view...");
    },
    drawGraph(g, container) {
      jsnx.draw(g, {
        element: container,
        weighted: true,
        edgeStyle: {
          "stroke-width": 10,
          fill: "#b4b4b4",
        },
        layoutAttr: {
          charge: -800,
          linkDistance: 100,
        },
        height: 300,
        optBind: true,
        labelStyle: { fill: "#5C3069" },
        withLabels: true,
        nodeLabels: "label",
        nodeStyle: {
          stroke: "#8feddc",
          fill: "#84dcdf",
          cursor: "pointer",
          nodeShape: "s",
        },
      });
    },
    openRegistration() {
      var self = this;
      if (self.userInfo && self.userInfo.login) {
        self.$swal
          .fire({
            customClass: "scale-in-center",
            title: "Why should I register my schema?",
            html: `<ul class="text-muted text-left">
                <li>
                  <small>
                     Share your work with other members of the community. Your schema definition could be helpful to many others in the community as a starting point for their reserach.
                  </small>
                </li>
                <li>
                  <small>
                     By registering a schema derived from an existing schema you are helping to maintain the <a href="https://www.go-fair.org/fair-principles/" target="_blank">FAIR</a> (Findable, Accessible, Interoperable, Reusable) principles of data-sharing/creation.
                  </small>
                </li>
                <li>
                  <small>
                     It's easy to register your schema! If everything looks good here all you have to do is choose a namespace for your schema's homepage.
                  </small>
                </li>
                <li>
                  <small>
                     You'll be able to easily share your schema and visualize it in a way that it's easy to undertand.
                  </small>
                </li>
              </ul>`,
            footer: "<p>If everything looks good, click <b> Continue</b></p>",
            showCancelButton: true,
            confirmButtonColor: "#5C3069",
            cancelButtonColor: "#006476",
            confirmButtonText: "Continue",
          })
          .then((result) => {
            if (result.value) {
              self.$swal
                .fire({
                  title: "Registration",
                  input: "text",

                  customClass: "scale-in-center",
                  text: "Choose a namespace (a-z,0-9)",
                  footer: `<small>Namespace must be unique and cannot be 'metadata','dataset' or 'schema'</small>`,
                  confirmButtonColor: "#5C3069",
                  cancelButtonColor: "#006476",
                  showCancelButton: true,
                  confirmButtonText: "Register",
                  inputValidator: (input) => {
                    return new Promise((resolve) => {
                      var re = /^[a-zA-Z0-9_.-]*$/;
                      if (!re.test(input)) {
                        resolve("Namespace contains invalid characters");
                      } else {
                        axios
                          .head(self.apiUrl + `/api/registry/` + input)
                          .then(function (res) {
                            resolve(
                              '<small>Sorry, that namespace is already taken: <a href="/ns/' +
                                input +
                                '/" target="_blank">http://discovery.biothings.io/ns/' +
                                input +
                                "</a></small>"
                            );
                          })
                          .catch((err) => {
                            resolve();
                            throw err;
                          });
                      }
                    });
                  },
                  showLoaderOnConfirm: true,
                  preConfirm: (input) => {
                    let data = {
                      namespace: input,
                      url: encodeURI(self.userSchemaURL),
                    };
                    let config = {
                      headers: {
                        "content-type": "application/json",
                      },
                    };
                    return axios
                      .post(self.apiUrl + "/api/registry", data, config)
                      .then((res) => {
                        return res.data;
                      })
                      .catch((err) => {
                        return err;
                        throw err;
                      });
                  },
                  allowOutsideClick: () => !self.$swal.isLoading(),
                  backdrop: true,
                })
                .then((result) => {
                  if (result.value) {
                    // console.log("FINAL",result)
                    if (result.value.success) {
                      let name = result.value.url.split("/").splice(-1, 1);
                      self.$gtag.event("click", {
                        event_category: "schema_added",
                        event_label: name,
                        event_value: 1,
                      });
                      self.$gtag.event("click", {
                        event_category: "schema_added",
                        event_label: "ALL",
                        event_value: 1,
                      });

                      let timerInterval;
                      self.$swal.fire({
                        type: "success",
                        title: "Registration Successful",

                        customClass: "scale-in-center",
                        html: "Taking you to your schema homepage in <strong></strong> seconds.",
                        timer: 3000,
                        onBeforeOpen: () => {
                          const content = self.$swal.getContent();
                          const $ = content.querySelector.bind(content);
                          self.$swal.showLoading();
                          timerInterval = setInterval(() => {
                            self.$swal
                              .getContent()
                              .querySelector("strong").textContent = (
                              self.$swal.getTimerLeft() / 1000
                            ).toFixed(0);
                          }, 100);
                        },
                        onClose: () => {
                          clearInterval(timerInterval);
                          navigateTo({ path: "/ns/" + name + "/" });
                        },
                      });
                    } else {
                      if (result.value.response.statusText) {
                        self.$swal.fire({
                          type: "error",
                          toast: true,
                          position: "top center",
                          title: "Registration Failed: ",
                          text: result.value.response.statusText,
                        });
                      } else {
                        console.error("Error:", result);
                        self.$swal.fire({
                          type: "error",
                          toast: true,
                          position: "top center",
                          title: "Registration Failed: ",
                          text: "Check console",
                        });
                      }
                    }
                  }
                });
            }
          });
      } else {
        self.$swal.fire({
          type: "error",
          toast: true,
          position: "top",
          title: "You Must Log-in To Register a Schema",
        });
      }
    },
    extend(itemname) {
      var self = this;
      self.$swal
        .fire({
          title: "Extend class: " + itemname,
          html: "<small>By entending this class you are creating a more specific version of this class</small>",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",

          customClass: "scale-in-center",
          confirmButtonText: "Extend",
        })
        .then((result) => {
          if (result.value) {
            let q = self.findClass(itemname);
            console.log("q", q);
            if (q) {
              axios
                .get(
                  self.apiUrl + "/api/registry/" + q.namespace + "/" + q.name
                )
                .then((res) => {
                  let obj = JSON.stringify(res.data);
                  localStorage.setItem("EditorData", obj);
                  localStorage.setItem("EditorStartingPoint", q.name);
                  self.$router.push({ path: "/editor" });
                })
                .catch((err) => {
                  throw err;
                });
            } else {
            }
          }
        });
    },
    showAll() {
      this.$store.dispatch("toggleShowAll");
    },
  },
  mounted: function () {
    let self = this;
    const runtimeConfig = useRuntimeConfig();
    this.apiUrl = runtimeConfig.public.apiUrl;
    const route = useRoute();
    this.namespace = route.params.namespace;
    this.query = route.params.query;
    tippy("#showButton", {
      content: `<div class='m-0'><table class='table'>
              <tr>
                <td>
                  <small class='mainTextDark'>Show All Inherited Properties</small>
                </td>
                <td>
                  <small>Shows all parents classes of the current class and their properties</small>
                </td>
              </tr>
              <tr>
                <td>
                  <small class='mainTextDark'> Show Used Properties Only</small>
                </td>
                <td>
                  <small>Shows only the current class and properties used specified in the <b>validation</b> field</small>
                </td>
              </tr>
            </table></div>`,
      placement: "left",
      allowHTML: true,
      theme: "light",
    });
    console.log(
      "%c NAMESPACe: " + this.namespace,
      "background: hotpink; color:white; padding:4px;"
    );
    console.log(
      "%c QUERY " + this.query,
      "background: blue; color:white; padding:4px;"
    );
    self.checkIfNamespaceIsRegistered(self.namespace);
  },
};
</script>
