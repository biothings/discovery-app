<template>
  <header id="header">
    <title>Data Discovery Engine</title>
    <nav class="navbar navbar-expand-md navbar-light bg-light fixed-top">
      <router-link class="navbar-brand" :to="{ name: 'Home' }">
        <img
          src="@/assets/img/dde-logo-o.svg"
          width="30"
          height="30"
          alt="DDE"
          class="d-none d-md-inline"
        />
        <i class="fas fa-home d-inline d-md-none mainTextDark"></i>
      </router-link>
      <router-link
        id="logo"
        class="navbar-brand caps logoText d-none d-md-inline logoFont"
        :to="{ name: 'Home' }"
        >Data Discovery Engine</router-link
      >
      <button
        class="navbar-toggler alert-secondary"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="collapse navbar-collapse justify-content-end"
        id="navbarSupportedContent"
      >
        <ul class="navbar-nav" id="user_link">
          <li
            class="nav-item headTip"
            data-tippy-content="Create discoverable metadata"
          >
            <router-link
              class="nav-link h-link mainTextLight"
              to="/best-practices"
              >Discovery Guide</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link h-link mainTextDark headTip"
              to="/schema-playground"
              data-tippy-content="Create and Visualize a Schema"
              >Schema Playground</router-link
            >
          </li>
          <li class="nav-item dropdown">
            <router-link
              class="nav-link dropdown-toggle"
              to="/portal"
              id="navbarDropdown"
              role="button"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Data Portals
            </router-link>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <router-link class="dropdown-item" to="/portal/cd2h">
                <img
                  src="@/assets/img/dde-logo-o.svg"
                  width="20"
                  height="20"
                  alt="CTSA"
                  title="CTSA Portal"
                />
                CD2H <i class="fas fa-chevron-right mainTextLight"></i>
              </router-link>
              <router-link class="dropdown-item" to="/portal/n3c">
                <img
                  src="@/assets/img/N3Co.png"
                  width="20"
                  height="20"
                  alt="N3C"
                  title="N3C"
                />
                N3C <i class="fas fa-chevron-right mainTextLight"></i>
              </router-link>
              <router-link class="dropdown-item" to="/portal/outbreak">
                <img
                  src="@/assets/img/outbreak.png"
                  width="20"
                  height="20"
                  alt="Outbreak.info"
                  title="Outbreak.info"
                />
                Outbreak.info <i class="fas fa-chevron-right mainTextLight"></i>
              </router-link>
              <router-link class="dropdown-item" to="/portal/niaid">
                <img
                  src="@/assets/img/niaid/icon.svg"
                  width="20"
                  height="20"
                  alt="NIAID"
                  title="NIAID Data Portal"
                />
                NIAID <i class="fas fa-chevron-right mainTextLight"></i>
              </router-link>
            </div>
          </li>
          <li class="nav-item dropdown d-inline">
            <router-link
              class="nav-link dropdown-toggle"
              to="/registries"
              id="navbarDropdown"
              role="button"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Registry
            </router-link>
            <div
              class="dropdown-menu p-1"
              aria-labelledby="navbarDropdown"
              style="max-width: none"
            >
              <router-link
                class="dropdown-item mainTextLight text-left"
                to="/dataset"
                >Metadata Registry <i class="fas fa-chevron-right"></i
              ></router-link>
              <router-link
                class="dropdown-item mainTextDark text-left"
                to="/registry"
                >Schema Registry <i class="fas fa-chevron-right"></i
              ></router-link>
            </div>
          </li>
          <login></login>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script>
import tippy from "tippy.js";

import Login from "./Login.vue";

export default {
  name: "Nav",
  components: {
    Login,
  },
  mounted: function () {
    tippy(".headTip", {
      placement: "bottom",
      theme: "light",
      animation: "fade",
    });
  },
};
</script>
