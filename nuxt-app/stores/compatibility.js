import { defineStore } from "pinia";

export const useCompatibilityStore = defineStore("compatibilityStore", {
  state: () => ({
    data: [],
    data_reset: [],
    query: "",
    filters: {
      requiresLogin: false,
      schema_compliant: false,
      categories: [],
      recommended: [],
    },
  }),
  actions: {
    saveData(payload) {
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
        this.filters.categories.push({ name: o, active: false })
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
        this.filters.recommended.push({ name: o, active: false })
      );

      this.data = data;
      this.data_reset = data;

      //   console.log('data', this.data)
    },
    saveQuery(payload) {
      this.query = payload["q"];
    },
    updateResults() {
      let res = [];
      //check for filters
      let cats = new Set();
      this.filters.categories.forEach((c) => {
        if (c.active) {
          cats.add(c.name);
        }
      });
      let category_filters = [...cats];

      let rec = new Set();
      this.filters.recommended.forEach((c) => {
        if (c.active) {
          rec.add(c.name);
        }
      });
      let rec_filters = [...rec];

      this.data = this.data_reset;

      if (this.query) {
        for (let i = 0; i < this.data.length; i++) {
          let item = this.data[i];
          let add = false;
          //query match
          if (item["name"].toLowerCase().includes(this.query.toLowerCase())) {
            add = true;
          } else {
            add = false;
          }

          if (add) {
            res.push(item);
          }
        }
      } else {
        res = this.data;
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
          add = this.filters["requiresLogin"]
            ? item.requiresLogin === true
              ? true
              : false
            : true;
        }

        if (add) {
          add = this.filters["schema_compliant"]
            ? item.schemaorgCompliant === true
              ? true
              : false
            : true;
        }

        if (add) {
          filtered_res.push(item);
        }
      }

      this.data = filtered_res;
    },
    resetData() {
      this.data = this.data_reset;
    },
    toggleLoginFilter() {
      this.filters["requiresLogin"] = !this.filters["requiresLogin"];
    },
    toggleCompliant() {
      this.filters["schema_compliant"] = !this.filters["schema_compliant"];
    },
    activateCategory(payload) {
      let cat_name = payload["category"]["name"];
      this.filters.categories.forEach((c) => {
        if (cat_name == c.name) {
          c.active = !c.active;
        }
      });
    },
    activateRecommended(payload) {
      let rec_name = payload["recommended"]["name"];
      this.filters.recommended.forEach((c) => {
        if (rec_name == c.name) {
          c.active = !c.active;
        }
      });
    },
  },
  getters: {
    getCategories: (state) => {
      return state.filters.categories;
    },
    getRecommended: (state) => {
      return state.filters.recommended;
    },
    requiresLogin: (state) => {
      return state.filters.requiresLogin;
    },
    schema_compliant: (state) => {
      return state.filters.schema_compliant;
    },
  },
});

// export const compatibility = {
//   state: {
//     data: [],
//     data_reset: [],
//     query: "",
//     filters: {
//       requiresLogin: false,
//       schema_compliant: false,
//       categories: [],
//       recommended: [],
//     },
//   },
//   strict: true,
//   mutations: {
//     saveData(state, payload) {
//       let data = payload["data"];

//       let cat_f = new Set();
//       let rec_f = new Set();

//       data.forEach((d) => {
//         let categories = new Array();
//         d.category.forEach((c) => {
//           if (c !== null) {
//             cat_f.add(c);
//             categories.push(c);
//           }
//         });
//         d.category = categories;
//       });

//       [...cat_f].forEach((o) =>
//         this.filters.categories.push({ name: o, active: false })
//       );

//       data.forEach((d) => {
//         let recommended = new Array();
//         d.recommender.forEach((r) => {
//           if (r !== null) {
//             rec_f.add(r);
//             recommended.push(r);
//           }
//         });
//         d.recommender = recommended;
//       });

//       [...rec_f].forEach((o) =>
//         this.filters.recommended.push({ name: o, active: false })
//       );

//       this.data = data;
//       this.data_reset = data;

//       //   console.log('data', this.data)
//     },
//     saveQuery(state, payload) {
//       this.query = payload["q"];
//     },
//     updateResults(state) {
//       let res = [];
//       //check for filters
//       let cats = new Set();
//       this.filters.categories.forEach((c) => {
//         if (c.active) {
//           cats.add(c.name);
//         }
//       });
//       let category_filters = [...cats];

//       let rec = new Set();
//       this.filters.recommended.forEach((c) => {
//         if (c.active) {
//           rec.add(c.name);
//         }
//       });
//       let rec_filters = [...rec];

//       this.data = this.data_reset;

//       if (this.query) {
//         for (let i = 0; i < this.data.length; i++) {
//           let item = this.data[i];
//           let add = false;
//           //query match
//           if (item["name"].toLowerCase().includes(this.query.toLowerCase())) {
//             add = true;
//           } else {
//             add = false;
//           }

//           if (add) {
//             res.push(item);
//           }
//         }
//       } else {
//         res = this.data;
//       }

//       let filtered_res = [];

//       for (let i = 0; i < res.length; i++) {
//         let item = res[i];
//         let add = true;
//         //apply filters
//         if (category_filters.length) {
//           add = category_filters.every((elem) => item.category.includes(elem));
//         }

//         if (rec_filters.length) {
//           add = rec_filters.every((elem) => item.recommender.includes(elem));
//         }

//         if (add) {
//           add = this.filters["requiresLogin"]
//             ? item.requiresLogin === true
//               ? true
//               : false
//             : true;
//         }

//         if (add) {
//           add = this.filters["schema_compliant"]
//             ? item.schemaorgCompliant === true
//               ? true
//               : false
//             : true;
//         }

//         if (add) {
//           filtered_res.push(item);
//         }
//       }

//       this.data = filtered_res;
//     },
//     resetData(state) {
//       this.data = this.data_reset;
//     },
//     toggleLoginFilter(state) {
//       this.filters["requiresLogin"] = !this.filters["requiresLogin"];
//     },
//     toggleCompliant(state) {
//       this.filters["schema_compliant"] = !this.filters["schema_compliant"];
//     },
//     activateCategory(state, payload) {
//       let cat_name = payload["category"]["name"];
//       this.filters.categories.forEach((c) => {
//         if (cat_name == c.name) {
//           c.active = !c.active;
//         }
//       });
//     },
//     activateRecommended(state, payload) {
//       let rec_name = payload["recommended"]["name"];
//       this.filters.recommended.forEach((c) => {
//         if (rec_name == c.name) {
//           c.active = !c.active;
//         }
//       });
//     },
//   },
//   getters: {
//     getQuery: (state) => {
//       return this.query;
//     },
//     getData: (state) => {
//       return this.data;
//     },
//     getQuery: (state) => {
//       return this.query;
//     },
//     getCategories: (state) => {
//       return this.filters.categories;
//     },
//     getRecommended: (state) => {
//       return this.filters.recommended;
//     },
//     getFilters: (state) => {
//       return this.filters;
//     },
//     requiresLogin: (state) => {
//       return this.filters.requiresLogin;
//     },
//     schema_compliant: (state) => {
//       return this.filters.schema_compliant;
//     },
//   },
// };
