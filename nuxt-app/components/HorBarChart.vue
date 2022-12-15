<template>
  <div class="p-1">
    <canvas :id="name"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

export default {
  name: "Chart",
  data: function () {
    return {
      myChart: null,
    };
  },
  props: ["name", "totals"],
  methods: {
    getRandomColor() {
      var letters = "0123456789ABCDEF";
      var color = "#";
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    getColors(vals) {
      return vals.map((v) => {
        return v == 100
          ? "#52bf5d"
          : v >= 50
          ? "#c8e856"
          : v >= 30
          ? "#d6c45c"
          : v >= 20
          ? "#e89f56"
          : "#f44335";
      });
    },
    visualize() {
      Chart.register(...registerables);
      this.myChart = new Chart(document.getElementById(this.name), {
        type: "bar",
        data: {
          labels: Object.keys(this.totals.coverage),
          datasets: [
            {
              backgroundColor: this.getColors(
                Object.values(this.totals.coverage)
              ),
              data: Object.values(this.totals.coverage),
            },
          ],
        },
        options: {
          indexAxis: "y",
          // Elements options apply to all of the options unless overridden in a dataset
          // In this case, we are setting the border of each horizontal bar to be 2px wide
          elements: {
            bar: {
              borderWidth: 2,
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Coverage %",
              },
            },
          },
          responsive: true,
          plugins: {
            legend: {
              display: false,
            },
            title: {
              display: true,
              text: `${this.name} (${this.totals.count || "N/A"})`,
              color: "#63296b",
              font: {
                size: 22,
              },
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return context.raw + "%";
                },
              },
            },
          },
        },
      });
    },
  },
  watch: {
    totals: function (n) {
      this.myChart.destroy();
      this.visualize();
    },
  },
  mounted: function () {
    this.visualize();
  },
};
</script>
