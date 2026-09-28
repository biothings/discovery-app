import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import SourceBadge from "../app/components/SourceBadge.vue";

async function mountBadge(status: string) {
  const wrapper = mount(SourceBadge, { props: { status } });
  await wrapper.vm.$nextTick();
  return wrapper;
}

describe("SourceBadge", () => {
  it("shows N/A for an unknown status", async () => {
    const wrapper = await mountBadge("999");
    expect(wrapper.text()).toContain("N/A");
  });

  it("shows ok and bg-success for status 200", async () => {
    const wrapper = await mountBadge("200");
    expect(wrapper.text()).toContain("ok");
    expect(wrapper.find(".bg-success").exists()).toBe(true);
  });

  it("shows ok for status 299", async () => {
    const wrapper = await mountBadge("299");
    expect(wrapper.text()).toContain("ok");
    expect(wrapper.find(".bg-success").exists()).toBe(true);
  });

  it("shows not found and bg-danger for status 404", async () => {
    const wrapper = await mountBadge("404");
    expect(wrapper.text()).toContain("not found");
    expect(wrapper.find(".bg-danger").exists()).toBe(true);
  });

  it("shows broken for status 500", async () => {
    const wrapper = await mountBadge("500");
    expect(wrapper.text()).toContain("broken");
  });

  it("shows invalid for status 400", async () => {
    const wrapper = await mountBadge("400");
    expect(wrapper.text()).toContain("invalid");
  });
});
