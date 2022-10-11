<template>
  <div>
    <input
      type="text"
      v-model="userInput"
      class="form-control"
      placeholder="enter text here"
    />
    <div v-if="hitResults" class="row m-0 alert-dark">
      <div class="col-sm-12">
        <small
          @click.prevent="hitResults = false"
          class="float-right pointer m-1 text-danger"
          >dismiss</small
        >
      </div>
      <div class="col-sm-12" style="max-height: 200px; overflow-y: scroll">
        <h6 v-if="window.location.href.includes('n3c')" class="text-muted mt-2">
          <font-awesome-icon
            icon="fas fa-exclamation-circle"
            class="text-info"
          ></font-awesome-icon>
          Similar Dataset(s) found. Avoid submitting duplicate dataset requests.
        </h6>
        <h6 v-else class="text-muted mt-2">
          <font-awesome-icon
            icon="fas fa-exclamation-circle"
            class="text-info"
          ></font-awesome-icon>
          Similar Dataset(s) found:
        </h6>
        <table class="table table-sm table-striped">
          <tbody>
            <template v-for="hit in hits">
              <tr class="m-1">
                <b class="d-block">
                  <small>
                    <span class="text-dark" v-text="hit.name"></span>.
                    <a :href="'/dataset/' + hit['_id']" target="_blank"
                      >Show me this dataset
                      <font-awesome-icon
                        icon="fas fa-chevron-right"
                      ></font-awesome-icon
                    ></a>
                  </small>
                </b>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

export default {
  name: "NameSpecial",
  data: function () {
    return {
      hits: [],
      hitResults: false,
    };
  },
  props: ["info", "name"],
  computed: {
    userInput: {
      get() {
        return this.$store.getters.getValidationValue(this.name);
      },
      set(newValue) {
        var payload = {};
        if (name.includes("date")) {
          let v = moment(newValue).format("YYYY-MM-DD");
          payload["completed"] = { name: this.name, value: v };
        } else {
          payload["completed"] = { name: this.name, value: newValue };
        }
        this.$store.commit("markCompleted", payload);
        this.$store.dispatch("saveProgress");
      },
    },
  },
  watch: {
    userInput: function (v) {
      v && v.length > 10 ? this.look_existing(v) : (this.hits = []);
    },
  },
  methods: {
    look_existing(q) {
      let self = this;
      let config = useRuntimeConfig();
      axios
        .get(
          config.public.apiUrl +
            `/api/dataset/query?size=100&q=name:${q}&meta=true`
        )
        .then((res) => {
          let portal_hits = [];
          res.data.hits.forEach((hit) => {
            if (
              hit["_meta"].hasOwnProperty("guide") &&
              hit["_meta"]["guide"] == window.location.pathname
            ) {
              portal_hits.push(hit);
            }
          });
          self.hits = portal_hits;
          self.hits.length
            ? (self.hitResults = true)
            : (self.hitResults = false);
        })
        .catch((err) => {
          self.hitResults = false;
          throw err;
        });
    },
    loadSelected(selected) {
      this.$swal
        .fire({
          title: "Load item into form?",
          text: "You are about to edit an existing record, please make sure to revise your contributions before submitting.",
          footer:
            "[Warning] Data structure is not guaranteed to match that of this form which may result in formatting errors. For such cases clearing that field might be required.",
          animation: false,
          customClass: "scale-in-center",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          confirmButtonText: "Yes",
        })
        .then((result) => {
          if (result.value) {
            for (key in selected) {
              if (!["@context", "@type", "_id"].includes(key)) {
                var payload = {};
                if (typeof selected[key] === "object") {
                  let value = [selected[key]];
                  payload["completed"] = { name: key, value: value };
                  this.$store.commit("markCompleted", payload);
                } else {
                  let value = selected[key];
                  payload["completed"] = { name: key, value: value };
                  this.$store.commit("markCompleted", payload);
                }
              }
            }
          }
        });
    },
  },
};
</script>
