<script setup>
import Login from "./Login.vue";
import { useStore } from "vuex";
import { ref } from "vue";

import validator_img from "../assets/img/validator.svg";
import generator_img from "../assets/img/generator.svg";
import res_reg from "../assets/img/resource_reg.svg";
import schema_reg from "../assets/img/schema-reg.svg";

let store = useStore();
let portals = store.getters.getPortals;
let menu = ref(false);
</script>
<template>
  <header id="header">
    <title>Data Discovery Engine</title>
    <nav
      class="navbar navbar-expand-md navbar-dark bg-dde-mid fixed-top shadow"
    >
      <nuxt-link class="navbar-brand" to="/">
        <img
          src="@/assets/img/dde-logo-o-text-back.png"
          alt="DDE"
          height="50"
        />
      </nuxt-link>
      <button
        class="navbar-toggler alert-secondary"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
        @click="menu = !menu"
      >
        Menu
      </button>
      <div
        :class="!menu ? 'collapse ' : ''"
        class="navbar-collapse justify-content-end"
        id="navbarSupportedContent"
      >
        <ul class="navbar-nav" id="user_link">
          <li class="nav-item">
            <nuxt-link class="nav-link h-link" to="/about">About</nuxt-link>
          </li>
          <li
            class="nav-item"
            data-tippy-content="Create discoverable metadata"
          >
            <nuxt-link class="nav-link h-link" to="/best-practices"
              >Discovery Guide</nuxt-link
            >
          </li>
          <li class="nav-item">
            <nuxt-link
              class="nav-link h-link"
              to="/schema-playground"
              data-tippy-content="Create and Visualize a Schema"
              >Schema Playground</nuxt-link
            >
          </li>
          <!-- <li class="nav-item">
            <nuxt-link
              class="nav-link h-link"
              to="/validator"
              data-tippy-content="Validate metadata against a chosen schema"
              >Metadata Validator</nuxt-link
            >
          </li> -->
          <li class="nav-item dropdown d-inline">
            <nuxt-link
              class="nav-link dropdown-toggle"
              to="/metadata-playground"
              id="metaDropdown"
              role="button"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Metadata Toolkit
            </nuxt-link>
            <div
              class="dropdown-menu p-1"
              aria-labelledby="metaDropdown"
              style="max-width: none"
            >
              <nuxt-link
                class="dropdown-item mainTextLight text-left"
                to="/validator"
              >
                <img
                  :src="validator_img"
                  width="20"
                  height="20"
                  alt="Validator" />
                Metadata Validator <i class="fas fa-chevron-right"></i
              ></nuxt-link>
              <nuxt-link
                class="dropdown-item mainTextDark text-left"
                to="/markup-generator"
              >
                <img
                  :src="generator_img"
                  width="20"
                  height="20"
                  alt="Generator" />
                Markup Generator<i class="fas fa-chevron-right"></i
              ></nuxt-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <nuxt-link
              class="nav-link dropdown-toggle"
              to="/portal"
              id="navbarDropdown"
              role="button"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Data Portals
            </nuxt-link>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <template v-for="portal in portals" :key="portal.keyName">
                <nuxt-link
                  class="dropdown-item"
                  :to="'/portal/' + portal.keyName"
                >
                  <img
                    :src="portal.portalicon"
                    width="20"
                    height="20"
                    :alt="portal.name"
                    :title="portal.name"
                  />
                  {{ portal.shortName }}
                  <i class="fas fa-chevron-right mainTextLight"></i>
                </nuxt-link>
              </template>
            </div>
          </li>
          <li class="nav-item dropdown d-inline">
            <nuxt-link
              class="nav-link dropdown-toggle"
              to="/registries"
              id="navbarDropdown"
              role="button"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Registry
            </nuxt-link>
            <div
              class="dropdown-menu p-1"
              aria-labelledby="navbarDropdown"
              style="max-width: none"
            >
              <nuxt-link
                class="dropdown-item mainTextLight text-left"
                to="/resource"
              >
                <img :src="res_reg" width="20" height="20" alt="Validator" />
                Resource Registry <i class="fas fa-chevron-right"></i
              ></nuxt-link>
              <nuxt-link
                class="dropdown-item mainTextDark text-left"
                to="/registry"
              >
                <img :src="schema_reg" width="20" height="20" alt="Validator" />
                Schema Registry <i class="fas fa-chevron-right"></i
              ></nuxt-link>
            </div>
          </li>
          <login></login>
        </ul>
      </div>
    </nav>
  </header>
</template>
