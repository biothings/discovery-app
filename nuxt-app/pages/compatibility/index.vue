<template>
  <div
    id="flowchart"
    class="flowchart d-flex justify-content-center align-items-center"
  >
    <div v-if="loading" class="loader">
      <img src="@/assets/img/ripple.svg" />
    </div>
    <div class="row m-0 w-100 mt-5">
      <div class="mt-3 col-sm-12">
        <Flowchart class="col-sm-12 col-md-8 m-auto border"></Flowchart>
      </div>
      <div class="col-sm-12">
        <form class="row m-0">
          <div class="col-sm-12 bg-dark p-3 mt-5 text-light">
            <h3 class="text-center">
              Check data portal compatibility with schema.org structured
              metadata
            </h3>
            <input
              type="text"
              class="form-control w-50 m-auto"
              placeholder="Search by name"
              v-model="query"
            />
            <div>
              <p class="text-center text-muted">
                <small
                  >Eg.
                  <i class="pointer" @click="query = 'zenodo'">Zenodo</i></small
                >
              </p>
            </div>
          </div>

          <div class="col-sm-12 p-0">
            <div class="row m-0">
              <div class="col-sm-12 col-md-3 row m-0 alert-dark pt-3">
                <div class="form-group col-sm-12">
                  <label for="recc"
                    >Categories (<b v-text="categories.length"></b>)</label
                  >
                  <div class="filterBox alert-secondary">
                    <template v-for="(cat, i) in categories" :key="i">
                      <div
                        @click="activateCategory(cat)"
                        class="pointer badge d-block w-100 mb-1 text-left"
                        :class="[
                          cat.active ? 'alert-success jello' : 'bg-light',
                        ]"
                      >
                        <span v-text="cat.name"></span>
                      </div>
                    </template>
                  </div>
                </div>
                <div class="form-group col-sm-12">
                  <label for="recc"
                    >Recommended By (<b v-text="recommended.length"></b>)</label
                  >
                  <div class="filterBox alert-secondary">
                    <template v-for="(item, i) in recommended" :key="i">
                      <div
                        @click="activateRecommended(item)"
                        class="pointer badge d-block w-100 mb-1 text-left"
                        :class="[item.active ? 'alert-info jello' : 'bg-light']"
                      >
                        <span v-text="item.name"></span>
                      </div>
                    </template>
                  </div>
                </div>
                <div class="form-group col-sm-12">
                  <div class="form-check p-2">
                    <input
                      class="slider mr-2"
                      type="checkbox"
                      name="login"
                      id="login"
                      v-model="with_login"
                    />
                    <label class="form-check-label" for="login">
                      Requires Login
                    </label>
                  </div>
                </div>
                <div class="form-group col-sm-12">
                  <div class="form-check p-2">
                    <input
                      class="slider mr-2"
                      type="checkbox"
                      name="schema_compliant"
                      id="schema_compliant"
                      v-model="schema_compliant"
                    />
                    <label class="form-check-label" for="schema_compliant">
                      Schema.org Compliant
                    </label>
                  </div>
                </div>
              </div>
              <div class="col-sm-12 col-md-9">
                <div class="col-sm-12">
                  <small class="text-danger"
                    >(<b v-text="results.length"></b> results)</small
                  >
                  <div class="resTable context">
                    <ul class="list-group">
                      <template v-for="(r, i) in results" :key="i">
                        <CompatibilityResult :r="r"></CompatibilityResult>
                      </template>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CompatibilityResult from "~~/components/CompatibilityResult.vue";
import Flowchart from "~~/components/Flowchart.vue";
import { useCompatibilityStore } from "../../stores/compatibility";
import { mapState, mapActions } from "pinia";

export default {
  name: "Compatibility",
  head() {
    return {
      title: "DDE | Data Portal Compatibility",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/YCQ2ZNL0/compatibility.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/YCQ2ZNL0/compatibility.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/compatibility",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/compatibility",
        },
        {
          property: "og:description",
          content:
            "Check data portal compatibility with schema.org structured metadata",
        },
        {
          name: "description",
          content:
            "Check data portal compatibility with schema.org structured metadata",
        },
        {
          name: "twitter:card",
          content:
            "Check data portal compatibility with schema.org structured metadata",
        },
      ],
    };
  },
  components: {
    Flowchart,
    CompatibilityResult,
  },
  data: function () {
    return {
      url: "https://raw.githubusercontent.com/SuLab/dataset-repository-selector/main/dataset_repositories.json",
      loading: false,
    };
  },
  methods: {
    ...mapActions(useCompatibilityStore, [
      "saveData",
      "activateCategory",
      "updateResults",
      "saveQuery",
      "toggleLoginFilter",
      "updateResults",
      "toggleCompliant",
      "resetData",
      "activateRecommended",
    ]),
    getData: function () {
      let self = this;
      self.loading = true;
      axios
        .get(self.url)
        .then((res) => {
          self.saveData({ data: res.data });
          self.loading = false;
        })
        .catch((err) => {
          self.loading = false;
          throw err;
        });
    },
    activateCategory(cat) {
      this.activateCategory({ category: cat });
      this.updateResults();
    },
    activateRecommended(rec) {
      this.activateRecommended({ recommended: rec });
      this.updateResults();
    },
  },
  computed: {
    ...mapState(useCompatibilityStore, ["getQuery", "requiresLogin"]),
    ...mapState(useCompatibilityStore, {
      categories: "getCategories",
      recommended: "getRecommended",
      results: "getData",
      sc: "schema_compliant",
      filters: "getFilters",
    }),
    query: {
      get() {
        return this.getQuery;
      },
      set(v) {
        this.saveQuery({ q: v });
      },
    },
    with_login: {
      get() {
        return this.requiresLogin;
      },
      set() {
        this.toggleLoginFilter();
        this.updateResults();
      },
    },
    schema_compliant: {
      get() {
        return this.sc;
      },
      set() {
        this.toggleCompliant();
        this.updateResults();
      },
    },
  },
  watch: {
    query: function (q) {
      q ? this.updateResults() : this.resetData();
    },
  },
  mounted: function () {
    this.getData();
  },
};
</script>
