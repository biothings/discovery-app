<script setup>
  import showdown from "showdown";
  import { computed, ref } from 'vue'
  import { useStore } from "vuex";
  import Notify from "simple-notify";

  const { $swal } = useNuxtApp()

  const route = useRoute();
  const store = useStore();
  const id = route.params.id;
  let metadata = ref({});
  let isN3C = ref(false);
  let meta_id = ref("");
  let n3c_status = ref("");
  let scriptText = ref("");
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
      months[date.getMonth()] +
      " " +
      date.getDate() +
      ", " +
      date.getFullYear()
    );
  }

  function download() {
    var a = document.createElement("a");
    var file = new Blob(
      [
        "<sc" +
          'ript type="application/ld+json" >' +
          JSON.stringify(metadata, null, 2) +
          "</scr" +
          "ipt>",
      ],
      { type: "text/plain" }
    );
    a.href = URL.createObjectURL(file);
    a.download = "meta-download";
    a.click();
  }

  function getPreview() {
    let txt =
      "&lt;sc" +
      'ript type="application/ld+json" &gt;' +
      JSON.stringify(metadata.value, null, 2) +
      "&lt;/scr" +
      "ipt&gt;";
    $swal.fire({
      position: "center",
      confirmButtonColor: "#63296b",
      cancelButtonColor: "#4a7d8f",
      customClass: "scale-in-center",
      html:
        `<h6 class="text-center mainTextDark">Copy this code</h6><div class="text-left alert-secondary">
                  <div>
                    <small>
                      <pre>` +
        txt +
        `</pre>
                    </small>
                  </div>
                </div>`,
    });
  }

  function getMetadata(id) {
    id = id.replace("/", "");
    generateScriptText(id);
    meta_id.value = id;
    const runtimeConfig = useRuntimeConfig()
    store.commit('setLoading', {value: true});

    fetch(runtimeConfig.public.apiUrl + "/api/dataset/" + id + "?meta=true")
      .then((response) => response.json())
      .then((data) => {
        metadata.value = data;
        useHead({
          title: metadata.value.name,
          meta:[
            {
              'name': 'description',
              'content': metadata.value.description
            }
          ],
          link:[
            {
              'rel': 'canonical',
              'href': metadata.value.url
            }
          ]
        })
        store.commit('setLoading', {value: false});
        if (
          Object.prototype.hasOwnProperty.call(
            metadata.value["_meta"],
            "n3c"
          ) &&
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
        console.log(err)
        $swal.fire({
          icon: "error",
          title: "Page does not exist",
          html: "<a href='/dataset' rel='nonreferrer'>Go To Registry</a>",
        });
        store.commit('setLoading', {value: false});
        throw err;
      });
  }

  function copyScript(id) {
    var copyText = document.getElementById(id);
    copyText.select();
    document.execCommand("Copy");
    new Notify({
      status: 'success',
      title: 'Copied!',
      autoclose: true,
      autotimeout: 2000
    })
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
  })

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
      return chosen_only;
  })

  const schemaLink = computed(() => {
    if (
        metadata.value.hasOwnProperty("@type") &&
        metadata.value["@type"].includes(":")
      ) {
        let parts = metadata.value["@type"].split(":");
        return "/view/" + parts[0] + "/" + parts[1];
      }
      return false;
  })

  getMetadata(id);

</script>

<template>
  <div class="alert-secondary">
    <div v-if="metadata && metadata.name" class="container">
      <div class="text-left" style="margin: auto">
        <div class="text-light mainBackLight">
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
            <small
              v-if="metadata && metadata.version"
              class="text-light d-block text-center"
              v-text="'Version ' + metadata.version"
            ></small>
            <small v-if="last_updated" class="text-light d-block text-center">
              Last updated <b v-text="last_updated"></b>
            </small>
            <div class="text-center" v-if="isN3C">
              <div class="badge badge-pill text-light m-auto" :class="color">
                <span v-text="n3c_status"></span>
              </div>
            </div>
          </div>
          <div class="text-center alert-dark p-2">
            <template v-if="metadata && metadata._meta.username">
              <small
                ><router-link :to="'/contributor/' + metadata._meta.username"
                  >more by user</router-link
                ></small
              >
              |
              <small
                ><a :href="'/api/dataset/' + meta_id" rel="noopener"
                  >raw json-ld</a
                ></small
              >
              |
              <template v-if="schemaLink">
                <small><a :href="schemaLink" rel="noopener">schema</a></small>
              </template>
            </template>
          </div>
        </div>
        <div class="bg-light p-4 text-center">
          <div class="p-3 text-left">
            <span
              class="text-dark m-auto"
              v-html="processMarkdown(metadata.description)"
            ></span>
          </div>
          <template v-for="(content, name) in viewMetadata" :key="name">
            <ResourceFieldBox
              :name="name"
              :content="content"
              isChild="false"
            ></ResourceFieldBox>
          </template>
          <div class="d-flex flex-wrap mt-5 justify-content-center">
            <template v-for="item in metadata.keywords">
              <small class="text-muted m-1"
                ># <span v-text="item"></span
              ></small>
            </template>
          </div>
        </div>
        <div class="alert alert-info text-muted mt-5">
          <h5>Embed this structured dataset metadata on your website</h5>
          <h6>Embedding options:</h6>
          <div class="row">
            <div class="col-sm-12 col-md-6 p-3">
              <h6>Dynamic Embedding</h6>
              <p>
                <small
                  >Leave it up to us! Just copy the following code and paste it
                  anywhere before the closing <code>&lt;/head&gt;</code> tag on
                  your website's code.</small
                >
              </p>
              <p class="text-info">
                <small
                  >Changes to metadata will be applied automatically.</small
                >
              </p>
              <small class="d-block text-muted">
                <b>CLICK TO COPY</b>
              </small>
              <input
                id="myInput"
                @click="copyScript('myInput')"
                title="Learn More About FAIR Principles"
                class="form-control p-2 w-75 m-auto pointer"
                v-model="scriptText"
                type="text"
              />
            </div>
            <div class="col-sm-12 col-md-6 p-3">
              <h6>Hard Coded</h6>
              <p>
                <small
                  >In your website's code anywhere before the closing
                  <code>&lt;/head&gt;</code> tag, paste the code below.</small
                >
              </p>
              <p class="text-info">
                <small>Changes to metadata need to be updated manually.</small>
              </p>
              <small class="d-block text-muted">
                <b>COPY THIS CODE:</b>
              </small>
              <button
                class="btn-secondary text-light btn m-auto"
                @click="getPreview()"
              >
                View Code
              </button>
              <br />
              <small
                ><a class="pointer" @click="download()">Download Code</a></small
              >
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
