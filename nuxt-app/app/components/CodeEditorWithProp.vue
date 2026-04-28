<template>
  <div id="CM-WP" class="text-left"></div>
</template>

<script>
import Notify from "simple-notify";
import { basicSetup, EditorView } from "codemirror";
import { EditorState, Compartment } from "@codemirror/state";
import { json } from "@codemirror/lang-json";
import { autocompletion } from "@codemirror/autocomplete";
import {
  defaultHighlightStyle,
  syntaxHighlighting,
} from "@codemirror/language";
import { history } from "@codemirror/commands";

export default {
  name: "CodeEditor",
  props: ["item"],
  data: function () {
    return {
      editor: null,
    };
  },
  methods: {
    openEditor() {
      let self = this;
      let language = new Compartment(),
        tabSize = new Compartment();

      let state = EditorState.create({
        doc: JSON.stringify(self.item?.validation || self.item, null, 2),
        extensions: [
          basicSetup,
          history(),
          autocompletion(),
          language.of(json()),
          tabSize.of(EditorState.tabSize.of(8)),
          syntaxHighlighting(defaultHighlightStyle),
        ],
      });

      this.editor = new EditorView({
        state,
        parent: document.body.querySelector("#CM-WP"),
      });
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
