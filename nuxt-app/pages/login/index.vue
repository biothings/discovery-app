<template>
  <div id="login" class="min-100">
    <Title title="Select Login Method"></Title>
    <div
      class="jumbotron bg-light d-flex justify-content-center align-items-center"
    >
      <div class="row m-0 w-100">
        <div class="col-sm-6 jumbotron text-center bg-dde-dark">
          <a id="ghButton" role="button" class="btn btn-light mainTextDark"
            >Login with Github
            <font-awesome-icon icon="fa fa-chevron-right"></font-awesome-icon
          ></a>
        </div>
        <div class="col-sm-6 jumbotron text-center bg-dde-mid">
          <a id="samlLink" role="button" class="btn btn-light mainTextLight"
            >Login with NCATS UNA
            <font-awesome-icon icon="fa fa-chevron-right"></font-awesome-icon
          ></a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  head() {
    return {
      title: "DDE | Login Page",
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
          content: "http://discovery.biothings.io/login",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/login",
        },
        {
          property: "og:description",
          content: "Log in to start using the Data Discovery Engine",
        },
        {
          name: "description",
          content: "Log in to start using the Data Discovery Engine",
        },
        {
          name: "twitter:card",
          content: "Log in to start using the Data Discovery Engine",
        },
      ],
    };
  },
  mounted: function () {
    let config = useRuntimeConfig();
    document
      .getElementById("samlLink")
      .setAttribute(
        "href",
        config.public.apiUrl + "/saml/login/" + window.location.search
      );
    document
      .getElementById("ghButton")
      .setAttribute(
        "href",
        config.public.apiUrl + "/oauth/" + window.location.search
      );
    if (this.$route.fullPath.includes("n3c")) {
      var btn = document.getElementById("ghButton");
      btn.href = "#";
      btn.classList.remove("btn-light");
      btn.classList.add("alert-dark");
    }
  },
};
</script>
