import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import InputPreview from "../app/components/guide/InputPreview.vue";

const stubs = { "font-awesome-icon": true };
const removeItem = vi.fn();

describe("InputPreview", () => {
  it("renders a badge for an object input using item.name", () => {
    const wrapper = mount(InputPreview, {
      props: { userInput: { name: "Alice" }, removeItem, name: "author" },
      global: { stubs },
    });
    expect(wrapper.text()).toContain("Alice");
  });

  it("shows prop name when object has no .name", () => {
    const wrapper = mount(InputPreview, {
      props: { userInput: { id: 1 }, removeItem, name: "author" },
      global: { stubs },
    });
    expect(wrapper.text()).toContain("author");
  });

  it("renders one badge per item for an array input", () => {
    const wrapper = mount(InputPreview, {
      props: { userInput: ["x", "y", "z"], removeItem, name: "tags" },
      global: { stubs },
    });
    expect(wrapper.findAll(".kwbadge")).toHaveLength(3);
  });

  it("shows the string value for string array items", () => {
    const wrapper = mount(InputPreview, {
      props: { userInput: ["alpha", "beta"], removeItem, name: "tags" },
      global: { stubs },
    });
    expect(wrapper.text()).toContain("alpha");
    expect(wrapper.text()).toContain("beta");
  });

  it("shows person.name for object array items", () => {
    const wrapper = mount(InputPreview, {
      props: { userInput: [{ name: "Bob" }, { name: "Carol" }], removeItem, name: "authors" },
      global: { stubs },
    });
    expect(wrapper.text()).toContain("Bob");
    expect(wrapper.text()).toContain("Carol");
  });
});
