<template>
  <form class="my-1">
    <label class="text-info m-0" for="cardinalitys"
      ><small>Choose cardinality:</small></label
    >
    <select
      class="px-2 py-1 font-weight-bold"
      :class="[selection == 'many' ? 'text-primary' : 'text-info']"
      name="cardinality"
      id="cardinality"
      @change="handleChange()"
      v-model="selection"
    >
      <option value="one">One</option>
      <option value="many">Many</option>
    </select>
  </form>
</template>

<script>
import { mapActions } from "pinia";
import { useEditorStore } from "../stores/editor";

export default {
  name: "CardinalitySelector",
  props: ["propname", "val"],
  data: function () {
    return {
      selection: "",
    };
  },
  mounted: function () {
    if (Object.hasOwnProperty.call(this.val, "owl:cardinality")) {
      this.selection = this.val["owl:cardinality"];
    }
  },
  methods: {
    ...mapActions(useEditorStore, ["setValidation"]),
    handleChange() {
      this.setValidation({
        // follow structure of val options
        validation: { validation: { "owl:cardinality": self.selection } },
        name: self.propname,
      });
    },
  },
};
</script>
