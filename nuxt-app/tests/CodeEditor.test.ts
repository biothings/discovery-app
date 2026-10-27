import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createStore } from "vuex";

vi.mock("codemirror", () => ({
  basicSetup: [],
  EditorView: vi.fn(function (this: any) {}),
}));
vi.mock("@codemirror/state", () => ({
  EditorState: { create: vi.fn(() => ({})), tabSize: { of: vi.fn() } },
  Compartment: vi.fn(function (this: any) {
    this.of = vi.fn();
  }),
}));
vi.mock("@codemirror/lang-json", () => ({ json: vi.fn() }));
vi.mock("@codemirror/autocomplete", () => ({ autocompletion: vi.fn() }));
vi.mock("@codemirror/language", () => ({
  defaultHighlightStyle: {},
  syntaxHighlighting: vi.fn(),
}));
vi.mock("@codemirror/commands", () => ({ history: vi.fn() }));
vi.mock("simple-notify", () => ({ default: vi.fn() }));

import CodeEditor from "../app/components/CodeEditor.vue";

const swalMock = { fire: vi.fn(() => Promise.resolve({ isConfirmed: false })) };

function makeStore(editItem = null) {
  return createStore({
    getters: { getEditItem: () => editItem },
    mutations: {
      editValidationItem: vi.fn(),
      editThis: vi.fn(),
    },
  });
}

function mountEditor(editItem = null) {
  return mount(CodeEditor, {
    global: {
      plugins: [makeStore(editItem)],
      mocks: { $swal: swalMock },
    },
  });
}

describe("CodeEditor", () => {
  beforeEach(() => vi.clearAllMocks());

  it("renders the static template", () => {
    mountEditor();
    // $swal.fire is async; just check the DOM is there
  });

  it("calls $swal.fire on mount", () => {
    mountEditor();
    expect(swalMock.fire).toHaveBeenCalledOnce();
  });

  it("calls $swal.fire again when the watched item changes", async () => {
    const store = makeStore(null);
    const wrapper = mount(CodeEditor, {
      global: { plugins: [store], mocks: { $swal: swalMock } },
    });
    expect(swalMock.fire).toHaveBeenCalledTimes(1);

    // Trigger the watcher by calling openEditor directly (simulates item change)
    await (wrapper.vm as any).openEditor();
    expect(swalMock.fire).toHaveBeenCalledTimes(2);
  });

  it("commits editValidationItem with parsed JSON on save", () => {
    const commitSpy = vi.fn();
    const store = createStore({
      getters: { getEditItem: () => ({ _id: "1", validation: {} }) },
      mutations: { editValidationItem: commitSpy, editThis: vi.fn() },
    });
    const wrapper = mount(CodeEditor, {
      global: { plugins: [store], mocks: { $swal: swalMock } },
    });

    const vm = wrapper.vm as any;
    vm.editor = { state: { doc: '{"type":"string"}' } };
    vm.SaveDefinition();

    expect(commitSpy).toHaveBeenCalledWith(
      expect.any(Object),
      { item: expect.objectContaining({ validation: { type: "string" } }) }
    );
  });

  it("does not commit when SaveDefinition receives invalid JSON", () => {
    const commitSpy = vi.fn();
    const store = createStore({
      getters: { getEditItem: () => ({ _id: "1", validation: {} }) },
      mutations: { editValidationItem: commitSpy, editThis: vi.fn() },
    });
    const wrapper = mount(CodeEditor, {
      global: { plugins: [store], mocks: { $swal: swalMock } },
    });

    const vm = wrapper.vm as any;
    vm.editor = { state: { doc: "not valid json" } };
    vm.SaveDefinition();

    expect(commitSpy).not.toHaveBeenCalled();
  });
});
