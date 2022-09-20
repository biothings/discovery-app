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
      $.notify("Download Mode OFF", {
        globalPosition: "right",
        style: "danger",
        showDuration: 40,
      });
    },
    addDownload(state, payload) {
      try {
        let existingIndex = state.downloadList.indexOf(payload.value.id);
        if (existingIndex > -1) {
          state.downloadList.splice(existingIndex, 1);
          $.notify("Item Removed", {
            globalPosition: "right",
            style: "danger",
            showDuration: 40,
          });
        } else {
          state.downloadList.unshift(payload.value.id);
          $.notify("Item Added", {
            globalPosition: "right",
            style: "success",
            showDuration: 40,
          });
        }
      } catch (error) {
        $.notify("Failed to add download", {
          globalPosition: "right",
          style: "danger",
          showDuration: 40,
        });
      }
    },
  },
};
