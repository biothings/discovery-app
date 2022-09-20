<script setup>
import { ref, watchEffect } from "vue";

const props = defineProps({
  imagePath: { type: String },
});

const logo = ref();
watchEffect(async () => {
  logo.value = (
    await import(/* @vite-ignore */ `../assets/img/${props.imagePath}`)
  ).default;
});
</script>

<template>
  <img :src="logo" v-bind="$attrs" />
</template>
