<template>
  <template v-if="!loggedIn">
    <li class="nav-item">
      <a class="nav-link" :href="'/login?next=' + nextPath">Login</a>
    </li>
  </template>
  <template v-else>
    <li class="nav-item">
      <nuxt-link
        class="nav-link pulse headTip bg-info"
        id="navPhotoLink"
        to="/dashboard/"
        data-tippy-content="Manage your contributions"
      >
        <small class="mr-1">{{ userInfo?.login }}</small>
        <img
          v-if="!userInfo.avatar_url"
          id="navPhoto"
          class="userImage"
          src="@/assets/img/default.png"
          alt="user photo"
        />
        <img
          v-else
          id="navPhoto"
          class="userImage"
          :src="userInfo.avatar_url"
          alt="user photo"
        />
      </nuxt-link>
    </li>
    <li class="nav-item">
      <a class="nav-link" :href="'/logout?next=' + nextPath">Logout</a>
    </li>
  </template>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Login",
  methods: {
    ...mapActions(["checkUser"]),
  },
  computed: {
    ...mapGetters(["loggedIn", "userInfo"]),
    nextPath: function () {
      return this.$route.path;
    },
  },
  mounted: function () {
    this.checkUser();
  },
};
</script>
