<template>
  <div
    class="m-0 rounded-0"
    :class="[isChild ? 'p-1 bg-op-2' : 'p-1 border-bottom']"
  >
    <!-- 🌈 Array 🌈 -->
    <template v-if="type == 'array'">
      <div class="row m-0">
        <div class="text-left">
          <small
            class="pointer"
            :class="[
              name == 'required' ? 'badge badge-danger' : 'mainTextDark',
            ]"
          >
            <span v-text="name"></span> (<span v-text="content.length"></span>)
          </small>
          <i
            class="fas pointer"
            @click="expandArray = !expandArray"
            :class="[
              expandArray
                ? 'fa-caret-square-down text-danger'
                : 'fa-plus-square text-primary',
            ]"
          ></i>
        </div>
        <div class="col-sm-12" v-if="expandArray">
          <div>
            <template v-if="content.length > perPage">
              <select
                class="form-control form-control-sm m-auto w-25"
                v-model="perPage"
                @change="calculatePages"
                id="perPage"
              >
                <option value="" disabled selected>Shown Per Page</option>
                <option value="10">10 per page</option>
                <option value="25">25 per page</option>
                <option value="100">100 per page</option>
              </select>
              <div class="paginati flex-wrap p-1 mt-2">
                <div class="badge rounded-0" :class="{ disabled: page <= 1 }">
                  <a class="page-link p-1" @click.prevent="prevPage()"
                    ><i class="fas fa-step-backward"></i
                  ></a>
                </div>
                <div
                  class="badge rounded-0"
                  :class="{
                    active: page == n,
                    'bg-primary': page == n,
                    'white-text': page == n,
                  }"
                  v-for="n in pages"
                >
                  <a
                    href="#"
                    class="page-link p-1"
                    @click.prevent="page = n"
                    v-text="n"
                  ></a>
                </div>
                <div
                  class="badge rounded-0"
                  :class="{ disabled: page >= pages }"
                >
                  <a class="page-link p-1" @click.prevent="nextPage()"
                    ><i class="fas fa-step-forward"></i
                  ></a>
                </div>
              </div>
            </template>
          </div>
          <template v-for="item in arrayResults">
            <field-box
              :isRequirement="name == 'required' ? true : false"
              class="m-1"
              name=""
              :content="item"
              isChild="false"
            ></field-box>
          </template>
        </div>
      </div>
    </template>
    <!-- 🌈 String 🌈 -->
    <template v-if="type == 'string'">
      <div class="d-flex">
        <template v-if="isUrl(content)">
          <div class="text-left">
            <small class="mainTextDark">
              <span v-text="name"></span
              ><i v-if="!name" class="fas fa-circle"></i> <span v-else>:</span>
            </small>
          </div>
          <div class="ml-1">
            <a :href="content" target="_blank" rel="nonreferrer">
              <i v-if="isRequirement" class="fas fa-asterisk text-danger"></i>
              <small
                ><span v-text="content"></span>
                <i class="fas fa-external-link-alt"></i
              ></small>
            </a>
          </div>
        </template>
        <template v-else>
          <div class="d-flex">
            <small class="mainTextDark">
              <span v-text="name"></span>
              <span v-if="name" class="mr-1">:</span>
              <i v-if="isRequirement" class="fas fa-asterisk text-danger"></i>
            </small>
          </div>
          <div class="d-flex">
            <a
              class="ml-1"
              v-if="isUrl(content)"
              v-text="content"
              :href="content"
              target="_blank"
              rel="nonreferrer"
            ></a>
            <template v-else>
              <small>
                <i
                  v-if="name == '@type' && content == 'Person'"
                  class="fas fa-user text-muted"
                ></i>
                <i
                  v-if="name == '@type' && content == 'Organization'"
                  class="fas fa-building text-muted"
                ></i>
                <i
                  v-if="name == '@type' && content == 'CreativeWork'"
                  class="fas fa-lightbulb text-muted"
                ></i>
              </small>
              &nbsp;
              <small
                v-if="name == 'type'"
                class="badge badge-pill badge-dark"
                v-html="content"
              ></small>
              <small
                v-else-if="name == 'format'"
                class="badge badge-pill badge-secondary"
                v-html="content"
              ></small>
              <small v-else class="text-muted" v-html="content"></small>
            </template>
          </div>
        </template>
      </div>
    </template>

    <!-- 🌈 VOCAB 🌈 -->
    <div
      v-if="content && content.vocabulary"
      class="d-flex justify-content-center align-items-center"
    >
      <div>
        <a
          role="button"
          class="btn btn-sm btn-primary text-light m-1"
          @click="testOntologyLookup()"
        >
          <small
            class="badge"
            :class="[content.strict ? 'badge-danger' : 'badge-success']"
          >
            <b v-text="content.strict ? 'STRICT' : 'NON-STRICT'"></b>
          </small>
          Test Term Lookup <i class="fas fa-chevron-right"></i>
        </a>
      </div>
    </div>

    <!-- 🌈 Object 🌈 -->
    <template v-if="type == 'object'">
      <div class="d-flex">
        <div class="d-flex justify-content-start align-items-center">
          <span
            v-if="name !== 'properties'"
            class="badge bold text-light mr-1 mainTextDark"
          >
            <span v-text="name"></span> <i class="fas fa-caret-right"></i>
          </span>
        </div>
        <div>
          <template v-for="(value, key) in content">
            <field-box :name="key" :content="value" isChild="true"></field-box>
          </template>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import tippy from "tippy.js";

export default {
  name: "FieldBoxOld",
  data: function () {
    return {
      type: "",
      expandArray: false,
      perPage: 10,
      page: 1,
      pages: 1,
    };
  },
  props: ["name", "content", "isChild", "isRequirement"],
  methods: {
    getType(content) {
      var self = this;
      if (_.isPlainObject(content)) {
        self.type = "object";
      } else if (_.isArray(content)) {
        self.type = "array";
      } else if (_.isBoolean(content)) {
        self.type = "boolean";
      } else if (_.isNumber(content)) {
        self.type = "number";
      } else if (_.isString(content)) {
        self.type = "string";
      } else {
        self.type = "IDK";
      }
    },
    isUrl(txt) {
      if (txt.includes("url") || txt.includes("http")) {
        return true;
      } else {
        return false;
      }
    },
    calculatePages: function () {
      var self = this;
      self.pages = Math.ceil(self.content.length / self.perPage);
    },
    prevPage: function () {
      var self = this;
      if (self.page > 1) self.page -= 1;
    },
    nextPage: function () {
      var self = this;
      if (self.page < self.pages) self.page += 1;
    },
    testOntologyLookup() {
      var self = this;

      self.$swal
        .fire({
          title: self.name,
          text: "Search for an existing term here:",
          input: "text",
          confirmButtonColor: "#63296b",
          cancelButtonColor: "#63296b",
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
            let ontologies = self.content["vocabulary"]["ontology"].toString();
            let children = self.content["vocabulary"]["children_of"].toString();

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
                self.$swal.showValidationMessage(`Request failed: ${error}`);
              });
          },
          allowOutsideClick: () => !self.$swal.isLoading(),
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
                            <i class="fa fa-info-circle text-info modaltip" data-tippy-info='` +
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
              cancelButtonColor: "#63296b",
              animation: false,
              customClass: "scale-in-center",
            });
          }
        });
    },
  },
  mounted: function () {
    var self = this;
    self.getType(self.content);
    if (self.type == "array") {
      self.calculatePages();
    }
    // console.log("%c "+self.name,'color:lightblue')
    // console.log("%c "+self.type,'color:yellow')
    if (self.name == "required") {
      self.expandArray = true;
    }
  },
  computed: {
    arrayResults: function () {
      var start = (this.page - 1) * this.perPage,
        end = start + this.perPage;
      return this.content && this.content.slice(start, end);
    },
  },
};
</script>
