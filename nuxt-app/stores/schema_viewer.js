import { defineStore } from "pinia";

export const useSchemaViewerStore = defineStore("schemaViewerStore", {
  state: () => ({
    validationView: true,
    userSchema: Object,
    userSchemaProps: Array,
    queryContent: Object,
    showAll: true,
  }),
  actions: {
    toggleShowAll() {
      this.showAll = !this.showAll;
    },
    toggleView() {
      this.validationView = !this.validationView;
    },
    setValidationView(payload) {
      this.validationView = payload.value;
    },
    toggleShowAll() {
      this.showAll = !this.showAll;
    },
    saveSchemaForViewer(payload) {
      this.userSchema = payload["schema"];
      // console.log('saved schema 🦄 ...',this.userSchema)
    },
    saveProps(payload) {
      this.userSchemaProps = payload["props"];
      // console.log('saving props 🛍 ...',this.userSchemaProps)
    },
    checkIFValidationView(payload) {
      this.queryContent = payload["queryContent"];
      if (!this.queryContent.hasOwnProperty("validation")) {
        this.validationView = false;
      } else if (
        this.queryContent.hasOwnProperty("validation") &&
        this.queryContent["validation"] == null
      ) {
        this.validationView = false;
      }
      // console.log('saved Query Content 🌎...',this.queryContent)
    },
  },
  getters: {
    handleLink: (state) => (name) => {
      let prefix = "";
      let cName = "";
      let link = "";
      if (name.includes(":")) {
        prefix = name.split(":")[0];
        cName = name.split(":")[1];
      } else {
        cName = name;
      }
      // console.log('handling Link...',prefix,cName)
      for (var x = 0; x < state.userSchema.hits.length; x++) {
        if (state.userSchema.hits[x].label.includes(cName)) {
          if (prefix && prefix === "schema") {
            link = "/schema/" + cName;
          } else {
            link = "/" + cName;
          }
          return link;
        } else {
          link = state.userSchema.context[prefix] + cName;
        }
      }
      return link;
    },
    removeDomainsNotIncluded: (state) => (domains) => {
      let res = [];
      if (domains) {
        for (var i = 0; i < domains.length; i++) {
          for (var x = 0; x < state.userSchema.hits.length; x++) {
            if (domains[i].includes(state.userSchema.hits[x].label)) {
              if (!res.includes(domains[i])) {
                res.push(domains[i]);
              }
            }
          }
        }
      }
      return res;
    },
  },
});

// export const schema_viewer = {
//   state: {
//     validationView: true,
//     userSchema: Object,
//     userSchemaProps: Array,
//     queryContent: Object,
//     showAll: true,
//   },
//   strict: true,
//   mutations: {
//     toggleView(state) {
//       state.validationView = !state.validationView;
//     },
//     setValidationView(state, payload) {
//       state.validationView = payload.value;
//     },
//     toggleShowAll(state) {
//       state.showAll = !state.showAll;
//     },
//     saveSchemaForViewer(state, payload) {
//       state.userSchema = payload["schema"];
//       // console.log('saved schema 🦄 ...',state.userSchema)
//     },
//     saveProps(state, payload) {
//       state.userSchemaProps = payload["props"];
//       // console.log('saving props 🛍 ...',state.userSchemaProps)
//     },
//     checkIFValidationView(state, payload) {
//       state.queryContent = payload["queryContent"];
//       if (!state.queryContent.hasOwnProperty("validation")) {
//         state.validationView = false;
//       } else if (
//         state.queryContent.hasOwnProperty("validation") &&
//         state.queryContent["validation"] == null
//       ) {
//         state.validationView = false;
//       }
//       // console.log('saved Query Content 🌎...',state.queryContent)
//     },
//   },
//   getters: {
//     // exposed as store.getters.nameOfGetter
//     queryContent: (state) => {
//       return state.queryContent;
//     },
//     validationView: (state) => {
//       return state.validationView;
//     },
//     showAll: (state) => {
//       return state.showAll;
//     },
//     handleLink: (state) => (name) => {
//       let prefix = "";
//       let cName = "";
//       let link = "";
//       if (name.includes(":")) {
//         prefix = name.split(":")[0];
//         cName = name.split(":")[1];
//       } else {
//         cName = name;
//       }
//       // console.log('handling Link...',prefix,cName)
//       for (var x = 0; x < state.userSchema.hits.length; x++) {
//         if (state.userSchema.hits[x].label.includes(cName)) {
//           if (prefix && prefix === "schema") {
//             link = "/schema/" + cName;
//           } else {
//             link = "/" + cName;
//           }
//           return link;
//         } else {
//           link = state.userSchema.context[prefix] + cName;
//         }
//       }
//       return link;
//     },
//     removeDomainsNotIncluded: (state) => (domains) => {
//       let res = [];
//       if (domains) {
//         for (var i = 0; i < domains.length; i++) {
//           for (var x = 0; x < state.userSchema.hits.length; x++) {
//             if (domains[i].includes(state.userSchema.hits[x].label)) {
//               if (!res.includes(domains[i])) {
//                 res.push(domains[i]);
//               }
//             }
//           }
//         }
//       }
//       return res;
//     },
//   },
//   actions: {
//     toggleShowAll(context) {
//       context.commit("toggleShowAll");
//     },
//   },
// };
