<script setup>
import { useStore } from "vuex";
import cubeImg from "@/assets/img/cubeplus.svg";

const { $swal } = useNuxtApp();
const props = defineProps(["item"]);
const store = useStore();

function startDrag(evt, item) {
  let img = new Image();
  img.src = cubeImg;
  evt.dataTransfer.setDragImage(img, 10, 10);
  evt.dataTransfer.dropEffect = "move";
  evt.dataTransfer.effectAllowed = "move";
  evt.dataTransfer.setData("itemID", item._id);
}

function editValidationOption(item) {
  store.commit("editThis", { item: Object.assign({}, item) });
}

function deleteValidationOption(item) {
  $swal
    .fire({
      title: "Are you sure?",
      text: `You are deleting "${item.title}" permanently.`,
      showCancelButton: true,
      confirmButtonColor: "#63296b",
      cancelButtonColor: "#4a7d8f",
      customClass: "scale-in-center",
      confirmButtonText: "Delete",
    })
    .then((res) => {
      if (res.value) {
        store.commit("deleteValidationOption", { id: item._id });
      }
    });
}
</script>
<template>
  <div
    class="badge drag-el m-1 shadow"
    :class="[item.title.includes('DEF') ? 'badge-info' : 'badge-primary']"
    draggable="true"
    @dragstart="startDrag($event, item)"
  >
    <span class="mr-1"
      >{{ item.title }}
      <span v-if="JSON.stringify(item).includes('array')">(s)</span></span
    >
    <font-awesome-icon
      icon="fas fa-circle-info"
      class="mx-1"
      :data-tippy-content="JSON.stringify(item.validation, null, 2)"
    ></font-awesome-icon>
    <span
      data-tippy-content="EDIT"
      data-tippy-placement="bottom"
      data-tippy-theme="light"
      class="badge badge-light pointer mr-1 tip edit-val-btn"
      @click="editValidationOption(item)"
      ><font-awesome-icon icon="fas fa-pen-square"></font-awesome-icon
    ></span>
    <span
      v-if="item && item.can_delete"
      data-tippy-content="DELETE"
      data-tippy-placement="bottom"
      data-tippy-theme="light"
      class="badge badge-danger pointer del-val-btn"
      @click="deleteValidationOption(item)"
      ><font-awesome-icon icon="fas fa-times"></font-awesome-icon
    ></span>
  </div>
</template>
