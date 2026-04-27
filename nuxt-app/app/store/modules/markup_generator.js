export const mg = {
  state: () => ({
    mg_validation: {},
  }),
  mutations: {
    saveMGValidation(state, payload) {
      state.mg_validation = payload;
    },
  },
  actions: {
    checkUser({ commit }) {},
  },
  getters: {
    mg_validation: (state) => {
      return state.mg_validation;
    },
  },
};
