<template>
  <div
    id="jsoneditor"
    class="container"
    style="min-height: 100vh; padding-top: 60px"
  >
    <div class="bg-light text-center mt-1 py-5">
      <h1 class="text-dde-dark">JSON SCHEMA VIEWER</h1>
      <div class="mb-1">
        <form id="linkForm" class="col-sm-10 m-auto" @submit="loadSchema()">
          <small v-html="loadMsg"></small>
          <div class="input-group mb-3 shadow rounded">
            <input
              type="text"
              v-model="input"
              class="form-control"
              id="urlform"
              autocomplete=""
              required
              ref="my_input"
              aria-label="Paste your link here"
              placeholder="Paste your link here"
              aria-describedby="button-addon2"
            />
            <div class="input-group-append">
              <button
                :disabled="!input.length"
                @click.prevent="loadSchema()"
                id="button-addon2"
                class="btn btn-info"
                type="submit"
              >
                Go
              </button>
            </div>
          </div>
          <div v-if="loading" class="loader">
            <img src="@/assets/img/ripple.svg" />
          </div>
          <a href="#" @click="loadSchema('ex')" class="badge badge-secondary"
            >JSON Schema Example</a
          >
        </form>
      </div>
      <template v-if="schema['$schema']">
        <div class="row m-0">
          <div
            v-if="schemaType"
            class="col-sm-12 mb-0 p-0 d-flex justify-content-center align-items-center"
          >
            <div
              class="arrowclip mainBackDark text-light p-1 flex-fill text-center"
            >
              <h4><span v-text="schemaType"></span></h4>
            </div>
          </div>
          <div class="col-sm-12 p-0">
            <ul class="list-group list-group-flush text-left">
              <template
                v-for="(propinfo, propname) in schema['properties']"
                :key="propname"
              >
                <JS_PropertyBox
                  :propinfo="propinfo"
                  :propname="propname"
                ></JS_PropertyBox>
              </template>
            </ul>
          </div>
        </div>
        <div v-if="schema && schema['definitions']">
          <div class="col-sm-12 bg-secondary text-light py-4">
            <h4 class="m-1">Definitions</h4>
          </div>
          <div class="col-sm-12 p-0">
            <div class="row m-0 alert-secondary">
              <template
                v-for="(info, name) in schema['definitions']"
                :key="name"
              >
                <DefinitionBox :info="info" :name="name"></DefinitionBox>
              </template>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import DefinitionBox from "~~/components/JS_DefinitionBox.vue";
import JS_PropertyBox from "~~/components/JS_PropertyBox.vue";

export default {
  name: "JSONSchemaViewer",
  head() {
    return {
      title: "DDE | JSON Schema Viewer",
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
          content: "http://discovery.biothings.io/json-schema-viewer",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/json-schema-viewer",
        },
        {
          property: "og:description",
          content:
            "Test DDE compatibility before registering a schema namespace",
        },
        {
          name: "description",
          content:
            "Test DDE compatibility before registering a schema namespace",
        },
        {
          name: "twitter:card",
          content:
            "Test DDE compatibility before registering a schema namespace",
        },
      ],
    };
  },
  data: function () {
    return {
      input: "",
      loadMsg: "Visualize Json Schema Structure",
      loading: false,
      file: {
        $schema: "http://json-schema.org/draft-07/schema#",
        type: "object",
        "@type": "schema:Dataset",
        properties: {
          name: {
            description: "Descriptive name of the dataset",
            type: "string",
          },
          description: {
            description:
              "Longer description of what is contained in the dataset",
            type: "string",
          },
          measurementTechnique: {
            description:
              "A technique or technology used in a Dataset, corresponding to the method used for measuring the corresponding variable(s).",
            oneOf: [
              {
                $ref: "#/definitions/controlledVocabulary",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/controlledVocabulary",
                },
              },
            ],
          },
          identifier: {
            description:
              "Longer description of what is contained in the dataset",
            type: "string",
          },
          creator: {
            description:
              "Name of the author or organization that created the dataset.  Note: schema.org/creator and schema.org/organization have additional fields that can provide more information about the author/organization, if desired.",
            oneOf: [
              {
                $ref: "#/definitions/person",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/person",
                },
              },
            ],
          },
          distribution: {
            description:
              "DataDownload objects, which contain the URL link to download the raw, analyzed, and summary data associated with the dataset as well as associated metadata for the file.",
            oneOf: [
              {
                $ref: "#/definitions/dataDownload",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/dataDownload",
                },
              },
            ],
          },
          citation: {
            description:
              "Journal article or other publication associated with the dataset (stored as an object, not a string)",
            oneOf: [
              {
                $ref: "#/definitions/article",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/article",
                },
              },
            ],
          },
          funding: {
            description:
              "Funding that supports (sponsors) the collection of this dataset through some kind of financial contribution",
            oneOf: [
              {
                $ref: "#/definitions/funder",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/funder",
                },
              },
            ],
          },
          license: {
            description:
              "A license document that applies to this content, typically indicated by URL.",
            type: "string",
            format: "uri",
          },
          species: {
            description: "Species(es) from which dataset has been collected",
            oneOf: [
              {
                $ref: "#/definitions/miscControlledVocabulary",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/miscControlledVocabulary",
                },
              },
            ],
          },
          pathogen: {
            description: "Pathogen(s) which are the focus of the dataset",
            oneOf: [
              {
                $ref: "#/definitions/miscControlledVocabulary",
              },
              {
                type: "array",
                items: {
                  $ref: "#/definitions/miscControlledVocabulary",
                },
              },
            ],
          },
        },
        required: [
          "name",
          "description",
          "measurementTechnique",
          "creator",
          "distribution",
          "funding",
        ],
        definitions: {
          person: {
            description: "Reusable person definition",
            "@type": "Person",
            type: "object",
            properties: {
              name: {
                type: "string",
              },
            },
            required: ["name"],
          },
          controlledVocabulary: {
            description: "collection of vocabulary terms defined in ontologies",
            "@type": "CreativeWork",
            type: "string",
            vocabulary: {
              ontology: ["edam", "ncit"],
              children_of: [
                "http://edamontology.org/topic_3361",
                "http://purl.obolibrary.org/obo/NCIT_C20368",
              ],
            },
            strict: false,
          },
          miscControlledVocabulary: {
            description: "collection of vocabulary terms defined in ontologies",
            "@type": "CreativeWork",
            type: "string",
            vocabulary: {
              ontology: ["ncbitaxon"],
              children_of: [
                "http://purl.obolibrary.org/obo/NCBITaxon_10239",
                "http://purl.obolibrary.org/obo/NCBITaxon_131567l",
              ],
            },
            strict: false,
          },
          funder: {
            type: "object",
            "@type": "Organization",
            description: "Information about a single funder",
            properties: {
              name: {
                type: "string",
                description:
                  "An organization associated with a creator or funder of a dataset",
              },
              identifier: {
                type: "string",
                description:
                  "Unique identifier(s) for the grant(s) used to fund the Dataset",
              },
              description: {
                type: "string",
                description: "description about the funding organization",
              },
              url: {
                type: "string",
                description: "award URL",
              },
              parentOrganization: {
                type: "string",
                description: "name of the parent funding organization",
              },
            },
            required: ["name", "identifier"],
          },
          dataDownload: {
            description: "A dataset in downloadable form.",
            "@type": "DataDownload",
            type: "object",
            properties: {
              dateModified: {
                type: "string",
                format: "date",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["dateModified", "url"],
          },
          article: {
            description: "A scholarly article in which the dataset is cited.",
            "@type": "ScholarlyArticle",
            type: "object",
            properties: {
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["url"],
          },
        },
      },
    };
  },
  components: {
    DefinitionBox,
    JS_PropertyBox,
  },
  computed: {
    schema: function () {
      return this.$store.getters.getSchemaJSV;
    },
    schemaType: function () {
      return this.$store.getters.getType;
    },
  },
  methods: {
    loadSchema(ex) {
      let self = this;

      if (ex) {
        self.loadMsg = `<b class="text-success">Example loaded</b>`;
        let payload = {};
        payload["schema"] = self.file;
        this.$store.commit("saveSchemaJSV", payload);
      } else if (self.input) {
        axios
          .get(self.input)
          .then((res) => {
            console.log(res.data);
            let schema = res.data;
            if (schema && schema.hasOwnProperty("$schema")) {
              self.loadMsg = `<b class="text-success">Schema loaded</b>`;
              payload = {};
              payload["schema"] = schema;
              this.$store.commit("saveSchemaJSV", payload);
            } else if (schema && schema.hasOwnProperty("@context")) {
              self.loadMsg = `<b class="text-danger">ATTENTION! File is JSON-LD and only visualized partially. You should visualize this here: <a href="/schema-playground">Schema Playground</a> for a complete visualization.</b>`;
              if (schema && schema["@graph"]) {
                options = {};
                optionsLabels = {};
                for (var i = 0; i < schema["@graph"].length; i++) {
                  if (schema["@graph"][i].hasOwnProperty("$validation")) {
                    options[schema["@graph"][i]["rdfs:label"]] =
                      schema["@graph"][i];
                    optionsLabels[schema["@graph"][i]["rdfs:label"]] =
                      schema["@graph"][i]["rdfs:label"];
                  }
                }
                console.log("options", options);
                this.$swal.fire({
                  title: "Which would you like to visualize?",
                  input: "select",
                  inputOptions: optionsLabels,
                  inputPlaceholder: "Select a Class",
                  showCancelButton: true,
                  inputValidator: (value) => {
                    return new Promise((resolve) => {
                      console.log("value", value);
                      if (value) {
                        payload = {};
                        payload["schema"] = options[value]["$validation"];
                        this.$store.commit("saveSchemaJSV", payload);
                        resolve();
                      }
                    });
                  },
                });
              }
            } else {
              self.loadMsg = `<b class="text-danger">File is not JSON Schema Structure or JSON-LD</b>`;
            }
          })
          .catch((err) => {
            throw err;
          });
      }
    },
  },
};
</script>
