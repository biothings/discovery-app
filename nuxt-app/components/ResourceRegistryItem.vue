<template>
  <li class="list-group-item list-group-item-action p-0">
    <div class="row m-0">
      <div
        v-if="downloadMode"
        class="p-1 d-flex justify-content-center align-items-center"
        :class="[
          inDownloadCart ? 'btn-success text-light' : 'btn-light text-info',
        ]"
        @click="handleDownload()"
      >
        <font-awesome-icon v-if="!inDownloadCart" icon="fas fa-plus fa-2x" />
        <font-awesome-icon v-else icon="fas fa-check fa-2x" />
      </div>
      <div class="col-sm-7">
        <h5
          class="mb-1 mainTextDark d-inline gaText d-inline pointer"
          @click="goTo(item)"
        >
          <img :src="imgIcon" width="20" :alt="item.name" class="mr-1" />
          <nuxt-link :to="{ path: '/resource/' + item._id }">{{
            item.name
          }}</nuxt-link>
          <span
            v-if="item && item.name.includes('PPRL')"
            class="ml-2 badge smallBadge"
            >PPRL</span
          >
        </h5>
        <template v-if="item && item.name.includes('PPRL')">
          <span
            v-if="item && item.name.includes('Viral Variance')"
            class="ml-1 badge smallBadge bg-light"
            ><a href="/faq/n3c#VIRAL_VARIANCE" target="_blank">FAQ</a></span
          >
          <span
            v-if="item && item.name.includes('Mortality')"
            class="ml-1 badge smallBadge bg-light"
            ><a href="/faq/n3c#MORTALITY" target="_blank">FAQ</a></span
          >
        </template>
        <p v-if="item && item.description" class="text-muted">
          <small v-html="text"></small>
        </p>
      </div>
      <div class="col-sm-3">
        <small class="text-muted" v-if="last_updated">
          Last updated <b class="d-block" v-text="last_updated"></b>
        </small>
        <div
          v-if="isN3C"
          class="badge badge-pill text-light d-block mb-1"
          :class="color"
        >
          <span v-text="n3c_status"></span>
        </div>
      </div>
    </div>
  </li>
</template>

<script>
import moment from "moment";
import dde from "~~/assets/img/dde-logo-o.svg";
import n3cLogo from "~~/assets/img/N3Co.png";
import niaidIcon from "~~/assets/img/niaid/icon.svg";
import outbreakIcon from "~~/assets/img/icon-01.svg";
import nde from "~~/assets/img/niaid/nde.svg";
import creidIcon from "~~/assets/img/creid/icon.svg";

export default {
  name: "ResourceRegistryItem",
  data: function () {
    return {
      options: false,
      isN3C: false,
      n3c_status: "",
      color: "badge-light",
    };
  },
  props: ["item"],
  methods: {
    getSubclass(parents) {
      if (parents) {
        let sub = parents[0].split(", ");
        return sub[sub.length - 1];
      } else {
        return "This class has no subclass";
      }
    },
    getPropTotal() {
      if (this.item.hasOwnProperty("properties")) {
        return this.item.properties.length;
      } else {
        return "0";
      }
    },
    goTo(item) {
      gtag("event", "click", {
        event_category: "dataset_viewed",
        event_label: item._id,
        event_value: 1,
      });
    },
    handleDownload() {
      let doc = {
        id: this.item._id,
        name: this.item.name,
      };
      this.$store.commit("addDownload", { value: doc });
    },
  },
  computed: {
    imgIcon: function () {
      let self = this;
      let guide = Object.prototype.hasOwnProperty.call(
        self.item["_meta"],
        "guide"
      )
        ? self.item["_meta"]["guide"]
        : "";
      if (guide == "/guide") {
        return dde;
      } else if (guide.includes("niaid")) {
        return niaidIcon;
      } else if (guide.includes("outbreak")) {
        return outbreakIcon;
      } else if (guide.includes("n3c")) {
        return n3cLogo;
      } else if (guide.includes("nde")) {
        return nde;
      } else if (guide.includes("creid")) {
        return creidIcon;
      } else {
        return dde;
      }
    },
    text: function () {
      if (this.item.description.length > 150) {
        return this.item.description.substring(0, 150) + "...";
      } else {
        return this.item.description;
      }
    },
    detailLink: function () {
      return "/resource/" + this.item._id;
    },
    last_updated: function () {
      if (
        this.item.hasOwnProperty("_ts") &&
        this.item["_ts"].hasOwnProperty("last_updated")
      ) {
        return moment(this.item["_ts"]["last_updated"]).format("MMM Do YYYY");
      } else {
        if (
          this.item.hasOwnProperty("_meta") &&
          this.item["_meta"].hasOwnProperty("last_updated")
        ) {
          return moment(this.item["_meta"]["last_updated"]).format(
            "MMM Do YYYY"
          );
        } else {
          return false;
        }
      }
    },
    downloadMode: function () {
      return this.$store.getters.downloadMode;
    },
    inDownloadCart: function () {
      return this.$store.getters.downloadList.includes(this.item._id);
    },
  },
  mounted: function () {
    let self = this;
    if (
      Object.prototype.hasOwnProperty.call(self.item, "_n3c") &&
      Object.keys(self.item["_n3c"]).length
    ) {
      self.isN3C = true;
      self.n3c_status = Object.prototype.hasOwnProperty.call(
        self.item["_n3c"],
        "status"
      )
        ? self.item["_n3c"]["status"]
        : "Not Available";
      switch (self.n3c_status) {
        case "Available":
          self.color = "badge-success";
          break;
        case "Denied":
          self.color = "badge-danger";
          break;
        case "Approved for Import":
          self.color = "badge-purple";
          break;
        case "Pending Review":
          self.color = "badge-info";
          break;
        default:
          self.color = "badge-secondary";
          break;
      }
    }
  },
};
</script>
