<template>
  <div class="row m-0 valBox bg-dark m-1">
    <div class="col-sm-12 col-md-5">
      <div class="row">
        <div class="col-sm-12">
          <small class="text-light" v-text="propname"></small>
          <font-awesome-icon
            icon="fa fa-times-circle"
            class="pointer text-warning ml-1"
            @click="resetValidation()"
            data-tippy-content="Clear Validation"
          ></font-awesome-icon>
        </div>
        <div class="col-sm-12">
          <EditDescription :propname="propname" :val="val"></EditDescription>
          <CardinalitySelector
            v-if="addCardinality"
            :propname="propname"
            :val="val"
          ></CardinalitySelector>
        </div>
      </div>
    </div>
    <div
      class="col-sm-12 col-md-7 p-1 text-success drop-zone"
      style="font-size: 12px"
      @drop="onDrop($event, propname)"
      @dragleave="leaveDrag($event)"
      @dragover="allowDrop($event)"
      @dragenter.prevent
    >
      <template v-for="item in matches">
        <div
          v-if="val.type === item.validation.type"
          :data-tippy-content="JSON.stringify(item.validation, null, 2)"
          :style="{ 'background-color': item.color }"
          class="badge drag-el m-1"
          :key="item.title"
          draggable
          @dragstart="startDrag($event, item)"
          v-text="item.title"
        ></div>
      </template>
      <pre class="m-0" v-text="JSON.stringify(val, null, 2)"></pre>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import EditDescription from "./EditDescription.vue";
import CardinalitySelector from "./CardinalitySelector.vue";

import cubePlus from "@/assets/img/cubeplus.svg";

export default {
  name: "ValidationDropzone",
  props: ["propname", "val"],
  data: function () {
    return {
      matches: [],
    };
  },
  components: {
    EditDescription,
    CardinalitySelector,
  },
  methods: {
    allowDrop(ev) {
      $(ev.target).attr("drop-active", true);
      ev.preventDefault();
    },
    startDrag: (evt, item) => {
      let img = new Image();
      img.src = cubePlus;
      evt.dataTransfer.setDragImage(img, 10, 10);

      evt.dataTransfer.dropEffect = "move";
      evt.dataTransfer.effectAllowed = "move";
      evt.dataTransfer.setData("itemID", item._id);
    },
    onDrop(evt, name) {
      let self = this;
      self.matches = [];
      const itemID = evt.dataTransfer.getData("itemID");
      // const item = this.validation_options.find(item => item.id == itemID)
      this.validation_options.forEach((item) => {
        if (item._id == itemID) {
          // console.log(itemID, item)
          self.matches.push(item);
          let payload = {
            validation: item,
            name: name,
          };
          let audio = document.getElementById("dropsound");
          audio.play();
          self.$store.commit("setValidation", payload);
        }
      });
    },
    allowDrop(ev) {
      $(ev.target).attr("drop-active", true);
      ev.preventDefault();
    },
    leaveDrag(ev) {
      $(ev.target).removeAttr("drop-active");
      ev.preventDefault();
    },
    resetValidation() {
      let self = this;
      let payload = {
        name: self.propname,
      };
      self.matches = [];
      this.$store.commit("resetValidationFor", payload);
    },
  },
  computed: {
    ...mapGetters({
      validation_options: "getValidationOptions",
      addCardinality: "addCardinality",
    }),
  },
};
</script>
