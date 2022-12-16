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
          ? "#BCE42D"
          : v >= 20
          ? "#F5DE5E"
          : v >= 10
          ? "#FFA244"
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
              barThickness: 8,
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
              borderWidth: 0,
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Field Coverage %",
              },
            },
          },
          responsive: true,
          plugins: {
            legend: {
              display: false,
            },
            title: {
              display: false,
              text: `${this.name} (N=${this.totals.count || "N/A"})`,
              color: "#63296b",
              font: {
                size: 22,
                weight: "normal",
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
    sortObj(obj) {
      let sortable = [];
      for (var key in obj) {
        sortable.push([key, obj[key]]);
      }
      sortable.sort(function (a, b) {
        return a[1] - b[1];
      });
      sortable = sortable.reverse();
      let objSorted = {};
      sortable.forEach(function (item) {
        objSorted[item[0]] = item[1];
      });
      return objSorted;
    },
  },
  watch: {
    totals: function (n) {
      this.myChart.destroy();
      this.visualize();
    },
  },
  mounted: function () {
    this.totals.coverage = this.sortObj(this.totals.coverage);
    this.visualize();
  },
};
</script>
