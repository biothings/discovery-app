<script setup>
import { useNewsStore } from "../../stores/whatsnew";
let store = useNewsStore();
let news = store.news;

useHead({
  title: "DDE | What's New",
  meta: [
    {
      name: "twitter:image",
      content: "https://i.postimg.cc/pT9z7TVj/news.jpg",
    },
    {
      property: "og:image",
      content: "https://i.postimg.cc/pT9z7TVj/news.jpg",
    },
    {
      property: "og:url",
      content: "http://discovery.biothings.io/whats-new",
    },
    {
      name: "twitter:url",
      content: "http://discovery.biothings.io/whats-new",
    },
    {
      property: "og:description",
      content:
        "What are the latest features, fixes and improvements on the DDE",
    },
    {
      name: "description",
      content:
        "What are the latest features, fixes and improvements on the DDE",
    },
    {
      name: "twitter:card",
      content:
        "What are the latest features, fixes and improvements on the DDE",
    },
  ],
});
</script>

<template>
  <main class="alert-secondary p-2" style="min-height: 100vh">
    <div
      class="jumbotron bg-light text-center pb-4 rounded-0 bg-dark lines"
      style="margin-top: 40px"
    >
      <h1 class="text-light">What's New in the DDE</h1>
      <p class="text-light">
        Stay updated with the latest developments in the Data Discovery Engine
      </p>
    </div>
    <div class="container">
      <p>
        This page features a list of major improvements, fixes, and new features
        in the Data Discovery Engine.
      </p>
      <p>
        This list provides a comprehensive overview of recent upgrades,
        including improvements to search algorithms and the addition of new data
        sources. This list also highlights various bug fixes that have been
        implemented to improve the website's functionality, such as improved
        filtering options and enhanced data visualization tools.
      </p>
      <p>
        Furthermore, this list includes information about new features that have
        been added to the website, such as user-friendly dashboards, advanced
        analytics capabilities, and customizable data reports. Overall, major
        improvements, fixes, and new features of the Data Discovery Engine
        website serves as a valuable resource for users seeking to leverage the
        platform's full potential.
      </p>
      <template v-for="(months, year) in news" :key="year">
        <h2 class="mainTextLight">{{ year }}</h2>
         
        <template v-for="(items, month) in months" :key="month">
          <details :open="year == new Date().getFullYear() ? true : false">
            <summary>{{ month }} ({{ items.length }})</summary>
            <template v-for="item in items" :key="item.id">
              <details class="ml-5 alert alert-dark">
                <summary>
                  <img
                    :src="item.icon"
                    :alt="item.title"
                    width="50"
                    class="mr-2"
                  />
                  <h5 class="mainTextDark d-inline">
                    <b>{{ item.title }}</b>
                  </h5>
                </summary>
                <p v-html="item.description"></p>
                <p v-if="item.link">
                  <NuxtLink target="_blank" :to="{ path: item.link }"
                    >Click here to try it!</NuxtLink
                  >
                </p>
              </details>
            </template>
          </details>
        </template>
      </template>
    </div>
  </main>
</template>
