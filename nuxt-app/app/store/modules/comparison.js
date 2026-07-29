import axios from "axios";

export const comparison = {
  state: () => ({
    comparison_options:[]
  }),
  getters: {
    comparison_options: (state) => {
      return state.comparison_options;
    },
  },
  mutations: {
    saveComparisonOptions(state, payload) {
      state.comparison_options = payload;
    },
  },
  actions:{
    getComparisonOptions(context) {
      let config = useRuntimeConfig();
      axios
        .get(
          config.public.apiUrl +
            "/api/registry/query?fields=name&size=0&aggs=name&facet_size=1000"
        )
        .then((res) => {
          if (res.data?.facets?.name?.terms) {
            context.commit(
              "saveComparisonOptions",
              res.data?.facets?.name?.terms.map((agg) => agg.term)
            );
          }
        })
        .catch((err) => {
          console.log("Failed to get comparison options", err);
        });
    },
  }
};
