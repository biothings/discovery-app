<script setup>
const props = defineProps(["color"]);
</script>
<template>
  <svg
    version="1.1"
    x="0px"
    y="0px"
    viewBox="0 0 290.8 288.2"
    style="enable-background: new 0 0 290.8 288.2; width: 100px"
    xml:space="preserve"
  >
    <polygon
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 4px"
      points="38.4,260.3 38.4,252.3 134.7,252.3 134.7,217.4 38.4,217.4 38.4,203.2 160,203.2 160,168.4 38.4,168.4 
        38.4,159.1 175.4,159.1 175.4,124.2 38.4,124.2 38.4,115 234.1,115 234.1,80.1 38.4,80.1 38.4,70.8 251.3,70.8 251.3,36 38.4,36 
        38.4,20.8 31.4,20.8 31.4,267.3 264.8,267.3 264.8,260.3 "
    />
  </svg>
</template>
