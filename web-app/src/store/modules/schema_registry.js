import { TabulatorFull as Tabulator } from "tabulator-tables";
import { remove } from "lodash";

export const schema_registry = {
  state: {
    maxComparisons: 4,
    maxReached: false,
    compareItems: [],
    compareResults: [],
    compareUsedAvailable: true,
  },
  strict: true,
  mutations: {
    resetItems(state, payload) {
      state.compareItems = [];
      $.notify("Cleared", {
        globalPosition: "right",
        showDuration: 40,
        style: "success",
      });
    },
    addItem(state, payload) {
      let item = payload["item"];
      let dupCheck = false;

      if (state.compareItems.length !== state.maxComparisons) {
        if (!state.compareItems.length) {
          state.compareItems.push(item);
        } else {
          for (var i = 0; i < state.compareItems.length; i++) {
            if (state.compareItems[i]["name"] == item["name"]) {
              dupCheck = true;
            }
          }
          if (!dupCheck) {
            if (!item.hasOwnProperty("validation")) {
              state.compareUsedAvailable = false;
            }
            state.compareItems.push(item);
          } else {
            $.notify("Duplicate item ignored", {
              globalPosition: "right",
              showDuration: 40,
              style: "danger",
            });
          }
        }
      }
      if (state.compareItems.length == state.maxComparisons) {
        $.notify("Max items reached", {
          globalPosition: "right",
          style: "warning",
          showDuration: 40,
        });
        state.maxReached = true;
      }
    },
    removeItem(state, payload) {
      let item = payload["item"];
      remove(state.compareItems, function (n) {
        return n["name"] == item["name"];
      });
    },
    reset(state) {
      state.compareItems = [];
    },
    compareAll(state) {
      let finalResutls = [];

      function compare(main, other) {
        if (main.hasOwnProperty("properties")) {
          for (var i = 0; i < main.properties.length; i++) {
            let propName = main.properties[i]["curie"];
            let propLabel = main.properties[i]["label"];
            if (propName.includes("schema:")) {
              propLabel = "🔴 " + main.properties[i]["label"];
            } else {
              propLabel = "<span>🔵 " + main.properties[i]["curie"] + "</span>";
            }
            // look for prop in others
            let tableRow = { Property: propLabel };
            tableRow[main["name"]] = true;

            for (var o = 0; o < other.length; o++) {
              if (other[o].hasOwnProperty("properties")) {
                // iter other props
                //set to false by default but will change to true if match found
                tableRow[other[o]["name"]] = false;
                for (var op = 0; op < other[o].properties.length; op++) {
                  // console.log('%c PROP from OTHER '+other[o].properties[op]['label'],'color:pink')
                  if (other[o].properties[op]["curie"] == propName) {
                    tableRow[other[o]["name"]] = true;
                  }
                }
              }
            }
            //stringify to check prop obj duplication
            var index = finalResutls.findIndex((x) => x.Property == propLabel);
            // here you can check specific property for an object whether it exist in your array or not
            if (index === -1) {
              finalResutls.push(tableRow);
            }
          }
        }
      }

      //column formatting for table
      let cols = [
        {
          title: "Property",
          field: "Property",
          sorter: "string",
          formatter: "html",
        },
      ];

      for (let i = 0; i < state.compareItems.length; i++) {
        let copy = [...state.compareItems];
        let main = copy[i];
        let other = copy.splice(i, 1);
        //compare pulled item against others
        compare(main, copy);
        //create one formatting def per item compared
        cols.push({
          title: main["name"],
          field: main["name"],
          sorter: "boolean",
          hozAlign: "center",
          formatter: "tickCross",
        });
      }

      // console.log('RES', finalResutls)
      state.compareResults = finalResutls;
      // show modal
      var modal = document.getElementById("compareResults");
      modal.style.display = "block";
      var span = document.getElementById("closeBtn");
      span.onclick = function () {
        modal.style.display = "none";
      };
      //show table
      var table = new Tabulator("#example-table", {
        height: 500, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
        data: state.compareResults, //assign data to table
        layout: "fitColumns", //fit columns to width of table (optional)
        columns: cols,
      });

      let elements = document.querySelectorAll(".tabulator-col");
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.backgroundColor = "#4a7d8f";
        elements[i].style.color = "white";
      }

      var dl = document.getElementById("downloadCSV");
      dl.onclick = function () {
        table.download("csv", "schema_comparison_complete.csv");
      };
    },
    compareUsed(state) {
      let finalResutls = [];

      function compare(main, other) {
        if (main.hasOwnProperty("validation")) {
          let props = main.validation.properties;
          for (const prop in props) {
            let propName = prop;
            let propLabel = prop;

            let tableRow = { Property: propLabel };
            if (main.validation.required.includes(prop)) {
              //mark required todo
            }
            tableRow[main["name"]] = true;

            for (var o = 0; o < other.length; o++) {
              if (other[o].hasOwnProperty("validation")) {
                let other_props = other[o].validation.properties;
                tableRow[other[o]["name"]] = false;
                for (const other_prop in other_props) {
                  if (other_prop == propName) {
                    tableRow[other[o]["name"]] = true;
                  }
                }
              } else if (other[o].hasOwnProperty("properties")) {
                // $.notify(other[o]['name']+" does not specify props used, using ALL",{ globalPosition: 'right',style:"info", showDuration: 40, });
                // iter other props
                //set to false by default but will change to true if match found
                tableRow[other[o]["name"]] = false;
                for (var op = 0; op < other[o].properties.length; op++) {
                  //check label not name jsonschema does not have prefixes
                  if (other[o].properties[op]["label"] == propName) {
                    tableRow[other[o]["name"]] = true;
                  }
                }
              }
            }
            //stringify to check prop obj duplication
            //stringify to check prop obj duplication
            var index = finalResutls.findIndex((x) => x.Property == propLabel);
            // here you can check specific property for an object whether it exist in your array or not
            if (index === -1) {
              finalResutls.push(tableRow);
            }
          }
        } else if (main.hasOwnProperty("properties")) {
          $.notify(main["name"] + " does not specify props used, using ALL", {
            globalPosition: "right",
            style: "info",
            showDuration: 40,
          });
          for (var i = 0; i < main.properties.length; i++) {
            let propName = main.properties[i]["curie"];
            let propLabel = main.properties[i]["label"];
            if (propName.includes("schema:")) {
              propLabel = "🔴 " + main.properties[i]["label"];
            } else {
              propLabel = "<span>🔵 " + main.properties[i]["curie"] + "</span>";
            }
            // look for prop in others
            let tableRow = { Property: propLabel };
            tableRow[main["name"]] = true;

            for (var o = 0; o < other.length; o++) {
              if (other[o].hasOwnProperty("properties")) {
                // iter other props
                //set to false by default but will change to true if match found
                tableRow[other[o]["name"]] = false;
                for (var op = 0; op < other[o].properties.length; op++) {
                  // console.log('%c PROP from OTHER '+other[o].properties[op]['label'],'color:pink')
                  if (other[o].properties[op]["curie"] == propName) {
                    tableRow[other[o]["name"]] = true;
                  }
                }
              }
            }
            //stringify to check prop obj duplication
            var index = finalResutls.findIndex((x) => x.Property == propLabel);
            // here you can check specific property for an object whether it exist in your array or not
            if (index === -1) {
              finalResutls.push(tableRow);
            }
          }
        }
      }

      //column formatting for table
      let cols = [
        {
          title: "Property",
          field: "Property",
          sorter: "string",
          formatter: "html",
        },
      ];

      for (let i = 0; i < state.compareItems.length; i++) {
        let copy = [...state.compareItems];
        let main = copy[i];
        let other = copy.splice(i, 1);
        //compare pulled item against others
        compare(main, copy);
        //create one formatting def per item compared
        cols.push({
          title: main["name"],
          field: main["name"],
          sorter: "boolean",
          hozAlign: "center",
          formatter: "tickCross",
        });
      }

      // console.log('RES', finalResutls)
      state.compareResults = finalResutls;
      // show modal
      var modal = document.getElementById("compareResults");
      modal.style.display = "block";
      var span = document.getElementById("closeBtn");
      span.onclick = function () {
        modal.style.display = "none";
      };
      //show table
      var table = new Tabulator("#example-table", {
        height: 500, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
        data: state.compareResults, //assign data to table
        layout: "fitColumns", //fit columns to width of table (optional)
        columns: cols,
      });

      let elements = document.querySelectorAll(".tabulator-col");
      for (var i = 0; i < elements.length; i++) {
        elements[i].style.backgroundColor = "#63296b";
        elements[i].style.color = "white";
      }

      var dl = document.getElementById("downloadCSV");
      dl.onclick = function () {
        table.download("csv", "schema_comparison_used.csv");
      };
    },
  },
  getters: {
    // exposed as store.getters.nameOfGetter
    getMaxReached: (state) => {
      return state.maxReached;
    },
    getCompareItems: (state) => {
      return state.compareItems;
    },
    getResults: (state) => {
      return state.compareResults;
    },
    getCompareUsedAvailable: (state) => {
      return state.compareUsedAvailable;
    },
  },
};
