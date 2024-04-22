import { defineStore } from "pinia";

export const useMarkuptore = defineStore("markupStore", {
  state: () => ({
    mg_validation: {},
  }),
  actions: {
    saveMGValidation(payload) {
      this.mg_validation = payload;
    },
  },
});

// export const mg = {
//   state: () => ({
//     mg_validation: {},
//   }),
//   mutations: {
//     saveMGValidation(state, payload) {
//       state.mg_validation = payload;
//     },
//   },
//   actions: {
//     checkUser({ commit }) {},
//   },
//   getters: {
//     mg_validation: (state) => {
//       return state.mg_validation;
//     },
//   },
// };
