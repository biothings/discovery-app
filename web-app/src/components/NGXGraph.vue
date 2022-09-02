<template>
  <div id="classGraph" class="bg-light rounded"></div>
</template>

<script>
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";

import { mapGetters } from "vuex";

export default {
  name: "NGXGraph",
  data: function () {
    return {
      cyto_data: [],
      cy: null,
    };
  },
  computed: {
    ...mapGetters({
        classesAvailable: 'getSchema',
        propsSelected: 'getPropsSelected'
    })
  },
  watch: {
    propsSelected: function (v) {
      this.makeGraph();
    },
  },
  methods: {
    drawGraph() {
      // const t0 = performance.now();
      var self = this;

      cytoscape.use(dagre);

      var cy = (window.cy = cytoscape({
        container: document.getElementById("classGraph"),
        boxSelectionEnabled: false,
        autounselectify: true,
        layout: {
          name: "dagre",
          padding: 5,
        },
        style: [
          {
            selector: "node",
            style: {
              label: "data(id)",
              shape: "data(type)",
              "text-valign": "bottom",
              "text-halign": "center",
              height: "100px",
              width: "100px",
              "border-color": "white",
              height: 20,
              width: 20,
              "background-color": "data(color)",
              "font-size": "data(size)",
            },
          },

          {
            selector: "edge",
            style: {
              "curve-style": "haystack",
              "haystack-radius": 0,
              width: 5,
              opacity: 0.5,
              "line-color": "data(color)",
              "target-arrow-shape": "triangle",
              "target-arrow-color": "#257FC5",
            },
          },
          {
            selector: ":selected",
            css: {
              "background-color": "black",
              "line-color": "black",
              "target-arrow-color": "red",
              "source-arrow-color": "black",
            },
          },
        ],

        elements: self.cyto_data,
      }));

      cy.maxZoom(2);

      // const t1 = performance.now();
      // var seconds = (((t1 - t0) % 60000) / 1000).toFixed(0);
      // console.log(`%c Rendering graph took ${seconds} seconds.`, 'color:yellow');
    },
    makeGraph() {
      var self = this;

      let edges = [];
      let nodes = [];

      let blue = "#057BFE";
      let green = "#28A745";
      let yellow = "#FFC007";

      for (i = 0; i < self.classesAvailable.length; i++) {
        if (
          self.classesAvailable[i].hasOwnProperty("special") &&
          self.classesAvailable[i].special
        ) {
          let node = {
            group: "nodes",
            data: {
              id: self.classesAvailable[i].name,
              type: "star",
              color: yellow,
              size: "1em",
            },
          };
          nodes.push(node);
        } else {
          let node = {
            group: "nodes",
            data: {
              id: self.classesAvailable[i].name,
              type: "ellipse",
              color: blue,
              size: "1em",
            },
          };
          nodes.push(node);
        }
        if (self.classesAvailable[i].hasOwnProperty("parent_classes")) {
          let parents = self.classesAvailable[i]["parent_classes"];
          for (p = 0; p < parents.length; p++) {
            let branch_parents = parents[p].split(",");
            let parent = branch_parents[branch_parents.length - 1].trim();
            let edge = {
              // edge ab
              group: "edges",
              data: {
                source: parent,
                target: self.classesAvailable[i].name,
                color: "grey",
              },
            };
            edges.push(edge);
          }
        }
      }
      if (self.propsSelected.length) {
        for (i = 0; i < self.propsSelected.length; i++) {
          if (self.propsSelected[i]["special"]) {
            let node = {
              group: "nodes",
              data: {
                id: self.propsSelected[i]["name"],
                color: green,
                type: "diamond",
                size: ".5em",
              },
            };
            nodes.push(node);

            let edge = {
              // edge ab
              group: "edges",
              data: {
                source: self.propsSelected[i]["from"],
                target: self.propsSelected[i]["name"],
                color: yellow,
              },
            };
            edges.push(edge);
          } else {
            let node = {
              group: "nodes",
              data: {
                id: self.propsSelected[i]["name"],
                color: green,
                type: "diamond",
                size: ".5em",
              },
            };
            nodes.push(node);

            let edge = {
              // edge ab
              group: "edges",
              data: {
                source: self.propsSelected[i]["from"],
                target: self.propsSelected[i]["name"],
                color: blue,
              },
            };
            edges.push(edge);
          }
        }
      }

      self.cyto_data = [].concat(nodes).concat(edges);
      // console.log('DATA', self.cyto_data)

      self.drawGraph();
    },
  },
  mounted: function () {
    this.makeGraph();
  },
};
</script>
