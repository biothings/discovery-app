import Notify from "simple-notify";

export const resource_registry = {
  state: {
    downloadMode: false,
    downloadList: [],
  },
  strict: true,
  getters: {
    downloadMode: (state) => {
      return state.downloadMode;
    },
    downloadList: (state) => {
      return state.downloadList;
    },
  },
  mutations: {
    toggleDownloadMode(state) {
      state.downloadMode = !state.downloadMode;
    },
    setDownloadMode(state, payload) {
      state.downloadMode = payload.value;
    },
    clearDownloadList(state) {
      state.downloadList = [];
      new Notify({
        status: "warning",
        title: "Metadata Registry",
        text: "Download Mode OFF",
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
    addDownload(state, payload) {
      try {
        let existingIndex = state.downloadList.indexOf(payload.value.id);
        if (existingIndex > -1) {
          state.downloadList.splice(existingIndex, 1);

          new Notify({
            status: "error",
            title: "Metadata",
            text: "Item removed",
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
        } else {
          state.downloadList.unshift(payload.value.id);
          new Notify({
            status: "success",
            title: "Metadata",
            text: "Item added",
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
      } catch (error) {
        new Notify({
          status: "error",
          title: "Metadata",
          text: "Failed to add download",
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
    },
  },
};
