<template>
  <div id="about" style="min-height: 100vh" class="bg-white">
    <div class="container" style="margin-top: 40px">
      <div class="jumbotron bg-white mt-5">
        <h1 class="text-dde-dark mb-0">About the Data Discovery Project</h1>
      </div>

      <div class="p-1">
        <h5 class="mainTextDark caps">
          A streamlined process to create, distribute and harvest findable via
          interoperable and extensible
          <a href="https://schema.org/" rel="noreferrer" target="_blank"
            >Schema.org</a
          >
          schemas.
        </h5>
        <img
          class="w-100"
          src="@/assets/img/diagram.svg"
          alt="Project Diagram"
        />
        <div class="alert-secondary text-left p-5">
          <ol>
            <li>
              Users interested in registering metadata with the goal of making
              their metadata Findable, Accessible, Interoperable and Reusable
              (FAIR).
            </li>
            <li>
              Users interested in developing a schema to represent the data they
              are interested in via an existing extensible schema standard.
            </li>
            <li>
              Metadata forms that output compliant structured metadata based on
              specific project requirements.
            </li>
            <li>
              A group of tools to help you create a schema and validation rules
              by extending existing classes.
            </li>
            <li>
              Project specific portals that take advantage of all the tools in
              the DDE to register compliant metadata based on their own unique
              schema and tools to manage that data.
            </li>
            <li>
              Metadata based on Schema.org standards that makes it indexable by
              major search engines.
            </li>
          </ol>
        </div>
      </div>
      <div class="mt-5 mb-5">
        <h5 class="mainTextDark caps">About this project</h5>
        <p class="text-muted" style="font-size: 1.4em">
          The biomedical and informatics communities have largely endorsed the
          spirit and basic components of the
          <a
            data-tippy-content="Findable, Accessible, Interoperable, & Reusable"
            href="https://www.go-fair.org/fair-principles/"
            target="_blank"
            >FAIR</a
          >
          Data Principles. Biomedical data producers need actionable
          best-practice guidance on how to make their data discoverable and
          reusable, and bring the practical benefits of data sharing to
          researcher’s own research projects, as well as the research community
          as a whole.
        </p>
        <p class="text-muted" style="font-size: 1.4em">
          Data hubs produce many valuable datasets which can be shared across
          the broader research community. A significant gap exists between the
          data providers and the data discovery portals where researchers look
          for relevant datasets. Data providers typically lack sufficient guides
          to expose their dataset metadata to these data portals. This project
          is targeted to streamline and minimize the efforts from data providers
          while maximizing the data discoverability.
        </p>
      </div>
      <div class="message mb-5 p-5 text-dde-dark text-center">
        <h2>Our Team</h2>
        <template v-for="team in teams" :key="team.name">
          <img :src="team.image" :alt="team.name" width="300" class="m-5" />
          <h4>
            Department of Integrative, Structural and Computational Biology
          </h4>
          <div
            class="d-flex justify-content-center align-items-start flex-wrap"
          >
            <template v-for="member in team.members" :key="member.name">
              <div class="card m-2" style="min-width: 15vw">
                <div class="card-header">
                  <img :src="member.image" class="rounded" width="100" />
                </div>
                <div class="card-body">
                  <h6 data-tippy-content="Click to learn more about them">
                    <a target="_blank" :href="member.personal_site">
                      {{ member.name }} {{ member.lastname }}
                      <font-awesome-icon icon="fa fa-external-link-alt" />
                    </a>
                  </h6>
                  <p>{{ member.title }}</p>
                </div>
              </div>
            </template>
          </div>
        </template>
        <div>
          <hr />
          <h5>Past Team Members</h5>
          <template v-for="person in pastContributors" :key="person.name">
            <p>
              <a :href="person.github" target="_blank">
                <font-awesome-icon icon="fab fa-github" /> {{ person.name }}
                {{ person.lastname }}
                <font-awesome-icon icon="fa fa-external-link-alt" />
              </a>
            </p>
          </template>
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
import { mapGetters } from "vuex";

export default {
  name: "About",
  head() {
    return {
      title: "DDE | About",
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
          content: "http://discovery.biothings.io/about",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/about",
        },
        {
          property: "og:description",
          content:
            "The biomedical and informatics communities have largely endorsed the spirit and basic components of the FAIR Data Principles. Biomedical data producers, including CTSA hubs, need actionable best-practice guidance on how to make their data discoverable and reusable, and bring the practical benefits of data sharing to researcher’s own research projects, as well as the research community as a whole",
        },
        {
          name: "description",
          content:
            "The biomedical and informatics communities have largely endorsed the spirit and basic components of the FAIR Data Principles. Biomedical data producers, including CTSA hubs, need actionable best-practice guidance on how to make their data discoverable and reusable, and bring the practical benefits of data sharing to researcher’s own research projects, as well as the research community as a whole",
        },
        {
          name: "twitter:card",
          content:
            "The biomedical and informatics communities have largely endorsed the spirit and basic components of the FAIR Data Principles. Biomedical data producers, including CTSA hubs, need actionable best-practice guidance on how to make their data discoverable and reusable, and bring the practical benefits of data sharing to researcher’s own research projects, as well as the research community as a whole",
        },
      ],
    };
  },
  computed: {
    ...mapGetters(["teams", "pastContributors"]),
  },
};
</script>
