<template>
  <div>
    <div
      class="jumbotron bg-light text-center p-1 hero mb-0 d-flex justify-content-center align-items-center"
      style="min-height: 100vh"
    >
      <div>
        <Logo></Logo>
        <h1 id="home" class="mt-5 text-light">
          DATA<br class="d-sm-block d-md-none" />
          DISCOVERY<br class="d-sm-block d-md-none" />
          ENGINE
        </h1>
        <div class="m-5">
          <h4 class="text-dde-muted caps d-none d-md-block">
            Enhance Data Discovery with Customized Metadata Schemas
          </h4>
          <h6 class="text-dde-muted caps d-block d-md-none">
            Enhance Data Discovery with Customized Metadata Schemas
          </h6>
          <nuxt-link class="text-dde-accent" to="/about"
            >Learn More About FAIR data-sharing practices
            <font-awesome-icon icon="fas fa-chevron-right"
          /></nuxt-link>
        </div>
      </div>
    </div>

    <div class="jumbotron bg-light p-5 text-center text-dde-dark m-0 shareBack">
      <h2 class="caps">Schema Playground</h2>
      <div class="d-flex justify-content-center align-items-stretch flex-wrap">
        <ToolCard
          cls="bg-dde-mid text-light"
          :image="reg"
          image_alt="Browse"
          title="Build a Metadata Schema That Works"
          text="Browse an extensive registry of schemas and extend any schema class to create a schema that is right for you"
          link="/registry"
          link_text="Browse our schemas"
        ></ToolCard>
        <ToolCard
          cls="bg-dde-mid text-light"
          image_alt="Visualize"
          :image="viz"
          title="Visualize and Register Your Schema"
          text="Register and manage your brand new schema with us. The DDE provides easy ways to visualize and update your contributions."
          link="/ns"
          link_text="Visualize your schema"
        ></ToolCard>
      </div>
    </div>
    <div
      class="jumbotron alert-dark p-5 text-center text-dde-dark waves-hero m-0"
    >
      <h2 class="caps">Metadata ToolKit</h2>
      <div class="d-flex justify-content-center align-items-stretch flex-wrap">
        <ToolCard
          cls="bg-light text-dde-dark"
          image_alt="validate"
          :image="gen"
          title="Generate Metadata"
          text="Test and generate structured metadata based on any schema registered within the DDE. "
          link="/markup-generator"
          link_text="Create metadata"
        ></ToolCard>
        <ToolCard
          cls="bg-light text-dde-dark"
          image_alt="Validate"
          :image="val"
          title="Validate Metadata"
          text="Validate existing metadata or metadata created on-the-fly against any schema registered in the DDE. "
          link="/validator"
          link_text="Validate metadata"
        ></ToolCard>
      </div>
    </div>
    <div
      class="jumbotron bg-light p-5 text-center text-dde-dark discoveryIntroBack m-0"
    >
      <h2 class="caps">Data Portals</h2>
      <div class="d-flex justify-content-center align-items-stretch flex-wrap">
        <ToolCard
          cls="bg-dde-dark text-light"
          image_alt="data_portals"
          :image="por"
          title="Metadata Suite"
          text="The DDE provides various portals to support biomedical projects by offering a suite of tools for creating, maintaining, and sharing structured metadata."
          link="/portal"
          link_text="Explore Portals"
        >
          <ul class="text-left">
            <li>Register a custom schema</li>
            <li>Advanced metadata intake guides</li>
            <li>Share and embed your metadata easily</li>
            <li>Metadata field coverage</li>
            <li>Schema/Metadata management dashboard</li>
          </ul>
          <p>
            <a
              href="https://github.com/biothings/discovery-app/issues/new/choose"
              target="_blank"
              rel="nonreferrer"
              >Apply to get your project added to the DDE.</a
            >
          </p>
        </ToolCard>
        <div
          class="tool-card card text-center m-2 grad d-flex justify-content-center align-items-center"
        >
          <h4 class="text-center text-light">Data Portals Available:</h4>
          <div class="row m-0 powered-hero">
            <template
              v-if="portals.length"
              v-for="(portal, i) in portals"
              :key="portal.name"
            >
              <div
                class="col-sm-2 col-md-4 p-1 d-flex justify-content-center align-items-center"
              >
                <NuxtLink :to="'/portal/' + portal.linkname">
                  <img
                    :src="portal.image"
                    class="w-75"
                    data-aos="flip-left"
                    :data-aos-delay="i * 100"
                    :data-tippy-content="portal.name"
                  />
                </NuxtLink>
              </div>
            </template>
            <div class="col-sm-12 d-flex justify-content-center">
              <NuxtLink to="/portal">
                <MoreButton
                  style="width: 200px"
                  data-tippy-content="View All Portals"
                ></MoreButton>
              </NuxtLink>
            </div>
            <div class="alert bg-light text-dde-dark m-5 bold">
              <p>
                Feature your project here.
                <a
                  href="https://github.com/biothings/discovery-app/issues/new/choose"
                  target="_blank"
                  rel="nonreferrer"
                  >Fill out an application to get started today</a
                >.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="jumbotron bg-dde-dark reg-hero text-center m-0">
      <h1 class="text-light caps">Registries</h1>
      <div
        class="container d-flex justify-content-center align-items-center row m-auto flex-wrap"
      >
        <div
          id="bestPractices"
          class="jumbotron bg-none text-center pRelative col-sm-12 col-md-5"
        >
          <div class="link-wrapper">
            <nuxt-link
              class="link hover-1 mt-5"
              to="/registry"
              style="z-index: 2"
            >
              <img :src="schema_reg" width="150" alt="schema registry" />
              <h3 class="text-light">
                Schema Registry
                <font-awesome-icon
                  icon="fas fa-chevron-right"
                  class="d-inline text-dde-accent"
                />
              </h3>
            </nuxt-link>
            <p class="m-auto text-light o-0 d-none d-md-block">
              Search existing schemas and extend any class to create a schema
              that's right for you
            </p>
            <p class="m-auto text-light d-sm-block d-md-none">
              Search existing schemas and extend any class to create a schema
              that's right for you
            </p>
          </div>
        </div>
        <div
          id="schemaPlayground"
          class="jumbotron bg-none text-center pRelative col-sm-12 col-md-5"
        >
          <div class="link-wrapper">
            <nuxt-link
              class="link hover-1 mt-5"
              to="/dataset"
              style="z-index: 2"
            >
              <img :src="res_reg" width="150" alt="resource registry" />
              <h3 class="text-light">
                Metadata Registry
                <font-awesome-icon
                  icon="fas fa-chevron-right"
                  class="d-inline text-dde-light"
                />
              </h3>
            </nuxt-link>
            <p class="m-auto text-light o-0 d-none d-md-block">
              Browse registered structured metadata created using our schemas
            </p>
            <p class="m-auto text-light d-sm-block d-md-none">
              Browse registered structured metadata created using our schemas
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-dde-mid jumbotron m-0">
      <p class="text-center bold text-light">
        The Data Discovery Engine is a project from the
        <a href="http://wulab.io/" rel="noreferrer" target="_blank">Wu Lab</a>
        at Scripps Research and is supported by the National Center for
        Advancing Translational Sciences (5 U24 TR002306).
      </p>
    </div>
  </div>
</template>

<script>
import Logo from "../components/Logo.vue";
import MoreButton from "../components/MoreButton.vue";
import ToolCard from "../components/ToolCard.vue";
import validator_img from "../assets/img/validator.svg";
import generator_img from "../assets/img/generator.svg";
import portal_img from "../assets/img/portal.svg";
import res_reg from "../assets/img/resource_reg.svg";
import schema_reg from "../assets/img/schema-reg.svg";
import reg from "../assets/img/build-schema.svg";
import viz from "../assets/img/visualize-schema.svg";
import AOS from "aos";

export default {
  name: "Home",
  head() {
    return {
      title: "DDE | Home",
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
  components: {
    Logo,
    ToolCard,
  },
  computed: {
    portals: function () {
      return this.$store.getters.getPortals;
    },
  },
  data: function () {
    return {
      val: validator_img,
      gen: generator_img,
      por: portal_img,
      reg: reg,
      viz: viz,
      res_reg: res_reg,
      schema_reg: schema_reg,
    };
  },
  mounted: function () {
    setTimeout(() => {
      AOS.init();
    }, 1000);
  },
};
</script>
