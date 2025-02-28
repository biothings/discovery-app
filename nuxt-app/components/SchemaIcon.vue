<script setup>
const props = defineProps(["color"]);
</script>

<template>
  <svg viewBox="0 0 332.74 332.74" style="width: 100px">
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 3px"
      x="2.5"
      y="2.5"
      width="116.06"
      height="116.06"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 4px"
      x="222.36"
      y="222.36"
      width="107.89"
      height="107.89"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 10px"
      x="60.53"
      y="60.53"
      width="208.42"
      height="208.42"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 2px"
      x="69.89"
      y="70.34"
      width="40.05"
      height="40.05"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 5px"
      x="150.43"
      y="152.89"
      width="99.71"
      height="99.71"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 4px"
      x="25.92"
      y="29.88"
      width="269.71"
      height="269.71"
    />
  </svg>
</template>
