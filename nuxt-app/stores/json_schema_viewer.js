import { defineStore } from "pinia";

export const useJSONSchemaStore = defineStore("jsonSchemaStore", {
  state: () => ({
    schemaJSV: Object,
    showDescriptions: false,
  }),
  actions: {
    saveSchemaJSV(payload) {
      this.schemaJSV = payload["schema"];
      console.log("🍕🍕🍕 saved schemaJSV..🍕🍕🍕", this.schemaJSV);
    },
  },
  getters: {
    getSchemaJSV: (state) => {
      return state.schemaJSV;
    },
    getType: (state) => {
      if (state.schemaJSV) {
        return state.schemaJSV["@type"];
      }
    },
    getShowDescJSV: (state) => {
      return state.showDescriptions;
    },
    isPropRequired: (state) => (propname) => {
      if (state.schemaJSV && state.schemaJSV.hasOwnProperty("required")) {
        if (state.schemaJSV["required"].includes(propname)) {
          return true;
        } else {
          return false;
        }
      }
    },
  },
});

// export const json_schema_viewer = {
//   state: {
//     schemaJSV: Object,
//     showDescriptions: false,
//   },
//   strict: true,
//   mutations: {
//     saveSchemaJSV(state, payload) {
//       state.schemaJSV = payload["schema"];
//       console.log("🍕🍕🍕 saved schemaJSV..🍕🍕🍕", state.schemaJSV);
//     },
//   },
//   getters: {
//     getSchemaJSV: (state) => {
//       return state.schemaJSV;
//     },
//     getType: (state) => {
//       if (state.schemaJSV) {
//         return state.schemaJSV["@type"];
//       }
//     },
//     getShowDescJSV: (state) => {
//       return state.showDescriptions;
//     },
//     isPropRequired: (state) => (propname) => {
//       if (state.schemaJSV && state.schemaJSV.hasOwnProperty("required")) {
//         if (state.schemaJSV["required"].includes(propname)) {
//           return true;
//         } else {
//           return false;
//         }
//       }
//     },
//   },
// };
