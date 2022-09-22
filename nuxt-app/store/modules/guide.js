import { isArray, isPlainObject, isEqual } from "lodash";
import Ajv from "ajv";
import addFormats from "ajv-formats";
import Notify from 'simple-notify'

export const guide = {
  state: {
    schema: Object,
    required: Array,
    validation: null,
    schemaName: "",
    output: {},
    startingPoint: null,
    selectedPortals: [],
    step: Number,
    showDescriptions: true,
    bulkJSONItems: [],
    valid: Boolean,
    errors: [],
    guide_prefilled: {
      includedInDataCatalog: {
        name: "N3C Datasets",
        url: "https://ncats.nih.gov/n3c/",
      },
    },
    output_default: {},
    editingID: false,
    beginBulkRegistration: false,
    bulkReport: {
      Exists: [],
      Registered: [],
      Updated: [],
      Failed: [],
    },
  },
  strict: true,
  mutations: {
    addBulkReport(state, payload) {
      for (let key in state.bulkReport) {
        if (state.bulkReport[key].includes(payload.value)) {
          var found = state.bulkReport[key].indexOf(payload.value);
          while (found !== -1) {
            state.bulkReport[key].splice(found, 1);
            found = state.bulkReport[key].indexOf(payload.value);
          }
        }
      }
      state.bulkReport[payload.field].push(payload.value);
      // console.log(state.bulkReport)
    },
    resetBulkReport(state) {
      console.log("%c Resetting Report", "color: yellow");
      state.bulkReport = {
        Exists: [],
        Registered: [],
        Updated: [],
        Failed: [],
      };
    },
    toggleBeginBulkRegistration(state) {
      state.beginBulkRegistration = !state.beginBulkRegistration;
    },
    toggleDesc(state) {
      state.showDescriptions = !state.showDescriptions;
    },
    saveBulkItems(state, payload) {
      state.bulkJSONItems = payload["items"];
    },
    updateJsonItem(state, payload) {
      let item = payload["item"];
      let change = payload["change"];
      let field = payload["field"];

      for (var i = 0; i < state.bulkJSONItems.length; i++) {
        if (
          state.bulkJSONItems[i]["name"] == item["name"] ||
          state.bulkJSONItems[i]["description"] == item["description"]
        ) {
          state.bulkJSONItems[i][field] = change;

          Swal.fire({
            type: "success",
            toast: true,
            title: "Updated",
            showConfirmButton: false,
            timer: 1000,
          });
        }
      }
    },
    saveSchema(state, payload) {
      state.schema = payload["schema"];
      console.log("form properties", state.schema.validation.properties);
      state.output["@type"] = state.schema.name || state.schema.label;
      state.output["@context"] = payload["schema"]["@context"];
      let obj = Object.assign({}, state.output);
      state.output_default = obj;

      // helper func to decide right subcategory
      function getProp(propname) {
        let cat = {
          category: state.schema.label || state.schema.name,
        };
        if (state.schema.validation.required.includes(propname)) {
          cat.subcategory = "Required";
        } else {
          cat.subcategory = "Recommended";
        }
        return cat;
      }

      // Assign initial guide_categories
      for (var prop in state.schema.validation.properties) {
        if (
          state.schema.validation.properties[prop].hasOwnProperty("categories")
        ) {
          state.schema.validation.properties[prop]["categories"].unshift(
            getProp(prop)
          );
        } else {
          state.schema.validation.properties[prop]["categories"] = [];
          state.schema.validation.properties[prop]["categories"].unshift(
            getProp(prop)
          );
        }
      }
    },
    saveSchemaName(state, payload) {
      state.schemaName = payload["name"];
    },
    reset(state) {
      state.schema = {};
      state.validation = null;
      state.step = "1";
      state.selectedPortals = [];
      state.startingPoint = null;
      window.location.reload();
    },
    markSelected(state, payload) {
      let selection = payload["select"];
      for (let key in state.schema.validation.properties) {
        if (key === selection) {
          state.schema.validation.properties[selection]["selected"] = true;
        } else {
          state.schema.validation.properties[key]["selected"] = false;
        }
      }
    },
    selectNext(state) {
      for (let key in state.schema.validation.properties) {
        if (
          state.schema.validation.properties[key] &&
          !state.schema.validation.properties[key].value
        ) {
          state.schema.validation.properties[key]["selected"] = true;
          break;
        }
      }
    },
    highlight(state, payload) {
      let cat = payload["category"];
      let subcat = payload["subcategory"];
      for (prop in state.schema.validation.properties) {
        state.schema.validation.properties[prop]["highlighted"] = false;
      }
      for (prop in state.schema.validation.properties) {
        if (
          state.schema.validation.properties[prop].hasOwnProperty("categories")
        ) {
          for (
            var i = 0;
            i < state.schema.validation.properties[prop]["categories"].length;
            i++
          ) {
            if (
              state.schema.validation.properties[prop]["categories"][i][
                "category"
              ] === cat &&
              state.schema.validation.properties[prop]["categories"][i][
                "subcategory"
              ] === subcat
            ) {
              if (state.schema.validation.properties[prop]["highlighted"]) {
                state.schema.validation.properties[prop]["highlighted"] = false;
              } else {
                state.schema.validation.properties[prop]["highlighted"] = true;
              }
            }
          }
        }
      }
    },
    unhighlight(state) {
      for (prop in state.schema.validation.properties) {
        state.schema.validation.properties[prop]["highlighted"] = false;
      }
    },
    markCompleted(state, payload) {
      let selection = payload["completed"];
      if (state.schema.validation.properties.hasOwnProperty(selection.name)) {
        state.schema.validation.properties[selection.name]["value"] =
          selection.value;
        //check for duplicate keys or plural names
        if (
          selection.name + "s" in state.schema.validation.properties &&
          state.schema.validation.properties[
            selection.name + "s"
          ].hasOwnProperty("duplicate")
        ) {
          new Notify({
            status: 'warning',
            title: 'Guide',
            text: selection.name + "s < similar found and filled out",
            effect: 'fade',
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: true,
            autotimeout: 2000,
            gap: 20,
            distance: 20,
            type: 1,
            position: 'right top'
          })
          state.schema.validation.properties[selection.name + "s"]["value"] =
            selection.value;
        }
      }
    },
    clearValueOfProp(state, payload) {
      let selection = payload["clear"];
      if (
        state.schema.validation.properties[selection].hasOwnProperty("value")
      ) {
        delete state.schema.validation.properties[selection]["value"];
        state.schema.validation.properties[selection]["selected"] = false;
      } else {

        new Notify({
          status: 'error',
          title: 'Guide',
          text: selection + ": no value detected",
          effect: 'fade',
          speed: 300,
          customClass: null,
          customIcon: null,
          showIcon: true,
          showCloseButton: true,
          autoclose: true,
          autotimeout: 2000,
          gap: 20,
          distance: 20,
          type: 1,
          position: 'right top'
        })
      }
      if (
        !state.schema.validation.properties[selection].hasOwnProperty("value")
      ) {
        new Notify({
          status: 'success',
          title: 'Guide',
          text: selection + " was cleared",
          effect: 'fade',
          speed: 300,
          customClass: null,
          customIcon: null,
          showIcon: true,
          showCloseButton: true,
          autoclose: true,
          autotimeout: 2000,
          gap: 20,
          distance: 20,
          type: 1,
          position: 'right top'
        })
      }
    },
    removeArrayItemFrom(state, payload) {
      let field = payload["from"]; //name of prop
      let item = payload["item"]; //full info
      let props = state.schema.validation.properties;
      switch (props[field].value.constructor) {
        case Object:
          if (isEqual(props[field].value, item)) {
            delete props[field]["value"];
          } else {
            new Notify({
              status: 'error',
              title: 'Guide',
              text: "[OBJ] does not match value",
              effect: 'fade',
              speed: 300,
              customClass: null,
              customIcon: null,
              showIcon: true,
              showCloseButton: true,
              autoclose: true,
              autotimeout: 2000,
              gap: 20,
              distance: 20,
              type: 1,
              position: 'right top'
            })
          }
          break;
        case Array:
          if (props[field] && props[field].value) {
            for (var i = 0; i < props[field].value.length; i++) {
              let arr_item = props[field].value[i];
              switch (arr_item.constructor) {
                case String:
                  if (arr_item === item) {
                    delete props[field].value[i];
                    new Notify({
                      status: 'success',
                      title: 'Guide',
                      text: item + " removed",
                      effect: 'fade',
                      speed: 300,
                      customClass: null,
                      customIcon: null,
                      showIcon: true,
                      showCloseButton: true,
                      autoclose: true,
                      autotimeout: 2000,
                      gap: 20,
                      distance: 20,
                      type: 1,
                      position: 'right top'
                    })
                  }
                  break;
                case Object:
                  if (isEqual(arr_item, item)) {
                    delete props[field].value[i];
                    new Notify({
                      status: 'success',
                      title: 'Guide',
                      text: "Item removed",
                      effect: 'fade',
                      speed: 300,
                      customClass: null,
                      customIcon: null,
                      showIcon: true,
                      showCloseButton: true,
                      autoclose: true,
                      autotimeout: 2000,
                      gap: 20,
                      distance: 20,
                      type: 1,
                      position: 'right top'
                    })
                  }
                  break;
                default:
                  console.log("not handled");
              }
            }
          } else {
            console.log("NO VALUE", props[field]);
          }
          break;
        case String:
          for (var i = 0; i < props[field].value.length; i++) {
            let prop_val = props[field].value[i];
            if (prop_val === item) {
              delete props[field].value[i];
              new Notify({
                status: 'success',
                title: 'Guide',
                text: item + " removed",
                effect: 'fade',
                speed: 300,
                customClass: null,
                customIcon: null,
                showIcon: true,
                showCloseButton: true,
                autoclose: true,
                autotimeout: 2000,
                gap: 20,
                distance: 20,
                type: 1,
                position: 'right top'
              })
            }
          }
          break;
        default:
          console.log("not handled");
      }

      if (props[field].hasOwnProperty("value")) {
        if (
          props[field].value.constructor === Array &&
          props[field].value.length == 0
        ) {
          delete props[field]["value"];
        }
      }
    },
    addToArrayFrom(state, payload) {
      let field = payload["from"];
      let item = payload["item"];
      //Initialize array
      if (!state.schema.validation.properties[field].value) {
        state.schema.validation.properties[field]["value"] = item;
      } else {
        if (
          state.schema.validation.properties[field]["value"].constructor ===
          Object
        ) {
          state.schema.validation.properties[field]["value"] = [
            state.schema.validation.properties[field]["value"],
          ];
          state.schema.validation.properties[field]["value"].push(item);
        } else if (
          state.schema.validation.properties[field]["value"].constructor ===
          Array
        ) {
          state.schema.validation.properties[field]["value"].push(item);
        } else {
          state.schema.validation.properties[field]["value"] = [
            state.schema.validation.properties[field]["value"],
          ];
          state.schema.validation.properties[field]["value"].push(item);
        }
      }
    },
    formPreviewForGuide(state) {
      let props = state.schema.validation.properties;
      // Add prefilled values from config
      state.output = Object.assign({}, state.output_default);

      for (var key in state.guide_prefilled) {
        state.output[key] = state.guide_prefilled[key];
      }
      for (let key in props) {
        if (props[key].hasOwnProperty("value")) {
          if (props[key]["value"] || props[key]["value"] === false) {
            if (
              isArray(props[key]["value"]) &&
              props[key]["value"].length === 1
            ) {
              state.output[key] = props[key].value[0];
            } else {
              state.output[key] = props[key].value;
            }
          }
        }
      }
      // VALIDATION ON COMPLETE
      var ajv = new Ajv({ allErrors: true, strict: false });
      addFormats(ajv);
      var schema = state.schema.validation;
      var data = state.output;
      const isValid = ajv.validate(schema, data);

      // ajv.addKeyword('required', {
      //   validate: function validate (schema, data) {
      //     validate.errors = [{keyword: 'required', message: 'This field is required.', params: {keyword: 'required'}}];
      //     return false;
      //   },
      //   errors: true
      // });

      if (!isValid) {
        state.valid = false;
        state.errors = ajv.errors;
        for (var key in props) {
          delete props[key]["hasIssue"];
        }
        let issues = [];
        for (var i = 0; i < state.errors.length; i++) {
          if (state.errors[i]["dataPath"]) {
            let parts = state.errors[i]["dataPath"].split("/");
            for (var x = 0; x < parts.length; x++) {
              let k = parts[x];
              if (k in props) {
                if ("hasIssue" in props[k]) {
                  props[k]["hasIssue"].push(state.errors[i]["message"]);
                } else {
                  props[k]["hasIssue"] = [state.errors[i]["message"]];
                }
              }
            }
          }
          if (state.errors[i]["params"].hasOwnProperty("missingProperty")) {
            let missing = state.errors[i]["params"]["missingProperty"];
            if (props.hasOwnProperty(missing)) {
              if ("hasIssue" in props[missing]) {
                props[missing]["hasIssue"].push(state.errors[i]["message"]);
              } else {
                props[missing]["hasIssue"] = [state.errors[i]["message"]];
              }
            }
          }
        }
      } else {
        state.valid = true;
        state.errors = [];
        for (var key in props) {
          delete props[key]["hasIssue"];
        }
      }
    },
    mergeCategoryProps(state, payload) {
      let origin = payload["origin"];
      let catprops = payload["catprops"];
      let catpropsrequired = payload["catpropsrequired"];
      // add requirements to main reqs
      for (var i = 0; i < catpropsrequired.length; i++) {
        if (!state.schema.validation.required.includes(catpropsrequired[i])) {
          state.schema.validation.required.push(catpropsrequired[i]);
        }
      }
      // helper func to decide right succategory
      function getProp(propname) {
        let cat = {
          category: origin,
        };
        if (catpropsrequired.includes(propname)) {
          cat["subcategory"] = "Required";
        } else {
          cat["subcategory"] = "Recommended";
        }
        return cat;
      }

      // if matching add cat {name:orgin, subcategory: req/rec}
      // else add new prop with origin = name
      for (prop in catprops) {
        if (prop in state.schema.validation.properties) {
          // check if prop has guide_categories
          // if YES push new
          // if NO set-up and add
          if (
            state.schema.validation.properties[prop].hasOwnProperty(
              "categories"
            )
          ) {
            state.schema.validation.properties[prop]["categories"].unshift(
              getProp(prop)
            );
          } else {
            state.schema.validation.properties[prop]["categories"] = [];
            state.schema.validation.properties[prop]["categories"].unshift(
              getProp(prop)
            );
          }
        } else if (prop.slice(0, -1) in state.schema.validation.properties) {
          //plural form exists
          let newProp = catprops[prop];
          newProp["categories"] = [];
          // set origin to remove by origin
          newProp["origin"] = origin;
          // is a duplicate
          newProp["duplicate"] = true;
          newProp["categories"].unshift(getProp(prop));
          state.schema.validation.properties[prop] = newProp;
        } else {
          let newProp = catprops[prop];
          newProp["categories"] = [];
          // set origin to remove by origin
          newProp["origin"] = origin;
          newProp["categories"].unshift(getProp(prop));
          state.schema.validation.properties[prop] = newProp;
        }
      }
      new Notify({
        status: 'success',
        title: 'Guide',
        text: origin + " added",
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 2000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'right top'
      })
    },
    removeCategory(state, payload) {
      let origin = payload["origin"];
      let catpropsrequired = [];
      new Notify({
        status: 'warning',
        title: 'Guide',
        text: origin + " removed",
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 2000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'right top'
      })
      for (var i = 0; i < state.selectedPortals.length; i++) {
        if (state.selectedPortals[i]["label"] === origin) {
          catpropsrequired = state.selectedPortals[i]["validation"]["required"];
        }
      }
      for (prop in state.schema.validation.properties) {
        // if origin matches remove prop
        if (
          state.schema.validation.properties[prop].hasOwnProperty("origin") &&
          state.schema.validation.properties[prop]["origin"] === origin
        ) {
          delete state.schema.validation.properties[prop];
        } else {
          // if not check categories and remove mention of origin
          if (
            state.schema.validation.properties[prop].hasOwnProperty(
              "categories"
            )
          ) {
            for (
              var i = 0;
              i < state.schema.validation.properties[prop]["categories"].length;
              i++
            ) {
              if (
                state.schema.validation.properties[prop]["categories"][i][
                  "category"
                ] === origin
              ) {
                state.schema.validation.properties[prop]["categories"].splice(
                  i,
                  1
                );
              }
            }
          }
        }
      }
    },
    setStartingPoint(state, payload) {
      state.startingPoint = payload["startingPoint"];
    },
    addPortalSchema(state, payload) {
      let portal = payload["portal"];
      state.selectedPortals.push(portal);
    },
    changeStep(state, payload) {
      state.step = payload["step"];
    },
    addValue(state, payload) {
      let name = payload["name"];
      let info = payload["info"];
      let value = payload["value"];
      let props = state.schema.validation.properties;
      for (let key in props) {
        if (key === name) {
          if (info.hasOwnProperty("type") && info["type"] == "object") {
            console.log("OBJECT");
            //SAVE OBJECT
            if (props[name].value) {
              Swal.fire({
                title: "Value Already Exists",
                text: "Do you want to replace the value of: " + name,
                showCancelButton: true,
                confirmButtonText: "Yes",
              }).then((result) => {
                if (result.value) {
                  props[name]["value"] = value;
                }
              });
            } else {
              props[name]["value"] = value;
            }
          } else if (info.hasOwnProperty("anyOf")) {
            console.log("ANY OF");
            // SAVE OBJECT TO ARRAY IF AVAILABLE
            for (var i = 0; i < info["anyOf"].length; i++) {
              if (
                info["anyOf"][i].hasOwnProperty("type") &&
                info["anyOf"][i]["type"] == "array"
              ) {
                // CAN BE ARRAY
                if (props[name].value) {
                  let val = props[name].value;
                  if (isPlainObject(val)) {
                    // will replace
                    Swal.fire({
                      title: "Value Exists",
                      text: "Do you want to replace the value of: " + name,
                      showCancelButton: true,
                      confirmButtonText: "Yes",
                    }).then((result) => {
                      if (result.value) {
                        props[name]["value"] = value;
                      }
                    });
                  } else if (isArray(val)) {
                    //push to existing array
                    props[name]["value"].push(value);
                  } else {
                    //no value yet
                    props[name]["value"] = value;
                  }
                } else {
                  //no value yet
                  props[name]["value"] = value;
                }
              } else {
                //no ability to be array
                console.log("no ability to be array");
                props[name]["value"] = value;
              }
            }
          } else if (info.hasOwnProperty("oneOf")) {
            console.log("ONE OF");
            // SAVE OBJECT TO ARRAY IF AVAILABLE
            for (var i = 0; i < info["oneOf"].length; i++) {
              if (
                info["oneOf"][i].hasOwnProperty("type") &&
                info["oneOf"][i]["type"] == "array"
              ) {
                // CAN BE ARRAY
                if (props[name].value) {
                  let val = props[name].value;
                  if (isPlainObject(val)) {
                    // will replace
                    Swal.fire({
                      title: "Value Exists",
                      text: "Do you want to replace the value of: " + name,
                      showCancelButton: true,
                      confirmButtonText: "Yes",
                    }).then((result) => {
                      if (result.value) {
                        props[name]["value"] = value;
                      }
                    });
                  } else if (isArray(val)) {
                    //push to exisiting array
                    props[name]["value"].push(value);
                  } else {
                    //no value yet
                    props[name]["value"] = value;
                  }
                } else {
                  //no value yet
                  props[name]["value"] = value;
                }
              } else {
                //no ability to be array
                console.log("no ability to be array");
                props[name]["value"] = value;
              }
            }
          } else {
            props[name]["value"] = value;
          }
        }
      }
    },
    setEditMode(state, payload) {
      new Notify({
        status: 'success',
        title: 'Guide',
        text: "Edit Mode: ON",
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 2000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'right top'
      })
      state.editingID = payload["id"];
    },
  },
  getters: {
    getBulkReport: (state) => {
      return state.bulkReport;
    },
    beginBulkRegistration: (state) => {
      return state.beginBulkRegistration;
    },
    editingID: (state) => {
      return state.editingID;
    },
    getBulkJSONItems: (state) => {
      return state.bulkJSONItems;
    },
    getValidStatus: (state) => {
      return state.valid;
    },
    getErrors: (state) => {
      return state.errors;
    },
    showDesc: (state) => {
      return state.showDescriptions;
    },
    schema: (state) => {
      return state.schema;
    },
    getValidation: (state) => {
      if (state.schema.hasOwnProperty("validation")) {
        return state.schema.validation;
      } else {
        return false;
      }
    },
    fieldsLeft: (state) => {
      if (state.schema.hasOwnProperty("validation")) {
        let v = state.schema.validation;
        let n = 0;
        for (var key in v["properties"]) {
          if (!v["properties"][key]["value"]) {
            n += 1;
          }
        }
        return n;
      } else {
        return 0;
      }
    },
    getValidationValue: (state) => (propname) => {
      return state.schema.validation?.properties?.[propname]?.value;
    },
    isRequired: (state) => (propname) => {
      if (state.schema.validation.required.includes(propname)) {
        return true;
      } else {
        return false;
      }
    },
    isInputHidden: (state) => (propname) => {
      if (propname in state.guide_prefilled) {
        return true;
      } else {
        return false;
      }
    },
    getSchemaName: (state) => {
      return state.schemaName;
    },
    getValueOf: (state) => (propname) => {
      if (
        state.schema.validation.properties[propname].hasOwnProperty("value")
      ) {
        return state.schema.validation.properties[propname].value;
      } else {
        console.log(state.schema.validation.properties[propname]);
        console.log("return null");
        return null;
      }
    },
    getTotals: (state) => {
      let completeCount = 0;
      if (state.schema.hasOwnProperty("validation")) {
        let totalprops = Object.keys(state.schema.validation.properties).length;
        for (let key in state.schema.validation.properties) {
          if (
            state.schema.validation.properties[key] &&
            state.schema.validation.properties[key].value
          ) {
            completeCount++;
          }
        }
        let left = totalprops - completeCount;
        if (left === 0) {
          state.complete = true;
        }
        let res = { left: left, complete: completeCount, total: totalprops };
        return res;
      }
    },
    getCategoryTotals: (state) => {
      let cats = {};
      if (state.schema.hasOwnProperty("validation")) {
        for (let key in state.schema.validation.properties) {
          if (
            state.schema.validation.properties[key].hasOwnProperty("categories")
          ) {
            for (
              var i = 0;
              i < state.schema.validation.properties[key]["categories"].length;
              i++
            ) {
              let c =
                state.schema.validation.properties[key]["categories"][i][
                  "category"
                ];
              if (!cats.hasOwnProperty(c)) {
                cats[c] = {};
                cats[c]["Required"] = { completed: 0, todo: 0 };
                cats[c]["Recommended"] = { completed: 0, todo: 0 };

                switch (
                  state.schema.validation.properties[key]["categories"][i][
                    "subcategory"
                  ]
                ) {
                  case "Required":
                    cats[c]["Required"]["todo"] += 1;
                    break;
                  case "Recommended":
                    cats[c]["Recommended"]["todo"] += 1;
                    break;
                  default:
                }
              } else {
                switch (
                  state.schema.validation.properties[key]["categories"][i][
                    "subcategory"
                  ]
                ) {
                  case "Required":
                    cats[c]["Required"]["todo"] += 1;
                    break;
                  case "Recommended":
                    cats[c]["Recommended"]["todo"] += 1;
                    break;
                  default:
                }
              }
            }
          }
        }
        // UPDATE TOTALS
        for (let key in state.schema.validation.properties) {
          if (
            (state.schema.validation.properties[key] &&
              state.schema.validation.properties[key].value) ||
            state.schema.validation.properties[key].value === false
          ) {
            if (
              state.schema.validation.properties[key].hasOwnProperty(
                "categories"
              )
            ) {
              for (
                var i = 0;
                i <
                state.schema.validation.properties[key]["categories"].length;
                i++
              ) {
                let c =
                  state.schema.validation.properties[key]["categories"][i][
                    "category"
                  ];

                switch (
                  state.schema.validation.properties[key]["categories"][i][
                    "subcategory"
                  ]
                ) {
                  case "Required":
                    cats[c]["Required"]["todo"] -= 1;
                    cats[c]["Required"]["completed"] += 1;
                    break;
                  case "Recommended":
                    cats[c]["Recommended"]["todo"] -= 1;
                    cats[c]["Recommended"]["completed"] += 1;
                    break;
                  default:
                }
              }
            }
          }
        }
      }
      return cats;
    },
    getPreview(state) {
      return state.output;
    },
    isComplete(state) {
      let complete = false;
      if (
        state.schema &&
        state.schema.hasOwnProperty("validation") &&
        state.schema.validation.hasOwnProperty("required")
      ) {
        let required = state.schema.validation["required"];
        for (var i = 0; i < required.length; i++) {
          if (
            (state.schema.validation.properties.hasOwnProperty(required[i]) &&
              state.schema.validation.properties[required[i]].value) ||
            state.schema.validation.properties[required[i]].value === false
          ) {
            complete = true;
          } else {
            complete = false;
            break;
          }
        }
      }
      return complete;
    },
    getOutput(state) {
      return state.output;
    },
    startingPoint: (state) => {
      return state.startingPoint;
    },
    getSelectedPortals: (state) => {
      return state.selectedPortals;
    },
    getStep: (state) => {
      return state.step;
    },
  },
  actions: {
    reset({ commit }) {
      commit("reset");
    },
    saveProgress({ commit, state }) {
      commit("formPreviewForGuide");
      let obj = state.output;
      sessionStorage.setItem("guideProgress", JSON.stringify(obj));
    },
  },
};
