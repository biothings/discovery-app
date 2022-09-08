<template>
  <div
    class="m-1 text-center p-2 tip rounded"
    :data-tippy-info="cat"
    style="max-height: 109px; outline: none !important"
  >
    <small class="bold text-info d-block">
      <i v-if="cat === 'Google'" class="fab fa-google googleText mr-1"></i>
      <span v-text="cat + ' Progress'"></span>
      <i
        v-if="canRemove"
        class="fas fa-minus-square text-danger pointer desc"
        data-tippy-info="Remove"
        @click="removeCat()"
      ></i>
    </small>
    <div class="d-flex justify-content-around">
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
    var self = this;
    let sp = self.$store.getters.startingPoint;
    console.log(sp);
    if (sp.name == self.cat) {
      self.canRemove = false;
    }
  },
};
</script>
