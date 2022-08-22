<template>
  <Nav></Nav>
  <div id="modals-go-here"></div>
  <main>
    <RouterView />
  </main>
  <Footer></Footer>
</template>

<script>
import Nav from "./components/Nav.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "Home",
  components: {
    Nav,
    Footer,
  }
};
</script>
