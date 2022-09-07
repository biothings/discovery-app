<template>
  <button class="btn btn-sm btn-info mt-4 mb-1" @click="handleEdit()">
    <small>edit description <i class="fas fa-pen-square"></i></small>
  </button>
</template>

<script>
import "../assets/js/notify.min.js";

export default {
  name: "EditDescription",
  props: ["propname", "val"],
  methods: {
    handleEdit() {
      let self = this;
      let hasDesc = false;
      if (Object.hasOwnProperty.call(self.val, "description")) {
        hasDesc = true;
      } else {
        $.notify("Adding new description", {
          globalPosition: "right",
          style: "info",
          showDuration: 200,
        });
      }
      self.$swal
        .fire({
          title: "Edit description",
          text: hasDesc
            ? "Current: " + self.val.description
            : "Enter new description",
          input: "textarea",
          inputPlaceholder: "Enter text here",
          showCancelButton: true,
          animation: false,
          confirmButtonColor: "{{color_main}}",
          cancelButtonColor: "{{color_sec}}",
          customClass: "scale-in-center",
          confirmButtonText: "Save",
          showLoaderOnConfirm: true,
          preConfirm: (method) => {
            return method;
          },
          allowOutsideClick: () => !Swal.isLoading(),
        })
        .then((result) => {
          let payload = {
            // follow structure of val options
            validation: { validation: { description: result.value } },
            name: self.propname,
          };
          self.$store.commit("setValidation", payload);
        });
    },
  },
};
</script>
