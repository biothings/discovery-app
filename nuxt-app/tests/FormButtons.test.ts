import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";

vi.mock("clipboard", () => ({ default: vi.fn(function (this: any) {}) }));
vi.mock("simple-notify", () => ({ default: vi.fn() }));

import CopyBtn from "../app/components/global/CopyBtn.vue";
import EditDescription from "../app/components/EditDescription.vue";

const swalMock = { fire: vi.fn(() => Promise.resolve({ value: "new desc" })) };
const storeMock = { commit: vi.fn() };
const stubs = { "font-awesome-icon": true };

// ── CopyBtn ───────────────────────────────────────────────────────────────────

describe("CopyBtn", () => {
  beforeEach(() => vi.clearAllMocks());

  it("renders msg text when msg prop is provided", () => {
    const wrapper = mount(CopyBtn, {
      props: { msg: "Copy link", copy_this: "https://example.com" },
      global: { mocks: { $swal: swalMock }, stubs },
    });
    expect(wrapper.text()).toContain("Copy link");
  });

  it("renders icon slot when msg is not provided", () => {
    const wrapper = mount(CopyBtn, {
      props: { copy_this: "https://example.com" },
      global: { mocks: { $swal: swalMock }, stubs },
    });
    expect(wrapper.find("font-awesome-icon-stub").exists()).toBe(true);
  });

  it("fires swal with success toast on click", async () => {
    const wrapper = mount(CopyBtn, {
      props: { copy_msg: "Copied!", copy_this: "text" },
      global: { mocks: { $swal: swalMock }, stubs },
    });
    await wrapper.find("button").trigger("click");
    expect(swalMock.fire).toHaveBeenCalledWith(
      expect.objectContaining({ icon: "success", title: "Copied!" })
    );
  });

  it("uses default copy_msg when not provided", async () => {
    const wrapper = mount(CopyBtn, {
      props: { copy_this: "text" },
      global: { mocks: { $swal: swalMock }, stubs },
    });
    await wrapper.find("button").trigger("click");
    expect(swalMock.fire).toHaveBeenCalledWith(
      expect.objectContaining({ title: "Link Copied" })
    );
  });
});

// ── EditDescription ───────────────────────────────────────────────────────────

describe("EditDescription", () => {
  beforeEach(() => vi.clearAllMocks());

  it("renders an edit description button", () => {
    const wrapper = mount(EditDescription, {
      props: { propname: "name", val: {} },
      global: { mocks: { $swal: swalMock, $store: storeMock }, stubs },
    });
    expect(wrapper.find("button").text()).toContain("edit description");
  });

  it("calls $swal.fire when the button is clicked", async () => {
    const wrapper = mount(EditDescription, {
      props: { propname: "name", val: {} },
      global: { mocks: { $swal: swalMock, $store: storeMock }, stubs },
    });
    await wrapper.find("button").trigger("click");
    expect(swalMock.fire).toHaveBeenCalledOnce();
  });

  it("passes current description text to swal when val has description", async () => {
    const wrapper = mount(EditDescription, {
      props: { propname: "name", val: { description: "old text" } },
      global: { mocks: { $swal: swalMock, $store: storeMock }, stubs },
    });
    await wrapper.find("button").trigger("click");
    expect(swalMock.fire).toHaveBeenCalledWith(
      expect.objectContaining({ text: expect.stringContaining("old text") })
    );
  });
});
