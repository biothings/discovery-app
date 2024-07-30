<template>
  <div class="tool-card card text-center m-2" :class="cls" data-aos="fade-up">
    <div class="p-5">
      <h2>{{ title }}</h2>
      <img :src="image" :alt="image_alt" width="150" />
      <p class="text-left">{{ text }}</p>
      <slot></slot>
      <NuxtLink :to="link" class="btn themeButton btn-lg text-light">
        {{ link_text }}
      </NuxtLink>
    </div>
  </div>
</template>

<script>
export default {
  name: "ToolCard",
  props: ["image", "link", "title", "text", "link_text", "image_alt", "cls"],
};
</script>
