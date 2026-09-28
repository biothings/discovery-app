import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import CollapsibleText from "../app/components/CollapsibleText.vue";

describe("CollapsibleText", () => {
  it("shows expand button and hides collapse button initially", async () => {
    const wrapper = mount(CollapsibleText, {
      props: { text: "Hello world" },
    });

    expect(wrapper.text()).toContain("Click to expand");
    expect(wrapper.text()).not.toContain("Collapse");

    await wrapper.find("a").trigger("click");

    expect(wrapper.text()).toContain("Collapse");
    expect(wrapper.text()).not.toContain("Click to expand");
  });
});
