<template>
  <div class="message text-center text-muted p-4">
    <h4 class="m-1">
      <i class="fas fa-circle text-info"></i>
      <span v-text="preset.name"></span>
    </h4>
    <small><span v-text="preset.description"></span></small>
    <br />
    <a
      role="button"
      @click="handleClick()"
      class="btn btn-lg themeButton text-light pulse m-1"
      href="javascript:void(0)"
      ><i class="fas fa-code-branch"></i> Extend</a
    >
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PresetBox",
  props: ["preset"],
  methods: {
    handleClick() {
      var self = this;
      axios
        .get(
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
          window.location.href = "/editor";
        })
        .catch((err) => {
          throw err;
        });
    },
  },
};
</script>
