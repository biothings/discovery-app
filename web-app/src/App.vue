<template>
  <Nav></Nav>
  <div id="modals-go-here"></div>
  <div v-if="loading" class="loader">
    <img src="@/assets/img/ripple.svg" />
  </div>
  <main>
    <RouterView />
  </main>
  <Footer></Footer>
</template>

<script>
import Nav from "./components/Nav.vue";
import Footer from "./components/Footer.vue";
import { mapGetters } from "vuex";

export default {
  name: "Home",
  components: {
    Nav,
    Footer,
  },
  computed: {
    ...mapGetters(["loading"]),
  },
};
</script>
