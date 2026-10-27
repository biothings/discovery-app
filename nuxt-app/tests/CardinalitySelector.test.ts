import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import CardinalitySelector from "../app/components/CardinalitySelector.vue";

const commitSpy = vi.fn();
const storeMock = { commit: commitSpy };

function mountSelector(val = {}, propname = "myProp") {
  return mount(CardinalitySelector, {
    props: { propname, val },
    global: { mocks: { $store: storeMock } },
  });
}

describe("CardinalitySelector", () => {
  it("renders the label and both options", () => {
    const wrapper = mountSelector();
    expect(wrapper.text()).toContain("Choose cardinality:");
    const options = wrapper.findAll("option");
    expect(options).toHaveLength(2);
    expect(options[0].text()).toBe("One");
    expect(options[1].text()).toBe("Many");
  });

  it("starts with no selection when val has no owl:cardinality", () => {
    const wrapper = mountSelector({});
    expect((wrapper.vm as any).selection).toBe("");
  });

  it("initializes selection from val owl:cardinality on mount", () => {
    const wrapper = mountSelector({ "owl:cardinality": "many" });
    expect((wrapper.vm as any).selection).toBe("many");
  });

  it("applies text-primary class when selection is many", async () => {
    const wrapper = mountSelector({ "owl:cardinality": "many" });
    await wrapper.vm.$nextTick();
    expect(wrapper.find("select").classes()).toContain("text-primary");
  });

  it("applies text-info class when selection is one", async () => {
    const wrapper = mountSelector({ "owl:cardinality": "one" });
    await wrapper.vm.$nextTick();
    expect(wrapper.find("select").classes()).toContain("text-info");
  });

  it("commits setValidation with correct payload on change", async () => {
    commitSpy.mockClear();
    const wrapper = mountSelector({}, "testProp");
    const select = wrapper.find("select");
    await select.setValue("many");
    expect(commitSpy).toHaveBeenCalledWith("setValidation", {
      validation: { validation: { "owl:cardinality": "many" } },
      name: "testProp",
    });
  });
});
