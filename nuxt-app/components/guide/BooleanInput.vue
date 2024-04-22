<template>
  <div class="d-flex justify-content-center align-items-center p-2">
    <div
      :class="[
        done === true ? 'text-success border-success bold' : 'text-muted',
      ]"
      @click="markCompletedBoolean(true)"
      class="border rounded p-1 mx-2 pointer w-25 text-center"
    >
      <font-awesome-icon icon="fas fa-check"></font-awesome-icon> Yes
    </div>
    <div
      :class="[
        done === false ? 'text-danger border-danger bold' : 'text-muted',
      ]"
      @click="markCompletedBoolean(false)"
      class="border rounded p-1 mx-2 pointer w-25 text-center"
    >
      <font-awesome-icon icon="fas fa-times"></font-awesome-icon> No
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "pinia";
import { useGuideStore } from "../../stores/guide";

export default {
  name: "BooleanInput",
  props: ["name", "info"],
  methods: {
    ...mapActions(useGuideStore, ["addValue", "saveProgress"]),
    markCompletedBoolean(val) {
      this.addValue({ name: this.name, info: this.info, value: val });
      this.saveProgress();
    },
  },
  computed: {
    ...mapState(useGuideStore, ["getValidationValue"]),
    done: {
      get() {
        return this.getValidationValue(this.name);
      },
    },
  },
};
</script>
