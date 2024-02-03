<script setup>
import { onMounted } from "vue";

const props = defineProps(["status"]);
let randomID = Math.floor(Math.random() * 90000) + 10000;
let cls = ref("bg-secondary");
let text = ref("N/A");

onMounted(() => {
  switch (props?.status?.toString()) {
    case "200":
      text.value = "ok";
      cls.value = "bg-success";
      break;
    case "299":
      text.value = "ok";
      cls.value = "bg-success";
      break;
    case "400":
      text.value = "invalid";
      cls.value = "bg-invalid";
      break;
    case "499":
      text.value = "invalid";
      cls.value = "bg-invalid";
      break;
    case "500":
      text.value = "broken";
      cls.value = "bg-broken";
      break;
    case "404":
      text.value = "not found";
      cls.value = "bg-danger";
      break;
    default:
      break;
  }
});
</script>

<template>
  <div class="source-badge mx-1" :id="randomID">
    <div>schema</div>
    <div :class="cls">{{ text }}</div>
  </div>
</template>
