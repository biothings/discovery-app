<template>
  <div class="container mt-5">
    <div class="text-center jumbotron bg-light">
      <h1 class="mainTextDark">SCHEMA PLAYGROUND</h1>
      <div class="d-flex justify-content-center align-items-center flex-wrap">
        <nuxt-link to="/registry">Schema Registry</nuxt-link>
        <span class="mx-2">|</span>
        <nuxt-link to="/ns">Schema Viewer</nuxt-link>
        <span class="mx-2">|</span>
        <nuxt-link to="/editor">Schema Editor</nuxt-link>
        <span class="mx-2">|</span>
        <nuxt-link to="/validator">Validate Metadata Against Schema</nuxt-link>
      </div>
    </div>
    <section class="my-5 grad-dark p-4 rounded shadow">
      <div class="row m-0">
        <div class="col-sm-2">
          <img
            src="@/assets/img/paper.gif"
            alt="register"
            class="w-100"
            style="border-radius: 50%"
          />
        </div>
        <div class="col-sm-10 p-2 text-light">
          <h2 class="font-weight-bold">
            Visualize and Register Your Own Schema
          </h2>
          <p>
            Validate and visualize your schema online. Register your schema on
            the Data Discovery Engine to share, maintain, and easily visualize
            your schema anytime.
          </p>
        </div>
      </div>
      <div class="jumbotron d-flex justify-content-center m-3 p-2">
        <div class="col-sm-12 col-md-8">
          <h4 class="mt-3 mb-3 text-dark">Get started:</h4>
          <SchemaViewerForm></SchemaViewerForm>
        </div>
      </div>
    </section>
    <section class="my-5 grad-dark p-4 rounded shadow">
      <div class="row m-0">
        <div class="col-sm-2">
          <img
            src="@/assets/img/wave.gif"
            alt="register"
            class="w-100"
            style="border-radius: 50%"
          />
        </div>
        <div class="col-sm-10 p-2 text-light">
          <h2 class="font-weight-bold">Browse a Registry of Schemas</h2>
          <p>
            Browse a comprehensive registry of data structures to save time and
            effort by making it easy to find and use well-defined, reusable data
            structures. This centralized repository of reusable schemas allow
            users to easily find and retrieve the schema they need for their
            project.
          </p>
        </div>
      </div>
      <div class="jumbotron d-flex justify-content-center m-3 p-2">
        <div class="col-sm-12 col-md-8">
          <h4 class="mt-3 mb-3 text-dark">
            Find a specific schema that meets the requirements for your project
            or application.
          </h4>
          <p class="text-dark">
            Visualize (<font-awesome-icon
              icon="fas fa-eye"
              class="text-info"
            />), extend (<font-awesome-icon
              icon="fas fa-code-branch"
              class="mainTextLight"
            />) and compare properties (<font-awesome-icon
              icon="fas fa-not-equal"
              class="mainTextDark"
            />) from available schema classes.
          </p>
          <p class="text-dark">
            Identify schema classes that provide metadata validation rules (<img
              src="@/assets/img/cube.svg"
              width="15"
              title="validation available"
              class="tip"
              data-tippy-content="Validation available"
            />)
          </p>
          <nuxt-link
            role="button"
            class="btn btn-lg btn-info text-light m-3"
            to="/registry"
            >To Schema Registry
            <font-awesome-icon
              icon="fas fa-chevron-right"
              class="mr-1"
            ></font-awesome-icon
          ></nuxt-link>
        </div>
      </div>
    </section>
    <section class="my-5 grad-dark p-4 rounded shadow">
      <div class="row m-0">
        <div class="col-sm-2">
          <img
            src="@/assets/img/computer.gif"
            alt="register"
            class="w-100"
            style="border-radius: 50%"
          />
        </div>
        <div class="col-sm-10 p-2 text-light">
          <h2 class="font-weight-bold">Create Your Own Schema</h2>
          <p>
            Extend any schema and use it as a base to create your own. Inherit
            all of its properties automatically and add new ones specific to
            your needs.
          </p>
        </div>
      </div>
      <div class="jumbotron d-flex justify-content-center m-3 p-2">
        <div class="col-sm-12">
          <h4 class="text-dark">Common starting points:</h4>
          <div class="col-sm-8">
            <template v-for="item in startingPoints" :key="item">
              <PresetBox :preset="item"></PresetBox>
            </template>
          </div>
          <h4 class="mt-3 mb-3 text-dark">Search for a starting point:</h4>
          <nuxt-link
            role="button"
            class="btn btn-lg btn-info text-light"
            to="/registry"
            >To Schema Registry
            <font-awesome-icon
              icon="fas fa-chevron-right"
              class="mr-1"
            ></font-awesome-icon
          ></nuxt-link>
        </div>
      </div>
    </section>
    <section>
      <div
        class="jumbotron container bg-light row m-auto d-flex justify-content-center align-items-center p-1"
      >
        <div class="col-sm-12 pt-5 pb-5 text-dark">
          <h2 class="text-center text-muted mb-4 mt-4">
            Reasons why schemas are important
          </h2>
          <p class="text-dark">
            Schemas are useful for a variety of reasons. Firstly, they provide a
            clear and consistent structure for data, which helps to ensure that
            data is accurate, complete, and easily understood by both humans and
            machines. This can be particularly important in large-scale data
            environments, where data is being shared and used by multiple
            parties or systems.
          </p>
          <p class="text-dark">
            Secondly, Schemas help to validate data and ensure that it adheres
            to certain rules or constraints. This can help to identify and
            prevent errors, and can also help to ensure that data is consistent
            across different systems or applications.
          </p>
          <p class="text-dark">
            Thirdly, Schemas can also be used to enforce security and access
            controls. Since data is organized in a specific way, it is easier to
            control who has access to it and what they can do with it.
          </p>
          <p class="text-dark">
            Finally, Schemas can also be useful for optimizing data storage and
            retrieval. By defining the structure of data in advance, it can be
            stored in a more efficient way and searched or queried more quickly.
          </p>
          <p class="text-dark">
            Overall, Schemas provide a way to organize and manage data in a
            structured and consistent way, which can help to ensure data
            quality, security, and performance.
          </p>
          <div class="w-100">
            <div class="row m-0">
              <!-- card -->
              <div class="col-sm-12 col-md-4 p-2">
                <img src="@/assets/img/sp1-01.svg" alt="Planning" />
                <h4 class="text-center mainTextDark caps">Planning</h4>
                <div class="mt-3">
                  <p class="text-muted">
                    Organize and structure your data right from the start in a
                    way that not only humans but computers can understand. A
                    schema is a blueprint that graphically depicts the structure
                    of your data.
                  </p>
                </div>
              </div>
              <div class="col-sm-12 col-md-4 p-2">
                <img src="@/assets/img/sp2-01.svg" alt="Hierarchy" />
                <h4 class="text-center mainTextDark caps">Hierarchy</h4>
                <div class="mt-3">
                  <p class="text-muted">
                    Schemas follow a logical hierarchical structure each with
                    properties inherited to all children. For example:
                    <small>
                      <ul class="text-muted">
                        <li>
                          <i
                            >A
                            <a href="https://schema.org/Person" target="_blank"
                              >Person</a
                            >
                            has a property of
                            <a
                              href="https://schema.org/birthDate"
                              target="_blank"
                              >birthDate</a
                            ></i
                          >
                        </li>
                        <li>
                          <i
                            ><a href="https://schema.org/Thing" target="_blank"
                              >Thing</a
                            >
                            &gt;
                            <a
                              href="https://schema.org/CreativeWork"
                              target="_blank"
                              >CreativeWork</a
                            >
                            &gt;
                            <a href="https://schema.org/Dataset" target="_blank"
                              >Dataset</a
                            ></i
                          >
                        </li>
                      </ul>
                    </small>
                  </p>
                </div>
              </div>
              <!-- card -->
              <div class="col-sm-12 col-md-4 p-2">
                <img src="@/assets/img/sp3-01.svg" alt="Reusability" />
                <h4 class="text-center mainTextDark caps">Interoperability</h4>
                <div class="mt-3">
                  <p class="text-muted">
                    Schemas allow for data to be completely understood by
                    different interfaces and let computers access, exchange,
                    integrate data in a uniform manner.<br />
                    <small
                      >- Learn about
                      <a
                        data-tippy-content="Learn More About FAIR Principles"
                        target="_blank"
                        href="https://www.go-fair.org/fair-principles/"
                        >FAIR</a
                      >
                      principles.</small
                    >
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import PresetBox from "~~/components/PresetBox.vue";

export default {
  name: "SchemaPlayground",
  head() {
    return {
      title: "DDE | Schema Playground",
      meta: [
        {
          name: "twitter:image",
          content: "https://i.postimg.cc/7hf2495v/playground.jpg",
        },
        {
          property: "og:image",
          content: "https://i.postimg.cc/7hf2495v/playground.jpg",
        },
        {
          property: "og:url",
          content: "http://discovery.biothings.io/schema-playground",
        },
        {
          name: "twitter:url",
          content: "http://discovery.biothings.io/schema-playground",
        },
        {
          property: "og:description",
          content: "Create, Visualize and Register Your Own Schema",
        },
        {
          name: "description",
          content: "Create, Visualize and Register Your Own Schema",
        },
        {
          name: "twitter:card",
          content: "Create, Visualize and Register Your Own Schema",
        },
      ],
    };
  },
  data: function () {
    return {
      suggestedURL: "",
      slug: "",
      number: "",
      loading: false,
      startingPoints: [
        {
          namespace: "schema",
          prefix: "schema",
          name: "Dataset",
          guide: "/guide",
          description:
            "A body of structured information describing some topic(s) of interest.",
        },
        {
          namespace: "niaid",
          prefix: "niaid",
          name: "ComputationalTool",
          guide: "/guide/niaid/ComputationalTool",
          description:
            "A schema describing a minimal ComputationalTool for the National Institute of Allergy and Infectious Disease (NIAID). A ComputationalTool is a software used for the collection, processing, distribution, analysis, visualization, interpretation, etc. of data. Additional schema.org and/or custom properties could be added.",
        },
      ],
    };
  },
  components: { PresetBox },
};
</script>
