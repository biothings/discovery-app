<template>
  <div>
    <div
      class="expandContainer"
      v-bind:class="{ 'max-height-none': fullTXT, 'max-height-200': !fullTXT }"
    >
      <div class="text-center">
        <a
          class="btn btn-sm btn-secondary text-light"
          v-if="fullTXT"
          @click.prevent="fullTXT = !fullTXT"
        >
          Collapse
        </a>
      </div>

      <div class="blue-grey-text" v-html="text"></div>

      <div class="text-center">
        <a
          class="btn btn-sm btn-secondary text-light"
          v-if="fullTXT"
          @click.prevent="fullTXT = !fullTXT"
        >
          Collapse
        </a>
      </div>

      <div v-if="!fullTXT" class="whiteFadeBox text-center">
        <a
          class="btn btn-sm btn-secondary text-light"
          v-if="!fullTXT"
          @click.prevent="fullTXT = !fullTXT"
          >Click to expand</a
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CollapsibleText",
  data: function () {
    return {
      result: null,
      fullTXT: false,
    };
  },
  props: ["text"],
};
</script>
