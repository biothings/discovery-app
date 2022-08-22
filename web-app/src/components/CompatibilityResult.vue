<template>
  <li
    class="list-group-item row m-0 d-flex justify-content-center align-items-stretch p-0"
  >
    <div
      class="col-sm-3 d-flex justify-content-center align-items-center text-light"
      :class="[r.schemaorgCompliant ? 'bg-success' : 'bg-danger']"
    >
      <div class="text-center">
        <h6
          v-text="
            r.schemaorgCompliant
              ? 'Schema.org compliant'
              : 'Not Schema.org compliant'
          "
        ></h6>
        <i
          class="far fa-2x"
          :class="[
            r.schemaorgCompliant ? 'fa-check-circle' : 'fa-times-circle',
          ]"
        ></i>
        <a
          class="d-block pointer alert alert-light mt-1 p-1"
          @click="expand = !expand"
          href="javascript:void(0)"
        >
          <small>What does this mean?</small>
        </a>
      </div>
    </div>
    <div class="col-sm-9">
      <h5>
        <span v-text="r.name"></span>
      </h5>
      <small class="d-block"
        ><a class="mr-2" :href="r.url" target="_blank">Learn more</a></small
      >
      <small v-if="r.NIHFunded"
        >Funding: <b class="text-info" v-text="r.NIHFunded"></b
      ></small>
      <div>
        <small v-if="r.recommender && r.recommender.length"
          >Recommended by:
        </small>
        <template v-for="(item, i) in r.recommender" :key="i">
          <small
            class="text-muted mr-1"
            v-if="item !== null"
            v-text="i !== r.recommender.length - 1 ? item + ', ' : item"
          ></small>
        </template>
      </div>
      <div>
        <a
          class="mr-2 tip"
          :data-tippy-info="'Last tested: ' + r.dateTested"
          :href="r.test"
          target="_blank"
          ><i class="fas fa-vial"></i> test</a
        >
      </div>
      <div>
        <template v-for="(c, i) in r.category" :key="i">
          <small
            class="text-muted mr-1"
            v-if="c !== null"
            v-text="'#' + c"
          ></small>
        </template>
      </div>
      <small class="float-right"
        >Access
        <i
          class="fas"
          :class="[
            !r.requiresLogin
              ? 'fa-lock-open text-success'
              : 'fa-lock text-warning',
          ]"
        ></i
      ></small>
    </div>
    <div
      v-if="expand"
      class="col-sm-12 alert m-0 rounded-0"
      :class="[r.schemaorgCompliant ? 'alert-success' : 'alert-danger']"
    >
      <template v-if="r.schemaorgCompliant">
        <p class="m-1 text-success">
          <b v-text="r.name"></b> is
          <a target="_blank" href="https://schema.org/" rel="nonreferrer"
            >schema.org</a
          >
          compliant!
        </p>
        <div class="text-center">
          <img
            class="w-50 m-auto"
            alt="compliant"
            src="@/assets/img/compliant.png"
          />
        </div>
        <div class="m-1">
          Your dataset is findable on:
          <ul>
            <li>
              <a
                :href="
                  'https://datasetsearch.research.google.com/search?query=' +
                  r.testUrl
                "
                target="_blank"
                >Google Dataset Search</a
              >
            </li>
            <li>
              <a href="https://figshare.com/" target="_blank">Figshare</a> (via
              <a href="https://discovery.biothings.io/niaid/" target="_blank"
                >NIAID Data Portal</a
              >)
            </li>
            <li>
              <a href="https://discovery.biothings.io/niaid/" target="_blank"
                >NIAID Data Portal</a
              >
            </li>
            <li>and more!</li>
          </ul>
        </div>
        <h3>That's great! ...but what does that mean?</h3>
        <p class="m-1">
          Being
          <a target="_blank" href="https://schema.org/" rel="nonreferrer"
            >schema.org</a
          >
          compliant means that computers can read and understand your content.
          This content is findable by search engines, it is interoperable
          meaning similar efforts can integrate and process your contributions,
          and it's based on a established reusable standard so you are helping
          maintain and promote
          <a target="_blank" href="https://www.go-fair.org/fair-principles/"
            >FAIR</a
          >
          data sharing best-practices.
        </p>
      </template>
      <template v-else>
        <p class="m-1 text-danger">
          <b v-text="r.name"></b> is <b>NOT</b>
          <a target="_blank" href="https://schema.org/" rel="nonreferrer"
            >schema.org</a
          >
          compliant.
        </p>
        <div class="text-center">
          <img
            class="w-50 m-auto"
            alt="not compliant"
            src="@/assets/img/notcompliant.png"
          />
        </div>
        <h3>OK...but so what?</h3>
        <p class="m-1">
          Search engines have a limited understanding of what is being displayed
          on a web page. Even tho your metadata is displayed on a web page it
          does not mean it's reachable or understood by machines.
        </p>
        <p class="m-1">
          By adding additional structured metadata search engines can understand
          your content and it's meaning and since its structure is based on a
          reusable standard it means that your metadata is interoperable so
          similar efforts can take advantage of your findings.
        </p>
        <h3>I need to make my dataset discoverable!</h3>
        <p class="m-1">
          Data Discovery Engine provides a way to easily structure, host and
          submit metadata to various schema.org compliant repositories.
        </p>
        <p class="m-1">
          <img width="150px" alt="go" src="@/assets/img/hand.png" />
          <a role="button" href="/best-practices" class="btn btn-warning"
            >Register your dataset now</a
          >
        </p>
      </template>
    </div>
  </li>
</template>

<script>
export default {
  name: "CompatibilityResult",
  data: function () {
    return {
      expand: false,
    };
  },
  props: ["r"],
  mounted: function () {
    // this.expand = this.r['schemaorgCompliant'] ? false : true;
  },
};
</script>
