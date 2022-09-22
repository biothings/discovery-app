<template>
  <div class="p-1" style="width: 90px; height: 90px">
    <div class="text-center">
      <small :class="[name === 'Required' ? 'text-danger' : 'text-muted']">
        <span v-text="name"></span>
      </small>
    </div>
    <canvas :id="uniqueID"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

export default {
  name: "Chart",
  data: function () {
    return {
      shouldHighlight: false,
      myChart: null,
      uniqueID: Math.floor(Math.random()*90000) + 10000,
    };
  },
  props: ["name", "totals", "unique", "maincategory"],
  methods: {
    visualize() {
      var self = this;
      let progressColor = self["totals"]["todo"] === 0 ? "#28A744" : "#17A2B7";
      let mainColor = self.name === "Required" ? "#9fa7aa" : "#b4b7b8";
      Chart.register(...registerables);
      self.myChart = new Chart(document.getElementById(self.uniqueID), {
        type: "pie",
        maintainAspectRatio: false,
        responsive: true,
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
          plugins: {
            title: {
              display: false,
            },
            legend: {
              display: false,
            },
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
      var payload = {};
      payload["category"] = this.maincategory;
      payload["subcategory"] = this.name;
      this.$store.commit("highlight", payload);
    },
    updateChart(data) {
      this.myChart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
      });
      let progressColor = data["todo"] === 0 ? "#28A744" : "#17A2B7";
      let mainColor = this.name === "Required" ? "#9fa7aa" : "#b4b7b8";
      this.myChart.data.datasets = [
        {
          backgroundColor: [progressColor, mainColor],
          data: [data["completed"], data["todo"]],
        },
      ];
      this.myChart.update();
    },
  },
  watch: {
    totals: function (n) {
      // this.updateChart(n);
      this.myChart.destroy();
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
  },
};
</script>
