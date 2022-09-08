<template>
  <div>
    <div class="text-center">
      <small :class="[name === 'Required' ? 'text-danger' : 'text-muted']">
        <span v-text="name"></span>
      </small>
    </div>
    <canvas :id="unique" width="90"></canvas>
  </div>
</template>

<script>
import tippy from "tippy.js";
import { Chart } from "chart.js";

export default {
  name: "Chart",
  data: function () {
    return {
      shouldHighlight: false,
      myChart: null,
    };
  },
  props: ["name", "totals", "unique", "maincategory"],
  methods: {
    visualize() {
      var self = this;
      let progressColor = self["totals"]["todo"] === 0 ? "#28A744" : "#17A2B7";
      let mainColor = self.name === "Required" ? "#9fa7aa" : "#b4b7b8";
      self.myChart = new Chart(document.getElementById(self.unique), {
        type: "pie",
        data: {
          labels: ["Done", "To-Do"],
          datasets: [
            {
              backgroundColor: [progressColor, mainColor],
              data: [self.totals["completed"], self.totals["todo"]],
            },
          ],
        },
        options: {
          animation: false,
          responsive: true,
          title: {
            display: false,
            text: self.name,
          },
          legend: {
            display: false,
          },
          elements: {
            arc: {
              borderWidth: 0,
            },
          },
        },
      });
    },
    highlight() {
      var self = this;

      var payload = {};
      payload["category"] = self.maincategory;
      payload["subcategory"] = self.name;
      this.$store.commit("highlight", payload);
    },
  },
  watch: {
    totals: function (n) {
      this.visualize();
    },
    shouldHighlight: function (h) {
      if (h) {
        this.highlight();
      } else {
        this.$store.commit("unhighlight");
      }
    },
  },
  mounted: function () {
    this.visualize();
    tippy(".fa-highlighter", {
      maxWidth: "200px",
      placement: "top",
      content:
        '<div class="text-muted m-0" style="border-radius:none">Highlight All</div>',
      animation: "fade",
      theme: "light",
    });
  },
};
</script>
