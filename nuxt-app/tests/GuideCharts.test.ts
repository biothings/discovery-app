import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";

const { ChartConstructor } = vi.hoisted(() => {
  const ChartConstructor = vi.fn(function (this: any) {
    this.destroy = vi.fn();
    this.update = vi.fn();
    this.data = { datasets: [] };
  }) as any;
  ChartConstructor.register = vi.fn();
  return { ChartConstructor };
});

vi.mock("chart.js", () => ({ Chart: ChartConstructor, registerables: [] }));

import Chart from "../app/components/guide/Chart.vue";
import Category from "../app/components/guide/Category.vue";

const stubs = { "font-awesome-icon": true, Chart: true };

// ── Chart ─────────────────────────────────────────────────────────────────────

describe("Chart", () => {
  const storeMock = { commit: vi.fn() };
  const baseTotals = { completed: 3, todo: 2 };

  beforeEach(() => vi.clearAllMocks());

  function mountChart(name = "Optional", totals = baseTotals) {
    return mount(Chart, {
      props: { name, totals, unique: "test", maincategory: "General" },
      global: { mocks: { $store: storeMock }, stubs: { "font-awesome-icon": true } },
    });
  }

  it("renders a canvas element", () => {
    const wrapper = mountChart();
    expect(wrapper.find("canvas").exists()).toBe(true);
  });

  it("renders the name text", () => {
    const wrapper = mountChart("Required");
    expect(wrapper.text()).toContain("Required");
  });

  it("applies text-danger to the Required category", () => {
    const wrapper = mountChart("Required");
    expect(wrapper.find("small").classes()).toContain("text-danger");
  });

  it("applies text-muted to non-Required categories", () => {
    const wrapper = mountChart("Recommended");
    expect(wrapper.find("small").classes()).toContain("text-muted");
  });

  it("calls Chart.register and creates a Chart instance on mount", () => {
    mountChart();
    expect(ChartConstructor.register).toHaveBeenCalled();
    expect(ChartConstructor).toHaveBeenCalledOnce();
  });

  it("destroys and re-creates the chart when totals change", async () => {
    const wrapper = mountChart();
    const instance = (wrapper.vm as any).myChart;
    await wrapper.setProps({ totals: { completed: 5, todo: 0 } });
    expect(instance.destroy).toHaveBeenCalledOnce();
    expect(ChartConstructor).toHaveBeenCalledTimes(2);
  });

  it("commits highlight when shouldHighlight becomes true", async () => {
    const wrapper = mountChart("Required");
    (wrapper.vm as any).shouldHighlight = true;
    await wrapper.vm.$nextTick();
    expect(storeMock.commit).toHaveBeenCalledWith("highlight", {
      category: "General",
      subcategory: "Required",
    });
  });

  it("commits unhighlight when shouldHighlight becomes false", async () => {
    const wrapper = mountChart();
    const vm = wrapper.vm as any;
    vm.shouldHighlight = true;
    await wrapper.vm.$nextTick();
    storeMock.commit.mockClear();
    vm.shouldHighlight = false;
    await wrapper.vm.$nextTick();
    expect(storeMock.commit).toHaveBeenCalledWith("unhighlight");
  });
});

// ── Category ──────────────────────────────────────────────────────────────────

describe("Category", () => {
  const swalMock = { fire: vi.fn(() => Promise.resolve({ value: false })) };

  beforeEach(() => vi.clearAllMocks());

  function makeStore(startingPointName = "Other") {
    return {
      getters: { startingPoint: { name: startingPointName } },
      commit: vi.fn(),
    };
  }

  function mountCategory(cat = "Biology", startingPointName = "Other") {
    return mount(Category, {
      props: { cat, subcats: null, totals: {} },
      global: { mocks: { $store: makeStore(startingPointName), $swal: swalMock }, stubs },
    });
  }

  it("renders 'cat Progress' text", () => {
    const wrapper = mountCategory("Biology");
    expect(wrapper.text()).toContain("Biology Progress");
  });

  it("shows the Google icon when cat is Google", () => {
    const wrapper = mountCategory("Google");
    const icons = wrapper.findAll("font-awesome-icon-stub");
    const googleIcon = icons.find((i) => i.attributes("icon")?.includes("fa-google"));
    expect(googleIcon?.exists()).toBe(true);
  });

  it("hides the Google icon for non-Google categories", () => {
    const wrapper = mountCategory("Biology");
    const icons = wrapper.findAll("font-awesome-icon-stub");
    const googleIcon = icons.find((i) => i.attributes("icon")?.includes("fa-google"));
    expect(googleIcon).toBeUndefined();
  });

  it("shows the remove button when cat is not the starting point", () => {
    const wrapper = mountCategory("Biology", "Other");
    expect(wrapper.find(".text-danger").exists()).toBe(true);
  });

  it("hides the remove button when cat is the starting point", async () => {
    const wrapper = mountCategory("Biology", "Biology");
    await wrapper.vm.$nextTick();
    expect(wrapper.find(".text-danger").exists()).toBe(false);
  });

  it("calls $swal.fire when the remove button is clicked", async () => {
    const wrapper = mountCategory("Biology", "Other");
    await wrapper.find(".text-danger").trigger("click");
    expect(swalMock.fire).toHaveBeenCalledOnce();
  });

  it("renders a Chart stub for each subcat", () => {
    const subcats = { Required: { completed: 2, todo: 1 }, Optional: { completed: 0, todo: 3 } };
    const wrapper = mount(Category, {
      props: { cat: "General", subcats, totals: {} },
      global: { mocks: { $store: makeStore(), $swal: swalMock }, stubs },
    });
    expect(wrapper.findAll("chart-stub")).toHaveLength(2);
  });
});
