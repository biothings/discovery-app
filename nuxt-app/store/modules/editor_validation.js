import Notify from "simple-notify";
// editor default options
import { validation_options } from "./editor_options/validation_options";
import { definition_options } from "./editor_options/definition_options";

export const editor_validation = {
  state: {
    editThis: null,
    editThisDefinition: null,
    validation_options: validation_options,
    definition_options: definition_options,
    addCardinality: false,
  },
  strict: true,
  mutations: {
    toggleCardinality(state) {
      state.addCardinality = !state.addCardinality;
      //remove all marginality in validation
      if (!state.addCardinality) {
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
        for (const name in state.finalschema["@graph"][0]["$validation"][
          "properties"
        ]) {
          if (
            Object.hasOwnProperty.call(
              state.finalschema["@graph"][0]["$validation"]["properties"][name],
              "owl:cardinality"
            )
          ) {
            let newV =
              state.finalschema["@graph"][0]["$validation"]["properties"][name];
            delete newV["owl:cardinality"];
            state.finalschema["@graph"][0]["$validation"]["properties"][name] =
              newV;
          }
        }
      }
    },
    deleteValidationOption(state, payload) {
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
      for (let i = 0; i < state.validation_options.length; i++) {
        if (state.validation_options[i]["_id"] == payload.id) {
          state.validation_options.splice(i, 1);
          localStorage.setItem(
            "custom_validation",
            JSON.stringify(state.validation_options)
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
    deleteDefinitionOption(state, payload) {
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
      for (let i = 0; i < state.definition_options.length; i++) {
        if (state.definition_options[i]["_id"] == payload.id) {
          state.definition_options.splice(i, 1);
          localStorage.setItem(
            "custom_definitions",
            JSON.stringify(state.definition_options)
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
    updateValidationOptions(state, payload) {
      state.validation_options = payload["validation"];
      // console.log('validation updated from localStorage')
    },
    updateDefinitionOptions(state, payload) {
      state.definition_options = payload["definitions"];
      // console.log('validation updated from localStorage')
    },
    addValidationOption(state, payload) {
      let item = payload["validation"];
      state.validation_options.push(item);
      localStorage.setItem(
        "custom_validation",
        JSON.stringify(state.validation_options)
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
    addDefinitionOption(state, payload) {
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
      state.definition_options.push(item);
      //automatically add validation options with this def
      state.validation_options.push({
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
      state.validation_options.push({
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
        JSON.stringify(state.definition_options)
      );
      localStorage.setItem(
        "custom_validation",
        JSON.stringify(state.validation_options)
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
    editValidationItem(state, payload) {
      let itemID = payload["item"]["_id"];
      let newItem = payload["item"];
      for (let i = 0; i < state.validation_options.length; i++) {
        let item = state.validation_options[i];
        if (item["_id"] == itemID) {
          state.validation_options[i] = newItem;
          state.editThis = "";
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
        JSON.stringify(state.validation_options)
      );
    },
    editDefinitionItem(state, payload) {
      let itemID = payload["item"]["_id"];
      let newItem = payload["item"];
      for (let i = 0; i < state.definition_options.length; i++) {
        let item = state.definition_options[i];
        if (item["_id"] == itemID) {
          state.definition_options[i] = newItem;
          state.editThisDefinition = "";
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
        JSON.stringify(state.definition_options)
      );
    },
    editThis(state, payload) {
      let item = payload["item"];
      state.editThis = item;
    },
    editThisDefinition(state, payload) {
      let item = payload["item"];
      state.editThisDefinition = item;
    },
  },
  getters: {
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
  },
  actions: {},
};
