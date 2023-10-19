import axios from "axios";
import Notify from "simple-notify";

export const editor = {
  state: {
    schema: [],
    startingPoint: "",
    prefix: "",
    finalschema: {
      "@context": {
        schema: "http://schema.org/",
        rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        rdfs: "http://www.w3.org/2000/01/rdf-schema#",
      },
      "@graph": [],
    },
    removeValidation: false,
    validation: {
      $schema: "http://json-schema.org/draft-07/schema#",
      type: "object",
      properties: {},
      required: [],
      recommended: [],
      optional: [],
    },
    parentDataReceived: false,
    showDescriptions: false,
    previousPreviewProps: {},
    top_class_validation: {},
    schema_version: "",
  },
  strict: true,
  mutations: {
    saveSchemaVersion(state, payload) {
      state.schema_version = payload.v;
      console.log(
        "%c Schema.org version: " + state.schema_version,
        "background-color: green; color: white; padding: 1em"
      );
    },
    setRemoveValidation(state, payload) {
      state.removeValidation = payload.value;
    },
    toggleRemoveValidation(state) {
      state.removeValidation = !state.removeValidation;
      if (state.removeValidation) {
        new Notify({
          status: "warning",
          title: "Editor",
          text: "Validation OFF",
          effect: "fade",
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
          position: "right top",
        });
      } else {
        new Notify({
          status: "success",
          title: "Editor",
          text: "Validation ON",
          effect: "fade",
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
          position: "right top",
        });
      }
    },
    restoreStore(state, payload) {
      let restore = payload.schema;
      for (const key in restore) {
        state[key] = restore[key];
      }
      console.log("✅ Restore Complete!");
    },
    toggleDesc(state) {
      state.showDescriptions = !state.showDescriptions;
    },
    saveSchemaForEditor(state, payload) {
      let names = state.schema.map((cls) => cls.name);
      // console.log(names)
      if (!names.includes(payload["schema"].name)) {
        console.log("✅ Adding Class: ", payload["schema"].name);
        state.schema.push(payload["schema"]);
        state.startingPoint = payload["start"];
        if (payload["schema"].hasOwnProperty("validation")) {
          //save on initial load as state.schema will change
          //later on validation will not be available.
          state.top_class_validation = payload["schema"].validation;
          // check existing cardinality and toggle ON
          let cardinalityPresent = false;
          for (const k in payload["schema"].validation.properties) {
            if (
              Object.hasOwnProperty.call(
                payload["schema"].validation.properties[k],
                "owl:cardinality"
              )
            ) {
              cardinalityPresent = true;
              break;
            }
          }
          if (cardinalityPresent) {
            state.addCardinality = true;
          }
        }
        console.log("✅ saved schema...", state.schema);
      } else {
        console.warn("🚫 Class already exists", payload["schema"].name);
      }
    },
    setValidation(state, payload) {
      let item = payload["validation"];
      let name = payload["name"];
      let newval = Object.assign(
        {},
        state.finalschema["@graph"][0]["$validation"]["properties"][name],
        item["validation"]
      );
      state.finalschema["@graph"][0]["$validation"]["properties"][name] =
        newval;
    },
    resetValidationFor(state, payload) {
      let name = payload["name"];
      let obj = {};
      try {
        obj.description =
          state.finalschema["@graph"][0]["$validation"]["properties"][name][
            "description"
          ];
      } catch (error) {
        obj = {};
      }
      state.finalschema["@graph"][0]["$validation"]["properties"][name] = obj;
      new Notify({
        status: "success",
        title: "Editor",
        text: "Validation cleared",
        effect: "fade",
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
        position: "right top",
      });
    },
    savePrefix(state, payload) {
      state.prefix = payload["prefix"];
      state.finalschema["@context"][state.prefix] =
        "https://discovery.biothings.io/view/" + state.prefix + "/";
    },
    saveParent(state, payload) {
      let parent = payload["parent"];
      // sort props alphabetically
      if (Object.hasOwnProperty.call(parent, "properties")) {
        // parent.properties = $_.orderBy(parent.properties, ["label"], ["asc"]);
        function compare(a, b) {
          if (a["label"] < b["label"]) {
            return -1;
          }
          if (a["label"] > b["label"]) {
            return 1;
          }
          return 0;
        }
        parent.properties.sort(compare);
      }
      let names = state.schema.map((cls) => cls.name);
      // console.log(names)
      if (!names.includes(parent.name)) {
        console.log("🟣 Adding Parent Class: ", parent.name);
        state.schema.push(parent);
      }
    },
    addClass(state, payload) {
      let newClass = {};
      newClass["special"] = true;
      newClass["label"] = payload["name"];
      newClass["description"] = payload["description"];
      newClass["name"] = state.prefix + ":" + payload["name"];
      newClass["prefix"] = state.prefix;
      newClass["parent_classes"] = [state.schema[0].name];
      console.log("🟠 Adding User Class: ", payload["name"]);
      state.schema.unshift(newClass);
    },
    addProperty(state, payload) {
      let newProp = {};
      newProp["label"] = payload["name"];
      newProp["curie"] = state.prefix + ":" + payload["name"];
      newProp["description"] = payload["description"];
      newProp["name"] = state.prefix + ":" + payload["name"];
      newProp["range"] = payload["range"];
      newProp["domain"] = state.prefix + ":" + payload["domain"];
      // if new prop added it should appear in validation by default
      newProp["selected"] = payload["special"];

      for (var i = 0; i < state.schema.length; i++) {
        if (state.schema[i].special) {
          if (Object.hasOwnProperty.call(state.schema[i], "properties")) {
            state.schema[i].properties.push(newProp);
          } else if (
            !Object.hasOwnProperty.call(state.schema[i], "properties")
          ) {
            state.schema[i]["properties"] = [];
            state.schema[i].properties.push(newProp);
          }
        }
      }
    },
    selectProp(state, payload) {
      let label = payload["label"];
      for (var i = 0; i < state.schema.length; i++) {
        if (Object.hasOwnProperty.call(state.schema[i], "properties")) {
          for (var x = 0; x < state.schema[i]["properties"].length; x++) {
            if (
              state.schema[i]["properties"][x].hasOwnProperty("label") &&
              state.schema[i]["properties"][x].label === label
            ) {
              if (state.schema[i]["properties"][x].hasOwnProperty("selected")) {
                state.schema[i]["properties"][x]["selected"] =
                  !state.schema[i]["properties"][x]["selected"];
                //If unselected also mark as not required
                if (!state.schema[i]["properties"][x]["selected"]) {
                  // reset all marginality
                  state.schema[i]["properties"][x]["isRequired"] = false;
                  state.schema[i]["properties"][x]["isOptional"] = false;
                  state.schema[i]["properties"][x]["isRecommended"] = false;
                }
              } else {
                state.schema[i]["properties"][x]["selected"] = true;
              }
            }
          }
        }
      }
    },
    requireProp(state, payload) {
      let label = payload["label"];
      for (var i = 0; i < state.schema.length; i++) {
        if (Object.hasOwnProperty.call(state.schema[i], "properties")) {
          for (var x = 0; x < state.schema[i]["properties"].length; x++) {
            if (
              state.schema[i]["properties"][x].hasOwnProperty("label") &&
              state.schema[i]["properties"][x].label === label
            ) {
              if (
                state.schema[i]["properties"][x].hasOwnProperty("isRequired")
              ) {
                state.schema[i]["properties"][x]["isRequired"] =
                  !state.schema[i]["properties"][x]["isRequired"];
              } else {
                state.schema[i]["properties"][x]["isRequired"] = true;
              }
              //reset other marginality
              if (
                state.schema[i]["properties"][x] &&
                state.schema[i]["properties"][x]["isRequired"]
              ) {
                state.schema[i]["properties"][x]["isOptional"] = false;
                state.schema[i]["properties"][x]["isRecommended"] = false;
              }
            }
          }
        }
      }
    },
    optionalProp(state, payload) {
      let label = payload["label"];
      for (var i = 0; i < state.schema.length; i++) {
        if (Object.hasOwnProperty.call(state.schema[i], "properties")) {
          for (var x = 0; x < state.schema[i]["properties"].length; x++) {
            if (
              state.schema[i]["properties"][x].hasOwnProperty("label") &&
              state.schema[i]["properties"][x].label === label
            ) {
              if (
                state.schema[i]["properties"][x].hasOwnProperty("isOptional")
              ) {
                state.schema[i]["properties"][x]["isOptional"] =
                  !state.schema[i]["properties"][x]["isOptional"];
              } else {
                state.schema[i]["properties"][x]["isOptional"] = true;
              }
              //reset other marginality
              if (
                state.schema[i]["properties"][x] &&
                state.schema[i]["properties"][x]["isOptional"]
              ) {
                state.schema[i]["properties"][x]["isRequired"] = false;
                state.schema[i]["properties"][x]["isRecommneded"] = false;
              }
            }
          }
        }
      }
    },
    recommendProp(state, payload) {
      let label = payload["label"];
      for (var i = 0; i < state.schema.length; i++) {
        if (Object.hasOwnProperty.call(state.schema[i], "properties")) {
          for (var x = 0; x < state.schema[i]["properties"].length; x++) {
            if (
              state.schema[i]["properties"][x].hasOwnProperty("label") &&
              state.schema[i]["properties"][x].label === label
            ) {
              if (
                state.schema[i]["properties"][x].hasOwnProperty("isRecommended")
              ) {
                state.schema[i]["properties"][x]["isRecommended"] =
                  !state.schema[i]["properties"][x]["isRecommended"];
              } else {
                state.schema[i]["properties"][x]["isRecommended"] = true;
              }
              //reset other marginality
              if (
                state.schema[i]["properties"][x] &&
                state.schema[i]["properties"][x]["isRecommended"]
              ) {
                state.schema[i]["properties"][x]["isRequired"] = false;
                state.schema[i]["properties"][x]["isOptional"] = false;
              }
            }
          }
        }
      }
    },
    removeProperty(state, payload) {
      let label = payload["label"];
      for (var i = 0; i < state.schema.length; i++) {
        if (state.schema[i].special) {
          new Notify({
            status: "warning",
            title: "Editor",
            text: label + " deleted",
            effect: "fade",
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
            position: "right top",
          });
          for (var x = 0; x < state.schema[i].properties.length; x++) {
            if (state.schema[i].properties[x].label === label) {
              state.schema[i].properties.splice(x, 1);
              new Notify({
                status: "warning",
                title: "Editor",
                text: label + " deleted",
                effect: "fade",
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
                position: "right top",
              });
            }
          }
        }
      }
    },
    formPreview(state) {
      try {
        state.previousPreviewProps =
          state.finalschema["@graph"][0]["$validation"]["properties"];
      } catch (error) {
        console.log("NO previousPreviewProps", state.previousPreviewProps);
      }
      state.finalschema["@graph"] = [];
      state.validation["properties"] = {};
      state.validation["required"] = [];

      for (var i = 0; i < state.schema.length; i++) {
        if (state.schema[i].special) {
          //Add Main Class to Graph
          let mainClass = {};
          mainClass["@id"] = state.schema[i]["name"];
          mainClass["@type"] = "rdfs:Class";
          mainClass["rdfs:comment"] = state.schema[i]["description"];
          mainClass["rdfs:label"] = state.schema[i]["label"];
          mainClass["rdfs:subClassOf"] = { "@id": state.startingPoint };
          mainClass["$validation"] = {};
          // Add schema.org version
          if (state.schema_version) {
            mainClass["schemaVersion"] = [
              `https://schema.org/docs/releases.html#v${state.schema_version}`,
            ];
          }
          //Add New Class
          state.finalschema["@graph"].push(mainClass);
          //Handle main Class Properties
          if (state.schema[i]?.properties) {
            for (var x = 0; x < state.schema[i].properties.length; x++) {
              let mainProp = {};
              mainProp["@id"] = state.schema[i].properties[x]["name"];
              mainProp["@type"] = "rdf:Property";
              mainProp["rdfs:comment"] =
                state.schema[i].properties[x]["description"];
              mainProp["rdfs:label"] = state.schema[i].properties[x]["label"];
              mainProp["schema:domainIncludes"] = state.schema[i]["name"];
              //Ranges of Property
              if (state.schema[i].properties[x]["range"]) {
                let ranges = state.schema[i].properties[x]["range"].split(",");
                mainProp["schema:rangeIncludes"] = [];
                for (
                  var rangeIndex = 0;
                  rangeIndex < ranges.length;
                  rangeIndex++
                ) {
                  mainProp["schema:rangeIncludes"].push({
                    "@id": ranges[rangeIndex],
                  });
                }
              }
              if (state.schema[i].properties[x].selected) {
                let propValue = {};

                if (
                  state.previousPreviewProps.hasOwnProperty(
                    state.schema[i].properties[x].label
                  )
                ) {
                  // keep existing validation if any
                  propValue = Object.assign(
                    {},
                    state.previousPreviewProps[
                      state.schema[i].properties[x].label
                    ]
                  );
                } else {
                  //for first time add description
                  propValue["description"] =
                    state.schema[i].properties[x].description;
                }
                state.validation["properties"][
                  state.schema[i].properties[x].label
                ] = propValue;
              }
              if (state.schema[i].properties[x].isRequired) {
                let p = state.schema[i].properties[x].label;
                if (!state.validation["required"].includes(p)) {
                  state.validation["required"].push(p);
                }
              }
              if (state.schema[i].properties[x].isRecommended) {
                let p = state.schema[i].properties[x].label;
                if (!state.validation["recommended"].includes(p)) {
                  state.validation["recommended"].push(p);
                }
              }
              if (state.schema[i].properties[x].isOptional) {
                let p = state.schema[i].properties[x].label;
                if (!state.validation["optional"].includes(p)) {
                  state.validation["optional"].push(p);
                }
              }
              //Add New Prop
              state.finalschema["@graph"].push(mainProp);
            }
          }
        } else {
          //Handle Parent Classes
          if (Object.hasOwnProperty.call(state.schema[i], "properties")) {
            let myLabel = "";
            for (let y = 0; y < state.schema[i].properties.length; y++) {
              if (state.schema[i].properties[y].selected) {
                let propValue = {};
                let prop_label = state.schema[i].properties[y]["label"];
                if (state.previousPreviewProps.hasOwnProperty(prop_label)) {
                  // keep existing validation if any
                  propValue = Object.assign(
                    {},
                    state.previousPreviewProps[prop_label]
                  );
                } else {
                  //for first time add description
                  propValue["description"] =
                    state.schema[i].properties[y].description;
                }
                myLabel = state.schema[i].properties[y].label;
                state.validation["properties"][myLabel] = propValue;
              }
              if (state.schema[i].properties[y].isRequired) {
                if (!state.validation["required"].includes(myLabel)) {
                  state.validation["required"].push(myLabel);
                }
              }
              if (state.schema[i].properties[y].isRecommended) {
                if (!state.validation["recommended"].includes(myLabel)) {
                  state.validation["recommended"].push(myLabel);
                }
              }
              if (state.schema[i].properties[y].isOptional) {
                if (!state.validation["optional"].includes(myLabel)) {
                  state.validation["optional"].push(myLabel);
                }
              }
              //pre populate validation from inherited if available
              if (
                Object.hasOwnProperty.call(
                  state.top_class_validation,
                  "properties"
                )
              ) {
                // console.log('pre-populating validation... ')
                for (const propName in state.top_class_validation.properties) {
                  if (
                    Object.hasOwnProperty.call(
                      state.validation["properties"],
                      propName
                    )
                  ) {
                    // console.log('validation has ' + propName, Object.keys(state.validation['properties'][propName]).length)
                    if (
                      Object.keys(state.validation["properties"][propName])
                        .length == 1
                    ) {
                      //begin to add existing validation if validation only has default desc field.
                      for (const key in state.top_class_validation.properties[
                        propName
                      ]) {
                        if (key !== "description") {
                          // console.log('adding existing '+ key +' to ' + propName)
                          state.validation["properties"][propName][key] =
                            state.top_class_validation.properties[propName][
                              key
                            ];
                        }
                      }
                    }
                  }
                }
              }
              //definitions
              let defs_found = new Set();

              function addRefsMentioned(obj) {
                if (typeof obj === "object" && !Array.isArray(obj)) {
                  if ("$ref" in obj) {
                    return obj["$ref"].split("#/definitions/")[1];
                  } else {
                    for (const key in obj) {
                      if (Array.isArray(obj[key])) {
                        for (let i = 0; i < obj[key].length; i++) {
                          const element = obj[key][i];
                          return addRefsMentioned(element);
                        }
                      } else if (
                        typeof obj[key] === "object" &&
                        !Array.isArray(obj[key])
                      ) {
                        return addRefsMentioned(obj[key]);
                      } else if (typeof obj === "string") {
                        continue;
                      } else {
                        return false;
                      }
                    }
                  }
                } else {
                  return false;
                }
              }
              //check for definitions
              for (const key in state.validation.properties) {
                let ref = addRefsMentioned(state.validation.properties[key]);
                if (ref) {
                  // console.log('ref found', ref)
                  defs_found.add(ref);
                }
              }
              if ([...defs_found].length) {
                let defs = [...defs_found];
                state.validation["definitions"] = {};
                defs.forEach((def) => {
                  state.definition_options.forEach((val) => {
                    if (val.title == def) {
                      // console.log('validation found',)
                      if (Object.hasOwnProperty.call(val, "validation")) {
                        state.validation.definitions[def] = val.validation;
                      }
                    }
                  });
                });
              }
              //Once done add temp validation to finalschema
              if (state.finalschema["@graph"].length) {
                state.finalschema["@graph"][0]["$validation"] =
                  state.validation;
              }
            }
          }
        }
      }
      // Check validation is complete
      let incomplete = 0;
      if (Object.hasOwnProperty.call(state?.validation, "properties")) {
        for (let key in state.validation["properties"]) {
          let keys = Object.keys(state.validation["properties"][key]).length;
          if (keys <= 1) {
            incomplete += 1;
          }
        }
        if (incomplete && !state.removeValidation) {
          new Notify({
            status: "warning",
            title: "Editor",
            text: incomplete + " properties still need validation rules",
            effect: "fade",
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
            position: "right top",
          });
        }
      }
      // REMOVE VALIDATION
      if (state.removeValidation) {
        state.finalschema["@graph"].forEach((cls) => {
          if (Object.hasOwnProperty.call(cls, "$validation")) {
            delete cls["$validation"];
            console.log("%c Removed Validation", "color: hotpink");
          }
        });
      }
      //check if bioschemas is mentioned if so add bioschemas to context
      if (JSON.stringify(state.finalschema).includes("bioschemas")) {
        state.finalschema["@context"]["bioschemas"] =
          "https://discovery.biothings.io/view/bioschemas/";
      }
    },
  },
  getters: {
    removeValidation: (state) => {
      return state.removeValidation;
    },
    getSchema: (state) => {
      return state.schema;
    },
    getValidationProps: (state) => {
      return state.validation?.["properties"];
    },
    getStartingPoint: (state) => {
      return state.startingPoint;
    },
    getPrefix: (state) => {
      return state.prefix;
    },
    getFinalSchema: (state) => {
      return state.finalschema;
    },
    getShowDesc: (state) => {
      return state.showDescriptions;
    },
    isDuplicateProp: (state) => (name) => {
      for (var i = 0; i < state.schema.length; i++) {
        if (state.schema[i] && state.schema[i].hasOwnProperty("properties")) {
          let props = state.schema[i]["properties"];
          for (var x = 0; x < props.length; x++) {
            if (props[x]["label"] === name) {
              return true;
            }
          }
        }
      }
      return false;
    },
    isDuplicateClass: (state) => (name) => {
      for (var i = 0; i < state.schema.length; i++) {
        if (state.schema[i] && state.schema[i].hasOwnProperty("label")) {
          if (state.schema[i]["label"] === name) {
            return true;
          }
        }
      }
      return false;
    },
    getPropsSelected: (state) => {
      let props = [];
      for (var i = 0; i < state.schema.length; i++) {
        if (state.schema[i].hasOwnProperty("properties")) {
          for (var x = 0; x < state.schema[i]["properties"].length; x++) {
            if (
              state.schema[i]["properties"][x].hasOwnProperty("selected") &&
              state.schema[i]["properties"][x]["selected"]
            ) {
              if (
                state.schema[i].hasOwnProperty("special") &&
                state.schema[i].special
              ) {
                props.push({
                  from: state.schema[i]["name"],
                  name: state.schema[i]["properties"][x]["curie"],
                  special: true,
                });
              } else {
                props.push({
                  from: state.schema[i]["name"],
                  name: state.schema[i]["properties"][x]["curie"],
                  special: false,
                });
              }
            }
          }
        }
      }
      return props;
    },
    schema_version: (state) => {
      return state.schema_version;
    },
  },
  actions: {
    async getSchemaOrgVersion({ commit, state }) {
      if (!state.schema_version) {
        let config = useRuntimeConfig();
        axios
          .get(config.public.apiUrl + "/api/schema/schema?meta=1")
          .then((res) => {
            if (res.data?._meta?.version) {
              commit("saveSchemaVersion", { v: res.data?._meta?.version });
            } else {
              console.log("Schema.org version not found");
            }
            commit("saveSchemaVersion", { v: res.data?._meta?.version });
          })
          .catch((err) => {
            console.log("Error getting schema.org version: " + err);
          });
      }
    },
    SelectExistingProps({ commit, state }) {
      state.schema.forEach((schema) => {
        if (Object.hasOwnProperty.call(schema, "validation")) {
          if (Object.hasOwnProperty.call(schema.validation, "properties")) {
            Object.keys(schema.validation["properties"]).forEach((propName) => {
              commit("selectProp", { label: propName });
            });
          }
        }
      });
      console.log("Preselected properties ✅");
    },
    applyExistingValidationRules({ commit, state }) {
      console.log("%c Applying VALIDATION", "color:orange");
      state.schema.forEach((schema) => {
        if (Object.hasOwnProperty.call(schema, "validation")) {
          console.log("Applying Parent Validation...", schema.validation);
          if (Object.hasOwnProperty.call(schema.validation, "optional")) {
            schema.validation["optional"].forEach((propName) => {
              commit("optionalProp", { label: propName });
            });
          }
          if (Object.hasOwnProperty.call(schema.validation, "recommended")) {
            schema.validation["recommended"].forEach((propName) => {
              commit("recommendProp", { label: propName });
            });
          }
          if (Object.hasOwnProperty.call(schema.validation, "required")) {
            schema.validation["required"].forEach((propName) => {
              commit("requireProp", { label: propName });
            });
          }
        }
      });
      console.log("Applied existing validation and marginality ✅");
    },
    async getParents({ commit, state }) {
      let list = [];
      for (var i = 0; i < state.schema[0].parent_classes.length; i++) {
        list = list.concat(
          state.schema[0].parent_classes[i].split(", ").reverse()
        );
      }
      let uniqueParents = new Set(list);
      let pList = [...uniqueParents];
      let requests = pList.map((parent) =>
        axios.get(
          "https://discovery.biothings.io/api/registry/" +
            parent.split(":")[0] +
            "/" +
            parent
        )
      );

      commit("setLoading", { value: true });
      try {
        const res = await Promise.all(requests);
        const data = res.map((res) => res.data);
        data.forEach((parentInfo) =>
          commit("saveParent", { parent: parentInfo })
        );
        commit("setLoading", { value: false });
        console.log("✅ Parent classes info received");
      } catch (error) {
        console.log(error);
        commit("setLoading", { value: false });
        console.warn("Failed query for parent class");
        new Notify({
          status: "error",
          title: "Editor",
          text: "Error loading schema, contact us",
          effect: "fade",
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
          position: "right top",
        });
      }
    },
  },
};
