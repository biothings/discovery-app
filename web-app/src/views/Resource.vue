<template>
  <div class="alert-secondary">
    <div v-if="metadata && metadata.name" class="container">
      <div class="text-left" style="margin: auto">
        <div class="text-light" style="background-color: #0b566f">
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

<script>
import showdown from "showdown";

export default {
  name: "Resource",
  props: ["id"],
  data: function () {
    return {
      query: "",
      loading: false,
      scriptText: "",
      meta_id: "",
      metadata: {},
      isN3C: false,
      n3c_status: "",
      color: "badge-light",
    };
  },
  methods: {
    generateScriptText(id) {
      this.scriptText =
        "<sc" +
        'ript src="' +
        "https://discovery.biothings.io/api/dataset/" +
        id +
        '.js"/></scr' +
        "ipt>";
    },
    copyScript(id) {
      var copyText = document.getElementById(id);
      copyText.select();
      document.execCommand("Copy");
      self.$swal.fire({
        type: "success",
        toast: true,
        title: "Copied",
        showConfirmButton: false,
        timer: 1000,
      });
    },
    getMetadata(id) {
      var self = this;
      id = id.replace("/", "");
      self.generateScriptText(id);
      self.loading = true;
      self.meta_id = id;

      fetch(self.$apiUrl + "/api/dataset/" + id + "?meta=true")
        .then((response) => response.json())
        .then((data) => {
          self.loading = false;
          self.metadata = data;
          if (
            Object.prototype.hasOwnProperty.call(
              self.metadata["_meta"],
              "n3c"
            ) &&
            Object.keys(self.metadata["_meta"]["n3c"]).length
          ) {
            self.isN3C = true;
            self.n3c_status = Object.prototype.hasOwnProperty.call(
              self.metadata["_meta"]["n3c"],
              "status"
            )
              ? self.metadata["_meta"]["n3c"]["status"]
              : "Not Available";
            switch (self.n3c_status) {
              case "Done/Imported":
                self.color = "badge-success";
                break;
              case "Done/Rejected":
                self.color = "badge-danger";
                break;
              case "Ready for Import":
                self.color = "badge-purple";
                break;
              case "In Review":
                self.color = "badge-info";
                break;
              default:
                self.color = "badge-secondary";
                break;
            }
          }
          self.createScript();
          self.updateMetaTags(data);
        })
        .catch((err) => {
          self.loading = false;
          self.$swal.fire({
            icon: "error",
            title: "Page does not exist",
            html: "<a href='/dataset' rel='nonreferrer'>Go To Registry</a>",
          });
          throw err;
        });
    },
    updateMetaTags(data) {
      if (data.hasOwnProperty("name") && data.hasOwnProperty("description")) {
        let meta = null;
        // Open graph and Meta
        meta = document.createElement("meta");
        meta.setAttribute("property", "og:title");
        meta.setAttribute("content", "Data Discovery Engine | " + data.name);
        document.getElementsByTagName("head")[0].appendChild(meta);

        meta = document.createElement("meta");
        meta.setAttribute("name", "description");
        meta.setAttribute("content", data.description);
        document.getElementsByTagName("head")[0].appendChild(meta);

        meta = document.createElement("meta");
        meta.setAttribute("property", "og:description");
        meta.setAttribute("content", data.description);
        document.getElementsByTagName("head")[0].appendChild(meta);

        meta = document.createElement("meta");
        meta.setAttribute("property", "og:url");
        meta.setAttribute("content", window.location.href);
        document.getElementsByTagName("head")[0].appendChild(meta);

        meta = document.createElement("meta");
        meta.setAttribute("property", "og:locale");
        meta.setAttribute("content", "en_US");
        document.getElementsByTagName("head")[0].appendChild(meta);

        // Twitter
        meta = document.createElement("meta");
        meta.setAttribute("name", "twitter:title");
        meta.setAttribute("content", "Data Discovery Engine | " + data.name);
        document.getElementsByTagName("head")[0].appendChild(meta);

        meta = document.createElement("meta");
        meta.setAttribute("name", "twitter:url");
        meta.setAttribute("content", window.location.href);
        document.getElementsByTagName("head")[0].appendChild(meta);

        meta = document.createElement("meta");
        meta.setAttribute("name", "twitter:description");
        meta.setAttribute("content", data.description);
        document.getElementsByTagName("head")[0].appendChild(meta);
      }
    },
    createScript() {
      let self = this;
      let scriptTag = document.createElement("script");

      let obj = Object.assign({}, self.metadata);
      obj["@context"] = "http://schema.org/";
      obj["@type"] = "Dataset";
      //modify original in order to pass check on Rich Results test
      // "@context": "http://schema.org/",
      // "@type": "Dataset",
      let str = JSON.stringify(obj, null, 2);

      scriptTag.setAttribute("type", "application/ld+json");
      scriptTag.text = str;
      // console.log('embedding json-ld',scriptTag)
      document.body.appendChild(scriptTag);
      self.createCanonicalTag(self.metadata);
      if (self.metadata.name)
        document.title = "CTSA DATA DISCOVERY ENGINE / " + self.metadata.name;
      if (self.metadata.description)
        document.description =
          "CTSA DATA DISCOVERY ENGINE / " + self.metadata.description;
    },
    createCanonicalTag(meta) {
      if (meta && meta.url) {
        let linkTag = document.createElement("link");
        linkTag.setAttribute("rel", "canonical");
        linkTag.setAttribute("href", meta.url);
        document.head.appendChild(linkTag);
      }
    },
    getPreview() {
      var self = this;
      let txt =
        "&lt;sc" +
        'ript type="application/ld+json" &gt;' +
        JSON.stringify(self.metadata, null, 2) +
        "&lt;/scr" +
        "ipt&gt;";
      self.$swal.fire({
        position: "center",
        confirmButtonColor: "#63296b",
        cancelButtonColor: "#4a7d8f",
        customClass: "scale-in-center",
        html:
          `<h6 class="text-center mainTextDark">Copy this code</h6><div class="text-left alert-secondary">
                    <div>
                      <small>
                        <pre>` + txt +
                          `</pre>
                      </small>
                    </div>
                  </div>`,
      });
    },
    download() {
      var self = this;
      var a = document.createElement("a");
      var file = new Blob(
        [
          "<sc" +
            'ript type="application/ld+json" >' +
            JSON.stringify(self.metadata, null, 2) +
            "</scr" +
            "ipt>",
        ],
        { type: "text/plain" }
      );
      a.href = URL.createObjectURL(file);
      a.download = "meta-download";
      a.click();
    },
    formatDate(timestamp) {
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
    },
    processMarkdown(txt) {
      var conv = new showdown.Converter();
      txt = conv.makeHtml(txt);
      return txt.replace(/(?:\r\n|\r|\n)/g, "<br>");
    },
  },
  mounted: function () {
    var self = this;
    if (self.id) {
      self.query = self.id;
      console.log('ID', self.id)
      self.getMetadata(self.query);
    }
  },
  computed: {
    viewMetadata: function () {
      let self = this;
      let chosen_only = {};
      const ignore = [
        "_id",
        "@type",
        "@context",
        "name",
        "description",
        "keywords",
      ];
      Object.keys(self.metadata).forEach(function (v, i) {
        if (!ignore.includes(v)) {
          chosen_only[v] = self.metadata[v];
        }
      });
      return chosen_only;
    },
    schemaLink: function () {
      var self = this;
      if (
        self.metadata.hasOwnProperty("@type") &&
        self.metadata["@type"].includes(":")
      ) {
        let parts = self.metadata["@type"].split(":");
        return "/view/" + parts[0] + "/" + parts[1];
      }
      return false;
    },
    last_updated: function () {
      if (
        this.metadata.hasOwnProperty("_meta") &&
        this.metadata["_meta"].hasOwnProperty("last_updated")
      ) {
        return this.formatDate(this.metadata["_meta"]["last_updated"]);
      } else {
        return false;
      }
    },
  },
};
</script>

<style scoped>
.badge-purple {
  background-color: rgb(100, 45, 136);
}
.smallBadge {
  color: #fff !important;
  margin: 2px;
  padding: 3px 6px;
  border: 0;
  font-size: 9px;
  font-weight: 700;
  border-radius: 10px;
  margin-right: 3px;
  vertical-align: top;
  border: 1.5px solid #d3d3d3;
  white-space: nowrap !important;
  cursor: default;
  background-color: rgb(196, 27, 91);
}
</style>
