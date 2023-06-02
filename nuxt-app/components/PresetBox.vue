<template>
  <div class="row m-0 m-1 shadow">
    <div class="col-sm-10 alert-dark text-muted p-2 rounded-left border-dark">
      <h5>
        <font-awesome-icon icon="fas fa-circle" class="text-info mr-2" />
        <nuxt-link :to="{ path: `/ns/${preset.namespace}/${preset.prefix}:${preset.name}`}">
          {{ preset.prefix }}:{{ preset.name }}
        </nuxt-link>
      </h5>
      <p class="m-0">{{ preset.description }}</p>
    </div>
    <div
      class="col-sm-2 p-1 bg-dark d-flex align-items-center justify-content-around rounded-right"
    >
      <span
        class="fa-stack fa-1x pointer tip mr-2 ml-2"
        @click="handleClick()"
        :data-tippy-content="'Extend ' + preset.name"
      >
        <font-awesome-icon
          icon="fas fa-circle"
          class="fa-stack-2x mainTextLight"
        />
        <font-awesome-icon
          icon="fas fa-code-branch"
          class="fa-stack-1x text-light"
        />
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PresetBox",
  props: ["preset"],
  methods: {
    handleClick() {
      const runtimeConfig = useRuntimeConfig();
      var self = this;
      axios
        .get(
          runtimeConfig.public.apiUrl +
            "/api/registry/" +
            self.preset.namespace +
            "/" +
            self.preset.prefix +
            ":" +
            self.preset.name
        )
        .then((res) => {
          let obj = JSON.stringify(res.data);
          localStorage.setItem("EditorData", obj);
          localStorage.setItem(
            "EditorStartingPoint",
            self.preset.prefix + ":" + self.preset.name
          );
          self.$router.push({ path: "/editor" });
        })
        .catch((err) => {
          throw err;
        });
    },
  },
};
</script>
