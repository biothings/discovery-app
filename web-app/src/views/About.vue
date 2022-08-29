<template>
  <div id="about" style="min-height: 100vh" class="bg-white">
    <div class="container" style="margin-top: 40px">
      <div class="jumbotron bg-white">
        <h1 class="text-center text-muted mb-0">About</h1>
        <h1 class="text-center">
          <span class="logoText caps">Data Discovery Engine</span>
        </h1>
      </div>

      <div class="text-center p-1 bg-light">
        <h5 class="mainTextDark caps">
          A streamlined process to create, distribute and harvest findable
          metadata<br class="d-none d-md-inline" />
          via interoperable
          <a href="https://schema.org/" rel="noreferrer" target="_blank"
            >Schema.org</a
          >
          schemas
        </h5>
        <img
          class="w-100"
          src="@/assets/img/diagram.png"
          alt="Project Diagram"
        />
        <small class="text-muted d-block">CD2H Project Diagram</small>
      </div>
      <div class="mt-5 mb-5">
        <h5 class="mainTextDark caps">About this project</h5>
        <p class="text-muted" style="font-size: 1.4em">
          The biomedical and informatics communities have largely endorsed the
          spirit and basic components of the
          <a
            class="fair"
            href="https://www.go-fair.org/fair-principles/"
            target="_blank"
            >FAIR</a
          >
          Data Principles. Biomedical data producers, including CTSA hubs, need
          actionable best-practice guidance on how to make their data
          discoverable and reusable, and bring the practical benefits of data
          sharing to researcher’s own research projects, as well as the research
          community as a whole.
        </p>
        <p class="text-muted" style="font-size: 1.4em">
          CTSA hubs produce many valuable datasets which can be shared across
          the broader research community. A significant gap exists between the
          data providers and the data discovery portals where researchers look
          for relevant datasets. Data providers typically lack sufficient guides
          to expose their dataset metadata to these data portals. This project
          is targeted to streamline and minimize the efforts from data providers
          while maximizing the data discoverability.
        </p>
      </div>
      <div class="message mb-5">
        <p class="text-muted text-center">
          <img
            class="m-auto"
            src="@/assets/img/cd2h-logo.png"
            style="width: 30vw; max-width: 300px"
            alt="logo"
          />
          <a
            target="_blank"
            href="https://ctsa.ncats.nih.gov/cd2h/"
            class="d-block"
            rel="noreferrer"
          >
            Learn More About CD2H
            <font-awesome-icon icon="fas fa-chevron-right" />
          </a>
        </p>
      </div>
      <div class="message mb-5 text-muted text-center p-2">
        <h4>Learn About Related Projects</h4>
        <a
          href="http://metadataplus.biothings.io/"
          target="_blank"
          rel="noreferrer"
          >METADATA PLUS <font-awesome-icon icon="fas fa-chevron-right"
        /></a>
        <br />
        <a href="https://crawler.biothings.io/" target="_blank" rel="noreferrer"
          >Metadata Crawler <font-awesome-icon icon="fas fa-chevron-right"
        /></a>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";

export default {
  name: "About",
  mounted: function () {
    tippy(".fair", {
      interactive: true,
      content: `(Findable,Accessible,Interoperable,Reusable)`,
      animation: "fade",
      theme: "light",
    });
  },
};
</script>
