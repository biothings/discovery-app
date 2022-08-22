<template>
  <main class="bg-light" style="min-height: 100vh">
    <div class="jumbotron bg-light text-center pt-5" style="margin-top: 40px">
      <h1 class="logoText" v-text="name"></h1>
      <small class="text-muted">
        Jump To:
        <template v-for="section in faq" :key="section + '1'">
          <a
            class="badge badge-secondary mr-2"
            v-text="section.sectionName.replace('_', ' ')"
            :href="'#' + section.sectionName"
          ></a>
        </template>
      </small>
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
                <i class="fas fa-chevron-right"></i
              ></a>
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
              data-tippy="Copy link"
              class="tip anchor"
              >
              <CopyBtn class="btn ml-1 btn-sm btn-secondary" :copy_this="window.location.href + '#' + section.sectionName">
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
                    :value="window.location + item.anchor"
                  >
                    <span v-text="item.question"></span>
                    <a
                      :href="'#' + item.anchor"
                      data-tippy="Copy link"
                      class="tip anchor"
                      >
                      <CopyBtn class="btn ml-1 btn-sm btn-secondary" :copy_this="window.location.href + '#' + item.anchor">
                          copy
                      </CopyBtn>
                      </a>
                  </div>
                  <DynamicImage
                    v-if="item?.image"
                    :imagePath="item.image"
                    :alt="section"
                    class="w-100"
                  ></DynamicImage>
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

<script>
import DynamicImage from "../components/DynamicImage.vue";

export default {
  name: "FAQ",
  data: function () {
    return {
      faq: [],
      name: "",
      window: window,
    };
  },
  components: {
    DynamicImage,
},
  props: ["portal"],
  mounted: function () {
    switch (this.portal) {
      case "n3c":
        this.name = "FAQ for N3C PPRL Datasets";
        break;
      default:
        this.name = "FAQ";
    }

    this.faq = this.$store.getters.getFAQ(this.portal);
  },
};
</script>
