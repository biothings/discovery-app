<template>
  <div
    class="m-1 rounded text-dark bg-light"
    :style="style"
    style="min-width: 45%"
  >
    <button
      v-if="!isChild"
      @click="expand = !expand"
      :class="[expand ? 'btn-primary' : 'btn-dark']"
      class="btn btn-sm d-block w-100 rounded-0"
    >
      <b v-text="optionName"></b>
      <small
        class="text-warning ml-1"
        v-text="!expand ? 'show' : 'hide'"
      ></small>
    </button>
    <template v-if="expand">
      <div class="alert-light" v-if="!option.items">
        <h6
          class="m-0"
          v-if="option && option['@type']"
          v-text="option['@type']"
        ></h6>
        <small
          v-if="option && option.description"
          v-text="option.description"
        ></small>
      </div>
      <small
        class="badge badge-pill badge-dark text-warning m-2"
        v-text="option.type == 'string' ? 'string' : ''"
      ></small>
      <!-- 🌈 VOCAB 🌈 -->
      <div v-if="option && option.vocabulary" class="text-center p-1">
        <button
          type="button"
          class="btn btn-sm btn-success text-light m-1"
          @click="testOntologyLookup()"
        >
          <small
            class="badge"
            :class="[option.strict ? 'badge-danger' : 'badge-info']"
          >
            <b v-text="option.strict ? 'STRICT' : 'NON-STRICT'"></b>
          </small>
          Term Lookup <font-awesome-icon icon="fas fa-search" />
        </button>
        <table class="table table-sm table-striped text-left">
          <thead>
            <th>Examples:</th>
          </thead>
          <tbody>
            <tr v-for="(example, i) in ontologyExamples" :key="i + 'ont'">
              <td>
                <small
                  v-text="example.label"
                  :data-tippy-content="JSON.stringify(example, null, 2)"
                ></small>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- 🌈 OBJECT 🌈 -->
      <div v-if="option && option.properties">
        <ObjectBox
          :properties="option.properties"
          :required="option.required"
        ></ObjectBox>
      </div>
      <!-- 🌈 ENUM 🌈 -->
      <div v-if="option && option.enum">
        <Enumeration :enumeration="option.enum"></Enumeration>
      </div>
      <!-- 🌈 LIST OF 🌈 -->
      <div v-if="option.items" class="bg-light p-1">
        <b class="text-muted font-weight-bold">LIST OF:</b>
        <OneOf :name="name" :option="option.items" :isChild="true"></OneOf>
      </div>
    </template>
  </div>
</template>

<script>
import axios from "axios";
import tippy from "tippy.js";
import Enumeration from "~~/components/Enumeration.vue";
import ObjectBox from "~~/components/ObjectBox.vue";

export default {
  name: "OneOF",
  components: {
    Enumeration,
    ObjectBox,
  },
  data: function () {
    return {
      expand: false,
      style: {},
      ontologyExamples: [],
    };
  },
  props: ["option", "name", "isChild"],
  methods: {
    getRandomColor() {
      let self = this;
      var letters = "0123456789ABCDEF";
      var color = "#";
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      self.style = {
        "border-color": color,
        "border-width": "3px",
        "border-style": "solid",
      };
    },
    testOntologyLookup() {
      var self = this;

      self.$swal
        .fire({
          title: self.name,
          text: "Search for an existing term here:",
          input: "text",
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#4a7d8f",
          animation: false,
          customClass: "scale-in-center",
          inputAttributes: {
            autocapitalize: "off",
          },
          showCancelButton: true,
          confirmButtonText: "Look up",
          showLoaderOnConfirm: true,
          focusConfirm: false,
          preConfirm: (query) => {
            let ontologies = self.option["vocabulary"]["ontology"].toString();
            let children = self.option["vocabulary"]["children_of"].toString();

            let url =
              `https://www.ebi.ac.uk/ols4/api/search?q=` +
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
                self.$swal.showValidationMessage(`Request failed: ${error}`);
              });
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
          backdrop: true,
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

            self.$swal.fire({
              title: "Top 10 Results",
              html: html,
              confirmButtonColor: "#63296b",
              cancelButtonColor: "#4a7d8f",
              animation: false,
              customClass: "scale-in-center",
            });
          }
        });
    },
    getTermExamples() {
      let self = this;
      let query = "gene OR chemical";
      let ontologies = self.option["vocabulary"]["ontology"].toString();
      let children = self.option["vocabulary"]["children_of"].toString();

      if (ontologies) {
        let url =
          `https://www.ebi.ac.uk/ols4/api/search?q=` +
          query +
          "&ontology=" +
          ontologies +
          "&childrenOf=" +
          children +
          "&type=class&fieldList=id,iri,label,description,obo_id,short_form,ontology_prefix" +
          "&queryFields=label" +
          "&rows=5";

        axios
          .get(url)
          .then((res) => {
            self.ontologyExamples = res.data.response.docs;
          })
          .catch((err) => {
            throw err;
          });
      } else {
        self.ontologyExamples = [{ label: "No examples available" }];
      }
    },
  },
  computed: {
    optionName: function () {
      let self = this;
      if (
        self.option.hasOwnProperty("items") &&
        self.option["items"].hasOwnProperty("@type")
      ) {
        return "List of " + self.option["items"]["@type"] + "(s)";
      } else if (
        self.option.hasOwnProperty("items") &&
        self.option["items"].hasOwnProperty("type")
      ) {
        return "List of " + self.option["items"]["type"] + "(s)";
      } else if (
        self.option.hasOwnProperty("@type") ||
        self.option.hasOwnProperty("type")
      ) {
        return self.option["@type"] || self.option["type"];
      } else if (self.option.hasOwnProperty("enum")) {
        return "enum item";
      } else {
        return "item";
      }
    },
  },
  mounted: function () {
    var self = this;
    // console.log(self.name, self.option)

    if (self.isChild) {
      self.style = {
        "border-color": "#e1e1e1",
        "border-width": "3px",
        "border-style": "solid",
      };
    } else {
      self.getRandomColor();
    }
    if (Object.hasOwnProperty.call(this.option, "vocabulary")) {
      self.getTermExamples();
    }
    if (self.isChild) {
      self.expand = true;
    }
  },
};
</script>
