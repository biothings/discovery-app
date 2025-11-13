<template>
  <div id="guides" class="container-fluid text-dark min-100">
    <PageTitle title="Resource Discovery Best Practices"></PageTitle>
    <div class="text-center mb-5">
      <div class="col-md-8 col-sm-12 m-auto p-3 container text-left text-dark">
        <p class="d-flex justify-content-center align-items-center">
          <nuxt-link to="/resource">Metadata Registry</nuxt-link>
          <span class="mx-2">|</span>
          <nuxt-link to="/coverage">Metadata Coverage</nuxt-link>
        </p>
        <p>
          This guide provides an easy way to create discoverable structured
          dataset metadata with little to no
          <a
            data-tippy-content="Learn More About Schema.org"
            href="https://schema.org/"
            target="_blank"
            >Schema.org</a
          >
          microdata markup or
          <a
            data-tippy-content="Learn More About FAIR Principles"
            target="_blank"
            href="https://www.go-fair.org/fair-principles/"
            >FAIR</a
          >
          data-sharing best-practices knowledge.
        </p>
        <p>
          Let the guided wizard do all the hard work and just fill out the
          fields provided and register your metadata.
        </p>
      </div>
      <div class="text-center mb-5">
        <div class="row m-0">
          <div class="col-sm-12 col-md-4 align-items-stretch d-flex p-0">
            <div class="row m-0">
              <div
                class="col-sm-12 d-flex justify-content-center align-items-center bg-dde-dark text-light text-center py-4"
              >
                <div>
                  <span class="fa-stack fa-1x m-2">
                    <font-awesome-icon
                      icon="fas fa-circle"
                      class="mainTextLight fa-stack-2x"
                    />
                    <font-awesome-icon
                      icon="fas fa-cogs"
                      class="fa-stack-1x text-light"
                    />
                  </span>
                  <h6 class="caps">
                    Produce
                    <a
                      data-tippy-content="Learn More About FAIR Principles"
                      class="bold"
                      target="_blank"
                      href="https://www.go-fair.org/fair-principles/"
                      >FAIR</a
                    >
                    data<br />
                    right from the start.
                  </h6>
                </div>
              </div>
              <div
                class="col-sm-12 d-flex justify-content-center align-items-center bg-dde-dark text-light text-center py-4"
              >
                <div>
                  <span class="fa-stack fa-1x m-2">
                    <font-awesome-icon
                      icon="fas fa-circle"
                      class="mainTextLight fa-stack-2x"
                    />
                    <font-awesome-icon
                      icon="fas fa-list-ol"
                      class="fa-stack-1x text-light"
                    />
                  </span>
                  <h6 class="caps">
                    Fast and easy to use <br />Step-by-step guide.
                  </h6>
                </div>
              </div>
              <div
                class="col-sm-12 d-flex justify-content-center align-items-center bg-dde-dark text-light text-center py-4"
              >
                <div>
                  <span class="fa-stack fa-1x m-2">
                    <font-awesome-icon
                      icon="fas fa-circle"
                      class="mainTextLight fa-stack-2x"
                    />
                    <font-awesome-icon
                      icon="fas fa-tasks"
                      class="fa-stack-1x text-light"
                    />
                  </span>
                  <h6 class="caps">
                    Customize discoverability<br />
                    by Data Portals.
                  </h6>
                </div>
              </div>
              <div
                class="col-sm-12 d-flex justify-content-center align-items-center bg-dde-dark text-light text-center py-4"
              >
                <div>
                  <span class="fa-stack fa-1x m-2">
                    <font-awesome-icon
                      icon="fas fa-circle"
                      class="mainTextLight fa-stack-2x"
                    />
                    <font-awesome-icon
                      icon="fas fa-lightbulb"
                      class="fa-stack-1x text-light"
                    />
                  </span>
                  <h6 class="caps">
                    Generate findable metadata<br />
                    by computers and humans.
                  </h6>
                </div>
              </div>
            </div>
          </div>
          <div
            class="jumbotron rounded-0 col-sm-12 col-md-8 m-0 d-flex justify-content-center align-items-center grad-light"
          >
            <div class="col-sm-12 col-md-8">
              <img
                src="@/assets/img/discoverable-01.png"
                alt="DISCOVERY"
                width="200"
              />
              <h1 class="text-light">DISCOVERY GUIDE</h1>
              <a
                class="btn btn-lg themeButton text-light m-2 px-3 py-3"
                href="#choose"
                >GET STARTED</a
              >
            </div>
          </div>
        </div>
      </div>
      <div class="container px-5" id="choose">
        <h1 class="text-dde-dark">Data Portals</h1>
        <div class="container">
          <p class="text-muted">
            Learn how this metadata will be available via our
            <a
              href="https://crawler.biothings.io/"
              target="_blank"
              rel="nonreferrer"
              >API</a
            >.
          </p>
        </div>
        <div
          class="d-flex justify-content-center align-items-stretch flex-wrap"
        >
          <template v-for="portal in portals" :key="portal.shortName">
            <div class="card text-center m-1" style="width: 18rem">
              <div
                class="card-header text-light"
                :style="{ backgroundColor: portal.colors[1].hex }"
              >
                <h5>
                  <nuxt-link
                    class="text-light"
                    :to="'/portal/' + portal.linkname"
                    >{{ portal.shortName }}</nuxt-link
                  >
                </h5>
              </div>
              <img
                :src="portal.portalicon"
                :alt="portal.shortName"
                class="w-25 m-auto"
                width="50px"
              />
              <div class="card-body d-flex flex-column justify-content-around">
                <h5 class="card-title">{{ portal.shortName }}</h5>
                <div class="card-text text-left" v-html="portal.header"></div>
                <small class="text-left text-muted p-1 mt-2">
                  In this portal you can register the following resources:
                </small>
                <ul class="list-group list-group-flush text-left">
                  <li
                    class="list-group-item"
                    v-for="guide in portal.guides"
                    :key="guide.name"
                  >
                    <font-awesome-icon
                      icon="fas fa-check"
                      class="text-dde-accent"
                    />
                    {{ guide.name }}
                  </li>
                </ul>
                <nuxt-link class="card-link" :to="'/portal/' + portal.linkname"
                  >Learn More</nuxt-link
                >
              </div>
              <div class="card-footer text-light"></div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BestPractices",
  head() {
    return {
      title: "DDE | Data Discovery Best Practices",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/wTG3pgRY/featured.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/wTG3pgRY/featured.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/best-practices",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/best-practices",
        },
        {
          property: "og:description",
          content:
            "The DDE metadata forms provide an easy way to create discoverable structured dataset metadata with little to no Schema.org microdata markup or FAIR data-sharing best-practices knowledge.",
        },
        {
          name: "description",
          content:
            "The DDE metadata forms provide an easy way to create discoverable structured dataset metadata with little to no Schema.org microdata markup or FAIR data-sharing best-practices knowledge.",
        },
        {
          name: "twitter:card",
          content:
            "The DDE metadata forms provide an easy way to create discoverable structured dataset metadata with little to no Schema.org microdata markup or FAIR data-sharing best-practices knowledge.",
        },
      ],
    };
  },
  computed: {
    portals: function () {
      return this.$store.getters.getPortals;
    },
  },
};
</script>
