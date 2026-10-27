import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createStore } from "vuex";

vi.mock("@/assets/img/validator.svg", () => ({ default: "validator.svg" }));
vi.mock("@/assets/img/generator.svg", () => ({ default: "generator.svg" }));
vi.mock("@/assets/img/resource_reg.svg", () => ({ default: "res_reg.svg" }));
vi.mock("@/assets/img/schema-reg.svg", () => ({ default: "schema_reg.svg" }));

import Nav from "../app/components/Nav.vue";

const NuxtLinkStub = { name: "NuxtLink", props: ["to"], template: "<a :href='to'><slot /></a>" };

function makeStore(portals: any[] = []) {
  return createStore({
    getters: { getPortals: () => portals },
  });
}

const stubs = { NuxtLink: NuxtLinkStub, Login: true };

describe("Nav", () => {
  it("renders the navbar element", () => {
    const wrapper = mount(Nav, { global: { plugins: [makeStore()], stubs } });
    expect(wrapper.find("nav").exists()).toBe(true);
  });

  it("renders primary navigation links", () => {
    const wrapper = mount(Nav, { global: { plugins: [makeStore()], stubs } });
    expect(wrapper.text()).toContain("About");
    expect(wrapper.text()).toContain("Registry");
    expect(wrapper.text()).toContain("Schema Playground");
    expect(wrapper.text()).toContain("Discovery Guide");
  });

  it("collapses the menu by default", () => {
    const wrapper = mount(Nav, { global: { plugins: [makeStore()], stubs } });
    expect(wrapper.find(".navbar-collapse").classes()).toContain("collapse");
  });

  it("expands the menu when the toggle button is clicked", async () => {
    const wrapper = mount(Nav, { global: { plugins: [makeStore()], stubs } });
    await wrapper.find(".navbar-toggler").trigger("click");
    expect(wrapper.find(".navbar-collapse").classes()).not.toContain("collapse");
  });

  it("collapses again on second toggle click", async () => {
    const wrapper = mount(Nav, { global: { plugins: [makeStore()], stubs } });
    await wrapper.find(".navbar-toggler").trigger("click");
    await wrapper.find(".navbar-toggler").trigger("click");
    expect(wrapper.find(".navbar-collapse").classes()).toContain("collapse");
  });

  it("renders a dropdown link for each portal from the store", () => {
    const portals = [
      { keyName: "niaid", shortName: "NIAID", name: "NIAID", portalicon: "" },
      { keyName: "ncats", shortName: "NCATS", name: "NCATS", portalicon: "" },
    ];
    const wrapper = mount(Nav, { global: { plugins: [makeStore(portals)], stubs } });
    expect(wrapper.text()).toContain("NIAID");
    expect(wrapper.text()).toContain("NCATS");
  });

  it("renders the Login component", () => {
    const wrapper = mount(Nav, { global: { plugins: [makeStore()], stubs } });
    expect(wrapper.find("login-stub").exists()).toBe(true);
  });
});
