import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import BooleanInput from "../app/components/guide/BooleanInput.vue";

const stubs = { "font-awesome-icon": true };

function makeStore(currentValue: boolean | null = null) {
  return {
    getters: { getValidationValue: (_name: string) => currentValue },
    commit: vi.fn(),
    dispatch: vi.fn(),
  };
}

function mountBoolean(currentValue: boolean | null = null) {
  return mount(BooleanInput, {
    props: { name: "testField", info: { id: 1 } },
    global: { mocks: { $store: makeStore(currentValue) }, stubs },
  });
}

describe("BooleanInput", () => {
  it("renders Yes and No buttons", () => {
    const wrapper = mountBoolean();
    expect(wrapper.text()).toContain("Yes");
    expect(wrapper.text()).toContain("No");
  });

  it("applies text-success to Yes when done is true", () => {
    const wrapper = mountBoolean(true);
    expect(wrapper.findAll(".w-25")[0].classes()).toContain("text-success");
  });

  it("applies text-danger to No when done is false", () => {
    const wrapper = mountBoolean(false);
    expect(wrapper.findAll(".w-25")[1].classes()).toContain("text-danger");
  });

  it("commits addValue and dispatches saveProgress on Yes click", async () => {
    const store = makeStore();
    const wrapper = mount(BooleanInput, {
      props: { name: "myField", info: { id: 1 } },
      global: { mocks: { $store: store }, stubs },
    });
    await wrapper.findAll(".w-25")[0].trigger("click");
    expect(store.commit).toHaveBeenCalledWith("addValue", { name: "myField", info: { id: 1 }, value: true });
    expect(store.dispatch).toHaveBeenCalledWith("saveProgress");
  });

  it("commits addValue with false on No click", async () => {
    const store = makeStore();
    const wrapper = mount(BooleanInput, {
      props: { name: "myField", info: {} },
      global: { mocks: { $store: store }, stubs },
    });
    await wrapper.findAll(".w-25")[1].trigger("click");
    expect(store.commit).toHaveBeenCalledWith("addValue", expect.objectContaining({ value: false }));
  });
});
