<template>
  <div>
    <div class="d-flex p-2" v-if="editingID">
      <span class="fa-stack mr-2">
        <font-awesome-icon
          icon="fas fa-circle"
          class="fa-stack-2x text-info"
        ></font-awesome-icon>
        <font-awesome-icon
          icon="fas fa-lock"
          class="fa-stack-1x fa-inverse"
        ></font-awesome-icon>
      </span>
      <small class="text-primary"
        ><b class="text-danger">Edit Mode:</b> This field is disabled in order
        to override existing record.</small
      >
    </div>
    <input
      :disabled="editingID"
      type="text"
      v-model="userInput"
      class="form-control"
      placeholder="enter text here"
    />
    <div v-if="hitResults" class="row m-0 alert-warning">
      <div class="col-sm-12">
        <small
          @click.prevent="hitResults = false"
          class="float-right pointer m-1 text-danger"
          >dismiss</small
        >
      </div>
      <div class="col-sm-12" style="max-height: 200px; overflow-y: scroll">
        <h6 class="text-muted mt-2">
          <font-awesome-icon
            icon="fas fa-exclamation-circle"
            class="text-danger"
          ></font-awesome-icon>
          Looks like a dataset with this identifier already exists:
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
        <h6 class="text-dark mt-1">
          <small
            >If you are the owner of this entry this operation will result in an
            overwrite, for all others this submission will be rejected.</small
          >
        </h6>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import { mapActions, mapState } from "pinia";
import { useGuideStore } from "../../stores/guide";

export default {
  name: "IdentifierSpecial",
  data: function () {
    return {
      hits: [],
      hitResults: false,
    };
  },
  props: ["info", "name"],
  computed: {
    ...mapState(useGuideStore, ["editingID", "getValidationValue"]),
    userInput: {
      get() {
        return this.getValidationValue(this.name);
      },
      set(newValue) {
        var payload = {};
        if (name.includes("date")) {
          let v = moment(newValue).format("YYYY-MM-DD");
          payload["completed"] = { name: this.name, value: v };
        } else {
          payload["completed"] = { name: this.name, value: newValue };
        }
        this.markCompleted(payload);
        this.saveProgress();
      },
    },
  },
  watch: {
    userInput: function (v) {
      v ? this.look_existing(v) : (this.hits = []);
    },
  },
  methods: {
    ...mapActions(useGuideStore, ["markCompleted", "saveProgress"]),
    look_existing(q) {
      let self = this;
      const runtimeConfig = useRuntimeConfig();
      axios
        .get(
          runtimeConfig.public.apiUrl +
            `/api/dataset/query?size=100&q=identifier:"${encodeURIComponent(
              q
            )}"&meta=true`
        )
        .then((res) => {
          self.hits = res.data.hits;
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
                  this.markCompleted(payload);
                } else {
                  let value = selected[key];
                  payload["completed"] = { name: key, value: value };
                  this.markCompleted(payload);
                }
              }
            }
          }
        });
    },
  },
};
</script>
