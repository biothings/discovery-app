<script setup>
import { useStore } from "vuex";
import cubeImg from "@/assets/img/cubeplus.svg";
import dragIcon from "@/assets/img/drag.svg";

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
      confirmButtonColor: "#43318d",
      cancelButtonColor: "#d83f87",
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
    :class="[item.title.includes('DEF') ? 'bg-dde-mid' : 'badge-primary']"
    draggable="true"
    @dragstart="startDrag($event, item)"
  >
    <svg
      viewBox="0 0 10 10"
      class="mr-1"
      width="10px"
      style="pointer-events: none"
    >
      <circle cx="1.8" cy="1.8" r=".9" />
      <circle cx="5" cy="1.8" r=".9" />
      <circle cx="8.1" cy="1.8" r=".9" />
      <circle cx="1.8" cy="8.1" r=".9" />
      <circle cx="5" cy="8.1" r=".9" />
      <circle cx="8.1" cy="8.1" r=".9" />
      <circle cx="1.8" cy="5" r=".9" />
      <circle cx="5" cy="5" r=".9" />
      <circle cx="8.1" cy="5" r=".9" />
    </svg>
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
