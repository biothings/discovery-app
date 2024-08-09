<script setup>
import { useStore } from "vuex";
let store = useStore();
let route = useRoute();
let faq = store.getters.getFAQ(route.params.portal);
let name = ref("");
switch (route.params.portal) {
  case "n3c":
    name.value = "FAQ for N3C PPRL Datasets";
    break;
  default:
    name.value = "FAQ";
}

useHead({
  title: "DDE | FAQ",
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
      content: "http://discovery.biothings.io/faq",
    },
    {
      name: "twitter:url",
      content: "http://discovery.biothings.io/faq",
    },
    {
      property: "og:description",
      content: "Get help with some of our most frequently asked questions",
    },
    {
      name: "description",
      content: "Get help with some of our most frequently asked questions",
    },
    {
      name: "twitter:card",
      content: "Get help with some of our most frequently asked questions",
    },
  ],
});
</script>

<template>
  <main class="bg-light text-dde-dark min-100">
    <Title :title="name"></Title>
    <div class="text-center p-2">
      <span>
        Jump To:
        <template v-for="section in faq" :key="section + '1'">
          <a
            class="text-primary mr-2"
            v-text="section.sectionName.replace('_', ' ')"
            :href="'#' + section.sectionName"
          ></a>
        </template>
      </span>
    </div>
    <div class="jumbotron container">
      <template v-for="section in faq" :key="section">
        <h6
          class="text-dark my-1"
          v-text="section.sectionName.replace('_', ' ')"
        ></h6>

        <div class="ml-3">
          <template v-for="item in section.questions" :key="item">
            <div>
              <a :href="'#' + item.anchor"
                ><span v-text="item.question"></span>
                <font-awesome-icon icon="fas fa-chevron-right"
              /></a>
            </div>
          </template>
        </div>
      </template>
    </div>
    <div class="container p-0" style="margin-bottom: 10vh">
      <template v-for="section in faq" :key="section">
        <div class="card">
          <h4
            class="text-light card-header pt-5 pb-5 grad anchorParent"
            :id="section.sectionName"
          >
            <span v-text="section.sectionName.replace('_', ' ')"></span>
            <a
              :href="'#' + section.sectionName"
              data-tippy-content="Copy link"
              class="tip anchor"
            >
              <CopyBtn
                class="btn ml-1 btn-sm btn-secondary"
                :copy_this="$route.fullPath + '#' + section.sectionName"
              >
                copy
              </CopyBtn>
            </a>
          </h4>
          <div class="card-body">
            <ul class="list-group card-text">
              <template v-for="item in section.questions" :key="item">
                <li class="list-group-item">
                  <div
                    class="mainTextDark bold anchorParent"
                    :id="item.anchor"
                    :value="$route.fullPath + item.anchor"
                  >
                    <span v-text="item.question"></span>
                    <a
                      :href="'#' + item.anchor"
                      data-tippy-content="Copy link"
                      class="tip anchor"
                    >
                      <CopyBtn
                        class="btn ml-1 btn-sm btn-secondary"
                        :copy_this="$route.fullPath.href + '#' + item.anchor"
                      >
                        copy
                      </CopyBtn>
                    </a>
                  </div>
                  <div v-if="item.image">
                    <img :src="item.image" class="w-100" />
                  </div>
                  <div class="text-muted p-2" v-html="item.answer"></div>
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
    </div>
  </main>
</template>
