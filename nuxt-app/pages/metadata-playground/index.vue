<template>
  <div
    class="jumbotron text-center d-flex justify-content-center align-items-center"
    style="min-height: 90vh"
  >
    <div class="p-2">
      <div class="row m-0">
        <div class="col-sm-12 text-center">
          <img
            src="@/assets/img/dde-logo-o.svg"
            width="100"
            height="100"
            alt="DDE"
          />
          <h3 class="text-muted caps">Validate and create great metadata</h3>
          <hr />
        </div>
        <div class="col-sm-12 row m-0 opt-bg py-5">
          <div class="col-sm-6 p-2">
            <router-link to="/validator" class="btn btn-light mainTextDark"
              >Validate your metadata against an existing schema
              <font-awesome-icon icon="fas fa-chevron-right"
            /></router-link>
          </div>
          <div class="col-sm-6 p-2">
            <router-link
              to="/markup-generator"
              class="btn btn-light mainTextLight"
              >Create new metadata based off an existing schema
              <font-awesome-icon icon="fas fa-chevron-right"
            /></router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Registries",
  head() {
    return {
      title: "DDE | Registries",
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
          content: "http://discovery.biothings.io/registries",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/registries",
        },
        {
          property: "og:description",
          content:
            "Browse structured resource metadata or available namespaces and schemas on the DDE",
        },
        {
          name: "description",
          content:
            "Browse structured resource metadata or available namespaces and schemas on the DDE",
        },
        {
          name: "twitter:card",
          content:
            "Browse structured resource metadata or available namespaces and schemas on the DDE",
        },
      ],
    };
  },
};
</script>
