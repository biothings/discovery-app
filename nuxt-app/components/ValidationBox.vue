<template>
  <div>
    <ul class="nav nav-tabs">
      <li class="nav-item text-primary pointer">
        <a
          class="nav-link text-primary"
          :class="[selected == 'all' ? 'bg-dark text-light' : 'text-dark']"
          @click="selected = 'all'"
        >
          ALL PROPERTIES ({{ Object.keys(validation.properties).length }})
        </a>
      </li>
      <li
        class="nav-item text-danger pointer"
        data-tippy-content="These properties must be included in your metadata in order to be compliant and provide minimum insight into your metadata"
      >
        <a
          class="nav-link"
          :class="[
            selected == 'required' ? 'bg-danger text-light' : 'text-danger',
          ]"
          @click="selected = 'required'"
        >
          <font-awesome-icon icon="fas fa-asterisk" /> REQUIRED ({{
            totals.req
          }})
        </a>
      </li>
      <li
        class="nav-item text-warning pointer"
        data-tippy-content="These properties are strongly suggested to be included in your metadata in order to provide more insight into your metadata"
      >
        <a
          class="nav-link text-warning"
          :class="[
            selected == 'recommended'
              ? 'bg-warning text-light'
              : 'text-warning',
          ]"
          @click="selected = 'recommended'"
        >
          <font-awesome-icon icon="fas fa-circle" /> RECOMMENDED ({{
            totals.rec
          }})
        </a>
      </li>
      <li
        class="nav-item text-info pointer"
        data-tippy-content="These properties are optional but for encouraged for completeness and better understanding about your metadata"
      >
        <a
          class="nav-link text-info"
          :class="[selected == 'optional' ? 'bg-info text-light' : 'text-info']"
          @click="selected = 'optional'"
        >
          <font-awesome-icon icon="fas fa-square" /> OPTIONAL ({{ totals.opt }})
        </a>
      </li>
      <li
        class="nav-item text-primary pointer"
        data-tippy-content="These properties can potentially satisfy other requirements. At least one of these properties is required."
      >
        <a
          class="nav-link text-primary"
          :class="[
            selected == 'potential' ? 'bg-primary text-light' : 'text-primary',
          ]"
          @click="selected = 'potential'"
        >
          <font-awesome-layers>
            <font-awesome-icon icon="fas fa-circle" />
            <font-awesome-icon
              icon="fas fa-asterisk"
              :class="[selected == 'potential' ? 'text-primary' : 'text-light']"
            />
          </font-awesome-layers>
          CONDITIONALLY REQUIRED ({{ totals.pot }})
        </a>
      </li>
    </ul>
  </div>
  <div class="p-0">
    <template v-for="(value, name) in sorted_props" :key="name">
      <PropertyBox
        :name="name"
        :fullInfo="value"
        :recommended="validation.recommended"
        :optional="validation.optional"
        :required="validation.required"
        :potential="potential"
      ></PropertyBox>
    </template>
  </div>
</template>

<script>
export default {
  name: "ValidationBox",
  props: ["validation"],
  data: function () {
    return {
      sorted_props: {},
      potential: [],
      selected: "all",
      view_props: [],
      totals: {
        req: 0,
        rec: 0,
        opt: 0,
        pot: 0,
      },
    };
  },
  watch: {
    selected: function () {
      this.sortByImportance();
    },
  },
  methods: {
    getByImportance(field) {
      let self = this;
      let sorted = {};
      switch (field) {
        case "potential":
          if (Object.hasOwnProperty.call(self.validation, "anyOf")) {
            self.validation.anyOf.forEach((item) => {
              if (item?.required && Array.isArray(item?.required)) {
                item?.required.forEach((i) => self.potential.push(i));
              } else if (typeof item?.required == "string") {
                self.potential.push(item?.required);
              }
            });
          }
          //gather props
          for (const prop in self.validation.properties) {
            if (self.potential.includes(prop)) {
              sorted[prop] = self.validation.properties[prop];
            }
          }
          break;
        default:
          if (Object.hasOwnProperty.call(self.validation, field)) {
            self.validation[field].forEach((item) => {
              if (item in self.validation.properties && !(item in sorted)) {
                sorted[item] = self.validation.properties[item];
              }
            });
          }
          break;
      }
      this.sorted_props = sorted;
    },
    sortByImportance() {
      switch (this.selected) {
        case "all":
          this.getAll();
          break;

        default:
          this.getByImportance(this.selected);
          break;
      }
    },
    getAll() {
      let self = this;
      self.totals = {
        req: 0,
        rec: 0,
        opt: 0,
        pot: 0,
      };
      let sorted = {};
      // get potential required
      if (Object.hasOwnProperty.call(self.validation, "anyOf")) {
        self.validation.anyOf.forEach((item) => {
          self.totals.pot++;
          if (item?.required && Array.isArray(item?.required)) {
            item?.required.forEach((i) => self.potential.push(i));
          } else if (typeof item?.required == "string") {
            self.potential.push(item?.required);
          }
        });
      }
      //get required
      if (Object.hasOwnProperty.call(self.validation, "required")) {
        self.validation.required.forEach((item) => {
          self.totals.req++;
          if (item in self.validation.properties && !(item in sorted)) {
            sorted[item] = self.validation.properties[item];
          }
        });
      }
      //get recommended
      if (Object.hasOwnProperty.call(self.validation, "recommended")) {
        self.validation.recommended.forEach((item) => {
          self.totals.rec++;
          if (item in self.validation.properties && !(item in sorted)) {
            sorted[item] = self.validation.properties[item];
          }
        });
      }
      //get optional
      if (Object.hasOwnProperty.call(self.validation, "optional")) {
        self.validation.optional.forEach((item) => {
          self.totals.opt++;
          if (item in self.validation.properties && !(item in sorted)) {
            sorted[item] = self.validation.properties[item];
          }
        });
      }
      //get not categorized
      for (const prop in self.validation.properties) {
        if (!(prop in sorted)) {
          sorted[prop] = self.validation.properties[prop];
        }
      }
      // console.log(sorted)
      self.sorted_props = sorted;
    },
  },
  mounted: function () {
    this.sortByImportance();
  },
};
</script>
