<template>
  <div class="bg-light text-dark p-2 rounded">
    <div class="border-bottom">
      <strong>{{ cls.properties.length }} properties</strong>
    </div>
    <template v-if="cls?.validation">
      <div class="border-bottom text-success">
        <img
          src="@/assets/img/cube.svg"
          width="15"
          title="validation available"
          class="m-1 tip"
          data-tippy-content="Validation available"
        />
        <b>{{ total }}</b> Validated Properties
      </div>
      <div class="ml-1">
        <div>
          <font-awesome-icon
            icon="fas fa-asterisk"
            class="text-danger"
          ></font-awesome-icon>
          <b>{{ cls.validation?.required?.length || 0 }}</b> Required
        </div>
        <div>
          <font-awesome-icon
            icon="fas fa-circle"
            class="text-warning"
          ></font-awesome-icon>
          <b>{{ cls.validation?.recommended?.length || 0 }}</b> Recommended
        </div>
        <div>
          <font-awesome-icon
            icon="fas fa-square"
            class="text-info"
          ></font-awesome-icon>
          <b>{{ cls.validation?.optional?.length || 0 }}</b> Optional
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { defineProps, computed } from "vue";

const props = defineProps({
  cls: {
    type: Object,
    default: () => ({}),
  },
});

const total = computed(() => {
  if (!props.cls?.validation) return 0;
  return (
    (props.cls.validation.required?.length || 0) +
    (props.cls.validation.recommended?.length || 0) +
    (props.cls.validation.optional?.length || 0)
  );
});
</script>
