import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";

vi.mock("@/assets/img/cubeplus.svg", () => ({ default: "cubeplus.svg" }));

import ValidationDropzone from "../app/components/ValidationDropzone.vue";

const stubs = {
  "font-awesome-icon": true,
  EditDescription: true,
  CardinalitySelector: true,
};

function makeStore({ validationOptions = [] as any[], addCardinality = false } = {}) {
  return {
    getters: {
      getValidationOptions: validationOptions,
      addCardinality: addCardinality,
    },
    commit: vi.fn(),
  };
}

describe("ValidationDropzone", () => {
  it("renders the propname label", () => {
    const wrapper = mount(ValidationDropzone, {
      props: { propname: "myProp", val: {} },
      global: { mocks: { $store: makeStore() }, stubs },
    });
    expect(wrapper.text()).toContain("myProp");
  });

  it("renders EditDescription", () => {
    const wrapper = mount(ValidationDropzone, {
      props: { propname: "myProp", val: {} },
      global: { mocks: { $store: makeStore() }, stubs },
    });
    expect(wrapper.find("edit-description-stub").exists()).toBe(true);
  });

  it("shows CardinalitySelector when addCardinality is true", () => {
    const wrapper = mount(ValidationDropzone, {
      props: { propname: "myProp", val: {} },
      global: { mocks: { $store: makeStore({ addCardinality: true }) }, stubs },
    });
    expect(wrapper.find("cardinality-selector-stub").exists()).toBe(true);
  });

  it("hides CardinalitySelector when addCardinality is false", () => {
    const wrapper = mount(ValidationDropzone, {
      props: { propname: "myProp", val: {} },
      global: { mocks: { $store: makeStore({ addCardinality: false }) }, stubs },
    });
    expect(wrapper.find("cardinality-selector-stub").exists()).toBe(false);
  });

  it("displays val as formatted JSON in the pre element", () => {
    const val = { type: "string", required: true };
    const wrapper = mount(ValidationDropzone, {
      props: { propname: "myProp", val },
      global: { mocks: { $store: makeStore() }, stubs },
    });
    expect(wrapper.find("pre").text()).toContain('"type": "string"');
  });

  it("commits resetValidationFor with propname when reset icon is clicked", async () => {
    const store = makeStore();
    const wrapper = mount(ValidationDropzone, {
      props: { propname: "fieldName", val: {} },
      global: { mocks: { $store: store }, stubs },
    });
    await wrapper.find(".text-warning").trigger("click");
    expect(store.commit).toHaveBeenCalledWith("resetValidationFor", { name: "fieldName" });
  });
});
