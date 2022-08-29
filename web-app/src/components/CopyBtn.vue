<template>
  <button
    v-bind="$attrs"
    class="btn-copy"
    @click="copy"
    title="Copy"
    :data-clipboard-text="copy_this"
  >
    <template v-if="msg">{{ msg }}</template>
    <font-awesome-icon v-else icon="fas fa-clipboard" />
  </button>
</template>

<script>
import ClipboardJS from "clipboard";

export default {
  name: "CopyBtn",
  props: {
    msg: {
      type: String,
    },
    copy_msg: {
      type: String,
      default: "Link Copied",
    },
    copy_this: {
      type: String,
      default: "",
    },
  },
  methods: {
    copy: function () {
      this.$swal.fire({
        icon: "success",
        toast: true,
        title: this.copy_msg,
        showConfirmButton: false,
        timer: 1000,
      });
    },
  },
  mounted: function () {
    new ClipboardJS(".btn-copy");
  },
};
</script>
