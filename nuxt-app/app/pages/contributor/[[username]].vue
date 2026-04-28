<template>
  <div
    id="cont-app"
    class="jumbotron mb-0 bg-light d-flex align-items-center justify-content-center mt-5"
    style="min-height: 80vh"
  >
    <div id="dashTippyParent" class="col-sm-12 col-md-8">
      <h4 class="text-dde-dark">
        <template v-if="$route.params.username.includes('@')">
          {{ $route.params.username }}
        </template>
        <template v-else>
          <a
            target="_blank"
            :href="'https://github.com/' + $route.params.username"
          >
            <font-awesome-icon icon="fab fa-github" />
            {{ $route.params.username }}</a
          >
        </template>
        's contributions
      </h4>
      <div class="mt-3 mainTextDark">
        <div class="badge badge-info" v-text="dashboardTotal"></div>
        Registered Schemas
      </div>
      <div v-for="item in dashboard" class="row m-1">
        <div
          class="col-sm-5 p-1 mainBackDark d-flex align-items-center justify-content-left"
        >
          <nuxt-link
            :to="{ path: '/ns/' + item.namespace }"
            v-text="item.namespace"
            class="d-inline m-2 text-light"
          ></nuxt-link>
        </div>
        <div
          class="col-sm-7 p-1 bg-dark actions d-flex align-items-center justify-content-around"
        >
          <div>
            <nuxt-link :to="{ path: '/ns/' + item.namespace }">
              <span
                class="fa-stack fa-1x pointer tip"
                data-tippy-content="Visualize"
              >
                <font-awesome-icon
                  icon="fas fa-circle"
                  class="text-muted fa-stack-2x"
                />
                <font-awesome-icon
                  icon="fas fa-eye"
                  class="fa-stack-1x text-light"
                />
              </span>
            </nuxt-link>
          </div>
        </div>
      </div>
      <div class="mt-3 mainTextLight">
        <div class="badge badge-info" v-text="datasetsTotal"></div>
        Registered Metadata
      </div>
      <div style="max-height: 800px; overflow-y: scroll">
        <div v-for="item in publicDatasets" class="row m-1">
          <div
            class="col-sm-5 p-1 mainBackLight d-flex align-items-center justify-content-left"
          >
            <nuxt-link
              :to="{ path: '/resource/' + item._id }"
              v-text="item.name"
              class="d-inline m-2 text-light"
            ></nuxt-link>
          </div>
          <div
            class="col-sm-7 p-1 bg-dark actions d-flex align-items-center justify-content-around"
          >
            <div>
              <nuxt-link :to="{ path: '/resource/' + item._id }">
                <span
                  class="fa-stack fa-1x pointer tip"
                  data-tippy-content="View Dataset"
                >
                  <font-awesome-icon
                    icon="fas fa-circle"
                    class="text-muted fa-stack-2x"
                  />
                  <font-awesome-icon
                    icon="fas fa-eye"
                    class="fa-stack-1x text-light"
                  />
                </span>
              </nuxt-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Contributor",
  data: function () {
    return {
      user: {},
      dashboard: [],
      dashboardTotal: 0,
      privateDatasets: [],
      publicDatasets: [],
      datasetsTotal: 0,
      selectedItem: {},
      slugInput: "",
      availableSlug: false,
      invalidChars: false,
      meta: {},
    };
  },
  methods: {
    getAll(q) {
      console.log("GETTING ALL");
      const runtimeConfig = useRuntimeConfig();
      let self = this;
      axios
        .get(runtimeConfig.public.apiUrl + "/api/registry?user=" + q)
        .then((res) => {
          // console.log("SCHEMAS",res.data)
          self.dashboard = res.data.hits;
          self.dashboardTotal = res.data.total;
        })
        .catch((err) => {
          throw err;
        });
      // DATASETS PUBLIC
      axios
        .get(
          runtimeConfig.public.apiUrl + "/api/dataset?&user=" + q + "&size=100"
        )
        .then((res) => {
          // console.log("PUBLIC",res.data)
          self.publicDatasets = self.publicDatasets.concat(res.data.hits);
          self.datasetsTotal += res.data.total;
        })
        .catch((err) => {
          throw err;
        });
    },
  },
  created: function () {
    var self = this;
    if (self.$route.params.username) {
      self.query = self.$route.params.username;
      self.getAll(self.query);
    }
  },
  head() {
    return {
      title: "DDE | User contributions",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/wTG3pgRY/featured.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/wTG3pgRY/featured.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/contributor",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/contributor",
        },
        {
          property: "og:description",
          content: "User metadata and schema namespace contributions",
        },
        {
          name: "description",
          content: "User metadata and schema namespace contributions",
        },
        {
          name: "twitter:card",
          content: "User metadata and schema namespace contributions",
        },
      ],
    };
  },
};
</script>
