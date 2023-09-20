<script setup>
import axios from "axios";
// import { reactive, computed, ref, watch, onMounted } from "vue";
import { useStore } from "vuex";
import Notify from "simple-notify";
// import { useRouter, useRoute } from "vue-router";

const { $swal } = useNuxtApp();
const runtimeConfig = useRuntimeConfig();
const store = useStore();

useHead({
  title: "DDE | Markup Generator",
  meta: [
    {
      property: "og:description",
      content: "Generate JSON based on a particular schema class specification and validation rules.",
    },
    {
      name: "description",
      content: "Generate JSON based on a particular schema class specification and validation rules.",
    },
    {
      name: "twitter:card",
      content: "Generate JSON based on a particular schema class specification and validation rules.",
    },
    {
      name: "og:url",
      content: "https://discovery.biothings.io/dataset/validator",
    },
    {
      name: "og:image",
      content: "https://i.postimg.cc/ZRm0nQ0h/dde-Validator.jpg",
    },
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/ZRm0nQ0h/dde-Validator.jpg",
    },
  ],
});

function getSchemaValidation(curie) {
      store.commit("setLoading", { value: true });
      axios
        .get(runtimeConfig.apiUrl + `/api/schema/${curie}/validation`)
        .then((res) => {
          console.log(res.data)
          store.commit("setLoading", { value: false });
          new Notify({
              status: "success",
              title: "Ready",
              text: curie + " loaded successfully",
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
        })
        .catch((err) => {
          store.commit("setLoading", { value: false });
          try {
            $swal.fire({
              type: "error",
              position: "center",
              title: "Failed because: ",
              text: err,
            });
          } catch (e) {
            throw e;
          }
          throw err;
        });
    }

onMounted(() =>{
  getSchemaValidation('n3c:Dataset')
})
</script>
<template>
  <div class="mt-5 p-0">
    <div class="container">
        <h1>Markup Generator</h1>
    </div>
  </div>
</template>
