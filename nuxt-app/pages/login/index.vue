<template>
  <div
    id="login"
    class="jumbotron text-center d-flex justify-content-center align-items-center"
    style="min-height: 95vh"
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
          <h3 class="text-muted">Select the login method</h3>
          <hr />
        </div>
        <div class="col-sm-12" v-if="$route.fullPath.includes('n3c')">
          <p class="m-0 text-info">
            N3C members please use NCATS UNA to log in. Login with GitHub is
            disabled.
          </p>
        </div>
        <div class="col-sm-12 row m-0 opt-bg py-5">
          <div class="col-sm-6 p-2">
            <a id="ghButton" role="button" class="btn btn-light mainTextDark"
              >Login with Github
              <font-awesome-icon icon="fa fa-chevron-right"></font-awesome-icon
            ></a>
          </div>
          <div class="col-sm-6 p-2">
            <a id="samlLink" role="button" class="btn btn-light mainTextLight"
              >Login with NCATS UNA
              <font-awesome-icon icon="fa fa-chevron-right"></font-awesome-icon
            ></a>
          </div>
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
