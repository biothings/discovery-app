<template>
  <div id="about" style="min-height: 100vh" class="reg-hero">
    <PageTitle title="Branding"></PageTitle>
    <div class="jumbotron bg-light p-5 mt-5 text-dde-dark">
      <h2>Terms of Use</h2>
      <p>
        If you use any of the Data Discovery Engine logos, illustrations or any
        other images approved for use under these brand guidelines, you agree
        that you will do so in compliance with the terms and conditions
        indicated on this page. If you do so, Data Discovery Engine and its
        partners grant you a non-transferable, non-exclusive, royalty-free
        limited license to use its creative assets, and only in accordance with
        these brand guidelines. This is not a trademark license.
      </p>
      <p>
        Please refer to these guidelines to achieve consistency and make sure
        the branded elements of Data Discovery Engine are used correctly across
        every application. We reserve the right to terminate or modify your
        permission to display our creative assets.
      </p>
      <p>
        Data Discovery Engine assets are provided to the public under
        <a
          href="https://creativecommons.org/licenses/by-nd/4.0/deed.en"
          target="_blank"
          >ATTRIBUTION-NODERIVS 4.0 INTERNATIONAL (CC BY-ND 4.0)</a
        >.
      </p>
    </div>
    <div class="d-flex flex-wrap justify-content-center align-items-center">
      <div
        v-for="color in colors"
        :style="{ 'background-color': color }"
        class="p-5 m-1 rounded text-dark bold"
        :key="color"
      >
        <div class="badge badge-light">
          {{ color }}
        </div>
      </div>
    </div>

    <div class="jumbotron text-light p-5 mt-5 bg-dde-dark">
      <h2>Images</h2>
      <p>
        Right click and save any image or click
        <a href="dde-logos.zip">HERE</a> to download them all (SVG and PNG
        versions).
      </p>
      <div class="d-flex flex-wrap justify-content-center align-items-center">
        <img
          src="@/assets/img/dde-logo-o.png"
          alt="logo"
          width="100"
          class="m-2"
        />
        <img
          src="@/assets/img/dde-logo-white.png"
          alt="logo"
          width="100"
          class="m-2"
        />
        <img
          src="@/assets/img/dde-logo-o-text.png"
          alt="logo"
          height="50"
          class="m-2"
        />
        <img
          src="@/assets/img/dde-logo-white-text.png"
          alt="logo"
          height="50"
          class="m-2"
        />
        <img
          src="@/assets/img/dde-logo-o-text-vertical.png"
          alt="logo"
          height="150"
          class="m-2"
        />
        <img
          src="@/assets/img/dde-logo-white-text-vertical.png"
          alt="logo"
          height="150"
          class="m-2"
        />
      </div>
    </div>
    <div
      class="d-flex flex-wrap justify-content-center align-items-middle bg-light"
    >
      <img src="@/assets/img/branding.svg" alt="branding" class="w-75" />
    </div>
  </div>
</template>

<script>
export default {
  name: "Branding",
  data: function () {
    return {
      colors: ["#2A1B3D", "#44328D", "#8265a7", "#D83F87", "#A4B3B6"],
    };
  },
  head() {
    return {
      title: "DDE | Branding",
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
};
</script>
