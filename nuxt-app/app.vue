<template>
  <div class="bg-light" id="#tippyRoot">
    <Nav></Nav>
    <div v-if="loading" class="loader">
      <img src="@/assets/img/ripple.svg" />
    </div>
    <NuxtPage></NuxtPage>
    <Footer></Footer>
  </div>
</template>
<script>
  import Nav from './components/Nav.vue';
  import Footer from './components/Footer.vue';
  import { delegate } from 'tippy.js';
  import { mapGetters } from "vuex";

  export default{
    components:{
      Nav,
      Footer
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
  },
    head(){
      return {
        'link': [
          {
            rel:"stylesheet",
            href:"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
            integrity:"sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
            crossorigin:"anonymous"
          },
          {
            href:"https://fonts.googleapis.com/css?family:Sulphur+Point&display:swap",
            rel:"stylesheet"
          },
          {
            src:"https://code.jquery.com/jquery-3.3.1.slim.min.js",
            integrity:"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
            crossorigin:"anonymous"
          },
          {
            src:"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
            integrity:"sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
            crossorigin:"anonymous"
          },
          {
            src:"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js",
            integrity:"sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy",
            crossorigin:"anonymous"
          },
          {
            type:"text/css",
            rel:"stylesheet",
            href:"https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.0/normalize.min.css"
          }
        ]
      }
    },
  }
</script>