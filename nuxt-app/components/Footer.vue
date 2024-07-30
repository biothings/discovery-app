<template>
  <footer class="section bg-black text-light footer">
    <div class="container p-5">
      <div class="d-flex justify-content-around flex-wrap align-items-start">
        <div class="p-2">
          <h6 class="text-dde-light">Data Discovery Engine</h6>
          <ul>
            <li>
              <nuxt-link class="d-block text-light" to="/">Home</nuxt-link>
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/about"
                >About</nuxt-link
              >
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/portal"
                >Data Portals</nuxt-link
              >
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/best-practices"
                >Discovery Guide</nuxt-link
              >
              <ul>
                <li>
                  <nuxt-link class="text-light" to="/resource"
                    >Resource Registry</nuxt-link
                  >
                </li>
                <li>
                  <nuxt-link class="text-light" to="/markup-generator"
                    >Metadata Generator</nuxt-link
                  >
                </li>
                <li>
                  <nuxt-link class="text-light" to="/validator"
                    >Metadata Validator</nuxt-link
                  >
                </li>
              </ul>
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/schema-playground"
                >Schema Playground</nuxt-link
              >
              <ul>
                <li>
                  <nuxt-link class="text-light" to="/registry"
                    >Schema Registry</nuxt-link
                  >
                </li>
                <li>
                  <nuxt-link class="text-light" to="/ns"
                    >Schema Visualizer</nuxt-link
                  >
                </li>
                <li>
                  <nuxt-link class="text-light" to="/json-schema-viewer"
                    >JSON schema validation viewer</nuxt-link
                  >
                </li>
              </ul>
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/compatibility"
                >Schema.org Project Compatibility Report</nuxt-link
              >
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/branding"
                >Branding</nuxt-link
              >
            </li>
            <li>
              <nuxt-link class="d-block text-light" to="/faq/dde"
                >FAQ</nuxt-link
              >
            </li>
          </ul>
        </div>
        <div class="p-2">
          <h6 class="text-dde-light">Contact Us</h6>
          <a
            class="d-block text-light"
            target="_blank"
            href="mailto:help@biothings.io"
            ><font-awesome-icon icon="fas fa-envelope" /> Email</a
          >
        </div>
        <div class="p-2">
          <h6 class="text-dde-light">Contribute | Issues</h6>
          <a
            class="d-block text-light"
            target="_blank"
            href="https://github.com/biothings/discovery-app"
            ><font-awesome-icon icon="fab fa-github" /> GitHub</a
          >
        </div>
      </div>
      <div
        class="d-flex justify-content-around align-items-center flex-wrap mt-3"
      >
        <a href="https://wulab.io/" target="_blank" rel="nonreferrer">
          <img src="@/assets/img/wulab.png" alt="wulab" height="100" />
        </a>
        <a href="https://sulab.org/" target="_blank" rel="nonreferrer">
          <img src="@/assets/img/sulab.png" alt="sulab" height="50" />
        </a>
        <a href="https://www.scripps.edu/" target="_blank" rel="nonreferrer">
          <img src="@/assets/img/scripps.png" alt="scripps" height="100" />
        </a>
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
