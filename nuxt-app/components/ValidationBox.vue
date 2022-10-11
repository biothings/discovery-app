<template>
  <div class="alert-secondary p-1">
    <small class="text-dark font-weight-bold">
      <span class="mr-1"
        ><font-awesome-icon icon="fas fa-asterisk" class="text-danger" />
        required</span
      >
      <span class="mr-1"
        ><font-awesome-icon icon="fas fa-circle" class="text-warning" />
        recommended</span
      >
      <span class="mr-1"
        ><font-awesome-icon icon="fas fa-square" class="text-info" />
        optional</span
      >
    </small>
    <div class="p-0">
      <template v-for="(value, name) in sorted_props" :key="name">
        <PropertyBox
          :name="name"
          :fullInfo="value"
          :recommended="validation.recommended"
          :optional="validation.optional"
          :required="validation.required"
        ></PropertyBox>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: "ValidationBox",
  props: ["validation"],
  data: function () {
    return {
      sorted_props: {},
    };
  },
  methods: {
    sortByImportance() {
      let self = this;
      let sorted = {};
      //get required
      if (Object.hasOwnProperty.call(self.validation, "required")) {
        self.validation.required.forEach((item) => {
          if (item in self.validation.properties && !(item in sorted)) {
            sorted[item] = self.validation.properties[item];
          }
        });
      }
      //get recommended
      if (Object.hasOwnProperty.call(self.validation, "recommended")) {
        self.validation.recommended.forEach((item) => {
          if (item in self.validation.properties && !(item in sorted)) {
            sorted[item] = self.validation.properties[item];
          }
        });
      }
      //get optional
      if (Object.hasOwnProperty.call(self.validation, "optional")) {
        self.validation.optional.forEach((item) => {
          if (item in self.validation.properties && !(item in sorted)) {
            sorted[item] = self.validation.properties[item];
          }
        });
      }
      //get not categorized
      for (const prop in self.validation.properties) {
        if (!(prop in sorted)) {
          sorted[prop] = self.validation.properties[prop];
        }
      }
      self.sorted_props = sorted;
    },
  },
  mounted: function () {
    this.sortByImportance();
  },
};
</script>
