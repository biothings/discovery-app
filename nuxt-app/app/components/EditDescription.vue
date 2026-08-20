<template>
  <button
    class="btn btn-sm themeButton text-light mt-4 mb-1"
    @click="handleEdit()"
  >
    <small>edit description <i class="fas fa-pen-square"></i></small>
  </button>
</template>

<script>

export default {
  name: "EditDescription",
  props: ["propname", "val"],
  methods: {
    async handleEdit(){
      let self = this;
      const { value: newDescription } = await self.$swal.fire({
          title: "Edit description",
          input: "textarea",
          text: self.val?.description
              ? "Current: " + self.val.description
              : "Enter new description",
          inputPlaceholder: "enter text here",
          customClass: {
            popup: "scale-in-center",
          },
        });

        if (newDescription) {
           let payload = {
            validation: { validation: { description: newDescription } },
            name: self.propname,
          };
          self.$store.commit("setValidation", payload);
        }
    }
  },
};
</script>
