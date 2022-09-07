<template>
  <form class="my-1">
    <label class="text-info" for="cardinalitys"
      ><small>Choose cardinality:</small></label
    >
    <select
      class="px-2 py-1"
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
export default {
  name: "CardinalitySelector",
  props: ["propname", "val"],
  data: function () {
    return {
      selection: "",
    };
  },
  methods: {
    handleChange() {
      let self = this;
      let payload = {
        // follow structure of val options
        validation: { validation: { "owl:cardinality": self.selection } },
        name: self.propname,
      };
      self.$store.commit("setValidation", payload);
    },
  },
};
</script>
