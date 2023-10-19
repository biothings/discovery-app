<template>
  <div class="p-1 m-1 bg-light rounded">
    <div class="form-group">
      <select multiple class="form-control" id="exampleFormControlSelect2">
        <template v-for="option in enumeration" :key="option">
          <option :value="option" v-text="option"></option>
        </template>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: "Enumeration",
  props: ["enumeration"],
};
</script>
