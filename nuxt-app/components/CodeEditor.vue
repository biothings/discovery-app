<template>
  <div>Editing option...</div>
</template>

<script>
import { mapGetters } from "vuex";
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
  data: function () {
    return {
      editor: null,
    };
  },
  computed: {
    ...mapGetters({
      item: "getEditItem",
    }),
  },
  methods: {
    SaveDefinition() {
      let self = this;
      let value = self.editor.state.doc;
      let copy = Object.assign({}, self.item);
      try {
        copy.validation = JSON.parse(value);
        this.$store.commit("editValidationItem", {
          item: copy,
        });
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
          autoclose: true, // Enable auto close
          autotimeout: 3000, // Set timeout in milliseconds (3 seconds)
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

      this.$swal
        .fire({
          title: "Edit Option",
          html: '<div id="CM" class="bg-light text-left"></div>',
          showCloseButton: true,
          showCancelButton: true,
          focusConfirm: false,
          customClass: "swal-xl",
          showDenyButton: true,
          showCancelButton: true,
          confirmButtonText: "Save",
          denyButtonText: `Don't save`,
          preConfirm: (someVal) => {
            try {
              //validate json
              JSON.parse(self.editor.state.doc);
              return true;
            } catch (error) {
              alert(`Invalid JSON Structure: ${error.toString()}`);
              return false;
            }
          },
          didOpen: () => {
            this.editor = new EditorView({
              state,
              parent: document.body.querySelector("#CM"),
            });
          },
        })
        .then((result) => {
          if (result.isConfirmed) {
            self.SaveDefinition();
          } else {
            //reset selected item, prevents auto pop up
            self.$store.commit("editThis", { item: null });
          }
        });
    },
  },
  watch: {
    item: function (v) {
      this.openEditor();
    },
  },
  mounted: function () {
    this.openEditor();
  },
};
</script>
