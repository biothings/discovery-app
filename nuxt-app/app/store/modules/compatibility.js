export const compatibility = {
  state: {
    data: [],
    data_reset: [],
    query: "",
    filters: {
      requiresLogin: false,
      schema_compliant: false,
      categories: [],
      recommended: [],
    },
  },
  strict: true,
  mutations: {
    saveData(state, payload) {
      let data = payload["data"];

      let cat_f = new Set();
      let rec_f = new Set();

      data.forEach((d) => {
        let categories = new Array();
        d.category.forEach((c) => {
          if (c !== null) {
            cat_f.add(c);
            categories.push(c);
          }
        });
        d.category = categories;
      });

      [...cat_f].forEach((o) =>
        state.filters.categories.push({ name: o, active: false })
      );

      data.forEach((d) => {
        let recommended = new Array();
        d.recommender.forEach((r) => {
          if (r !== null) {
            rec_f.add(r);
            recommended.push(r);
          }
        });
        d.recommender = recommended;
      });

      [...rec_f].forEach((o) =>
        state.filters.recommended.push({ name: o, active: false })
      );

      state.data = data;
      state.data_reset = data;

      //   console.log('data', state.data)
    },
    saveQuery(state, payload) {
      state.query = payload["q"];
    },
    updateResults(state) {
      let res = [];
      //check for filters
      let cats = new Set();
      state.filters.categories.forEach((c) => {
        if (c.active) {
          cats.add(c.name);
        }
      });
      let category_filters = [...cats];

      let rec = new Set();
      state.filters.recommended.forEach((c) => {
        if (c.active) {
          rec.add(c.name);
        }
      });
      let rec_filters = [...rec];

      state.data = state.data_reset;

      if (state.query) {
        for (let i = 0; i < state.data.length; i++) {
          let item = state.data[i];
          let add = false;
          //query match
          if (item["name"].toLowerCase().includes(state.query.toLowerCase())) {
            add = true;
          } else {
            add = false;
          }

          if (add) {
            res.push(item);
          }
        }
      } else {
        res = state.data;
      }

      let filtered_res = [];

      for (let i = 0; i < res.length; i++) {
        let item = res[i];
        let add = true;
        //apply filters
        if (category_filters.length) {
          add = category_filters.every((elem) => item.category.includes(elem));
        }

        if (rec_filters.length) {
          add = rec_filters.every((elem) => item.recommender.includes(elem));
        }

        if (add) {
          add = state.filters["requiresLogin"]
            ? item.requiresLogin === true
              ? true
              : false
            : true;
        }

        if (add) {
          add = state.filters["schema_compliant"]
            ? item.schemaorgCompliant === true
              ? true
              : false
            : true;
        }

        if (add) {
          filtered_res.push(item);
        }
      }

      state.data = filtered_res;
    },
    resetData(state) {
      state.data = state.data_reset;
    },
    toggleLoginFilter(state) {
      state.filters["requiresLogin"] = !state.filters["requiresLogin"];
    },
    toggleCompliant(state) {
      state.filters["schema_compliant"] = !state.filters["schema_compliant"];
    },
    activateCategory(state, payload) {
      let cat_name = payload["category"]["name"];
      state.filters.categories.forEach((c) => {
        if (cat_name == c.name) {
          c.active = !c.active;
        }
      });
    },
    activateRecommended(state, payload) {
      let rec_name = payload["recommended"]["name"];
      state.filters.recommended.forEach((c) => {
        if (rec_name == c.name) {
          c.active = !c.active;
        }
      });
    },
  },
  getters: {
    getQuery: (state) => {
      return state.query;
    },
    getData: (state) => {
      return state.data;
    },
    getQuery: (state) => {
      return state.query;
    },
    getCategories: (state) => {
      return state.filters.categories;
    },
    getRecommended: (state) => {
      return state.filters.recommended;
    },
    getFilters: (state) => {
      return state.filters;
    },
    requiresLogin: (state) => {
      return state.filters.requiresLogin;
    },
    schema_compliant: (state) => {
      return state.filters.schema_compliant;
    },
  },
};
