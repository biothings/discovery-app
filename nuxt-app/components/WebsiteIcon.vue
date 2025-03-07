<script setup>
const props = defineProps(["color"]);
</script>

<template>
  <svg viewBox="0 0 400.92 256.97" style="width: 100px">
    <polyline
      :style="{ stroke: props.color }"
      style="stroke-width: 10px; fill: none"
      points=".45 39.1 101.43 252.94 200.45 39.1 314.35 253.42 400.45 39.1"
    />
    <polyline
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 5px"
      points="45.89 1.12 123.93 166.38 200.45 1.12 288.47 166.75 355.01 1.12"
    />
    <polyline
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 10px"
      points="45.89 87.79 123.93 253.05 200.45 87.79 288.47 253.42 355.01 87.79"
    />
  </svg>
</template>
