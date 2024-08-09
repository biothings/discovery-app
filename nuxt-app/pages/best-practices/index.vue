<template>
  <div id="guides" class="container-fluid text-dark min-100">
    <Title title="Resource Discovery Best Practices"></Title>
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
        <h1 class="text-dde-dark">Choose a Template</h1>
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
          <div class="card text-center m-1" style="width: 18rem">
            <div class="card-header">
              Data Portal | <nuxt-link to="/portal/cd2h">CD2H</nuxt-link>
            </div>
            <img
              src="@/assets/img/cd2h-logo.png"
              alt="CD2H"
              class="w-50 m-auto"
              width="50px"
            />
            <div class="card-body d-flex flex-column justify-content-around">
              <h5 class="card-title">CD2H</h5>
              <p class="card-text">
                <b> CTSA National Center for Data to Health </b> (<a
                  href="https://ctsa.ncats.nih.gov/cd2h/"
                  target="_blank"
                  rel="nonreferrer"
                  >CD2H <font-awesome-icon icon="fas fa-external-link-alt" /></a
                >) biomedical dataset metadata based on this
                <nuxt-link to="/view/biomedical/" rel="nonreferrer"
                  >schema <font-awesome-icon icon="fas fa-external-link-alt"
                /></nuxt-link>
                structure.
                <small
                  class="text-info more"
                  data-tippy-content="You can choose data portals you are interested in and add their requirements"
                  >Customizable</small
                >
              </p>
              <nuxt-link
                to="/guide"
                @click="
                  $gtag.event('click', {
                    event_category: 'portal_guide',
                    event_label: '/guide',
                    event_value: 1,
                  })
                "
                class="btn btn-lg themeButton text-light"
                role="button"
              >
                <font-awesome-icon icon="fas fa-plus" /> Add Dataset Metadata
              </nuxt-link>
            </div>
            <div class="card-footer text-light bg-dde-mid">
              <b>About this guide:</b>
              <table class="table table-sm table-dark table-striped">
                <tbody>
                  <tr>
                    <td>
                      <small>Intend</small>
                    </td>
                    <td>
                      <small class="badge badge-dark">General Purpose</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Topics</small>
                    </td>
                    <td>
                      <small class="badge badge-light">Biomedical</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Associations</small>
                    </td>
                    <td>
                      <nuxt-link to="/portal/cd2h"
                        ><small class="badge badge-light"
                          >CD2H</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Schema</small>
                    </td>
                    <td>
                      <nuxt-link to="/view/biomedical"
                        ><small class="badge badge-light"
                          >Dataset</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="card text-center m-1" style="width: 18rem">
            <div class="card-header">
              Data Portal | <nuxt-link to="/portal/n3c">N3C</nuxt-link>
            </div>
            <img
              src="@/assets/img/N3C.png"
              alt="CD2H"
              class="w-50 m-auto"
              width="50px"
            />
            <div class="card-body d-flex flex-column justify-content-around">
              <h5 class="card-title">N3C</h5>
              <p class="card-text">
                <b> The National COVID Cohort Collaborative </b> (<a
                  href="https://covid.cd2h.org/N3C"
                  target="_blank"
                  rel="nonreferrer"
                  >N3C <font-awesome-icon icon="fas fa-external-link-alt" /></a
                >) dataset metadata based on this
                <nuxt-link to="/view/n3c/" rel="nonreferrer"
                  >schema <font-awesome-icon icon="fas fa-external-link-alt"
                /></nuxt-link>
                structure.
              </p>
              <nuxt-link
                to="/guide/n3c/dataset"
                @click="
                  $gtag.event('click', {
                    event_category: 'portal_guide',
                    event_label: '/guide/n3c/dataset',
                    event_value: 1,
                  })
                "
                class="btn btn-lg themeButton text-light"
                role="button"
              >
                <font-awesome-icon icon="fas fa-plus" /> Submit Request
              </nuxt-link>
            </div>
            <div class="card-footer text-light bg-dde-mid">
              <b>About this guide:</b>
              <table class="table table-sm table-dark table-striped">
                <tbody>
                  <tr>
                    <td>
                      <small>Intend</small>
                    </td>
                    <td>
                      <small class="badge badge-info">Portal Specific</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Topics</small>
                    </td>
                    <td>
                      <small class="badge badge-light">COVID-19</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Associations</small>
                    </td>
                    <td>
                      <nuxt-link to="/portal/cd2h"
                        ><small class="badge badge-light"
                          >CD2H</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Schema</small>
                    </td>
                    <td>
                      <nuxt-link to="/view/n3c"
                        ><small class="badge badge-light"
                          >Dataset</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="card text-center m-1" style="width: 18rem">
            <div class="card-header">
              Data Portal |
              <nuxt-link to="/portal/outbreak">Outbreak.info</nuxt-link>
            </div>
            <img
              src="@/assets/img/outbreak.svg"
              alt="outbreak.info"
              class="card-img-top p-2"
              width="150px"
            />
            <div class="card-body d-flex flex-column justify-content-around">
              <h5 class="card-title">Outbreak.info</h5>
              <p class="card-text">
                <b>Outbreak.info</b> (<a
                  href="https://outbreak.info/"
                  target="_blank"
                  rel="nonreferrer"
                  >Outbreak.info
                  <font-awesome-icon icon="fas fa-external-link-alt" /></a
                >) COVID-19 epidimiology dataset metadata based on this
                <nuxt-link to="/view/outbreak/" rel="nonreferrer"
                  >schema <font-awesome-icon icon="fas fa-external-link-alt"
                /></nuxt-link>
                structure.
              </p>
              <nuxt-link
                to="/guide/outbreak/dataset"
                @click="
                  $gtag.event('click', {
                    event_category: 'portal_guide',
                    event_label: '/guide/outbreak/dataset',
                    event_value: 1,
                  })
                "
                class="btn btn-lg themeButton text-light"
                role="button"
              >
                <font-awesome-icon icon="fas fa-plus" /> Add Dataset Metadata
              </nuxt-link>
            </div>
            <div class="card-footer text-light bg-dde-mid">
              <b>About this guide:</b>
              <table class="table table-sm table-dark table-striped">
                <tbody>
                  <tr>
                    <td>
                      <small>Intend</small>
                    </td>
                    <td>
                      <small class="badge badge-info">Portal Specific</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Topics</small>
                    </td>
                    <td>
                      <small class="badge badge-light">COVID-19</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Associations</small>
                    </td>
                    <td>
                      <nuxt-link to="/portal/outbreak"
                        ><small class="badge badge-light"
                          >Outbreak.info</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Schema</small>
                    </td>
                    <td>
                      <nuxt-link to="/view/outbreak"
                        ><small class="badge badge-light"
                          >Dataset</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="card text-center m-1" style="width: 18rem">
            <div class="card-header">
              Data Portal | <nuxt-link to="/portal/niaid">NIAID</nuxt-link>
            </div>
            <img
              src="@/assets/img/niaid/logo.svg"
              alt="NIAID"
              class="card-img-top p-2"
              width="150px"
            />
            <div class="card-body d-flex flex-column justify-content-around">
              <h5 class="card-title">NIAID Systems Biology</h5>
              <p class="card-text">
                <b
                  >National Institute of Allergy and Infectious Diseases (<a
                    href="https://www.niaid.nih.gov/"
                    target="_blank"
                    rel="nonreferrer"
                    >NIAID
                    <font-awesome-icon icon="fas fa-external-link-alt" /></a
                  >)</b
                >
                (<a
                  href="https://discovery.biothings.io/niaid/"
                  target="_blank"
                  rel="nonreferrer"
                  >NIAID Systems Biology
                  <font-awesome-icon icon="fas fa-external-link-alt" /></a
                >) dataset metadata based on this
                <nuxt-link to="/view/niaid/" rel="nonreferrer"
                  >schema <font-awesome-icon icon="fas fa-external-link-alt"
                /></nuxt-link>
                structure.
              </p>
              <nuxt-link
                to="/guide/niaid"
                @click="
                  $gtag.event('click', {
                    event_category: 'portal_guide',
                    event_label: '/guide/niaid',
                    event_value: 1,
                  })
                "
                class="btn btn-lg themeButton text-light"
                role="button"
              >
                <font-awesome-icon icon="fas fa-plus" /> Add Dataset Metadata
              </nuxt-link>
            </div>
            <div class="card-footer text-light bg-dde-mid">
              <b>About this guide:</b>
              <table class="table table-sm table-dark table-striped">
                <tbody>
                  <tr>
                    <td>
                      <small>Intend</small>
                    </td>
                    <td>
                      <small class="badge badge-info">Portal Specific</small>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Topics</small>
                    </td>
                    <td>
                      <small class="badge badge-light">Allergies</small>
                      <small class="badge badge-light"
                        >Infectious Diseases</small
                      >
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Associations</small>
                    </td>
                    <td>
                      <nuxt-link to="/portal/niaid"
                        ><small class="badge badge-light"
                          >NIAID</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <small>Schema</small>
                    </td>
                    <td>
                      <nuxt-link to="/view/niaid"
                        ><small class="badge badge-light"
                          >Dataset</small
                        ></nuxt-link
                      >
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
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
};
</script>
