<template>
  <div id="CM-WP" class="text-left"></div>
</template>

<script>
import { basicSetup, EditorView } from "codemirror";
import { EditorState } from "@codemirror/state";
import { html } from "@codemirror/lang-html";
import { keymap } from "@codemirror/view";
import { defaultKeymap } from "@codemirror/commands";

export default {
  name: "CodeEditorHTML",
  props: ["item"],
  data: function () {
    return {
      editor: null,
    };
  },
  methods: {
    openEditor() {
      let self = this;

      let state = EditorState.create({
        doc: self.item,
        extensions: [basicSetup, html(), keymap.of(defaultKeymap)],
      });

      this.editor = new EditorView({
        state,
        parent: document.body.querySelector("#CM-WP"),
      });
      this.$store.commit("setLoading", { value: false });
    },
  },
  watch: {
    item: function (v) {
      if (this.editor) {
        this.editor.dispatch({
          changes: {
            from: 0,
            to: this.editor.state.doc.length,
            insert: JSON.stringify(v, null, 2),
          },
        });
      }
    },
  },
  mounted: function () {
    this.$store.commit("setLoading", { value: true });
    setTimeout(() => {
      this.openEditor();
    }, 1000);
  },
};
</script>

<style>
#CM-WP > .cm-editor {
  height: 100vh;
}
</style>
