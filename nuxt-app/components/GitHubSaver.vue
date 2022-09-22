<template>
  <div class="bg-light" style="position: relative">
    <h4 class="logoText text-center m-2">
      <font-awesome-icon icon="fab fa-github-alt" /> Save your work to GitHub
    </h4>
    <p class="text-dark w-50 m-auto mb-2">
      <small
        ><font-awesome-icon
          icon="fas fa-exclamation-circle"
          class="text-info"
        />
        By continuing with this process you are giving us permission to access
        your GitHub account to create/edit <b>public</b> repos/files. This might
        include public organizations and repos that you are part of. If you DO
        NOT accept this please close this window and choose the
        <b>Download</b> option to save manually.</small
      >
    </p>
    <div v-if="!accepts">
      <h3 class="pointer text-center text-success m-4" @click="accepts = true">
        Continue
      </h3>
    </div>
    <div v-else class="row m-0 slit-in-vertical">
      <div
        class="text-center col-sm-12 m-auto"
        v-if="loading"
        style="position: absolute; top: 45%; z-index: 2000"
      >
        <font-awesome-icon
          icon="fab fa-github-alt"
          class="fa-spin fa-5x p-2 text-info"
        />
      </div>
      <div
        class="col-sm-12 col-md-4 border p-1"
        :class="[repo_selected ? 'alert-success' : 'alert-light']"
      >
        <h6 class="logoText">1. Choose a repository</h6>
        <small class="text-muted"
          >Choose an existing repository to save your work to.</small
        >
        <button
          type="button"
          class="btn themeButton text-light btn-sm"
          @click="getRepos()"
        >
          <font-awesome-icon icon="fab fa-github-alt" /> Get Repos
        </button>
        <template v-if="repos.length">
          <h6 class="text-muted">1. Choose one (All available):</h6>
          <select class="custom-select w-100" v-model="repo_selected">
            <option selected>Choose...</option>
            <template v-for="repo in repos">
              <option :value="repo" v-text="repo"></option>
            </template>
          </select>
          <h6 class="text-muted mt-4">Search by name:</h6>
          <input
            class="form-control form-control-sm"
            list="repo_options"
            name="browser"
            id="browser"
            v-model="filter"
          />
          <datalist id="repo_options">
            <template v-for="repo in repos">
              <option :value="repo"></option>
            </template>
          </datalist>
        </template>
        <template v-else>
          <p>
            <small class="text-muted">No results yet</small>
          </p>
        </template>
      </div>
      <div
        class="col-sm-12 col-md-4 border p-1"
        :class="[name_selected ? 'alert-success' : 'alert-light']"
      >
        <h6 class="logoText">2. Choose file</h6>
        <small class="text-muted">Create or update an existing file.</small>
        <div v-if="repo_selected">
          <small class="text-info d-block" v-if="!existing_file"
            >Do not include the file extension. It will be
            <code>.jsonld</code>.</small
          >
          <div class="alert alert-dark text-center">
            <template v-if="repo_selected && existing_file">
              <h6 class="text-muted">
                <font-awesome-icon icon="fas fa-sync-alt text-success" /> Update
                File
              </h6>
            </template>
            <template v-if="repo_selected && !existing_file">
              <h6 class="text-muted">
                <font-awesome-icon icon="fas fa-file-medical text-success" />
                Create File
              </h6>
            </template>
            <input
              @change="name_selected = ''"
              v-model="existing_file"
              class="form-control text-light tip m-auto slider"
              type="checkbox"
              checked
            />
          </div>
        </div>
        <template v-if="repo_selected && !existing_file">
          <small class="text-info bold"
            >A. New File: Name your file (without extension)</small
          >
          <div class="form-group row">
            <div class="col-sm-10">
              <input
                :disabled="!repo_selected"
                :class="{ disabled: !repo_selected }"
                v-model="name_selected"
                type="text"
                class="form-control form-control-sm"
                placeholder="enter your file name here"
              />
            </div>
          </div>
        </template>
        <template v-if="repo_selected && existing_file">
          <small class="text-info bold">A. Update File: Select one</small>
          <select
            :disabled="!repo_selected"
            class="custom-select w-100"
            v-model="name_selected"
          >
            <option selected>Choose...</option>
            <template v-for="file in files_available">
              <option :value="file" v-text="file"></option>
            </template>
          </select>
        </template>
        <template v-if="repo_selected">
          <small class="text-muted d-block"
            ><span class="text-info">B. (Optional)</span> Write a comment about
            this addition.</small
          >
          <div class="form-group row">
            <div class="col-sm-12">
              <textarea
                rows="4"
                :disabled="!repo_selected"
                :class="{ disabled: !repo_selected }"
                v-model="comment"
                type="text"
                class="form-control form-control-sm w-100"
                placeholder="write a comment here"
              >
              </textarea>
            </div>
          </div>
        </template>
        <div>
          <pre>
<code v-text="code" style="font-size:.5em; max-height:300px;"></code>
</pre>
        </div>
      </div>
      <div
        class="col-sm-12 col-md-4 border p-1"
        :class="[repo_saved ? 'alert-success' : 'alert-light']"
      >
        <h6 class="logoText">3. Save to GitHub</h6>
        <small v-if="!existing_file" class="text-muted"
          >A new file will be saved to this repository.</small
        >
        <small v-else class="text-muted"
          >The file chosen will be updated with your work.</small
        >
        <div class="text-muted text-center">
          <template v-if="name_selected && repo_selected">
            <h5 class="my-3">
              <span
                class="text-info"
                v-text="existing_file ? 'Update' : 'Create'"
              ></span
              >: <b v-text="repo_selected"></b>/<code
                v-text="name_selected"
              ></code
              >?
            </h5>
            <button
              type="button"
              class="btn btn-success text-light btn-sm"
              @click="saveWork()"
            >
              <font-awesome-icon icon="fab fa-github-alt" />
              <span v-text="existing_file ? 'Update' : 'Save'"></span>
            </button>
          </template>
          <template v-else>
            <small class="d-block"
              ><font-awesome-icon icon="fab fa-github-alt fa-2x"
            /></small>
          </template>
        </div>
        <div v-if="repo_saved && repo_link" class="text-center mt-3">
          <h6>
            <font-awesome-icon icon="fa fa-check" /> Work
            <span v-text="existing_file ? 'Updated' : 'Saved'"></span>!
          </h6>
          <small>
            <a :href="repo_link" target="_blank" rel="nonreferrer"
              ><b v-text="repo_link"></b>
              <font-awesome-icon icon="fas fa-external-link-alt"
            /></a>
          </small>
        </div>
      </div>
      <div
        class="col-sm-12 grad border border-success p-2 text-center"
        v-if="repo_link"
      >
        <p class="text-light mt-2 text-center">
          <template v-if="readyLink">
            <img
              src="@/assets/img/visualize-01.png"
              width="100px"
              alt="Visualize"
            />
            <h5>Visualize and register your work</h5>
            <div>
              <code v-text="readyLink"></code>
            </div>
            <button
              type="button"
              class="btn btn-lg btn-success m-3"
              @click="copyToInput(readyLink)"
            >
              Visualize Schema
            </button>
            <div v-if="loading">
              <h3 class="text-light">
                <font-awesome-icon icon="fas fa-cog fa-spin" /> Please Wait...
              </h3>
            </div>
          </template>
        </p>
      </div>
      <div class="col-sm-12 alert-secondary border p-1 text-center">
        <small
          >New changes or want to reset?
          <b @click="resetFields()" class="pointer text-danger"
            >click here</b
          ></small
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "GitHubSaver",
  data: function () {
    return {
      repoName: "",
      repos: [],
      repo_selected: "",
      filter: "",
      name_selected: "",
      comment: "",
      accepts: false,
      repo_saved: false,
      repo_link: "",
      existing_file: true,
      files_available: [],
      file_selected: "",
      slug: "",
      number: 0,
      input: "",
      data: [],
      apiUrl: ''
    };
  },
  methods: {
    resetFields() {
      let self = this;
      this.$store.commit("setLoading", { state: true });
      setTimeout(function () {
        self.repo_selected = "";
        self.name_selected = "";
        self.comment = "";
        self.repo_saved = false;
        self.repo_link = "";
        self.files_available = [];
        self.file_selected = "";
      }, 1000);
      this.$store.commit("setLoading", { state: false });
    },
    checkRepo() {
      let self = this;
      this.$store.commit("setLoading", { state: true });
      axios
        .get(self.apiUrl + "/api/gh/" + self.repoName)
        .then((res) => {
          this.$store.commit("setLoading", { state: false });
          if (res.data.success) {
            return "https://github.com/" + res.data.msg;
          } else {
            self.$swal.fire({
              type: "error",
              title: "Unsuccesful...",
              text: JSON.stringify(res.data, null, 2),
            });
          }
        })
        .catch((err) => {
          this.$store.commit("setLoading", { state: false });
          self.$swal.fire({
            type: "error",
            title: "Oops...Something went really wrong!",
            text: err,
          });
          throw err;
        });
    },
    getRepos() {
      var self = this;
      this.$store.commit("setLoading", { state: true });
      axios
        .get(self.apiUrl + "/api/gh")
        .then((res) => {
          this.$store.commit("setLoading", { state: false });
          if (res.data.success) {
            self.repos = res.data.msg;
          } else {
            self.$swal.fire({
              type: "error",
              title: "Problems getting your repos, try again later.",
              text: JSON.stringify(res.data, null, 2),
            });
          }
        })
        .catch((err) => {
          this.$store.commit("setLoading", { state: false });
          self.$swal.fire({
            type: "error",
            title: "Oops!",
            text: err?.response?.data?.error,
          });
          throw err;
        });
    },
    updateFile() {
      let self = this;

      data = {
        name: self.repo_selected,
        file: self.name_selected,
        data: this.$store.getters.getFinalSchema,
        existing: true,
        comment: self.comment,
        existing_file: true,
      };

      let config = {
        headers: {
          "content-type": "application/json",
        },
      };

      this.$store.commit("setLoading", { state: true });

      return axios
        .put(self.apiUrl + "/api/gh", data, config)
        .then((res) => {
          this.$store.commit("setLoading", { state: false });
          if (res.data.success) {
            self.repo_saved = true;
            self.repo_link = "https://github.com/" + res.data.msg;
          } else {
            self.repo_saved = false;
            self.$swal.fire({
              type: "error",
              title: "Problems updating your file, please try again later.",
              text: JSON.stringify(res.data, null, 2),
            });
          }
        })
        .catch((err) => {
          this.$store.commit("setLoading", { state: false });
          self.repo_saved = false;
          self.$swal.fire({
            type: "error",
            title: "Oops...Something went wrong!",
            text: err,
          });
          throw err;
        });
    },
    saveWork() {
      let self = this;

      if (self.existing_file === true) {
        console.log("updating file");
        self.updateFile();
      } else {
        data = {
          name: self.repo_selected,
          file: self.name_selected + ".jsonld",
          data: this.$store.getters.getFinalSchema,
          existing: true,
          comment: self.comment,
        };

        let config = {
          headers: {
            "content-type": "application/json",
          },
        };

        this.$store.commit("setLoading", { state: true });

        return axios
          .post(self.apiUrl + "/api/gh", data, config)
          .then((res) => {
            this.$store.commit("setLoading", { state: false });
            if (res.data.success) {
              self.repo_saved = true;
              self.repo_link = "https://github.com/" + res.data.msg;
            } else {
              self.repo_saved = false;
              self.$swal.fire({
                type: "error",
                title: "Problems saving to GitHub, please try again later.",
                text: JSON.stringify(res.data, null, 2),
              });
            }
          })
          .catch((err) => {
            this.$store.commit("setLoading", { state: false });
            self.repo_saved = false;
            self.$swal.fire({
              type: "error",
              title: "Oops...Something went wrong!",
              text: err,
            });
            throw err;
          });
      }
    },
    assignTempName(hits) {
      let self = this;
      if (hits.length) {
        if (hits[0].hasOwnProperty("namespace")) {
          self.slug = hits[0]["namespace"];
        } else if (hits[0].hasOwnProperty("name")) {
          self.slug = hits[0]["name"].split(":")[0];
        } else {
          self.slug = "temp";
        }
        var modal = document.getElementById("ghOptions");
        modal.style.display = "none";
        self.makeURLandRedirect();
      } else {
        self.$swal("Error parsing schema", "No classes found", "error");
      }
    },
    sendRequest(url, backupURL = "") {
      let self = this;
      this.$store.commit("setLoading", { state: true });
      axios
        .get(self.apiUrl + "/api/view?url=" + url)
        .then((res) => {
          console.log(res.data);
          self.data = res.data;
          this.$store.commit("setLoading", { state: false });
          localStorage.setItem(
            "user-schema-classes",
            JSON.stringify(self.data)
          );
          localStorage.setItem("user-schema-url", url);
          self.assignTempName(res.data.hits);
        })
        .catch((err) => {
          this.$store.commit("setLoading", { state: false });
          if (backupURL) {
            self.sendRequest(backupURL);
          } else {
            // console.log('err',err.response.data)
            let culprit = "<h6>" + err.response.data.error + "</h6>";
            if (err.response.data && err.response.data.path) {
              culprit +=
                "<h5>Culprit: <b class='text-danger'>" +
                err.response.data.path +
                "</b></h5>";
            }
            if (err.response.data.parent && err.response.data.parent.path) {
              if (true) {
                culprit +=
                  "<h5>Under: <b class='text-danger'>" +
                  err.response.data.parent.path +
                  "</b></h5>";
              }
              if (err.response.data.parent && err.response.data.parent.reason) {
                culprit +=
                  "<div class='alert alert-warning'><small>" +
                  err.response.data.parent.reason +
                  "</small></div>";
              }
            }
            if (
              err.response.data.hasOwnProperty("validator_value") &&
              err.response.data.validator_value.length
            ) {
              culprit +=
                "<div class='alert alert-info'><small> Hint: " +
                err.response.data.validator_value +
                "</small></div>";
            }
            self.$swal.fire({
              type: "error",
              position: "top center",
              title: "Failed because: ",
              html: culprit,
            });
            throw err;
          }
        });
    },
    makeURLandRedirect() {
      let self = this;
      this.setLastViewed();

      self.$swal
        .fire({
          title: "Visualization Ready",
          text: "Do you want to see it now?",
          icon: "success",
          showCancelButton: true,
          confirmButtonText: "Let's see it!",
        })
        .then((result) => {
          if (result.isConfirmed) {
            window.open("./view/" + this.slug + this.number + "/", "_blank");
          }
        });
    },
    setLastViewed() {
      this.number = Math.floor(Math.random() * 90000) + 10000;
      let temp = this.slug + this.number;
      sessionStorage.clear();
      sessionStorage.setItem(temp, localStorage.getItem("user-schema-classes"));
      sessionStorage.setItem(
        temp + "-url",
        localStorage.getItem("user-schema-url")
      );
    },
    copyToInput(value) {
      let self = this;
      if (value.includes("blob") || value.includes("github.com")) {
        let master_url = value
          .replace("blob/", "")
          .replace("github.com", "raw.githubusercontent.com")
          .replace("www.github.com", "raw.githubusercontent.com");

        self.input = master_url;

        let main_url = master.replace("/master/", "/main/");

        self.sendRequest(master_url, main_url);

        // self.$swal({
        //   title: 'Link Converted',
        //   imageAlt: 'Warning',
        //   animation:false,
        //   customClass:'scale-in-center',
        //   html:
        //     '<p>We will need the direct link tot he raw data and have changed your url.</p> ' +
        //     '<p><a target="_blank" href="'+suggestedURL+'">'+suggestedURL+'</a></p>' +
        //     '<p>Proceed with this link?</p>',
        //   showCancelButton: true,
        //   confirmButtonColor:"{{color_main}}",
        //   cancelButtonColor:"{{color_sec}}",
        //   confirmButtonText: 'Yes, use this link!'
        // }).then((result) => {
        //   if (result.value) {
        //     self.input = suggestedURL
        //   }else{
        //     self.input = value
        //   }
        // });
      }
    },
  },
  computed: {
    ...mapGetters({
      loading: "loading",
      code: "getFinalSchema",
    }),
    readyLink: function () {
      let self = this;
      if (self.existing_file) {
        return self.repo_link + "/blob/main/" + self.name_selected;
      } else {
        return self.repo_link + "/blob/main/" + self.name_selected + ".jsonld";
      }
    },
  },
  watch: {
    repo_selected: function (name, oldname) {
      let self = this;
      if (self.repos.length && self.repos.includes(name)) {
        this.$store.commit("setLoading", { state: true });
        return axios
          .get(self.apiUrl + "/api/gh/" + name)
          .then((res) => {
            this.$store.commit("setLoading", { state: false });
            if (res.data.success) {
              self.files_available = res.data.msg;
            } else {
              self.$swal.fire({
                type: "error",
                title: "Problems saving to GitHub, please try again later.",
                text: JSON.stringify(res.data, null, 2),
              });
            }
          })
          .catch((err) => {
            this.$store.commit("setLoading", { state: false });
            self.$swal.fire({
              icon: "error",
              title: "Oops...Something went wrong!",
              text: err,
            });
            throw err;
          });
      }
    },
    filter: function (f) {
      let self = this;
      if (self.repos.length && self.repos.includes(f)) {
        self.repo_selected = f;
      }
    },
  },
  mounted: function(){
    const runtimeConfig = useRuntimeConfig()
    this.apiUrl = runtimeConfig.public.apiUrl;
  }
};
</script>
