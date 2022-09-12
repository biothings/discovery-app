<template>
  <div class="col-sm-12 py-3 text-left border-bottom border-info" :id="name">
    <div class="">
      <i
        class="fas fa-tiny fa-code text-muted float-right"
        :data-tippy-content="JSON.stringify(info, null, 2)"
      ></i>
      <a :href="'#' + name">
        <h6 v-text="name" class="font-weight-bold d-inline"></h6>
      </a>

      <small class="text-muted ml-3" v-text="info['description']"></small>
    </div>
    <div class="d-flex rounded-0">
      <div
        class="text-dark px-5 py-3 d-flex justify-content-center align-items-center"
      >
        <small>
          TAKES <i class="fas fa-chevron-right"></i>
          <i class="fas fa-chevron-right"></i>
        </small>
      </div>
      <div class="p-1 rounded-0">
        <!-- VOCABULARY -->

        <div
          v-if="info && info.vocabulary"
          class="d-flex justify-content-center align-items-center"
        >
          <div class="d-flex">
            <div class="d-flex justify-content-center align-items-center">
              <div>
                <div
                  class="badge badge-pill badge-dark m-1"
                  v-if="info['type'] == 'array'"
                  data-tippy-content="Array"
                >
                  A List
                </div>
                <div
                  class="badge badge-pill badge-dark m-1"
                  v-if="info['type'] == 'string'"
                  data-tippy-content="String"
                >
                  A String
                </div>
                <div
                  class="badge badge-pill badge-dark m-1"
                  v-if="info['type'] == 'object'"
                  data-tippy-content="Object"
                >
                  An Object
                </div>
                <div
                  class="badge badge-pill badge-dark m-1"
                  v-if="info['type'] == 'number'"
                  data-tippy-content="Number"
                >
                  A Number
                </div>
                <div
                  class="badge badge-pill badge-dark m-1"
                  v-if="info['type'] == 'boolean'"
                  data-tippy-content="Boolean"
                >
                  A Boolean T/F
                </div>
                <small
                  class="badge badge-secondary text-light"
                  v-text="info['format']"
                ></small>
              </div>
              <div class="d-flex justify-content-center align-items-center">
                <i class="fas fa-caret-right m-1 text-dark"></i>
              </div>
              <div class="d-flex justify-content-center align-items-center">
                <span class="mainTextDark">
                  <span class="badge badge-light m-1">type</span>
                  <span v-text="info['@type']"></span>
                </span>
              </div>
            </div>
            <div class="d-flex justify-content-center align-items-center">
              <i class="fas fa-chevron-right m-1 mainTextLight"></i>
            </div>
            <div class="d-flex justify-content-center align-items-center px-2">
              <div>
                <small class="text-muted d-block">
                  <b
                    class="text-danger font-weight-bold"
                    v-text="info.strict ? 'MUST' : 'CAN'"
                  ></b>
                  be from ontologies:
                </small>
                <template v-for="(ont, i) in info.vocabulary.ontology" :key="i">
                  <span class="text-info caps m-1 font-weight-bold">
                    <i class="fas fa-star fa-xs"></i> <i v-text="ont"></i>
                  </span>
                </template>
              </div>
            </div>
            <div class="d-flex justify-content-center align-items-center">
              <i class="fas fa-chevron-right m-1 mainTextLight"></i>
            </div>
            <div class="d-flex justify-content-center align-items-center px-2">
              <div>
                <small class="text-muted d-block"> children of: </small>
                <template
                  v-for="(ont, i) in info.vocabulary.children_of"
                  :key="i"
                >
                  <a
                    class="badge badge-primary d-block m-1 text-left"
                    :href="ont"
                    target="_blank"
                    rel="nonreferrer"
                  >
                    <small v-text="ont"></small>
                  </a>
                </template>
              </div>
            </div>
            <div
              class="d-flex justify-content-center align-items-center px-2 border-left border-info"
            >
              <a
                role="button"
                class="btn btn-sm btn-info text-light"
                @click="testOntologyLookup()"
                >Try It <i class="fas fa-chevron-right"></i
              ></a>
            </div>
          </div>
        </div>

        <!-- OBJECT -->

        <div v-if="info && info.type == 'object'">
          <div class="d-flex">
            <div class="d-flex justify-content-center align-items-center">
              <div
                class="badge badge-pill badge-dark m-1"
                data-tippy-content="Object"
              >
                An Object
              </div>
              <div class="d-flex justify-content-center align-items-center">
                <i class="fas fa-chevron-right m-1 text-dark"></i>
              </div>
              <span class="mainTextDark">
                <span class="badge badge-light m-1">type</span>
                <span v-text="info['@type']"></span>
              </span>
            </div>
            <div class="d-flex justify-content-center align-items-center">
              <i class="fas fa-chevron-right m-1 mainTextLight"></i>
            </div>
            <div class="d-flex justify-content-center align-items-center">
              <div class="border-left border-info pl-3">
                <template
                  v-for="(value, name) in info['properties']"
                  :key="name"
                >
                  <div class="border-left border-secondary my-3 pl-2">
                    <small class="mainTextDark"
                      ><i class="fas fa-circle"></i> <b v-text="name"></b
                    ></small>
                    <span
                      v-if="isRequired(name)"
                      class="text-danger caps"
                      style="zoom: 0.5"
                      >is required</span
                    >

                    <i class="fas fa-caret-right m-1 text-dark"></i>

                    <small
                      class="badge badge-pill alert-dark"
                      v-text="info['properties'][name]['type']"
                    ></small>
                    <small
                      class="badge badge-pill alert-light"
                      v-text="info['properties'][name]['format']"
                    ></small>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";

export default {
  name: "DefinitionBox",
  data: function () {
    return {
      userSchema: [],
      textColor: "",
      backColor: "",
      query: "",
      results: [],
    };
  },
  props: ["name", "info"],
  methods: {
    isRequired(name) {
      var self = this;
      if (
        self.info.hasOwnProperty("required") &&
        self.info["required"].includes(name)
      ) {
        return true;
      }
      return false;
    },
    testOntologyLookup() {
      var self = this;

      this.$swal
        .fire({
          title: self.name,
          text: "Search for an existing term here:",
          input: "text",
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
          animation: false,
          customClass: "scale-in-center",
          inputAttributes: {
            autocapitalize: "off",
          },
          backdrop: true,
          showCancelButton: true,
          confirmButtonText: "Look up",
          showLoaderOnConfirm: true,
          focusConfirm: false,
          preConfirm: (query) => {
            let ontologies = self.info["vocabulary"]["ontology"].toString();
            let children = self.info["vocabulary"]["children_of"].toString();

            let url =
              `https://www.ebi.ac.uk/ols/api/search?q=` +
              query +
              "&ontology=" +
              ontologies +
              "&childrenOf=" +
              children +
              "&type=class&fieldList=id,iri,label,description,obo_id,short_form,ontology_prefix" +
              "&queryFields=label" +
              "&rows=10";

            return fetch(url)
              .then((response) => {
                if (!response.ok) {
                  throw new Error(response.statusText);
                }
                return response.json();
              })
              .catch((error) => {
                this.$swal.showValidationMessage(`Request failed: ${error}`);
              });
          },
          allowOutsideClick: () => !this.$swal.isLoading(),
        })
        .then((result) => {
          if (result.value) {
            let html = "<div id='ontology' class='p-1 text-left'>";

            for (var i = 0; i < result.value.response.docs.length; i++) {
              tippy("#cb" + i, {
                content: result.value.response.docs[i],
              });

              let label = result.value.response.docs[i]["label"];
              if (label && label.length > 37) {
                label = label.substring(0, 37) + "...";
              }

              html +=
                `<div class="form-check">
                      <label class="form-check-label" for="cb` +
                i +
                `" title="` +
                result.value.response.docs[i]["label"] +
                `">
                          ` +
                label +
                `
                          <i class="fa fa-info-circle text-info modaltip" data-tippy-content='` +
                JSON.stringify(result.value.response.docs[i]) +
                `'></i>
                      </label>
                    </div>`;
            }
            html += "</div>";

            this.$swal.fire({
              title: "Top 10 Results",
              html: html,
              confirmButtonColor: "{{color_main}}",
              cancelButtonColor: "{{color_sec}}",
              animation: false,
              customClass: "scale-in-center",
            });
          }
        });
    },
  },
  mounted: function () {
    var self = this;
    if (self.parent) {
      self.textColor = "mainTextLight";
      self.backColor = "mainBackLight";
    } else {
      self.textColor = "mainTextDark";
      self.backColor = "mainBackDark";
    }
  },
};
</script>
