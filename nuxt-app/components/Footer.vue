<template>
  <footer class="section bg-dark text-light footer">
    <div class="container padding20">
      <div class="d-flex justify-content-around flex-wrap align-items-start">
        <div class="p-2">
          <h6 class="text-light">Data Discovery Engine</h6>
          <nuxt-link class="d-block text-light" to="/">Home</nuxt-link>
          <nuxt-link class="d-block text-light" to="/about">About</nuxt-link>
          <nuxt-link class="d-block text-light" to="/faq/dde">FAQ</nuxt-link>
          <nuxt-link class="d-block text-light" to="/best-practices"
            >Discovery Guide</nuxt-link
          >
          <nuxt-link class="d-block text-light" to="/schema-playground"
            >Schema Playground</nuxt-link
          >
        </div>
        <div class="p-2">
          <h6 class="text-light">Contact US</h6>
          <a
            class="d-block text-light"
            target="_blank"
            href="mailto:cd2h-metadata@googlegroups.com"
            ><font-awesome-icon icon="fas fa-envelope" /> Email</a
          >
        </div>
        <div class="p-2">
          <h6 class="text-light">Contribute</h6>
          <a
            class="d-block text-light"
            target="_blank"
            href="https://github.com/data2health/rdp-portal"
            ><font-awesome-icon icon="fab fa-github" /> GitHub</a
          >
        </div>
      </div>
      <p class="rights text-light text-center" style="margin: 0px">
        <small>
          <i class="fab fa-creative-commons"></i>
          <i class="fab fa-creative-commons-by"></i> {{ year }} Except where
          otherwise noted, content on this site is licensed under a
          <a
            class="text-light"
            href="https://creativecommons.org/licenses/by/4.0/"
            target="_blank"
            >Creative Commons Attribution 4.0 International license</a
          >.
        </small>
      </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
  data: function () {
    return {
      year: "",
    };
  },
  mounted: function () {
    let currentTime = new Date();
    this.year = currentTime.getFullYear();
  },
};
</script>
