<template>
  <div>
    <textarea id="code" name="code"></textarea>
    <div>
      <button
        type="button"
        class="btn btn-primary w-100"
        @click="SaveDefinition()"
      >
        Save
      </button>
    </div>
  </div>
</template>

<script>
import "@/assets/js/codemirror.js";
import { mapGetters } from "vuex";

export default {
  name: "DefinitionEditor",
  data: function () {
    return {
      editor: null,
    };
  },
  computed: {
    ...mapGetters({
      item: "getEditDefinitionItem",
    }),
  },
  methods: {
    SaveDefinition() {
      let self = this;
      let value = self.editor.getValue();
      let copy = Object.assign({}, self.item);
      copy.validation = JSON.parse(value);
      let payload = {
        item: copy,
      };
      store.commit("editDefinitionItem", payload);
    },
  },
  watch: {
    item: function (v) {
      let self = this;
      if (v) {
        self.editor.setValue(JSON.stringify(self.item.validation, null, 2));
      }
    },
  },
  mounted: function () {
    let self = this;
    self.editor = CodeMirror.fromTextArea(document.getElementById("code"), {
      mode: "json",
      lineNumbers: true,
    });
  },
};
</script>
