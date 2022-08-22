export const json_schema_viewer = {
  state: {
    schema: Object,
    showDescriptions: false,
  },
  strict: true,
  mutations: {
    saveSchema(state, payload) {
      state.schema = payload["schema"];
      console.log("🍕🍕🍕 saved schema..🍕🍕🍕", state.schema);
    },
  },
  getters: {
    getSchema: (state) => {
      return state.schema;
    },
    getType: (state) => {
      if (state.schema) {
        return state.schema["@type"];
      }
    },
    getShowDesc: (state) => {
      return state.showDescriptions;
    },
    isPropRequired: (state) => (propname) => {
      if (state.schema && state.schema.hasOwnProperty("required")) {
        if (state.schema["required"].includes(propname)) {
          return true;
        } else {
          return false;
        }
      }
    },
  },
};
