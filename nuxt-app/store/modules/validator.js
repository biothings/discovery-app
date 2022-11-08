export const validator = {
  state: () => ({
    validationSchema: {},
    optionSelected: false,
    validationSchemaOptions: [
      {
        name: "n3c:Dataset",
        url: "/api/schema/n3c:Dataset/validation",
      },
      {
        name: "niaid:Dataset",
        url: "/api/schema/niaid:Dataset/validation",
      },
      {
        name: "niaid:ComputationalTool",
        url: "/api/schema/niaid:ComputationalTool/validation",
      },
      {
        name: "outbreak:Dataset",
        url: "/api/schema/outbreak:Dataset/validation",
      },
    ],
    validationMetadata: {},
  }),
  mutations: {
    saveValidationSchema(state, payload) {
      state.validationSchema = payload["value"];
    },
    saveValidationMetadata(state, payload) {
      state.validationMetadata = payload["value"];
    },
    saveValidationOption(state, payload) {
      state.optionSelected = payload["value"];
      console.log("OPTION", state.optionSelected);
    },
    resetValidation(state) {
      state.validationSchema = {};
      state.validationMetadata = {};
      state.optionSelected = false;
    },
  },
  getters: {
    getValidationSchema: (state) => {
      return state.validationSchema;
    },
    getValidationMetadata: (state) => {
      return state.validationMetadata;
    },
    getValidationOption: (state) => {
      return state.optionSelected;
    },
    getValidationSchemaOptions: (state) => {
      return state.validationSchemaOptions;
    },
  },
};
