<template>
  <div>
    <div class="alert-info p-2 mb-2 rounded my-3">
      <small class="text-dark">
        <span class="badge badge-info">IMPORTANT</span> This field will be used to identify your resource. Please make sure that it is unique and not already in use by another resource.
      </small>
    </div>
    <span class="badge badge-info m-1" v-if="info?.oneOf">MULTIPLE ALLOWED</span>
    <div class="d-flex p-2 text-info" v-if="editingID">
      <small>This identifier is already in use.</small>
    </div>
    <input
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
          <span class="badge badge-danger m-1">WARNING</span>
          Looks like a resource with this identifier already exists:
        </h6>
        <table class="table table-sm table-striped">
          <tbody>
            <template v-for="hit in hits">
              <tr class="m-1">
                <td>
                  <b class="d-block">
                    <small>
                      <span class="text-dark" v-text="hit.name"></span>.
                      <a :href="'/resource/' + hit['_id']" target="_blank"
                        >Show me this dataset
                        <font-awesome-icon
                          icon="fas fa-chevron-right"
                        ></font-awesome-icon
                      ></a>
                    </small>
                  </b>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
        <h6 class="text-danger mt-1">
          <small
            >If you are the user that registered this resource: continuing will result in updating the resource with your changes. For all others this submission will be rejected. If you are unsure on what to do please stop and contact us.</small
          >
        </h6>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

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
    editingID: function () {
      return this.$store.getters.editingID;
    },
  },
  watch: {
    userInput: function (v) {
      v ? this.look_existing(v) : (this.hits = []);
    },
  },
  methods: {
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
