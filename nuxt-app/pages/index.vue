<template>
  <div>
    <div
      class="jumbotron bg-light text-center p-1 hero mb-0 d-flex justify-content-center align-items-center"
      style="min-height: 100vh"
    >
      <div>
        <h1 id="home" class="logoText mt-5 logoFont">
          DATA<br class="d-sm-block d-md-none" />
          DISCOVERY<br class="d-sm-block d-md-none" />
          ENGINE
        </h1>
        <div
          id="animation_container"
          style="
            background-color: rgba(68, 68, 68, 00);
            width: 640px;
            height: 480px;
            zoom: 0.5;
          "
        >
          <img
            alt="Vue logo"
            class="logo"
            src="@/assets/img/dde-logo-o.svg"
            width="400"
            height="400"
          />
          <div
            id="dom_overlay_container"
            style="
              pointer-events: none;
              overflow: hidden;
              width: 640px;
              height: 480px;
              position: absolute;
              left: 0px;
              top: 0px;
              display: block;
            "
          ></div>
        </div>
        <div class="m-5">
          <h4 class="text-muted lighter caps d-none d-md-block">
            A CD2H PROJECT TO PROMOTE FAIR DATA-SHARING BEST PRACTICES &
            MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS
          </h4>
          <h6 class="text-muted lighter caps d-block d-md-none">
            A CD2H PROJECT TO PROMOTE FAIR DATA-SHARING BEST PRACTICES &
            MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS
          </h6>
          <nuxt-link class="text-muted" to="/about"
            >Learn More <font-awesome-icon icon="fas fa-chevron-right"
          /></nuxt-link>
        </div>
      </div>
    </div>

    <div class="jumbotron grad">
      <div class="container d-flex justify-content-around m-auto flex-wrap">
        <div
          id="bestPractices"
          class="jumbotron bg-none text-center pRelative tip"
        >
          <div class="link-wrapper">
            <nuxt-link
              class="link hover-1 mt-5"
              to="/best-practices"
              style="z-index: 2"
            >
              <h3 class="text-light">
                DISCOVERY
                <font-awesome-icon
                  icon="fas fa-chevron-right"
                  class="d-inline d-md-none"
                />
              </h3>
            </nuxt-link>
            <p class="m-auto w-75 text-light o-0 d-none d-md-block">
              Follow best practices to make your data more findable
            </p>
            <p class="m-auto w-75 text-light d-sm-block d-md-none">
              Follow best practices to make your data more findable
            </p>
          </div>

          <div class="discoverBack"></div>
        </div>
        <div
          id="schemaPlayground"
          class="jumbotron bg-none text-center pRelative tip"
        >
          <div class="link-wrapper">
            <nuxt-link
              class="link hover-1 mt-5"
              to="/schema-playground"
              style="z-index: 2"
            >
              <h3 class="text-light">
                SCHEMA PLAYGROUND
                <font-awesome-icon
                  icon="fas fa-chevron-right"
                  class="d-inline d-md-none"
                />
              </h3>
            </nuxt-link>
            <p class="m-auto w-75 text-light o-0 d-none d-md-block">
              Build and host your own schema for better interoperability
            </p>
            <p class="m-auto w-75 text-light d-sm-block d-md-none">
              Build and host your own schema for better interoperability
            </p>
          </div>
          <div class="buildBack"></div>
        </div>
      </div>
      <div class="p-2 text-center text-light">
        <p class="lighter">
          Don't know where to start?
          <a
            id="demo"
            href="#"
            class="link text-light bold"
            @click.prevent="showHelp()"
            v-text="help ? 'Hide Help' : 'Click Here'"
          ></a>
        </p>
      </div>
    </div>

    <div class="jumbotron bg-light">
      <div class="container d-flex justify-content-around m-auto flex-wrap">
        <h2 class="text-muted lighter caps w-100 text-center">
          Discover & Access Dataset Metadata
        </h2>
        <h5 class="text-muted lighter caps mb-5 w-100 text-center">
          See what structured metadata can do
        </h5>
        <div class="m-0 p-5 text-center col-sm-12">
          <h3 class="logoText">Browse Registered Schemas & Metadata</h3>
          <nuxt-link class="btn btn-outline-info" role="button" to="/registries"
            >Continue</nuxt-link
          >
        </div>
        <div class="card col-sm-12 col-md-6">
          <img
            src="@/assets/img/logofull.svg"
            class="card-img-top p-2"
            alt="Metadata Plus"
            height="115px"
          />
          <div class="card-body">
            <h5 class="card-title mainTextDark">METADATA PLUS</h5>
            <h5 class="card-text text-muted">
              A service to transforms non-structured published metadata into
              <a href="https://schema.org/" rel="noreferrer" target="_blank"
                >Schema.org</a
              >-standard structured metadata.
            </h5>
            <a href="https://metadataplus.biothings.io" target="_blank">
              Learn More <font-awesome-icon icon="fas fa-external-link-alt" />
            </a>
          </div>
        </div>
        <div class="card col-sm-12 col-md-6">
          <img
            src="@/assets/img/crawlerfull.svg"
            class="card-img-top p-2"
            alt="Metadata Crawler"
            height="115px"
          />
          <div class="card-body">
            <h5 class="card-title mainTextDark">METADATA CRAWLER</h5>
            <h5 class="card-text text-muted">
              A service that harvests biomedical
              <a href="https://schema.org/" rel="noreferrer" target="_blank"
                >Schema.org</a
              >-standard structured dataset metadata and makes it available
              through an API.
            </h5>
            <a href="https://crawler.biothings.io" target="_blank">
              Learn More <font-awesome-icon icon="fas fa-external-link-alt" />
            </a>
          </div>
        </div>
      </div>
    </div>

    <div class="jumbotron bg-light text-muted text-center">
      <div class="container">
        <div class="row">
          <div class="col-sm-12 col-md-6">
            <img
              class="w-100 rounded"
              src="@/assets/img/involved-01.png"
              style="border-radius: 20px"
              alt="join us"
            />
          </div>
          <div class="col-sm-12 col-md-6 p-3">
            <h3 class="text-muted lighter caps" id="get-involved">
              Get Involved!
            </h3>
            <img
              class="margin20"
              src="@/assets/img/cd2h-logo.png"
              width="200px"
              alt="logo"
            />
            <p class="text-muted w-75 m-auto">
              The CD2H project uses the onboarding form to track community
              interest and engagement in CD2H projects and working groups. You
              are welcome to participate at any level, whether contributing
              requirements, code, or just casually following the project as it
              progresses. Simply check the box indicating you're interested in
              the 'discovery engine', we will get in touch.
              <a target="_blank" href="mailto:data2health@gmail.com"
                >Contact us</a
              >
              if you have any questions.
            </p>
            <a
              target="_blank"
              href="http://bit.ly/cd2h-onboarding-form"
              role="button"
              class="btn themeButton pulse text-light mt-4"
              >Join Now</a
            >
          </div>
        </div>
      </div>
    </div>

    <div class="jumbotron bg-light text-muted text-center">
      <div class="container">
        <div class="row">
          <div class="col-sm-12 col-md-6 p-3">
            <h3 class="text-muted lighter caps" id="connect">CONNECT</h3>
            <dl>
              <dt>
                <font-awesome-icon
                  icon="fab fa-github fa-2x"
                  class="mainTextDark"
                />
                <br />
                <a
                  class="mainTextDark"
                  target="_blank"
                  href="https://github.com/data2health/rdp-portal"
                >
                  Reusable data best practice portal (rdp-portal)</a
                >
              </dt>
              <dd class="text-muted">Learn more about our project on GitHub</dd>
              <dt>
                <font-awesome-icon
                  icon="fab fa-github fa-2x"
                  class="mainTextLight"
                />
                <br />
                <a
                  class="mainTextLight"
                  target="_blank"
                  href="https://github.com/biothings/discovery-app"
                >
                  Data Discovery Engine Github</a
                >
              </dt>
              <dd class="text-muted">
                Contribute to the development of this site on GitHub
              </dd>
            </dl>
          </div>
          <div class="col-sm-12 col-md-6">
            <img
              class="w-100 rounded"
              src="@/assets/img/connect.png"
              alt="join us"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tippy from "tippy.js";

export default {
  name: "Home",
  head() {
    return {
      title: "DDE | Home",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/",
        },
        {
          property: "og:description",
          content:
            "A project to promote FAIR data-sharing best practices & maximize the research impact of CTSA hubs.",
        },
        {
          name: "description",
          content:
            "A project to promote FAIR data-sharing best practices & maximize the research impact of CTSA hubs.",
        },
        {
          name: "twitter:card",
          content:
            "A project to promote FAIR data-sharing best practices & maximize the research impact of CTSA hubs.",
        },
      ],
    };
  },
  data: function () {
    return {
      help: false,
      bestPractices: null,
      schemaPlayground: null,
    };
  },
  watch: {
    help: function (h) {
      var self = this;
      if (h) {
        self.bestPractices[0].show();
        self.schemaPlayground[0].show();
      } else {
        self.bestPractices[0].hide();
        self.schemaPlayground[0].hide();
      }
    },
  },
  methods: {
    showHelp() {
      this.help = !this.help;
    },
  },
  mounted: function () {
    this.bestPractices = tippy("#bestPractices", {
      interactive: true,
      arrow: true,
      allowHTML: true,
      hideOnClick: false,
      trigger: "manual",
      content: `<div class="mainBackLight text-light text-center p-1">
                      BEST PRACTICES
                  </div>
                  <div class="alert alert-light m-0">
                    If you have a dataset, and want to share it properly, so that others can find it, use it for their research and attribute your work properly.
                  </div>`,
      animation: "fade",
      theme: "light",
    });
    this.schemaPlayground = tippy("#schemaPlayground", {
      interactive: true,
      arrow: true,
      allowHTML: true,
      hideOnClick: false,
      trigger: "manual",
      content: `<div class="mainBackDark text-light text-center p-1">
                    SCHEMA PLAYGROUND
                  </div>
                  <div class="alert alert-light m-0">
                    If you are starting a new project, and want to plan ahead, so that the data coming out of your project will be FAIR (Findable, Accessible, Interoperable, Reusable) from the beginning.
                  </div>`,
      animation: "fade",
      theme: "light",
    });
  },
};
</script>
