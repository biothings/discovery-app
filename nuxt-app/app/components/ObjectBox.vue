<template>
  <div class="p-1 m-1 bg-light rounded">
    <template
      v-for="(propContent, propName) in properties"
      :key="propName + '-prop'"
    >
      <PropertyBox
        :name="propName"
        :fullInfo="propContent"
        :required="required"
      ></PropertyBox>
    </template>
  </div>
</template>

<script>
export default {
  name: "ObjectBox",
  props: ["properties", "required"],
};
</script>
