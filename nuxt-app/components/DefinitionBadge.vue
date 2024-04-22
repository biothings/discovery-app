<script setup>
import { useEditorValidationStore } from "../stores/editor_validation";

const { $swal } = useNuxtApp();
const props = defineProps(["item"]);
const store = useEditorValidationStore();

function editDefinitionOption(item) {
  store.editThisDefinition({ item: Object.assign({}, item) });
}

function deleteDefinitionOption(item) {
  $swal
    .fire({
      title: "Are you sure?",
      html: `<b>Warning</b>: deleting this definition will remove it from your library entirely. <br>Definitions that are not referenced will not appear in your json schema validation. Continue?`,
      showCancelButton: true,
      confirmButtonColor: "#63296b",
      cancelButtonColor: "#4a7d8f",
      customClass: {
        popup: "scale-in-center",
      },
      confirmButtonText: "Yes, Delete",
    })
    .then((res) => {
      if (res.value) {
        store.deleteDefinitionOption({ id: item._id });
      }
    });
}
</script>

<template>
  <div class="badge m-1 text-light" :style="{ 'background-color': item.color }">
    <span v-text="item.title" class="mr-1"></span>
    <font-awesome-icon
      icon="fas fa-circle-info"
      class="mx-1"
      :data-tippy-content="JSON.stringify(item.validation, null, 2)"
    ></font-awesome-icon>
    <span
      data-tippy-content="EDIT"
      data-tippy-theme="light"
      data-tippy-placement="bottom"
      class="badge badge-light pointer mr-1"
      @click="editDefinitionOption(item)"
      ><font-awesome-icon icon="fas fa-pen-square"></font-awesome-icon
    ></span>
    <span
      v-if="item && item.can_delete"
      data-tippy-content="DELETE"
      data-tippy-placement="bottom"
      class="badge badge-danger pointer"
      @click="deleteDefinitionOption(item)"
      ><font-awesome-icon icon="fas fa-times"></font-awesome-icon
    ></span>
  </div>
</template>
