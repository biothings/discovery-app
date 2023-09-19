import axios from "axios";

export const validator = {
  state: () => ({
    validationSchema: {},
    validationSchemaOptions: [],
    validationMetadata: {},
  }),
  mutations: {
    saveValidationOptions(state, payload) {
      state.validationSchemaOptions = payload;
    },
    saveValidationSchema(state, payload) {
      state.validationSchema = payload["value"];
    },
    saveValidationMetadata(state, payload) {
      state.validationMetadata = payload["value"];
    },
    resetValidation(state) {
      state.validationSchema = {};
      state.validationMetadata = {};
    },
  },
  getters: {
    getValidationSchema: (state) => {
      return state.validationSchema;
    },
    getValidationMetadata: (state) => {
      return state.validationMetadata;
    },
    validationSchemaOptions: (state) => {
      return state.validationSchemaOptions;
    },
  },
  actions:{
    getValidationOptions(context) {
      let config = useRuntimeConfig();
      axios
      .get(config.public.apiUrl + "/api/registry/query?q=_exists_:validation&fields=name&size=0&aggs=name&facet_size=100")
      .then((res) => {
        if (res.data?.facets?.name?.terms) {
          context.commit("saveValidationOptions", res.data?.facets?.name?.terms.map((agg) => agg.term));
        }
      }).catch((err) => {
        console.log('Failed to get validation options', err)
      })
      
    },
  }
};
