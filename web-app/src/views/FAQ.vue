<template>
  <div class="bg-light" style="min-height: 100vh">
    <div class="jumbotron bg-light text-center pt-5" style="margin-top: 40px">
      <h1 class="logoText">FAQ</h1>
      <small class="text-muted">
        Jump To:
        <template v-for="section in faq" :key="section + '1'">
          <a
            class="badge badge-secondary mr-2"
            v-text="section.sectionName"
            :href="'#' + section.sectionName"
          ></a>
        </template>
      </small>
    </div>
    <div class="jumbotron container">
      <template v-for="section in faq" :key="section">
        <h6 class="text-dark my-1" v-text="section.sectionName"></h6>
        <template v-for="item in section.questions" :key="item">
          <div>
            <a :href="'#' + item.anchor"
              ><span v-text="item.question"></span>
              <i class="fas fa-chevron-right"></i
            ></a>
          </div>
        </template>
      </template>
    </div>
    <div class="container p-0" style="margin-bottom: 10vh">
      <template v-for="section in faq" :key="section">
        <div class="card">
          <h4
            class="text-light card-header pt-5 pb-5 grad"
            v-text="section.sectionName"
            :id="section.sectionName"
          ></h4>
          <div class="card-body">
            <ul class="list-group card-text">
              <template v-for="item in section.questions" :key="item">
                <li class="list-group-item">
                  <div
                    class="mainTextDark bold"
                    :id="item.anchor"
                    :value="window.location + item.anchor"
                  >
                    <span v-text="item.question"></span>
                    <a
                      :href="'#' + item.anchor"
                      data-tippy="Copy link"
                      class="secondary-content"
                      @click="
                        copyClipboard(window.location.href + '#' + item.anchor)
                      "
                      ><i class="fas fa-link"></i
                    ></a>
                  </div>
                  <div class="text-muted p-2" v-html="item.answer"></div>
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "FAQ",
  data: function () {
    return {
      window: window,
    };
  },
  computed: {
    ...mapGetters(["faq"]),
  },
  methods: {
    copyClipboard(link) {
      navigator.clipboard.writeText(link).then(
        function () {
          this.$swal.fire({
            type: "success",
            toast: true,
            title: "Link Copied",
            showConfirmButton: false,
            timer: 1000,
          });
        },
        function (err) {
          console.error("Async: Could not copy text: ", err);
        }
      );
    },
  },
};
</script>
