<script setup>
import Nav from './components/Nav.vue';
import Footer from './components/Footer.vue';
import { useStore } from 'vuex';
import { onMounted, computed } from 'vue';

const store = useStore();
let isLoading = computed(()=> store.getters.loading)

onMounted(()=>{
  setTimeout(() => {
    store.dispatch('setUpTips');
  }, 2000);
})

useHead({
        'link': [
          {
            rel:"stylesheet",
            href:"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
            integrity:"sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
            crossorigin:"anonymous"
          },
          {
            href:"https://fonts.googleapis.com/css?family:Sulphur+Point&display:swap",
            rel:"stylesheet"
          },
          {
            src:"https://code.jquery.com/jquery-3.3.1.slim.min.js",
            integrity:"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
            crossorigin:"anonymous"
          },
          {
            src:"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
            integrity:"sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
            crossorigin:"anonymous"
          },
          {
            src:"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js",
            integrity:"sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy",
            crossorigin:"anonymous"
          },
          {
            type:"text/css",
            rel:"stylesheet",
            href:"https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.0/normalize.min.css"
          }
        ]
      })
</script>
<template>
  <div class="bg-light" id="#tippyRoot">
    <Nav></Nav>
    <div v-if="isLoading" class="loader">
      <img src="@/assets/img/ripple.svg" />
    </div>
    <NuxtLoadingIndicator color="#63286b"/>
    <NuxtPage></NuxtPage>
    <Footer></Footer>
  </div>
</template>