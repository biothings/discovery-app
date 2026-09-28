import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createStore } from "vuex";

vi.mock("codemirror", () => ({
  basicSetup: [],
  EditorView: vi.fn(function (this: any) {}),
}));
vi.mock("@codemirror/state", () => ({
  EditorState: { create: vi.fn(() => ({})), tabSize: { of: vi.fn() } },
  Compartment: vi.fn(function (this: any) { this.of = vi.fn(); }),
}));
vi.mock("@codemirror/lang-html", () => ({ html: vi.fn() }));
vi.mock("@codemirror/lang-json", () => ({ json: vi.fn() }));
vi.mock("@codemirror/view", () => ({ keymap: { of: vi.fn() } }));
vi.mock("@codemirror/commands", () => ({ defaultKeymap: [], history: vi.fn() }));
vi.mock("@codemirror/autocomplete", () => ({ autocompletion: vi.fn() }));
vi.mock("@codemirror/language", () => ({
  defaultHighlightStyle: {},
  syntaxHighlighting: vi.fn(),
}));
vi.mock("simple-notify", () => ({ default: vi.fn() }));

import CodeEditorHTML from "../app/components/CodeEditorHTML.vue";
import CodeEditorWithProp from "../app/components/CodeEditorWithProp.vue";
import DefinitionEditor from "../app/components/DefinitionEditor.vue";

const swalMock = { fire: vi.fn(() => Promise.resolve({ isConfirmed: false })) };

// ── CodeEditorHTML ────────────────────────────────────────────────────────────

describe("CodeEditorHTML", () => {
  beforeEach(() => vi.clearAllMocks());

  it("renders the CM-WP container div", () => {
    const store = createStore({ mutations: { setLoading: vi.fn() } });
    const wrapper = mount(CodeEditorHTML, {
      props: { item: "<h1>Hello</h1>" },
      global: { plugins: [store] },
    });
    expect(wrapper.find("#CM-WP").exists()).toBe(true);
  });

  it("commits setLoading true on mount", () => {
    const commitSpy = vi.fn();
    const store = createStore({ mutations: { setLoading: commitSpy } });
    mount(CodeEditorHTML, {
      props: { item: "<p>test</p>" },
      global: { plugins: [store] },
    });
    expect(commitSpy).toHaveBeenCalledWith(expect.any(Object), { value: true });
  });

  it("commits setLoading false after the editor opens", async () => {
    vi.useFakeTimers();
    const commitSpy = vi.fn();
    const store = createStore({ mutations: { setLoading: commitSpy } });
    const wrapper = mount(CodeEditorHTML, {
      props: { item: "<p>test</p>" },
      global: { plugins: [store] },
    });
    vi.runAllTimers();
    await wrapper.vm.$nextTick();
    expect(commitSpy).toHaveBeenCalledWith(expect.any(Object), { value: false });
    vi.useRealTimers();
  });

  it("dispatches a change to the editor when the item prop changes", async () => {
    const store = createStore({ mutations: { setLoading: vi.fn() } });
    const dispatchSpy = vi.fn();
    const wrapper = mount(CodeEditorHTML, {
      props: { item: "<p>original</p>" },
      global: { plugins: [store] },
    });
    (wrapper.vm as any).editor = {
      state: { doc: { length: 10 } },
      dispatch: dispatchSpy,
    };
    await wrapper.setProps({ item: "<p>updated</p>" });
    expect(dispatchSpy).toHaveBeenCalledWith(
      expect.objectContaining({ changes: expect.objectContaining({ insert: expect.stringContaining("updated") }) })
    );
  });
});

// ── CodeEditorWithProp ────────────────────────────────────────────────────────

describe("CodeEditorWithProp", () => {
  beforeEach(() => vi.clearAllMocks());

  it("renders the CM-WP container div", () => {
    const wrapper = mount(CodeEditorWithProp, { props: { item: { validation: {} } } });
    expect(wrapper.find("#CM-WP").exists()).toBe(true);
  });

  it("dispatches a change to the editor when the item prop changes", async () => {
    const dispatchSpy = vi.fn();
    const wrapper = mount(CodeEditorWithProp, { props: { item: { validation: {} } } });
    (wrapper.vm as any).editor = {
      state: { doc: { length: 5 } },
      dispatch: dispatchSpy,
    };
    await wrapper.setProps({ item: { validation: { type: "string" } } });
    expect(dispatchSpy).toHaveBeenCalledWith(
      expect.objectContaining({ changes: expect.any(Object) })
    );
  });

  it("does not dispatch when editor is null and item changes", async () => {
    const wrapper = mount(CodeEditorWithProp, { props: { item: {} } });
    (wrapper.vm as any).editor = null;
    await wrapper.setProps({ item: { type: "number" } });
    // no throw = pass
  });
});

// ── DefinitionEditor ──────────────────────────────────────────────────────────

describe("DefinitionEditor", () => {
  beforeEach(() => vi.clearAllMocks());

  function mountEditor(editItem: any = { _id: "1", validation: {} }) {
    const store = createStore({
      getters: { getEditDefinitionItem: () => editItem },
      mutations: { editDefinitionItem: vi.fn(), editThisDefinition: vi.fn() },
    });
    return { wrapper: mount(DefinitionEditor, { global: { plugins: [store], mocks: { $swal: swalMock } } }), store };
  }

  it("renders the static template", () => {
    const { wrapper } = mountEditor();
    expect(wrapper.text()).toContain("Editing Definition");
  });

  it("calls $swal.fire on mount", () => {
    mountEditor();
    expect(swalMock.fire).toHaveBeenCalledOnce();
  });

  it("commits editDefinitionItem with parsed JSON on SaveDefinition", () => {
    const commitSpy = vi.fn();
    const store = createStore({
      getters: { getEditDefinitionItem: () => ({ _id: "1", validation: {} }) },
      mutations: { editDefinitionItem: commitSpy, editThisDefinition: vi.fn() },
    });
    const wrapper = mount(DefinitionEditor, {
      global: { plugins: [store], mocks: { $swal: swalMock } },
    });
    (wrapper.vm as any).editor = { state: { doc: '{"type":"string"}' } };
    (wrapper.vm as any).SaveDefinition();
    expect(commitSpy).toHaveBeenCalledWith(
      expect.any(Object),
      { item: expect.objectContaining({ validation: { type: "string" } }) }
    );
  });

  it("does not commit when SaveDefinition receives invalid JSON", () => {
    const commitSpy = vi.fn();
    const store = createStore({
      getters: { getEditDefinitionItem: () => ({ _id: "1", validation: {} }) },
      mutations: { editDefinitionItem: commitSpy, editThisDefinition: vi.fn() },
    });
    const wrapper = mount(DefinitionEditor, {
      global: { plugins: [store], mocks: { $swal: swalMock } },
    });
    (wrapper.vm as any).editor = { state: { doc: "not valid json" } };
    (wrapper.vm as any).SaveDefinition();
    expect(commitSpy).not.toHaveBeenCalled();
  });
});
