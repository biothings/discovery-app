import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createStore } from "vuex";
import Login from "../app/components/Login.vue";

const NuxtLinkStub = { name: "NuxtLink", props: ["to"], template: "<a :href='to'><slot /></a>" };

function makeStore({ loggedIn = false, userInfo = {} as any } = {}) {
  return createStore({
    getters: {
      loggedIn: () => loggedIn,
      userInfo: () => userInfo,
    },
    actions: { checkUser: vi.fn() },
  });
}

function mountLogin(opts: Parameters<typeof makeStore>[0] = {}, path = "/") {
  return mount(Login, {
    global: {
      plugins: [makeStore(opts)],
      mocks: { $route: { path } },
      stubs: { NuxtLink: NuxtLinkStub },
    },
  });
}

describe("Login", () => {
  it("shows login link when not logged in", () => {
    const wrapper = mountLogin({ loggedIn: false });
    expect(wrapper.find("a").text()).toContain("Login");
  });

  it("includes the current path in the login href", () => {
    const wrapper = mountLogin({ loggedIn: false }, "/explore");
    expect(wrapper.find("a").attributes("href")).toContain("/explore");
  });

  it("shows Hello with first name when logged in", () => {
    const wrapper = mountLogin({ loggedIn: true, userInfo: { name: "Jane Doe", avatar_url: "" } });
    expect(wrapper.text()).toContain("Hello, Jane");
    expect(wrapper.text()).toContain("Logout");
  });

  it("shows github login when logged in without a name", () => {
    const wrapper = mountLogin({ loggedIn: true, userInfo: { login: "jdoe", avatar_url: "" } });
    expect(wrapper.text()).toContain("jdoe");
  });

  it("renders default avatar img when avatar_url is empty", () => {
    const wrapper = mountLogin({ loggedIn: true, userInfo: { name: "A", avatar_url: "" } });
    expect(wrapper.find("img").attributes("src")).toContain("default.png");
  });

  it("renders avatar from avatar_url when present", () => {
    const wrapper = mountLogin({
      loggedIn: true,
      userInfo: { name: "A", avatar_url: "https://example.com/photo.jpg" },
    });
    expect(wrapper.find("img").attributes("src")).toBe("https://example.com/photo.jpg");
  });
});
