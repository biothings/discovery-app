<template>
  <div
    v-if="name !== '_meta'"
    class="m-0 rounded-0"
    :class="[isChild ? 'p-1 border-left' : 'p-1 border-bottom']"
  >
    <!-- 🌈 Array 🌈 -->
    <template v-if="type == 'array'">
      <div class="row m-0">
        <div class="text-left">
          <span
            class="text-primary"
            @click="expandArray = !expandArray"
            style="cursor: pointer"
          >
            <span v-text="readable_name"></span> (<span
              v-text="content.length"
            ></span
            >)
            <b v-if="!expandArray">+</b>
            <b v-if="expandArray">-</b>
          </span>
        </div>
        <div class="col-sm-12" v-if="expandArray">
          <div>
            <template v-if="content.length > perPage">
              <select
                class="form-control form-control-sm m-auto w-25"
                v-model="perPage"
                @change="calculatePages"
                id="perPage"
              >
                <option value="" disabled selected>Shown Per Page</option>
                <option value="10">10 per page</option>
                <option value="25">25 per page</option>
                <option value="100">100 per page</option>
              </select>
              <div class="d-flex flex-wrap justify-content-center p-1 mt-2">
                <div
                  class="page-item rounded-0"
                  :class="{ disabled: page <= 1 }"
                >
                  <a class="page-link p-1" @click.prevent="prevPage()"
                    ><font-awesome-icon icon="fas fa-step-backward"
                  /></a>
                </div>
                <template v-if="groupPages">
                  <div
                    class="page-item rounded-0"
                    v-show="!startCapLimitReached"
                  >
                    <a
                      href="#"
                      class="page-link p-1"
                      @click.prevent="previousGroup()"
                      >Previous 20</a
                    >
                  </div>
                </template>
                <template v-for="n in pages">
                  <div
                    v-if="n >= startCap && n <= endCap"
                    class="page-item rounded-0"
                    :class="{
                      active: page == n,
                      'bg-primary': page == n,
                      'white-text': page == n,
                    }"
                  >
                    <a
                      href="#"
                      class="page-link p-1"
                      @click.prevent="page = n"
                      v-text="n"
                    ></a>
                  </div>
                </template>
                <template v-if="groupPages">
                  <div class="page-item rounded-0" v-show="!endCapLimitReached">
                    <a
                      href="#"
                      class="page-link p-1"
                      @click.prevent="nextGroup()"
                      >Next 20</a
                    >
                  </div>
                </template>
                <div
                  class="page-item rounded-0"
                  :class="{ disabled: page >= pages }"
                >
                  <a class="page-link p-1" @click.prevent="nextPage()"
                    ><font-awesome-icon icon="fas fa-step-forward"
                  /></a>
                </div>
              </div>
            </template>
          </div>
          <template v-for="item in arrayResults">
            <ResourceFieldBox
              class="m-1"
              name=""
              :content="item"
              isChild="true"
            ></ResourceFieldBox>
          </template>
        </div>
      </div>
    </template>
    <!-- 🌈 String 🌈 -->
    <template v-if="type == 'string'">
      <div class="d-flex">
        <template v-if="isUrl(content)">
          <div class="text-left">
            <span class="mainTextDark">
              <b v-text="readable_name"></b>
              <font-awesome-icon v-if="!readable_name" icon="fas fa-circle" />
              <span v-else>:</span>
            </span>
          </div>
          <div class="ml-1">
            <a :href="content" target="_blank" rel="nonreferrer">
              <span
                ><span v-text="content"></span>
                <font-awesome-icon icon="fas fa-external-link-alt" class="ml-1"
              /></span>
            </a>
          </div>
        </template>
        <template v-else
          > 
          <div class="d-flex">
            <span class="mainTextDark">
              <b
                v-text="readable_name ? readable_name + ' :' : ''"
                class="mr-1"
              ></b>
            </span>
          </div>
          <div class="d-flex">
            <a
              class="ml-1"
              v-if="isUrl(content)"
              v-text="content"
              :href="content"
              target="_blank"
              rel="nonreferrer"
            ></a>
            <template v-else>
              <span>
                <font-awesome-icon
                  v-if="name == '@type' && content == 'Person'"
                  icon="fas fa-user"
                  class="text-dark"
                />
                <font-awesome-icon
                  v-if="name == '@type' && content == 'Organization'"
                  icon="fas fa-building"
                  class="text-dark"
                />
                <font-awesome-icon
                  v-if="name == '@type' && content == 'CreativeWork'"
                  icon="fas fa-lightbulb"
                  class="text-dark"
                />
              </span>
              &nbsp;
              <span class="text-dark text-left" v-html="content"></span>
            </template>
          </div>
        </template>
      </div>
    </template>
    <!-- 🌈 Object 🌈 -->
    <template v-if="type == 'object'">
      <div class="d-flex">
        <div class="d-flex justify-content-start align-items-center">
          <span class="mainTextDark">
            <b v-text="readable_name"></b>
            <font-awesome-icon icon="fas fa-chevron-right" class="mr-1" />
          </span>
        </div>
        <div>
          <template v-for="(value, key) in content" :key="key + 'child'">
            <ResourceFieldBox
              :name="key"
              :content="value"
              :isChild="true"
            ></ResourceFieldBox>
          </template>
        </div>
      </div>
    </template>
    <!-- 🌈 Boolean 🌈 -->
    <template v-if="type == 'boolean'">
      <div class="d-flex">
        <div class="d-flex justify-content-start align-items-center">
          <span class="mainTextDark">
            <b v-text="readable_name"></b> :&nbsp;
          </span>
        </div>
        <div>
          <span v-if="content === true"
            ><font-awesome-icon icon="fas fa-check" class="text-success" />
            <span v-text="content"></span
          ></span>
          <span v-else
            ><font-awesome-icon icon="fas fa-times" class="text-danger" />
            <span v-text="content"></span
          ></span>
        </div>
      </div>
    </template>
    <!-- 🌈 Number 🌈 -->
    <template v-if="type == 'number'">
      <div class="d-flex">
        <div class="d-flex justify-content-start align-items-center">
          <span class="mainTextDark">
            <b v-text="readable_name"></b> :&nbsp;
          </span>
        </div>
        <div>
          <span><span v-text="content"></span></span>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "ResourceFieldBox",
  data: function () {
    return {
      type: "",
      expandArray: false,
      perPage: 10,
      page: 1,
      pages: 1,
      startCap: 0,
      endCap: 20,
      groupPages: false,
      pageLimit: 20,
      startCapLimitReached: true,
      endCapLimitReached: false,
      readable_labels: {
        contain_phi: "Contains PHI",
        contain_geo_codes: "Contain Geological Codes",
        url: "URL",
      },
    };
  },
  props: ["name", "content", "isChild"],
  methods: {
    getType(content) {
      var self = this;
      if (content.constructor === Object) {
        self.type = "object";
      } else if (content.constructor === Array) {
        self.type = "array";
      } else if (content.constructor === Boolean) {
        self.type = "boolean";
      } else if (content.constructor === Number) {
        self.type = "number";
      } else if (content.constructor === String) {
        self.type = "string";
      } else {
        self.type = "IDK";
      }
    },
    isUrl(txt) {
      var pattern = new RegExp(
        "^(https?:\\/\\/)?" + // protocol
          "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
          "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
          "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
          "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
          "(\\#[-a-z\\d_]*)?$",
        "i"
      ); // fragment locator
      return pattern.test(txt);
    },
    calculatePages: function () {
      var self = this;
      self.pages = Math.ceil(self.content.length / self.perPage);

      if (self.pages > self.pageLimit) {
        self.groupPages = true;
      }
    },
    previousGroup: function () {
      var self = this;

      if (!self.startCapLimitReached) {
        if (self.startCap - 20 > 0) {
          self.page = self.startCap - 20;
          self.startCap = self.startCap - 20;
          self.endCap = self.endCap - 20;
          self.endCapLimitReached = false;
        } else {
          self.page = 1;
          self.startCap = 0;
          self.endCap = 20;
          self.startCapLimitReached = true;
          self.endCapLimitReached = false;
        }
      }
    },
    nextGroup: function () {
      var self = this;

      if (!self.endCapLimitReached) {
        if (self.endCap + 20 < self.pages) {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.endCap + 20;
          self.startCapLimitReached = false;
        } else {
          self.page = self.startCap + 20;
          self.startCap = self.startCap + 20;
          self.endCap = self.pages;
          self.endCapLimitReached = true;
          self.startCapLimitReached = false;
        }
      }
    },
    prevPage: function () {
      var self = this;
      if (self.page > 1) self.page -= 1;
    },
    nextPage: function () {
      var self = this;
      if (self.page < self.pages) self.page += 1;
    },
  },
  mounted: function () {
    var self = this;
    if (self.content) {
      self.getType(self.content);
    }
    if (self.type == "array") {
      self.calculatePages();
    }
  },
  computed: {
    arrayResults: function () {
      var start = (this.page - 1) * this.perPage,
        end = start + this.perPage;
      return this.content && this.content.slice(start, end);
    },
    readable_name: function () {
      if (
        Object.keys(this.readable_labels).length &&
        Object.hasOwnProperty.call(this.readable_labels, this.name)
      ) {
        return this.readable_labels[this.name];
      } else if (this.name.includes("_")) {
        let parts = this.name.split("_");
        parts = parts.map(
          (item) => item.charAt(0).toUpperCase() + item.slice(1)
        );
        parts = parts.join(" ");
        return parts;
      } else {
        if (/[A-Z]/.test(this.name)) {
          let parts = this.name.split(/(?=[A-Z])/);
          parts = parts.map(
            (item) => item.charAt(0).toUpperCase() + item.slice(1)
          );
          parts = parts.join(" ");
          return parts;
        } else {
          return this.name.charAt(0).toUpperCase() + this.name.slice(1);
        }
      }
    },
  },
};
</script>
