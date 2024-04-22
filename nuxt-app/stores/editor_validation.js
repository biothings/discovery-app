import Notify from "simple-notify";
// editor default options
import { validation_options } from "./editor_options/validation_options";
import { definition_options } from "./editor_options/definition_options";
import { bioschemas_by_property } from "./editor_options/bioschemas_by_property";
import {
  bioschemas_by_type,
  most_used,
} from "./editor_options/bioschemas_by_type";
import { defineStore } from "pinia";

export const useEditorValidationStore = defineStore("editorValidationStore", {
  state: () => ({
    // change version when major breaking changes are implemented
    // this will delete all user's custom settings locally and start fresh
    editor_version: "1.0",
    editThis: null,
    editThisDefinition: null,
    validation_options: validation_options
      .concat(bioschemas_by_property)
      .concat(bioschemas_by_type),
    definition_options: definition_options,
    addCardinality: false,
    bioschemas_most_used: most_used,
    recentlyUsed: [],
  }),
  getters: {
    getRecentlyUsed: (state) => {
      return state.recentlyUsed;
    },
    addCardinality: (state) => {
      return state.addCardinality;
    },
    getDefinitionOptions: (state) => {
      return state.definition_options;
    },
    getEditItem: (state) => {
      return state.editThis;
    },
    getEditDefinitionItem: (state) => {
      return state.editThisDefinition;
    },
    getValidationOptions: (state) => {
      return state.validation_options;
    },
    getBioschemasMostUsed: (state) => {
      return state.bioschemas_most_used;
    },
  },
  actions: {
    checkVersion() {
      let version = localStorage.getItem("editor_version");
      if (!version || version !== this.editor_version) {
        console.log(
          "%c New version of editor, all custom options will be deleted",
          "color: red"
        );
        this.deleteFrequentlyUsed();
        this.deleteLocalCustomValidationAndDefinitions();
        localStorage.setItem("editor_version", this.editor_version);
        console.log(
          "%c New version of editor: " + this.editor_version,
          "color: green"
        );
      } else {
        console.log(
          "%c Editor Up-to-date! Version: " + this.editor_version,
          "color: blue"
        );
      }
    },
    toggleCardinality() {
      this.addCardinality = !this.addCardinality;
      //remove all marginality in validation
      if (!this.addCardinality) {
        new Notify({
          status: "warning",
          title: "Editor",
          text: "Removing cardinality",
          effect: "fade",
          speed: 300,
          customClass: null,
          customIcon: null,
          showIcon: true,
          showCloseButton: true,
          autoclose: true,
          autotimeout: 2000,
          gap: 20,
          distance: 20,
          type: 1,
          position: "right top",
        });
        for (const name in this.finalschema["@graph"][0]["$validation"][
          "properties"
        ]) {
          if (
            Object.hasOwnProperty.call(
              this.finalschema["@graph"][0]["$validation"]["properties"][name],
              "owl:cardinality"
            )
          ) {
            let newV =
              this.finalschema["@graph"][0]["$validation"]["properties"][name];
            delete newV["owl:cardinality"];
            this.finalschema["@graph"][0]["$validation"]["properties"][name] =
              newV;
          }
        }
      }
    },
    deleteValidationOption(payload) {
      const msg = [
        "Adios!",
        "Bye!",
        "See Ya!",
        "Hasta la vista!",
        "Gone",
        "Poof!",
        "So Long!",
      ];
      const random = Math.floor(Math.random() * msg.length);
      for (let i = 0; i < this.validation_options.length; i++) {
        if (this.validation_options[i]["_id"] == payload.id) {
          this.validation_options.splice(i, 1);
          localStorage.setItem(
            "custom_validation",
            JSON.stringify(this.validation_options)
          );
          new Notify({
            status: "success",
            title: "Deleted!",
            text: msg[random],
            effect: "fade",
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: true,
            autotimeout: 2000,
            gap: 20,
            distance: 20,
            type: 1,
            position: "right top",
          });
        }
      }
    },
    deleteDefinitionOption(payload) {
      const msg = [
        "Adios!",
        "Bye!",
        "See Ya!",
        "Deleted!",
        "Gone",
        "Poof!",
        "So Long!",
      ];
      const random = Math.floor(Math.random() * msg.length);
      for (let i = 0; i < this.definition_options.length; i++) {
        if (this.definition_options[i]["_id"] == payload.id) {
          this.definition_options.splice(i, 1);
          localStorage.setItem(
            "custom_definitions",
            JSON.stringify(this.definition_options)
          );
          new Notify({
            status: "success",
            title: "Deleted!",
            text: msg[random],
            effect: "fade",
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: true,
            autotimeout: 2000,
            gap: 20,
            distance: 20,
            type: 1,
            position: "right top",
          });
        }
      }
    },
    updateValidationOptions(payload) {
      this.validation_options = payload["validation"];
      // console.log('validation updated from localStorage')
    },
    updateDefinitionOptions(payload) {
      this.definition_options = payload["definitions"];
      // console.log('validation updated from localStorage')
    },
    addValidationOption(payload) {
      let item = payload["validation"];
      this.validation_options.push(item);
      localStorage.setItem(
        "custom_validation",
        JSON.stringify(this.validation_options)
      );
      new Notify({
        status: "success",
        title: "Editor",
        text: "Option added",
        effect: "fade",
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 2000,
        gap: 20,
        distance: 20,
        type: 1,
        position: "right top",
      });
    },
    addDefinitionOption(payload) {
      function makeID(length) {
        var result = "";
        var characters =
          "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
          result += characters.charAt(
            Math.floor(Math.random() * charactersLength)
          );
        }
        return result;
      }

      function getRandomColor() {
        var letters = "0123456789ABCDEF";
        var color = "#";
        for (var i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      }

      let item = payload["definition"];
      this.definition_options.push(item);
      //automatically add validation options with this def
      this.validation_options.push({
        _id: makeID(5),
        title: "(DEF)" + item.title + "(s)",
        color: getRandomColor(),
        list: 2,
        validation: {
          oneOf: [
            {
              $ref: "#/definitions/" + item.title,
            },
            {
              type: "array",
              items: {
                $ref: "#/definitions/" + item.title,
              },
            },
          ],
        },
        can_delete: true,
      });
      this.validation_options.push({
        _id: makeID(5),
        title: "(DEF)" + item.title,
        color: getRandomColor(),
        list: 2,
        validation: {
          $ref: "#/definitions/" + item.title,
        },
        can_delete: true,
      });

      localStorage.setItem(
        "custom_definitions",
        JSON.stringify(this.definition_options)
      );
      localStorage.setItem(
        "custom_validation",
        JSON.stringify(this.validation_options)
      );

      new Notify({
        status: "success",
        title: "Editor",
        text: item.title + " definition added",
        effect: "fade",
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 2000,
        gap: 20,
        distance: 20,
        type: 1,
        position: "right top",
      });
    },
    editValidationItem(payload) {
      let itemID = payload["item"]["_id"];
      let newItem = payload["item"];
      for (let i = 0; i < this.validation_options.length; i++) {
        let item = this.validation_options[i];
        if (item["_id"] == itemID) {
          this.validation_options[i] = newItem;
          this.editThis = "";
          new Notify({
            status: "success",
            title: "Editor",
            text: "Edits saved",
            effect: "fade",
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: true,
            autotimeout: 2000,
            gap: 20,
            distance: 20,
            type: 1,
            position: "right top",
          });
        }
      }
      localStorage.setItem(
        "custom_validation",
        JSON.stringify(this.validation_options)
      );
    },
    editDefinitionItem(payload) {
      let itemID = payload["item"]["_id"];
      let newItem = payload["item"];
      for (let i = 0; i < this.definition_options.length; i++) {
        let item = this.definition_options[i];
        if (item["_id"] == itemID) {
          this.definition_options[i] = newItem;
          this.editThisDefinition = "";
          new Notify({
            status: "success",
            title: "Editor",
            text: "Edits saved",
            effect: "fade",
            speed: 300,
            customClass: null,
            customIcon: null,
            showIcon: true,
            showCloseButton: true,
            autoclose: true,
            autotimeout: 2000,
            gap: 20,
            distance: 20,
            type: 1,
            position: "right top",
          });
        }
      }
      localStorage.setItem(
        "custom_definitions",
        JSON.stringify(this.definition_options)
      );
    },
    editThis(payload) {
      let item = payload["item"];
      this.editThis = item;
    },
    editThisDefinition(payload) {
      let item = payload["item"];
      this.editThisDefinition = item;
    },
    addRecentlyUsed(payload) {
      if (!this.recentlyUsed.some((o) => o.title == payload.validation.title)) {
        this.recentlyUsed.unshift(payload.validation);
        this.recentlyUsed = this.recentlyUsed.slice(0, 20);
        localStorage.setItem("recentlyUsed", JSON.stringify(this.recentlyUsed));
      } else {
        console.log("already in frequently used.");
      }
    },
    deleteFrequentlyUsed() {
      this.recentlyUsed = [];
      localStorage.setItem("recentlyUsed", JSON.stringify(this.recentlyUsed));
    },
    checkIfFrequentlyUsed() {
      let v = localStorage.getItem("recentlyUsed");
      if (v) {
        this.recentlyUsed = JSON.parse(v);
      }
    },
    deleteLocalCustomValidationAndDefinitions() {
      localStorage.removeItem("custom_validation");
      localStorage.removeItem("custom_definitions");
    },
  },
});

// export const editor_validation = {
//   state: {
//     // change version when major breaking changes are implemented
//     // this will delete all user's custom settings locally and start fresh
//     editor_version: "1.0",
//     editThis: null,
//     editThisDefinition: null,
//     validation_options: validation_options
//       .concat(bioschemas_by_property)
//       .concat(bioschemas_by_type),
//     definition_options: definition_options,
//     addCardinality: false,
//     bioschemas_most_used: most_used,
//     recentlyUsed: [],
//   },
//   strict: true,
//   mutations: {
//     toggleCardinality(state) {
//       state.addCardinality = !state.addCardinality;
//       //remove all marginality in validation
//       if (!state.addCardinality) {
//         new Notify({
//           status: "warning",
//           title: "Editor",
//           text: "Removing cardinality",
//           effect: "fade",
//           speed: 300,
//           customClass: null,
//           customIcon: null,
//           showIcon: true,
//           showCloseButton: true,
//           autoclose: true,
//           autotimeout: 2000,
//           gap: 20,
//           distance: 20,
//           type: 1,
//           position: "right top",
//         });
//         for (const name in state.finalschema["@graph"][0]["$validation"][
//           "properties"
//         ]) {
//           if (
//             Object.hasOwnProperty.call(
//               state.finalschema["@graph"][0]["$validation"]["properties"][name],
//               "owl:cardinality"
//             )
//           ) {
//             let newV =
//               state.finalschema["@graph"][0]["$validation"]["properties"][name];
//             delete newV["owl:cardinality"];
//             state.finalschema["@graph"][0]["$validation"]["properties"][name] =
//               newV;
//           }
//         }
//       }
//     },
//     deleteValidationOption(state, payload) {
//       const msg = [
//         "Adios!",
//         "Bye!",
//         "See Ya!",
//         "Hasta la vista!",
//         "Gone",
//         "Poof!",
//         "So Long!",
//       ];
//       const random = Math.floor(Math.random() * msg.length);
//       for (let i = 0; i < state.validation_options.length; i++) {
//         if (state.validation_options[i]["_id"] == payload.id) {
//           state.validation_options.splice(i, 1);
//           localStorage.setItem(
//             "custom_validation",
//             JSON.stringify(state.validation_options)
//           );
//           new Notify({
//             status: "success",
//             title: "Deleted!",
//             text: msg[random],
//             effect: "fade",
//             speed: 300,
//             customClass: null,
//             customIcon: null,
//             showIcon: true,
//             showCloseButton: true,
//             autoclose: true,
//             autotimeout: 2000,
//             gap: 20,
//             distance: 20,
//             type: 1,
//             position: "right top",
//           });
//         }
//       }
//     },
//     deleteDefinitionOption(state, payload) {
//       const msg = [
//         "Adios!",
//         "Bye!",
//         "See Ya!",
//         "Deleted!",
//         "Gone",
//         "Poof!",
//         "So Long!",
//       ];
//       const random = Math.floor(Math.random() * msg.length);
//       for (let i = 0; i < state.definition_options.length; i++) {
//         if (state.definition_options[i]["_id"] == payload.id) {
//           state.definition_options.splice(i, 1);
//           localStorage.setItem(
//             "custom_definitions",
//             JSON.stringify(state.definition_options)
//           );
//           new Notify({
//             status: "success",
//             title: "Deleted!",
//             text: msg[random],
//             effect: "fade",
//             speed: 300,
//             customClass: null,
//             customIcon: null,
//             showIcon: true,
//             showCloseButton: true,
//             autoclose: true,
//             autotimeout: 2000,
//             gap: 20,
//             distance: 20,
//             type: 1,
//             position: "right top",
//           });
//         }
//       }
//     },
//     updateValidationOptions(state, payload) {
//       state.validation_options = payload["validation"];
//       // console.log('validation updated from localStorage')
//     },
//     updateDefinitionOptions(state, payload) {
//       state.definition_options = payload["definitions"];
//       // console.log('validation updated from localStorage')
//     },
//     addValidationOption(state, payload) {
//       let item = payload["validation"];
//       state.validation_options.push(item);
//       localStorage.setItem(
//         "custom_validation",
//         JSON.stringify(state.validation_options)
//       );
//       new Notify({
//         status: "success",
//         title: "Editor",
//         text: "Option added",
//         effect: "fade",
//         speed: 300,
//         customClass: null,
//         customIcon: null,
//         showIcon: true,
//         showCloseButton: true,
//         autoclose: true,
//         autotimeout: 2000,
//         gap: 20,
//         distance: 20,
//         type: 1,
//         position: "right top",
//       });
//     },
//     addDefinitionOption(state, payload) {
//       function makeID(length) {
//         var result = "";
//         var characters =
//           "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
//         var charactersLength = characters.length;
//         for (var i = 0; i < length; i++) {
//           result += characters.charAt(
//             Math.floor(Math.random() * charactersLength)
//           );
//         }
//         return result;
//       }

//       function getRandomColor() {
//         var letters = "0123456789ABCDEF";
//         var color = "#";
//         for (var i = 0; i < 6; i++) {
//           color += letters[Math.floor(Math.random() * 16)];
//         }
//         return color;
//       }

//       let item = payload["definition"];
//       state.definition_options.push(item);
//       //automatically add validation options with this def
//       state.validation_options.push({
//         _id: makeID(5),
//         title: "(DEF)" + item.title + "(s)",
//         color: getRandomColor(),
//         list: 2,
//         validation: {
//           oneOf: [
//             {
//               $ref: "#/definitions/" + item.title,
//             },
//             {
//               type: "array",
//               items: {
//                 $ref: "#/definitions/" + item.title,
//               },
//             },
//           ],
//         },
//         can_delete: true,
//       });
//       state.validation_options.push({
//         _id: makeID(5),
//         title: "(DEF)" + item.title,
//         color: getRandomColor(),
//         list: 2,
//         validation: {
//           $ref: "#/definitions/" + item.title,
//         },
//         can_delete: true,
//       });

//       localStorage.setItem(
//         "custom_definitions",
//         JSON.stringify(state.definition_options)
//       );
//       localStorage.setItem(
//         "custom_validation",
//         JSON.stringify(state.validation_options)
//       );

//       new Notify({
//         status: "success",
//         title: "Editor",
//         text: item.title + " definition added",
//         effect: "fade",
//         speed: 300,
//         customClass: null,
//         customIcon: null,
//         showIcon: true,
//         showCloseButton: true,
//         autoclose: true,
//         autotimeout: 2000,
//         gap: 20,
//         distance: 20,
//         type: 1,
//         position: "right top",
//       });
//     },
//     editValidationItem(state, payload) {
//       let itemID = payload["item"]["_id"];
//       let newItem = payload["item"];
//       for (let i = 0; i < state.validation_options.length; i++) {
//         let item = state.validation_options[i];
//         if (item["_id"] == itemID) {
//           state.validation_options[i] = newItem;
//           state.editThis = "";
//           new Notify({
//             status: "success",
//             title: "Editor",
//             text: "Edits saved",
//             effect: "fade",
//             speed: 300,
//             customClass: null,
//             customIcon: null,
//             showIcon: true,
//             showCloseButton: true,
//             autoclose: true,
//             autotimeout: 2000,
//             gap: 20,
//             distance: 20,
//             type: 1,
//             position: "right top",
//           });
//         }
//       }
//       localStorage.setItem(
//         "custom_validation",
//         JSON.stringify(state.validation_options)
//       );
//     },
//     editDefinitionItem(state, payload) {
//       let itemID = payload["item"]["_id"];
//       let newItem = payload["item"];
//       for (let i = 0; i < state.definition_options.length; i++) {
//         let item = state.definition_options[i];
//         if (item["_id"] == itemID) {
//           state.definition_options[i] = newItem;
//           state.editThisDefinition = "";
//           new Notify({
//             status: "success",
//             title: "Editor",
//             text: "Edits saved",
//             effect: "fade",
//             speed: 300,
//             customClass: null,
//             customIcon: null,
//             showIcon: true,
//             showCloseButton: true,
//             autoclose: true,
//             autotimeout: 2000,
//             gap: 20,
//             distance: 20,
//             type: 1,
//             position: "right top",
//           });
//         }
//       }
//       localStorage.setItem(
//         "custom_definitions",
//         JSON.stringify(state.definition_options)
//       );
//     },
//     editThis(state, payload) {
//       let item = payload["item"];
//       state.editThis = item;
//     },
//     editThisDefinition(state, payload) {
//       let item = payload["item"];
//       state.editThisDefinition = item;
//     },
//     addRecentlyUsed(state, payload) {
//       if (
//         !state.recentlyUsed.some((o) => o.title == payload.validation.title)
//       ) {
//         state.recentlyUsed.unshift(payload.validation);
//         state.recentlyUsed = state.recentlyUsed.slice(0, 20);
//         localStorage.setItem(
//           "recentlyUsed",
//           JSON.stringify(state.recentlyUsed)
//         );
//       } else {
//         console.log("already in frequently used.");
//       }
//     },
//     deleteFrequentlyUsed(state, payload) {
//       state.recentlyUsed = [];
//       localStorage.setItem("recentlyUsed", JSON.stringify(state.recentlyUsed));
//     },
//     checkIfFrequentlyUsed(state) {
//       let v = localStorage.getItem("recentlyUsed");
//       if (v) {
//         state.recentlyUsed = JSON.parse(v);
//       }
//     },
//     deleteLocalCustomValidationAndDefinitions() {
//       localStorage.removeItem("custom_validation");
//       localStorage.removeItem("custom_definitions");
//     },
//   },
//   getters: {
//     getRecentlyUsed: (state) => {
//       return state.recentlyUsed;
//     },
//     addCardinality: (state) => {
//       return state.addCardinality;
//     },
//     getDefinitionOptions: (state) => {
//       return state.definition_options;
//     },
//     getEditItem: (state) => {
//       return state.editThis;
//     },
//     getEditDefinitionItem: (state) => {
//       return state.editThisDefinition;
//     },
//     getValidationOptions: (state) => {
//       return state.validation_options;
//     },
//     getBioschemasMostUsed: (state) => {
//       return state.bioschemas_most_used;
//     },
//   },
//   actions: {
//     checkVersion({ commit, state }) {
//       let version = localStorage.getItem("editor_version");
//       if (!version || version !== state.editor_version) {
//         console.log(
//           "%c New version of editor, all custom options will be deleted",
//           "color: red"
//         );
//         commit("deleteFrequentlyUsed");
//         commit("deleteLocalCustomValidationAndDefinitions");
//         localStorage.setItem("editor_version", state.editor_version);
//         console.log(
//           "%c New version of editor: " + state.editor_version,
//           "color: green"
//         );
//       } else {
//         console.log(
//           "%c Editor Up-to-date! Version: " + state.editor_version,
//           "color: blue"
//         );
//       }
//     },
//   },
// };
