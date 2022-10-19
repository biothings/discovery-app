<script setup>
import { onMounted } from 'vue'
import { basicSetup, EditorView } from "codemirror";
import { EditorState, Compartment } from "@codemirror/state";
import { json } from "@codemirror/lang-json";
import { autocompletion } from "@codemirror/autocomplete";
import {
  defaultHighlightStyle,
  syntaxHighlighting,
} from "@codemirror/language";
import { history } from "@codemirror/commands";

const { $swal } = useNuxtApp()

useHead({
  title: "DDE | Metadata Validator",
  meta: [
    {
      property: "og:description",
      content: "An interactive metadata vs schema validator.",
    },
    {
      name: "description",
      content: "An interactive metadata vs schema validator.",
    },
    {
      name: "twitter:card",
      content: "An interactive metadata vs schema validator.",
    },
    {
      name: "og:url",
      content: "https://discovery.biothings.io/dataset/validator",
    },
    {
      name: "og:image",
      content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
    },
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
    },
  ],
});

let language = new Compartment(),
    tabSize = new Compartment();

let state = EditorState.create({
"doc": JSON.stringify({"test": "Marco Cano"}, null, 2),
"extensions": [
    basicSetup,
    history(),
    autocompletion(),
    language.of(json()),
    tabSize.of(EditorState.tabSize.of(8)),
    syntaxHighlighting(defaultHighlightStyle),
],
});

function openEditor(){
    let editor = new EditorView({
        state,
        parent: document.body.querySelector("#validatorInput"),
    });

    let value = editor.state.doc;
    console.log(value);
}

onMounted(()=>{
    $swal.fire(
    'Good job!',
    'You clicked the button!',
    'success'
    )
    openEditor();

})

</script>
<template>
    <div class="container alert-warning mt-5">
        <div class="jumbotron alert-success text-center">
            <h1 class="logoText logoFont">Metadata Validator</h1>
        </div>
        <div class="row">
            <div class="col-sm-12 col-md-6 alert-danger p-2">
                <div id="validatorInput"></div>
            </div>
            <div class="col-sm-12 col-md-6 alert-primary p-2">
                <div id="validatorOutput"></div>
            </div>
        </div>
    </div>
</template>