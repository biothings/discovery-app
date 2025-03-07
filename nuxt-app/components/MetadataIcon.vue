<script setup>
const props = defineProps(["color"]);
</script>

<template>
  <svg viewBox="0 0 379.59 357.08" style="width: 100px">
    <path
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 2px"
      d="M27.88,317.48s68.49,8.29,102.31-82.94S207.82,30.71,376.09,88.77"
    />
    <path
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 1px"
      d="M27.88,305.29s65.15-13.86,70.71-100.95S120.38,47.08,220.96,3.5"
    />
    <path
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 2px"
      d="M28.24,332.77s67.1,24.11,113.39-41.31c46.29-65.42,104.51-144.28,234.46-91.16"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 3px"
      x="3.5"
      y="284.11"
      width="54.76"
      height="69.47"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 7px"
      x="79.07"
      y="161.65"
      width="109.31"
      height="138.68"
    />
    <rect
      :style="{ stroke: props.color }"
      style="fill: none; stroke-width: 13px"
      x="220.96"
      y="3.5"
      width="155.13"
      height="196.8"
    />
  </svg>
</template>
