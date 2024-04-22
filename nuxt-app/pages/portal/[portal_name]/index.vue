<script setup>
import Notify from "simple-notify";

import { computed, ref } from "vue";
import { usePortalsStore } from "../../../stores/portals";

let store = usePortalsStore();

let portal = {};
let featuredImg = "";
let colors = ref([]);

let route = useRoute();
let portal_name = route.params.portal_name;

if (portal_name) {
  switch (portal_name) {
    case "nde":
      portal = store.portals.find((item) => item.keyName == portal_name);
      featuredImg = "https://i.postimg.cc/d1RJrJYk/niaidportal.jpg";
      break;
    case "niaid":
      portal = store.portals.find((item) => item.keyName == portal_name);
      featuredImg = "https://i.postimg.cc/J0QNFjbc/niaidportal.jpg";
      break;
    case "outbreak":
      portal = store.portals.find((item) => item.keyName == portal_name);
      featuredImg = "https://i.postimg.cc/3w4WfN01/outportal.jpg";
      break;
    case "cd2h":
      portal = store.portals.find((item) => item.keyName == portal_name);
      featuredImg = "https://i.postimg.cc/Dz2bCndY/cd2hportal.jpg";
      break;
    case "n3c":
      portal = store.portals.find((item) => item.keyName == portal_name);
      featuredImg = "https://i.postimg.cc/y87FGm7P/n3cportal.jpg";
      break;
    default:
      redirect();
  }
}
colors.value = portal["colors"];

const gradient = computed(() => {
  let color = "linear-gradient(45deg";
  colors.value.forEach(function (e) {
    color += "," + e.hex;
  });
  color += " 30%)";
  return color;
});

function redirect() {
  new Notify({
    status: "Error",
    title: "Portal Error",
    text: "Portal does not exist. back to portals..",
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
  setTimeout(() => {
    navigateTo({ path: "/portal" });
  }, 2000);
}

// let coverage = reactive({})
// let result = {}

// let endpoints = portal.coverage.map(label => axios.get(runtimeConfig.public.apiUrl + `/api/registry/query?q=namespace:${portal_name}%20AND%20label:${label}&size=1`));

// axios.all(endpoints)
//   .then(axios.spread((...responses) => {

//     responses.forEach(res => {
//       res.data?.hits.forEach(item => {
//         if (item?.parent_classes.length) {
//           result[item?.name] = item.parent_classes[0].split(', ').concat([item?.name])
//         }
//       });
//     });
//     let parent_endpoints = [];

//     for (const parentLabel in result) {
//       parent_endpoints = parent_endpoints.concat(result[parentLabel].map((clsName) => {
//         return {"url": runtimeConfig.public.apiUrl + "/api/coverage/" + clsName, "parent": clsName}
//       }));
//     }
//     console.log("PE", parent_endpoints)
//     let temp = {}

//     parent_endpoints.forEach(req => {
//       axios.get(req.url)
//       .then(res2=>{
//         temp[req.parent] = res2.data
//       }).catch(error2 => {
//         console.log("coverage not found for ", req.parent)
//       });
//     });

//     coverage.value = temp;
//     console.log('Coverage', coverage)

//   })).catch(errors => {
//     console.log("failed portal coverage")
//   });

// let visualize = ref(false);
// watch(coverage, (v)=>{
//   console.log('V', v)
//   visualize.value = true;
// })

useHead({
  title: "DDE | " + portal_name.toUpperCase() + " Portal",
  meta: [
    {
      property: "og:description",
      content: portal.description,
    },
    {
      name: "description",
      content: portal.description,
    },
    {
      name: "twitter:card",
      content: portal.description,
    },
    {
      name: "og:url",
      content: "https://discovery.biothings.io/portal/" + portal_name,
    },
    {
      name: "og:image",
      content: featuredImg,
    },
    {
      name: "twitter:image",
      content: featuredImg,
    },
  ],
});
</script>

<template>
  <div id="portal" class="container-fluid p-0" style="min-height: 80vh">
    <template v-if="portal?.name">
      <div class="row m-0">
        <div
          class="text-center col-sm-12 p-0"
          :style="{ background: gradient }"
        >
          <div class="lines p-5" style="min-height: 250px">
            <img
              class="mt-4"
              :src="portal?.image"
              :alt="portal?.name"
              width="300"
            />
            <nuxt-link to="/portal" class="d-block text-info"
              ><font-awesome-icon icon="fas fa-chevron-left" /> Back to
              Portals</nuxt-link
            >
          </div>
        </div>
        <div
          class="col-sm-12 col-md-8 py-5 d-flex justify-content-center align-items-center"
        >
          <div class="container">
            <div class="d-flex justify-content-start align-items-center">
              <img
                :src="portal.portalicon"
                :alt="portal.name"
                width="100"
                class="mr-2"
              />
              <h1 :style="{ color: portal.colors[1].hex }">
                <span v-text="portal.name"></span>
              </h1>
            </div>
            <h5 class="my-3 text-dark" v-text="portal.header"></h5>
            <div class="text-dark" v-html="portal.description"></div>
            <div
              class="border-top text-left text-muted p-2"
              v-if="portal.publications"
            >
              <h4>Publications</h4>
              <ul>
                <li v-for="pub in portal.publications" :key="pub.name">
                  <a :href="pub.link" target="_blank" rel="nonreferrer">
                    {{ pub.name }}
                    <font-awesome-icon icon="fas fa-external-link-alt" />
                  </a>
                </li>
              </ul>
            </div>
            <template v-if="route.fullPath == '/portal/n3c'">
              <div class="border-top text-center text-muted p-2">
                <h4>External Dataset Request</h4>
                <p>
                  To enable some integrated analysis with the N3C dataset, you
                  can request to include an external dataset in the N3C Enclave
                  environment.
                </p>
                <div class="text-center p-2 m-1 rounded p-3">
                  <nuxt-link
                    role="button"
                    :style="{ background: portal.colors[0].hex }"
                    class="btn text-light btn-lg nd mt-2 tip"
                    to="/guide/n3c/dataset"
                    :data-tippy-content="'Add a dataset for ' + portal.name"
                  >
                    Submit Request
                  </nuxt-link>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="border-top text-center text-muted p-2">
                <h4>Contribute</h4>
                <p>
                  Follow an easy-to-follow guide to help you contribute metadata
                  for <span v-text="portal.name"></span> following this schema's
                  <nuxt-link :to="{ path: portal.schema }">structure</nuxt-link
                  >:
                </p>
                <div
                  v-for="(g, i) in portal.guides"
                  :key="i + 'g'"
                  class="text-center p-2 m-1 rounded p-3"
                >
                  <nuxt-link
                    role="button"
                    :style="{ background: portal.colors[0].hex }"
                    @click="
                      $gtag.event('click', {
                        event_category: 'portal_guide',
                        event_label: g.guide,
                        event_value: 1,
                      })
                    "
                    class="btn text-light btn-lg nd mt-2 tip"
                    :to="{ path: g.guide }"
                  >
                    <font-awesome-icon icon="fas fa-plus" /> Add
                    <b v-text="g.name"></b> Metadata
                  </nuxt-link>
                </div>
              </div>
            </template>
          </div>
        </div>
        <div
          class="col-sm-12 col-md-4 d-flex flex-column justify-content-center align-items-stretch alert-dark p-5"
        >
          <div
            class="text-center p-2 m-1 rounded p-3"
            v-if="portal.showCoverage"
          >
            <CoverageIcon :color="portal?.colors[0]?.hex"></CoverageIcon>
            <nuxt-link
              :to="{ path: '/coverage' }"
              rel="noreferrer"
              class="nd mt-2 tip text-info rounded"
              data-tippy-content="Explore and visualize metadata coverage"
            >
              <h5>
                Coverage <font-awesome-icon icon="fas fa-chevron-right" />
              </h5>
            </nuxt-link>
          </div>
          <div class="text-center p-2 m-1 rounded p-3" v-if="portal.site">
            <WebsiteIcon :color="portal?.colors[0]?.hex"></WebsiteIcon>
            <a
              :href="portal.site"
              target="_blank"
              rel="noreferrer"
              class="nd mt-2 tip text-info"
              :data-tippy-content="'Explore the ' + portal.name + ' website'"
            >
              <h5>Site <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </a>
          </div>
          <div class="text-center p-2 m-1 rounded p-3">
            <SchemaIcon :color="portal?.colors[0]?.hex"></SchemaIcon>
            <nuxt-link
              :to="{ path: portal.schema }"
              class="nd mt-2 tip text-info"
              :data-tippy-content="'Explore the schema used in ' + portal.name"
            >
              <h5>Schema <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </nuxt-link>
          </div>
          <div
            v-for="(g, i) in portal.guides"
            :key="i + 'gg'"
            class="text-center p-2 m-1 rounded p-3"
          >
            <MetadataIcon :color="portal?.colors[0]?.hex"></MetadataIcon>
            <nuxt-link
              :to="g.registry"
              class="nd mt-2 tip text-info"
              :data-tippy-content="
                'Browse metadata in Data Discovery Engine for ' + g.name
              "
            >
              <h5>
                <span v-text="g.name + 's'"></span>
                <font-awesome-icon icon="fas fa-chevron-right" />
              </h5>
            </nuxt-link>
          </div>
          <div
            v-if="portal && portal.api"
            class="text-center p-2 m-1 rounded p-3"
          >
            <APIIcon :color="portal?.colors[0]?.hex"></APIIcon>
            <a
              :href="portal.api"
              target="_blank"
              rel="noreferrer"
              class="nd mt-2 tip text-info"
              :data-tippy-content="'Explore API for ' + portal.name"
            >
              <h5>API <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </a>
          </div>
          <div
            v-if="portal && portal.faq_link"
            class="text-center p-2 m-1 rounded p-3"
          >
            <FAQIcon :color="portal?.colors[0]?.hex"></FAQIcon>
            <nuxt-link
              :to="{ path: portal.faq_link }"
              class="nd mt-2 tip text-info"
              data-tippy-content="Frequently Asked Questions"
            >
              <h5>FAQ <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </nuxt-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
