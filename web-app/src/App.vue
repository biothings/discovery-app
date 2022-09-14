<template>
  <Nav></Nav>
  <div id="modals-go-here"></div>
  <div v-if="loading" class="loader">
    <img src="@/assets/img/ripple.svg" />
  </div>
  <main id="tippyRoot">
    <RouterView />
  </main>
  <Footer></Footer>
</template>

<script>
import Nav from "./components/Nav.vue";
import Footer from "./components/Footer.vue";
import { mapGetters } from "vuex";
import { delegate } from "tippy.js";

import "@/assets/js/notify.min.js";

export default {
  name: "Home",
  components: {
    Nav,
    Footer,
  },
  computed: {
    ...mapGetters(["loading"]),
  },
  mounted: function () {
    delegate("#tippyRoot", {
      target: "[data-tippy-content]",
      animation: "scale",
      theme: "ddeDark",
      allowHTML: true,
      onShown(instance) {
        let html =
          '<table class="table table-sm table-striped table-secondary m-0">';
        try {
          if (instance.reference.dataset.tippyContent.includes("{")) {
            let json = JSON.parse(instance.reference.dataset.tippyContent);
            for (const k in json) {
              html += `<tr>
              <td>${k}</td>
              <td>${json[k]}</td>
              </tr>`;
            }
            html += "</table>";
            instance.setContent(html);
          }
        } catch (error) {
          instance.setContent(instance.reference.dataset.tippyContent);
        }
      },
    });

    $.notify.addStyle("success", {
      html: "<div><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#28a745",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("danger", {
      html: "<div class='bg-danger text-light p-1'><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#dc3545",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("warning", {
      html: "<div class='bg-danger text-light p-1'><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#ffc107",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("info", {
      html: "<div class='bg-danger text-light p-1'><span data-notify-text/></div>",
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#17a2b8",
          padding: "5px",
          color: "white",
        },
      },
    });
    $.notify.addStyle("trophy", {
      html: `<div class="bg-dark p-1 text-light">
         <span data-notify-text/>
      </div>`,
      classes: {
        base: {
          "white-space": "nowrap",
          "background-color": "#343a40",
          padding: "5px",
          color: "white",
          "border-radius": "5px",
        },
      },
    });
  },
};
</script>
