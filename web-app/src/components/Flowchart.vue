<template>
  <div id="flow_chart" class="bg-light rounded"></div>
</template>

<script>
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";

export default {
  name: "Flowchart",
  data: function () {
    return {
      cyto_data: [],
      cy: null,
    };
  },
  methods: {
    drawGraph() {
      var self = this;
      cytoscape.use(dagre);

      var cy = (window.cy = cytoscape({
        container: document.getElementById("flow_chart"),
        boxSelectionEnabled: false,
        autounselectify: true,
        layout: {
          name: "dagre",
          padding: 15,
        },
        style: [
          {
            selector: "node",
            style: {
              label: "data(name)",
              shape: "data(type)",
              "text-valign": "center",
              "text-halign": "center",
              height: "100px",
              padding: 10,
              "text-wrap": "wrap",
              "text-max-width": function (ele) {
                return ele.data.hasOwnProperty("mw") ? ele.data["mw"] : 200;
              },
              "background-image": "data(image)",
              "background-image-opacity": 1,
              "background-width": "100%",
              "background-height": "data(nsize)",
              "border-width": 0,
              width: "100px",
              "border-color": "white",
              height: "data(nsize)",
              width: "data(nsize)",
              "background-color": "data(color)",
              "font-size": "data(size)",
              "border-color": "black",
              "border-opacity": "1",
              "text-background-opacity": 0.5,
              "text-background-color": "white",
            },
          },
          {
            selector: "edge",
            style: {
              label: "data(name)",
              "line-color": "data(color)",
              width: 7,
              opacity: 0.7,
              "target-arrow-shape": "triangle",
              "target-arrow-color": "data(color)",
              "curve-style": "bezier",
            },
          },
        ],
        elements: self.cyto_data,
      }));

      cy.zoomingEnabled(false);
    },
    makeGraph() {
      var self = this;

      let blue = "#057BFE";
      let green = "#28A745";
      let yellow = "#FFC007";
      let red = "#F54E5B";
      let gray = "#D5D8D9";

      let data = [
        {
          group: "nodes",
          data: {
            id: 0,
            name: "I have de-identified data ready to share publicly...",
            type: "diamond",
            color: yellow,
            size: "1.5em",
            mw: 600,
            image: false,
            nsize: 60,
          },
        },
        {
          group: "nodes",
          data: {
            id: 1,
            name: "Does a relevant domain-specific repository exist?",
            type: "ellipse",
            color: gray,
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 3,
            name: "Is there a generalist repository with a schema that adequately supports my data?",
            type: "ellipse",
            color: gray,
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 5,
            name: "Can I self host the dataset?",
            type: "ellipse",
            color: gray,
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 6,
            name: "Does this repository expose schema.org compliant metadata?",
            type: "ellipse",
            color: gray,
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 7,
            name: "Register your metadata on that repository",
            type: "ellipse",
            color: "lightblue",
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 8,
            name: "Update on DDE",
            type: "ellipse",
            color: gray,
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 9,
            name: "Contact sponsor",
            type: "ellipse",
            color: "lightblue",
            size: "1em",
            image: false,
            nsize: 40,
          },
        },
        {
          group: "nodes",
          data: {
            id: 10,
            name: "Register on Data Discovery Engine",
            type: "ellipse",
            color: "white",
            size: "1em",
            image: "/pub-img/dde-logo-o.png",
            nsize: 100,
          },
        },
        {
          group: "edges",
          data: {
            source: 0,
            target: 1,
            name: "",
            color: gray,
          },
        },
        {
          group: "edges",
          data: {
            source: 1,
            target: 3,
            name: "NO",
            color: red,
          },
        },
        {
          group: "edges",
          data: {
            source: 1,
            target: 6,
            name: "YES",
            color: green,
          },
        },
        {
          group: "edges",
          data: {
            source: 3,
            target: 5,
            name: "NO",
            color: red,
          },
        },
        {
          group: "edges",
          data: {
            source: 3,
            target: 6,
            name: "YES",
            color: green,
          },
        },
        {
          group: "edges",
          data: {
            source: 5,
            target: 10,
            name: "YES",
            color: green,
          },
        },
        {
          group: "edges",
          data: {
            source: 5,
            target: 9,
            name: "NO",
            color: red,
          },
        },
        {
          group: "edges",
          data: {
            source: 6,
            target: 7,
            name: "YES",
            color: green,
          },
        },
        {
          group: "edges",
          data: {
            source: 6,
            target: 10,
            name: "NO",
            color: red,
          },
        },
        {
          group: "edges",
          data: {
            source: 7,
            target: 8,
            name: "Optional",
            color: gray,
          },
        },
      ];

      self.cyto_data = data;

      self.drawGraph();
    },
  },
  mounted: function () {
    var self = this;
    self.makeGraph();
  },
};
</script>
