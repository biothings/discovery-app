<template>
  <button
    class="btn themeButton btn-sm text-light tip mr-2 ml-2"
    @click="handleClick()"
    type="button"
    :data-tippy-content="'Extend ' + curie"
  >
    Extend
  </button>
</template>

<script>
import axios from "axios";

export default {
  name: "ExtendClassBtn",
  props: ["ns", "curie"],
  methods: {
    handleClick() {
      const runtimeConfig = useRuntimeConfig();
      var self = this;
      self.$store.commit("setLoading", true);
      axios
        .get(
          runtimeConfig.public.apiUrl +
            "/api/registry/" +
            self.ns +
            "/" +
            self.curie
        )
        .then((res) => {
          let obj = JSON.stringify(res.data);
          // console.log("Editor Data", obj);
          localStorage.setItem("EditorData", obj);
          localStorage.setItem("EditorStartingPoint", self.curie);
          self.$store.commit("setLoading", false);
          self.$router.push({ path: "/editor" });
        })
        .catch((err) => {
          self.$store.commit("setLoading", false);
          throw err;
        });
    },
  },
};
</script>
