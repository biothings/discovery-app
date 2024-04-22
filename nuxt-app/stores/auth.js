import axios from "axios";
import { defineStore } from "pinia";

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    userInfo: {},
    loggedIn: false,
  }),
  actions: {
    checkUser() {
      if (process.env.NODE_ENV == "development") {
        this.userInfo = {
          user: {
            name: "Marco Cano",
            email: "artofmarco@gmail.com",
            login: "marcodarko",
            avatar_url: "https://avatars.githubusercontent.com/u/23092057?v=4",
          },
        }
        this.loggedIn = true;
        console.log('LOGGED IN', this.loggedIn)
      } else {
      let config = useRuntimeConfig();
      axios
        .get(config.public.apiUrl + "/user")
        .then((response) => {
          this.userInfo = { user: response.data };
          this.loggedIn = true;
        })
        .catch((err) => {
          this.userInfo = {};
          this.loggedIn = false;
          throw err;
        });
      }
    },
    resetUser(state) {
      state.userInfo = {};
      state.loggedIn = false;
    },
  },
});
