<script setup>
import { onMounted, watch } from "vue";
import { basicSetup, EditorView } from "codemirror";
import { EditorState, Compartment } from "@codemirror/state";
import { json } from "@codemirror/lang-json";
import { autocompletion } from "@codemirror/autocomplete";
import {
  defaultHighlightStyle,
  syntaxHighlighting,
} from "@codemirror/language";
import { history } from "@codemirror/commands";

let editor;

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  content: {
    type: Object,
    default: { name: "Data Discovery Engine" },
  },
});

let language = new Compartment(),
  tabSize = new Compartment();

function loadContent(target) {
  let state = EditorState.create({
    doc: JSON.stringify(props.content.value, null, 2),
    extensions: [
      basicSetup,
      history(),
      autocompletion(),
      language.of(json()),
      tabSize.of(EditorState.tabSize.of(8)),
      syntaxHighlighting(defaultHighlightStyle),
    ],
  });

  editor = new EditorView({
    state,
    parent: document.body.querySelector(target),
    extensions: [
      EditorView.updateListener.of(function (e) {
        console.log(props.name + " value changed:", e.state.doc.toString());
      }),
    ],
  });

  // let value = editor.state.doc;
  // console.log(value);
}

watch(props.content, (prop) => {
  if (editor) {
    editor.dispatch({
      changes: {
        from: 0,
        to: editor.state.doc.length,
        insert: JSON.stringify(prop.value, null, 2),
      },
    });
  }
});

onMounted(() => {
  loadContent("#" + props.name);
});
</script>

<template>
  <div :id="props.name"></div>
</template>
