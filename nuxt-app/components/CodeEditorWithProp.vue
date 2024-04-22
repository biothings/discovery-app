<template>
  <div id="CM-WP" class="bg-light text-left"></div>
</template>

<script>
import Notify from "simple-notify";
import { mapActions } from "pinia";
import { useEditorValidationStore } from "../stores/editor_validation";
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
    ...mapActions(useEditorValidationStore, ["editValidationItem"]),
    SaveDefinition() {
      let self = this;
      let value = self.editor.state.doc;
      let copy = Object.assign({}, self.item);
      try {
        copy.validation = JSON.parse(value);
        this.editValidationItem({ item: copy });
      } catch (error) {
        new Notify({
          status: "",
          title: "Validation Editor Error",
          text: error.toString(),
          effect: "fade",
          speed: 300,
          customClass: null,
          customIcon: null,
          showIcon: true,
          showCloseButton: true,
          autoclose: true,
          autotimeout: 3000,
          gap: 20,
          distance: 20,
          type: 1,
          position: "right top",
        });
      }
    },
    openEditor() {
      let self = this;
      let language = new Compartment(),
        tabSize = new Compartment();

      let state = EditorState.create({
        doc: JSON.stringify(self.item?.validation, null, 2),
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
    this.openEditor();
  },
};
</script>

<style>
#CM-WP > .cm-editor {
  height: 100vh;
}
</style>
