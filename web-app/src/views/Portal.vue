<template>
  <div id="portal" class="container-fluid p-0" style="min-height: 80vh">
    <template v-if="portal && portal.name">
      <div class="row m-0">
        <div
          class="text-center col-sm-12 p-0"
          :style="{ background: gradient }"
        >
          <div class="lines p-5">
            <DynamicImage
              class="mt-4"
              :imagePath="portal.image"
              :alt="portal.name"
              width="300"
            ></DynamicImage>
            <RouterLink to="/portal" class="d-block text-info"
              ><font-awesome-icon icon="fas fa-chevron-left" /> Back to
              Portals</RouterLink
            >
          </div>
        </div>
        <div
          class="col-sm-12 col-md-8 py-5 d-flex justify-content-center align-items-center"
        >
          <div>
            <div class="d-flex justify-content-start align-items-center">
              <DynamicImage
                :imagePath="portal.portalicon"
                :alt="portal.name"
                width="100"
                class="mr-2"
              ></DynamicImage>
              <h1 :style="{ color: portal.colors[1].hex }">
                <span v-text="portal.name"></span>
              </h1>
            </div>
            <h5 class="text-capitalize mt-3" v-text="portal.header"></h5>
            <div class="text-muted" v-html="portal.description"></div>
            <template v-if="window.location.pathname == '/portal/n3c'">
              <div class="border-top text-center text-muted p-2">
                <h4>External Dataset Request</h4>
                <p>
                  To enable some integrated analysis with the N3C dataset, you
                  can request to include an external dataset in the N3C Enclave
                  environment.
                </p>
                <div class="text-center p-2 m-1 rounded p-3">
                  <RouterLink
                    role="button"
                    :style="{ background: portal.colors[0].hex }"
                    class="btn text-light btn-lg nd mt-2 tip"
                    to="/guide/n3c/dataset"
                    :data-tippy-info="'Add a dtaset for ' + portal.name"
                  >
                    Submit Request
                  </RouterLink>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="border-top text-center text-muted p-2">
                <h4>Contribute</h4>
                <p>
                  Follow an easy-to-follow guide to help you contribute metadata
                  for <span v-text="portal.name"></span> following this schema's
                  <RouterLink :to="{path: portal.schema}">structure</RouterLink>:
                </p>
                <div
                  v-for="(g, i) in portal.guides"
                  :key="i + 'g'"
                  class="text-center p-2 m-1 rounded p-3"
                >
                  <RouterLink
                    role="button"
                    :style="{ background: portal.colors[0].hex }"
                    @click="
                      gtag('event', 'click', {
                        event_category: 'portal_guide',
                        event_label: g.guide,
                        event_value: 1,
                      })
                    "
                    class="btn text-light btn-lg nd mt-2 tip"
                    :to="{path: g.guide}"
                  >
                    <font-awesome-icon icon="fas fa-plus" /> Add
                    <b v-text="g.name"></b> Metadata
                  </RouterLink>
                </div>
              </div>
            </template>
          </div>
        </div>
        <div
          class="col-sm-12 col-md-4 d-flex flex-column justify-content-center align-items-stretch alert-secondary p-5"
        >
          <div
            class="text-center p-2 m-1 rounded p-3"
            @mouseenter="hover('web')"
          >
            <object
              id="web"
              type="image/svg+xml"
              :data="web_pic"
              width="100"
              alt="WEBSITE"
            ></object>
            <a
              :href="portal.site"
              target="_blank"
              rel="noreferrer"
              class="nd mt-2 tip text-info"
              :data-tippy-info="'Explore the ' + portal.name + ' website'"
            >
              <h5>Site <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </a>
          </div>
          <div
            class="text-center p-2 m-1 rounded p-3"
            @mouseenter="hover('schema')"
          >
            <object
              id="schema"
              type="image/svg+xml"
              :data="schema_pic"
              width="100"
              alt="SCHEMA"
            ></object>
            <RouterLink
              :to="{path: portal.schema}"
              class="nd mt-2 tip text-info"
              :data-tippy-info="'Explore the schema used in ' + portal.name"
            >
              <h5>Schema <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </RouterLink>
          </div>
          <div
            v-for="(g, i) in portal.guides"
            :key="i + 'gg'"
            class="text-center p-2 m-1 rounded p-3"
            @mouseenter="hover(i + 'data')"
          >
            <object
              :id="i + 'data'"
              type="image/svg+xml"
              :data="dataset_pic"
              width="100"
              :alt="g.name"
            ></object>
            <RouterLink
              :to="{path: g.registry}"
              class="nd mt-2 tip text-info"
              :data-tippy-info="
                'Browse metadata in Data Discovery Engine for ' + g.name
              "
            >
              <h5>
                <span v-text="g.name + 's'"></span>
                <font-awesome-icon icon="fas fa-chevron-right" />
              </h5>
            </RouterLink>
          </div>
          <div
            v-if="portal && portal.api"
            class="text-center p-2 m-1 rounded p-3"
            @mouseenter="hover('api')"
          >
            <object
              id="api"
              type="image/svg+xml"
              :data="api_pic"
              width="100"
              alt="API"
            ></object>
            <a
              :href="portal.api"
              target="_blank"
              rel="noreferrer"
              class="nd mt-2 tip text-info"
              :data-tippy-info="'Explore API for ' + portal.name"
            >
              <h5>API <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </a>
          </div>
          <div
            v-if="portal && portal.faq_link"
            class="text-center p-2 m-1 rounded p-3"
            @mouseenter="hover('api')"
          >
            <object
              id="api"
              type="image/svg+xml"
              :data="faq_pic"
              width="100px"
              alt="API"
            ></object>
            <RouterLink
              :to="{path: portal.faq_link}"
              class="nd mt-2 tip text-info"
              data-tippy-info="Frequently Asked Questions"
            >
              <h5>FAQ <font-awesome-icon icon="fas fa-chevron-right" /></h5>
            </RouterLink>
          </div>
        </div>
        <div class="text-center p-5 col-sm-12 mainBackLight p-2"></div>
      </div>
    </template>
  </div>
</template>

<script>
import Vivus from "vivus";
import tippy from "tippy.js";
import site from "../assets/img/site.svg";
import api from "../assets/img/api-01.svg";
import schema from "../assets/img/sp1-01.svg";
import faq from "../assets/img/faq-01.svg";
import dataset from "../assets/img/dataset-01.svg";

import DynamicImage from "../components/DynamicImage.vue";

export default {
  name: "Portal",
  data: function () {
    return {
      web_pic: site,
      api_pic: api,
      schema_pic: schema,
      faq_pic: faq,
      dataset_pic: dataset,
      window: window,
      portal: {},
      colors: [],
      portals: [
        {
          name: "Outbreak.info",
          header:
            "During outbreaks of emerging diseases such as COVID-19, efficiently collecting, sharing, and integrating data is critical to scientific research. Outbreak.info is a resource to aggregate all this information into a single location.",
          linkname: "outbreak",
          description: `<p>
            In response to the current outbreak of SARS-CoV-2 (the virus that causes COVID-19), researchers worldwide have been generating and openly sharing data, publications, reagents, code, protocols, and more. Broad sharing of these research resources improves the speed and efficiency of science. Unfortunately, there are no uniform standards and repositories for collecting all this information in one place.
            </p><p>
            Outbreak.info focuses on aggregating all SARS-CoV-2 / COVID-19 information into a single site. We focus on making the metadata about these resources more standardized, on creating web interfaces to make the resources more findable, and on a few focused data integration efforts to make data more usable.
            </p>`,
          image: "outbreak_white.svg",
          portalicon: "icon-01.svg",
          api: "https://api.outbreak.info/",
          site: "https://outbreak.info/",
          schema: "/view/outbreak",
          guides: [
            {
              guide: "/guide/outbreak/dataset",
              name: "Dataset",
              registry: "/dataset?guide=/guide/outbreak/dataset",
            },
          ],
          datasets: "/dataset?guide=/guide/outbreak/dataset",
          colors: [{ hex: "#D13B62" }, { hex: "#0A253D" }],
        },
        {
          name: "NIAID Data Portal",
          header:
            "AN AGGREGATOR OF OPEN DATASETS, WITH A PARTICULAR FOCUS ON ALLERGY AND INFECTIOUS DISEASES",
          linkname: "niaid",
          description: `<p>
            The NIAID (National Institute of Allergy and Infectious Diseases) Data Portal aggregates <b class="tip text-info" data-tippy-info="Omics DI,NCBI GEO, Zenodo, Harvard Dataverse, NYU Data Catalog, ImmPort, Data Discovery Engine">7 different data sources</b> together in a searchable platform, making it easier to find datasets.
            </p><p>
            We also standardize the dataset metadata to a common form, increasing the findability of these datasets. Schema.org provides a widely accepted format regonizable by major search engines and data portals.
            </p><p>
            While some dataset providers already use this format to describe their datasets, others provide structured metadata in their own format. Learn more about our efforts to encapsulate non-standard dataset metdata in schema.org's format.
            </p>`,
          image: "niaid/logo.svg",
          portalicon: "niaid/icon.svg",
          site: "https://discovery.biothings.io/niaid/",
          schema: "/view/niaid",
          guides: [
            {
              guide: "/guide/niaid",
              name: "Dataset",
              registry: "/dataset?guide=/guide/niaid",
            },
            {
              guide: "/guide/niaid/ComputationalTool",
              name: "Computational Tool",
              registry: "/dataset?guide=/guide/niaid/ComputationalTool",
            },
          ],
          datasets: "/dataset?guide=/guide/niaid",
          colors: [{ hex: "#369AC1" }, { hex: "#113B56" }],
        },
        {
          name: "CTSA National Center for Data to Health",
          header:
            "A CD2H PROJECT TO PROMOTE FAIR DATA-SHARING BEST PRACTICES & MAXIMIZE THE RESEARCH IMPACT OF CTSA HUBS",
          linkname: "cd2h",
          description: `<p>
              Informatics advancements, coupled with a shift towards open science, are in the process of fundamentally transforming how we approach translational research and clinical care. The CTSA Program is poised to help realize precision medicine by leveraging informatics tools and expertise within CTSA hubs to solve key informatics challenges across the translational spectrum.
            </p><p>
            The CD2H was funded in fall 2017 to coordinate and integrate informatics for the CTSA Program by promoting data reuse and interoperability, tool sharing, informatics fluency, and collaboration. We are here to serve the CTSA Program by creating additional resources, building impactful infrastructure, and further coalescing the community to develop and implement innovative solutions.
            </p><p>
            Towards these goals, CD2H seeks input from, and collaboration with, the CTSA Program. We convene the community through our CORES and Community Projects focused on data, software, and people; and partner with the community to iteratively develop solutions through CD2H Labs and our DREAM Challenges. The ultimate goal of the CD2H is to help CTSA Hubs thrive, accelerate advancements in informatics, and improve patient care.
            </p>`,
          image: "cd2h-logo-white.png",
          portalicon: "dde-logo-o.svg",
          site: "https://ctsa.ncats.nih.gov/cd2h/",
          schema: "/view/biomedical",
          guides: [
            {
              guide: "/guide",
              name: "Dataset",
              registry: "/dataset?guide=/guide",
            },
          ],
          api: "https://crawler.biothings.io/",
          datasets: "/dataset?guide=/guide",
          colors: [{ hex: "#63296B" }, { hex: "#4A7D8F" }],
        },
        {
          name: "The National COVID Cohort Collaborative (N3C)",
          header:
            "The N3C aims to improve the efficiency and accessibility of analyses using a very large row-level (patient-level) COVID-19 clinical dataset and demonstrate a novel approach for collaborative pandemic data sharing.",
          linkname: "n3c",
          description: `<p>
              The National COVID Cohort Collaborative (N3C) is a complementary and synergistic partnership among the <a href="https://ncats.nih.gov/ctsa" target="_blank">Clinical and Translational Science Awards (CTSA) Program</a> hubs, the <a href="https://cd2h.org/" target="_blank">National Center for Data to Health (CD2H)</a>, distributed clinical data networks (PCORnet, OHDSI, ACT/i2b2, TriNetX), and other partner organizations, with overall stewardship by NIH’s  <a href="https://ncats.nih.gov/" target="_blank">National Center for Advancing Translational Sciences (NCATS)</a>.
            </p><p>
              The N3C aims to improve the efficiency and accessibility of analyses using a very large row-level (patient-level) COVID-19 clinical dataset and demonstrate a novel approach for collaborative pandemic data sharing.
            </p>`,
          image: "N3Cwhite.png",
          portalicon: "N3Co.png",
          site: "https://covid.cd2h.org/N3C",
          schema: "/view/n3c",
          guides: [
            {
              guide: "/guide/n3c/dataset",
              name: "Dataset",
              registry: "/dataset?guide=/guide/n3c/dataset",
            },
          ],
          datasets: "/dataset?guide=/guide/n3c/dataset",
          colors: [{ hex: "#4B7E8F" }, { hex: "#64296B" }],
          faq_link: "/faq/n3c",
        },
      ],
    };
  },
  props: ["portal_name"],
  components: {
    DynamicImage,
  },
  methods: {
    redirect() {
      let timerInterval;
      this.$swal
        .fire({
          title: "Portal Does Not Exist!",
          icon: "error",
          html: "Taking you to the Portals page in <b></b> seconds...",
          timer: 2000,
          timerProgressBar: true,
          didOpen: () => {
            this.$swal.showLoading();
            const b = this.$swal.getHtmlContainer().querySelector("b");
            timerInterval = setInterval(() => {
              b.textContent = this.$swal.getTimerLeft();
            }, 100);
          },
          willClose: () => {
            clearInterval(timerInterval);
          },
        })
        .then((result) => {
          /* Read more about handling dismissals below */
          if (result.dismiss === this.$swal.DismissReason.timer) {
            this.$router.push({ name: "Portals" });
          }
        });
    },
    hover(id) {
      new Vivus(id, { duration: 100 });
    },
  },
  watch: {
    portal_name: {
      immediate: true,
      handler: function (v) {
        switch (v) {
          case "niaid":
            this.portal = this.portals[1];
            break;
          case "outbreak":
            this.portal = this.portals[0];
            break;
          case "cd2h":
            this.portal = this.portals[2];
            break;
          case "n3c":
            this.portal = this.portals[3];
            break;
          default:
            this.redirect();
        }
        this.colors = this.portal["colors"];
      },
    },
  },
  mounted: function () {
    tippy("[data-tippy-info]", {
      placement: "bottom",
      theme: "light",
      content: "loading",
      interactive: true,
      animation: "fade",
      onShow(instance) {
        instance.setContent(instance.reference.dataset.tippyInfo);
      },
    });
  },
  computed: {
    gradient() {
      let colors = "linear-gradient(45deg";
      this.colors.forEach(function (e) {
        colors += "," + e.hex;
      });
      colors += " 30%)";
      //   console.log(colors);
      return colors;
    },
  },
};
</script>
