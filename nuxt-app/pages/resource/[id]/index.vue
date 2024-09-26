<script setup>
import showdown from "showdown";
import { computed, ref } from "vue";
import { useStore } from "vuex";
import Notify from "simple-notify";

const { $swal } = useNuxtApp();

const route = useRoute();
const store = useStore();
const id = route.params.id;
let metadata = ref({});
let metadata_html = ref("");
let metadata_pure = ref({});
let isN3C = ref(false);
let meta_id = ref("");
let n3c_status = ref("");
let scriptText = ref("");
let ready = ref(false);
let expand = ref(false);
let color = ref("badge-light");

function processMarkdown(txt) {
  var conv = new showdown.Converter();
  txt = conv.makeHtml(txt);
  return txt.replace(/(?:\r\n|\r|\n)/g, "<br>");
}

function generateScriptText(id) {
  scriptText.value =
    "<sc" +
    'ript src="' +
    "https://discovery.biothings.io/api/dataset/" +
    id +
    '.js"/></scr' +
    "ipt>";
}

function formatDate(timestamp) {
  // Create a date object from the timestamp
  var date = new Date(timestamp);
  // Create a list of names for the months
  var months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  // return a formatted date
  return (
    months[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear()
  );
}

function download(format) {
  var a = document.createElement("a");
  var fileContent, fileType, fileName;

  if (format === "html") {
    fileContent =
      "<sc" +
      'ript type="application/ld+json" >\n' +
      JSON.stringify(metadata.value, null, 2) +
      "\n</scr" +
      "ipt>";
    fileType = "text/plain";
    fileName = "meta-download.txt";
  } else if (format === "json") {
    fileContent = JSON.stringify(metadata.value, null, 2);
    fileType = "application/json";
    fileName = "meta-download.json";
  } else {
    console.error("Unsupported format. Please use 'html' or 'json'.");
    return;
  }

  var file = new Blob([fileContent], { type: fileType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

function getFeatured(meta) {
  if (meta.value?._meta?.guide.includes("n3c")) {
    return "https://i.postimg.cc/ry0C25bK/n3cfeatured.jpg";
  }
  if (meta.value?._meta?.guide.includes("outbreak")) {
    return "https://i.postimg.cc/brs2gRj1/outbreakfeatured.jpg";
  }
  return "https://i.postimg.cc/wTG3pgRY/featured.jpg";
}

function getMetadata(id) {
  store.commit("setLoading", { value: true });
  id = id.replace("/", "");
  generateScriptText(id);
  meta_id.value = id;
  const runtimeConfig = useRuntimeConfig();
  store.commit("setLoading", { value: true });

  fetch(runtimeConfig.public.apiUrl + "/api/dataset/" + id + "?meta=true")
    .then((response) => response.json())
    .then((data) => {
      metadata.value = data;
      setTimeout(() => {
        ready.value = true;
        let o = Object.assign({}, data);
        delete o["_meta"];
        delete o["_id"];

        let txt =
          "<scr" +
          'ipt type="applicat' +
          'ion/ld+json">\n' +
          JSON.stringify(o, null, 2) +
          "\n<" +
          "/script>";
        metadata_pure.value = o;
        metadata_html.value = txt;
      }, 200);
      useHead({
        title: "DDE | " + metadata.value.name,
        meta: [
          {
            property: "og:description",
            content: metadata.value.description,
          },
          {
            name: "description",
            content: metadata.value.description,
          },
          {
            name: "twitter:card",
            content: metadata.value.description,
          },
          {
            name: "og:url",
            content: "https://discovery.biothings.io/dataset/" + id,
          },
          {
            name: "og:image",
            content: getFeatured(metadata),
          },
          {
            name: "twitter:image",
            content: getFeatured(metadata),
          },
        ],
        link: [
          {
            rel: "canonical",
            href:
              metadata.value.url ||
              "https://discovery.biothings.io/dataset" + id,
          },
        ],
        script: [
          {
            type: "application/ld+json",
            children: JSON.stringify(metadata.value, null, 2),
          },
        ],
      });
      store.commit("setLoading", { value: false });
      if (
        Object.prototype.hasOwnProperty.call(metadata.value["_meta"], "n3c") &&
        Object.keys(metadata.value["_meta"]["n3c"]).length
      ) {
        isN3C.value = true;
        n3c_status.value = Object.prototype.hasOwnProperty.call(
          metadata.value["_meta"]["n3c"],
          "status"
        )
          ? metadata.value["_meta"]["n3c"]["status"]
          : "Not Available";
        switch (n3c_status.value) {
          case "Done/Imported":
            color.value = "badge-success";
            break;
          case "Available":
            color.value = "badge-success";
            break;
          case "Done/Rejected":
            color.value = "badge-danger";
            break;
          case "Ready for Import":
            color.value = "badge-purple";
            break;
          case "In Review":
            color.value = "badge-info";
            break;
          default:
            color.value = "badge-secondary";
            break;
        }
      }
    })
    .catch((err) => {
      console.log(err);
      $swal.fire({
        icon: "error",
        title: "Page does not exist",
        html: "<a href='/dataset' rel='nonreferrer'>Go To Registry</a>",
      });
      store.commit("setLoading", { value: false });
      throw err;
    });
}

function copyScript(id) {
  var copyText = document.getElementById(id);
  copyText.select();
  document.execCommand("Copy");
  new Notify({
    status: "success",
    title: "Copied!",
    autoclose: true,
    autotimeout: 2000,
  });
}

function copyHTML() {
  navigator.clipboard
    .writeText(metadata_html.value)
    .then(() => {
      new Notify({
        status: "success",
        title: "Copied!",
        autoclose: true,
        autotimeout: 2000,
      });
    })
    .catch((err) => {
      console.error("Error copying HTML to clipboard: ", err);
    });
}

const last_updated = computed(() => {
  if (
    metadata.value.hasOwnProperty("_meta") &&
    metadata.value["_meta"].hasOwnProperty("last_updated")
  ) {
    return formatDate(metadata.value["_meta"]["last_updated"]);
  } else {
    return false;
  }
});

const viewMetadata = computed(() => {
  let chosen_only = {};
  const ignore = [
    "_id",
    "@type",
    "@context",
    "name",
    "description",
    "keywords",
  ];
  Object.keys(metadata.value).forEach(function (v, i) {
    if (!ignore.includes(v)) {
      chosen_only[v] = metadata.value[v];
    }
  });

  const ordered = Object.keys(chosen_only)
    .sort()
    .reduce((obj, key) => {
      obj[key] = chosen_only[key];
      return obj;
    }, {});
  return ordered;
});

const schemaLink = computed(() => {
  if (
    metadata.value.hasOwnProperty("@type") &&
    metadata.value["@type"].includes(":")
  ) {
    let parts = metadata.value["@type"].split(":");
    return "/ns/" + parts[0] + "/" + parts[1];
  }
  return false;
});

getMetadata(id);
</script>

<template>
  <div class="alert-secondary mt-5 pb-5">
    <div v-if="metadata && metadata.name" class="container">
      <div class="text-left" style="margin: auto">
        <div class="text-light grad-light">
          <div class="p-5">
            <h1 class="text-center mt-5">
              <span v-text="metadata.name"></span>
            </h1>
            <div
              class="text-center"
              v-if="metadata && metadata.name.includes('PPRL')"
            >
              <span class="ml-2 badge smallBadge">PPRL</span>
              <router-link
                to="/faq/n3c"
                class="badge smallBadge bg-info ml-1"
                style="cursor: pointer"
                >FAQ</router-link
              >
            </div>
            <span
              v-if="metadata && metadata.version"
              class="text-light d-block text-center"
              v-text="'Version ' + metadata.version"
            ></span>
            <span v-if="last_updated" class="text-light d-block text-center">
              Last updated <b v-text="last_updated"></b>
            </span>
            <div v-if="metadata && metadata._meta.username" class="text-center">
              <span>
                Registered by
                <router-link :to="'/contributor/' + metadata._meta.username">{{
                  metadata._meta.username
                }}</router-link>
              </span>
            </div>
            <div class="text-center" v-if="isN3C">
              <div class="badge badge-pill text-light m-auto" :class="color">
                <span v-text="n3c_status"></span>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-light p-4 text-center">
          <div class="text-left">
            Schema:
            <a :href="schemaLink" rel="noopener" target="_blank">
              <h5 class="d-inline">
                {{ metadata?.["@type"] }}
                <font-awesome-icon icon="fa fa-external-link-alt" />
              </h5>
            </a>
            <small style="float: right"
              ><a :href="'/api/dataset/' + meta_id" rel="noopener"
                >Metadata in JSON-LD</a
              ></small
            >
            <hr />
          </div>
          <div class="p-3 text-left">
            <span
              v-if="metadata.description && metadata.description.length < 500"
              class="text-dark m-auto"
              v-html="processMarkdown(metadata.description)"
            ></span>
            <CollapsibleText
              v-else
              :text="processMarkdown(metadata.description)"
            ></CollapsibleText>
          </div>
          <table class="table table-striped table-hover">
            <tbody>
              <tr v-for="(content, name) in viewMetadata" :key="name">
                <ResourceFieldBox
                  :name="name"
                  :content="content"
                  isChild="false"
                ></ResourceFieldBox>
              </tr>
            </tbody>
          </table>
          <div class="d-flex flex-wrap mt-5 justify-content-center">
            <template v-for="item in metadata.keywords">
              <span class="text-muted m-1"># <span v-text="item"></span></span>
            </template>
          </div>
        </div>
        <div class="alert alert-dark text-dde-dark mt-5">
          <h4>
            <b>For the resource owner:</b> Embed this structured metadata on
            your website describing this resource
            <span
              class="text-info"
              data-tippy-content="<b>TLDR</b>: This makes your dataset easier to be found from multiple search engines (Google, Bing etc.)<hr>
<b>A longer explanation</b>: This enhances discoverability by making your data easily searchable and accessible through web search engines like Google. The <a href='http://schema.org/' target='_blank'>schema.org</a> compatible, structured metadata in <a href='https://json-ld.org/' target='_blank'>JSON-LD</a> format is now <a target='_blank' href='https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data'>recommended by Google</a> and other search engines for better SEO (Search Engine Optimization). This capability facilitates data sharing and collaboration among researchers and developers. Additionally, it provides clear context and provenance for the datasets, ensuring users understand the source, quality, and relevance of the data."
              >[why?]</span
            >
          </h4>
          <div class="p-3">
            <h6>Dynamic Embedding</h6>
            <hr />
            <p>
              <span
                >Leave it up to us! Just copy the following code and paste it
                anywhere before the closing <code>&lt;/head&gt;</code> tag on
                your website's code.</span
              >
            </p>
            <p class="text-dde-mid bold">
              <span
                >Changes made to this metadata via this website will be applied
                to this script automatically.</span
              >
            </p>
            <span class="d-block text-muted text-center">
              <b>CLICK THE INPUT FIELD TO COPY</b>
            </span>
            <input
              id="myInput"
              @click="copyScript('myInput')"
              title="Learn More About FAIR Principles"
              class="form-control p-2 w-75 m-auto pointer"
              v-model="scriptText"
              type="text"
            />
          </div>
          <div class="p-3">
            <h6>Hard Coded Embedding</h6>
            <hr />
            <p>
              <span
                >In your website's code anywhere before the closing
                <code>&lt;/head&gt;</code> tag, copy and paste the HTML code
                below.</span
              >
            </p>
            <p class="text-dde-mid bold">
              <span
                >If you copy/paste this metadata manually all future changes to
                it will need to be applied manually as well.</span
              >
            </p>
            <div class="alert-info">
              <button
                @click="expand = !expand"
                class="btn d-block themeButton text-light w-100"
              >
                {{ expand ? "Close" : "View Metadata" }}
              </button>
              <div v-if="expand">
                <div
                  class="text-left p-1 d-flex justify-content-end align-items-center alert-dark"
                >
                  <a
                    class="btn btn-sm themeButton text-light mx-3"
                    @click="download('html')"
                    >Download</a
                  >
                  <a
                    class="btn btn-sm themeButton text-light mx-3"
                    @click="copyHTML()"
                    >Copy</a
                  >
                </div>
                <template v-if="ready">
                  <div style="max-height: 600px; overflow-y: scroll">
                    <CodeEditorHTML :item="metadata_html"></CodeEditorHTML>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="metadata && !metadata.name"
        class="jumbotron text-center text-muted"
      >
        <h2>Nothing to see here...</h2>
      </div>
    </div>
  </div>
</template>
