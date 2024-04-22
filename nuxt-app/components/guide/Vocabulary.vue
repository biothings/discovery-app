<template>
  <div class="row m-0 w-100 vocab-box">
    <div class="col-sm-12 mainBackLight text-light p-1 text-center classTab">
      <h5 class="m-0" v-text="main_name"></h5>
    </div>
    <div v-if="loading" class="loader">
      <img src="@/assets/img/ripple.svg" />
    </div>
    <!-- 🍏 SEARCH 🍏-->
    <div class="col-sm-12 p-1 bg-dark">
      <input
        type="text"
        class="form-control w-100"
        v-model="query"
        :placeholder="'Search ' + main_name + '(s)'"
      />
    </div>
    <!-- 🍏 RESULTS 🍏-->
    <div class="col-sm-12 p-1">
      <div class="row" v-if="results.length">
        <div class="col-sm-6">
          <small class="text-secondary m-1 d-block"
            >(<b v-text="results.length"></b>) Results:</small
          >
        </div>
        <div class="col-sm-6">
          <input
            type="text"
            class="form-control form-control-sm w-100"
            v-model="filter"
            placeholder="Filter Results"
          />
        </div>
      </div>
    </div>
    <div
      class="col-sm-12 p-2 mb-1 alert-secondary"
      style="max-height: 450px; overflow-y: scroll; word-break: break-all"
    >
      <table class="table table-sm table-hover">
        <tbody>
          <template v-for="result in results">
            <tr
              @click="addResult(result)"
              class="alert alert-light border-bottom p-1 m-0 rounded-0 pointer"
            >
              <th>
                <font-awesome-icon
                  icon="fas fa-plus"
                  class="text-success"
                ></font-awesome-icon>
              </th>
              <td><small v-text="result.label"></small></td>
              <td>
                <font-awesome-icon
                  icon="fas fa-info-circle"
                  class="text-info vocabTip"
                  :data-tippy-content="JSON.stringify(result, null, 2)"
                ></font-awesome-icon>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      <template v-if="!results.length">
        <h1 class="text-center">
          <font-awesome-icon
            icon="fas fa-search"
            class="text-muted"
          ></font-awesome-icon>
        </h1>
        <div v-if="query" class="text-center alert alert-light">
          <!-- 🍏 CUSTOM NON STRICT 🍏-->
          <template v-if="vocabInfo && !vocabInfo.strict">
            <small class="text-muted d-block">No results</small>
            <small
              @click="addCustomVocab()"
              class="text-primary pointer d-block"
              >Add <b class="text-danger" v-text="query"></b> anyway</small
            >
          </template>
        </div>
      </template>
    </div>
    <!-- 🍏 SELECTED 🍏-->
    <div class="col-sm-12 m-0 bg-light rounded-0 p-2" v-if="selected.length">
      <small class="text-success m-1 d-block"
        >(<b v-text="selected.length"></b>) Selected:</small
      >
      <div class="row m-0">
        <div
          class="col-sm-12 rounded border border-secondary alert-success p-1"
        >
          <template v-for="item in selected">
            <span
              class="badge badge-success m-1 vocabTip"
              @click="removeResult(item)"
              :data-tippy-content="JSON.stringify(item, null, 2)"
            >
              <span v-text="item.label || item.name || item"></span>
              <b class="text-danger">&times;</b>
            </span>
          </template>
        </div>
        <div class="col-sm-12 pt-1">
          <button
            :disabled="!selected.length"
            @click="submitVocab"
            type="button"
            class="btn w-100"
            :class="[selected.length ? 'btn-success' : 'btn-secondary']"
          >
            <span v-text="'Add ' + main_name + '(s)'"></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";
import { mapActions } from "pinia";
import { useGuideStore } from "../../stores/guide";

export default {
  name: "Vocabulary",
  data: function () {
    return {
      query: "",
      loading: false,
      selected: [],
      results: [],
      vocabInfo: {},
      filter: "",
    };
  },
  props: ["main_name", "info"],
  methods: {
    ...mapActions(useGuideStore, ["addToArrayFrom", "saveProgress"]),
    lookup(query, vocabInfo) {
      let self = this;

      query = query.includes(" ") ? query.replace(" ", " AND ") : query;

      let ontologies = vocabInfo["vocabulary"]["ontology"].toString();
      let children = vocabInfo["vocabulary"]["children_of"].toString();
      let url =
        `https://www.ebi.ac.uk/ols4/api/search?q=${query}` +
        "&ontology=" +
        ontologies +
        "&childrenOf=" +
        children +
        "&type=class&fieldList=id,iri,label,description,obo_id,short_form,ontology_prefix" +
        "&queryFields=label" +
        "&rows=100";

      self.results = [];
      self.loading = true;

      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          self.results = data.response.docs;
          self.loading = false;
        })
        .catch((err) => {
          self.loading = false;
          Swal.showValidationMessage(`Request failed: ${err}`);
        });
    },
    addResult(r) {
      let self = this;
      if (r.hasOwnProperty("label")) {
        var exists = self.selected.filter((obj) => {
          return obj["label"] === r["label"];
        });
        if (!exists.length) {
          self.selected.push(r);
        } else {
          Swal.fire({
            type: "error",
            toast: true,
            title: `Already added`,
            showConfirmButton: false,
            timer: 2000,
          });
        }
      } else {
        self.selected.push(r);
      }
    },
    removeResult(r) {
      let self = this;
      let res = [];
      res = _.filter(self.selected, function (o) {
        return o.label !== r.label;
      });
      self.selected = res;
    },
    filterResults(f) {
      let self = this;
      let res = [];
      f = f.toLowerCase();
      res = _.filter(self.results, function (o) {
        return o.label.toLowerCase().includes(f);
      });
      if (res.length) {
        self.results = res;
      }
    },
    submitVocab() {
      let self = this;
      if (self.selected.length) {
        self.selected.forEach((item) => {
          var payload = {};
          payload["item"] = self.getItem(item);
          payload["from"] = self.main_name;
          self.addToArrayFrom(payload);
          self.saveProgress();
        });
        self.selected = [];
        self.results = [];
        self.query = "";
        self.filter = "";
      }
    },
    getItem(item) {
      let self = this;
      if (item.constructor === String) {
        return item;
      } else if (item.constructor === Object) {
        switch (self.vocabInfo.type) {
          case "string":
            return item.iri;
            break;
          case "object":
            return self.formObject(self.vocabInfo.properties, item);
            break;
          default:
            return item.iri;
            break;
        }
      }
    },
    formObject(props, item) {
      for (key in props) {
        switch (key) {
          case "identifier":
            item[key] = item.iri || item.label;
            break;
          case "name":
            item[key] = item.label;
            break;
          case "url":
            item[key] = item.iri || item.label;
            break;
          default:
            item[key] = item.iri || item.label;
            break;
        }
      }
      return item;
    },
    addCustomVocab() {
      this.selected.push(this.query);
    },
  },
  watch: {
    query: function (q) {
      this.lookup(q, this.vocabInfo);
    },
    filter: function (f) {
      if (f) {
        this.filterResults(f);
      } else {
        this.lookup(this.query, this.vocabInfo);
      }
    },
  },
  mounted: function () {
    let self = this;

    tippy(".vocabTip", {
      placement: "right-end",
      animation: "fade",
      theme: "light",
      onShow(instance) {
        let info = instance.reference.dataset.tippyInfo;

        function getContent(value) {
          return value.constructor === String
            ? value
            : JSON.stringify(value, null, 2);
        }
        // REGULAR TIP DESCRIPTION
        try {
          let json = JSON.parse(info);
          let html = "";
          for (key in json) {
            html +=
              `<tr>
                            <td><small><b>` +
              key +
              `</b></small></td>
                            <td style="word-break:break-all;"><small>` +
              getContent(json[key]) +
              `</small></td>
                          </tr>`;
          }
          instance.setContent(
            "<table class='table table-sm table-striped'>" + html + "</table>"
          );
        } catch (err) {
          instance.setContent(
            "<div class='text-info text-left m-0 p-1 bg-white'><pre style='margin:0px !important;word-break:break-all;'>" +
              info +
              "</pre></div>"
          );
        }
      },
    });

    if (self.info.hasOwnProperty("vocabulary")) {
      self.vocabInfo = self.info;
    }
    if (self.info.hasOwnProperty("oneOf")) {
      self.info["oneOf"].forEach((op) => {
        if (op.hasOwnProperty("vocabulary")) {
          self.vocabInfo = op;
        }
      });
    }
    if (self.info.hasOwnProperty("anyOf")) {
      self.info["anyOf"].forEach((op) => {
        if (op.hasOwnProperty("vocabulary")) {
          self.vocabInfo = op;
        }
      });
    }
  },
};
</script>
