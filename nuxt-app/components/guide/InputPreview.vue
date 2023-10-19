<template>
  <div>
    <template v-if="type == 'obj'">
      <span
        :data-tippy-content="JSON.stringify(userInput, null, 2)"
        :data-tippy-id="0"
        class="badge kwbadge badge-success mr-1 pointer slit-in-vertical desc"
        title="remove"
      >
        <font-awesome-icon icon="fas fa-check"></font-awesome-icon>
        <template v-if="userInput && userInput.name">
          <span v-text="userInput.name"></span>
        </template>
        <template v-else>
          <span v-text="name"></span>
          <font-awesome-icon
            icon="fas fa-info-circle"
            class="text-info"
          ></font-awesome-icon>
        </template>
        <span
          style="opacity: 0"
          class="d-inline"
          @click="removeItem($event, userInput)"
        >
          <font-awesome-icon icon="fas fa-times"></font-awesome-icon
        ></span>
      </span>
    </template>
    <template v-else-if="type == 'arr'" v-for="(person, i) in userInput">
      <span
        :data-tippy-content="JSON.stringify(person, null, 2)"
        :data-tippy-id="i"
        class="badge kwbadge badge-success mr-1 pointer slit-in-vertical desc"
        title="remove"
      >
        <font-awesome-icon icon="fas fa-check"></font-awesome-icon>
        <template v-if="person && person.name">
          <span v-text="person.name"></span>
        </template>
        <template v-else-if="person && person.constructor == String">
          <span v-text="person"></span>
        </template>
        <span v-else v-text="name + ' ' + (i + 1)"></span>
        <span
          style="opacity: 0"
          class="d-inline"
          @click="removeItem($event, person)"
        >
          <font-awesome-icon icon="fas fa-times"></font-awesome-icon
        ></span>
      </span>
    </template>
  </div>
</template>

<script>
export default {
  name: "InputPreview",
  data: function () {
    return {
      userObj: {},
    };
  },
  props: ["userInput", "removeItem", "name"],
  computed: {
    type: function () {
      var self = this;
      if (self.userInput) {
        switch (self.userInput.constructor) {
          case Object:
            return "obj";
          case Array:
            return "arr";
          case String:
            return "str";
          default:
            return "arr";
        }
      }
    },
  },
};
</script>
