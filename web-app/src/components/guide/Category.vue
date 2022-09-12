<template>
  <div
    class="m-1 text-center p-2 tip rounded"
    :data-tippy-content="cat"
    style="max-height: 109px; outline: none !important"
  >
    <small class="bold text-info d-block">
      <font-awesome-icon
        v-if="cat === 'Google'"
        icon="fab fa-google"
        class="googleText mr-1"
      ></font-awesome-icon>
      <span v-text="cat + ' Progress'"></span>
      <font-awesome-icon
        v-if="canRemove"
        icon="fas fa-minus-square"
        class="text-danger pointer desc"
        data-tippy-content="Remove"
        @click="removeCat()"
      ></font-awesome-icon>
    </small>
    <div class="d-flex justify-content-around" v-if="subcats">
      <template v-for="(totals, subcat) in subcats" :key="cat + subcat">
        <Chart
          class="d-inline-block"
          :name="subcat"
          :unique="cat + subcat"
          :maincategory="cat"
          :totals="totals"
        ></Chart>
      </template>
    </div>
  </div>
</template>

<script>
import Chart from "./Chart.vue";

export default {
  name: "Category",
  data: function () {
    return {
      shouldHighlight: false,
      canRemove: true,
    };
  },
  components: {
    Chart,
  },
  props: ["cat", "subcats", "totals"],
  methods: {
    removeCat() {
      var self = this;
      this.$swal
        .fire({
          title: "Are you sure you want to remove " + self.cat + "?",
          showCancelButton: true,
          animation: false,
          customClass: "scale-in-center",
          showCancelButton: true,
          confirmButtonColor: "#5C3069",
          cancelButtonColor: "#006476",
          confirmButtonText: "Yes",
        })
        .then((result) => {
          if (result.value) {
            var payload = {};
            payload["origin"] = self.cat;
            self.$store.commit("removeCategory", payload);
            self.added = false;
          }
        });
    },
  },
  mounted: function () {
    let sp = this.$store.getters.startingPoint;
    console.log(this.subcats);
    if (sp.name == this.cat) {
      this.canRemove = false;
    }
  },
};
</script>
