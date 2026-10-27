import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import PageTitle from "../app/components/PageTitle.vue";
import Enumeration from "../app/components/Enumeration.vue";
import CompatibilityResult from "../app/components/CompatibilityResult.vue";
import CompareItemDetails from "../app/components/CompareItemDetails.vue";
import Footer from "../app/components/Footer.vue";
import MarkdownParser from "../app/components/MarkdownParser.vue";
import ToolCard from "../app/components/ToolCard.vue";
import ObjectBox from "../app/components/ObjectBox.vue";
import MoreButton from "../app/components/MoreButton.vue";

// Must go through stubs (not global.components) to override Nuxt's globally registered NuxtLink
const NuxtLinkStub = { name: "NuxtLink", props: ["to"], template: "<a><slot /></a>" };

const stubs = {
  "font-awesome-icon": true,
  PropertyBox: true,
  NuxtLink: NuxtLinkStub,
};

// ── PageTitle ─────────────────────────────────────────────────────────────────

describe("PageTitle", () => {
  it("renders the title in an h1", () => {
    const wrapper = mount(PageTitle, { props: { title: "Hello" } });
    expect(wrapper.find("h1").text()).toBe("Hello");
  });

  it("renders subtitle in h5 when provided", () => {
    const wrapper = mount(PageTitle, { props: { title: "T", subtitle: "Sub" } });
    expect(wrapper.find("h5").text()).toBe("Sub");
  });

  it("omits h5 when subtitle is not provided", () => {
    const wrapper = mount(PageTitle, { props: { title: "T" } });
    expect(wrapper.find("h5").exists()).toBe(false);
  });
});

// ── Enumeration ───────────────────────────────────────────────────────────────

describe("Enumeration", () => {
  it("renders one option per item", () => {
    const wrapper = mount(Enumeration, { props: { enumeration: ["a", "b", "c"] } });
    const options = wrapper.findAll("option");
    expect(options).toHaveLength(3);
    expect(options.map((o) => o.text())).toEqual(["a", "b", "c"]);
  });

  it("renders an empty select for an empty array", () => {
    const wrapper = mount(Enumeration, { props: { enumeration: [] } });
    expect(wrapper.findAll("option")).toHaveLength(0);
  });
});

// ── CompatibilityResult ───────────────────────────────────────────────────────

describe("CompatibilityResult", () => {
  const rOk = { schemaorgCompliant: true, name: "MySchema", url: "https://example.com" };
  const rFail = { schemaorgCompliant: false, name: "BadSchema", url: "https://example.com" };

  it("shows compliant text and bg-success when compliant", () => {
    const wrapper = mount(CompatibilityResult, { props: { r: rOk }, global: { stubs } });
    expect(wrapper.text()).toContain("Schema.org compliant");
    expect(wrapper.find(".bg-success").exists()).toBe(true);
  });

  it("shows non-compliant text and bg-danger when not compliant", () => {
    const wrapper = mount(CompatibilityResult, { props: { r: rFail }, global: { stubs } });
    expect(wrapper.text()).toContain("Not Schema.org compliant");
    expect(wrapper.find(".bg-danger").exists()).toBe(true);
  });

  it("renders name and learn-more link", () => {
    const wrapper = mount(CompatibilityResult, { props: { r: rOk }, global: { stubs } });
    expect(wrapper.text()).toContain("MySchema");
    expect(wrapper.find("a[target='_blank']").attributes("href")).toBe("https://example.com");
  });
});

// ── CompareItemDetails ────────────────────────────────────────────────────────

describe("CompareItemDetails", () => {
  it("displays property count", () => {
    const wrapper = mount(CompareItemDetails, {
      props: { cls: { properties: ["a", "b", "c"] } },
      global: { stubs },
    });
    expect(wrapper.text()).toContain("3 properties");
  });

  it("hides validation section when cls has no validation", () => {
    const wrapper = mount(CompareItemDetails, {
      props: { cls: { properties: [] } },
      global: { stubs },
    });
    expect(wrapper.text()).not.toContain("Validated Properties");
  });

  it("sums required + recommended + optional for total", () => {
    const cls = {
      properties: [],
      validation: { required: ["a", "b"], recommended: ["c"], optional: ["d", "e"] },
    };
    const wrapper = mount(CompareItemDetails, { props: { cls }, global: { stubs } });
    expect(wrapper.text()).toContain("5"); // total
    expect(wrapper.text()).toContain("2"); // required
    expect(wrapper.text()).toContain("1"); // recommended
  });
});

// ── Footer ────────────────────────────────────────────────────────────────────

describe("Footer", () => {
  it("renders the current year", async () => {
    const wrapper = mount(Footer, { global: { stubs } });
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain(new Date().getFullYear().toString());
  });

  it("renders Home, About, and Contact Us", () => {
    const wrapper = mount(Footer, { global: { stubs } });
    expect(wrapper.text()).toContain("Home");
    expect(wrapper.text()).toContain("About");
    expect(wrapper.text()).toContain("Contact Us");
  });
});

// ── MarkdownParser ────────────────────────────────────────────────────────────

describe("MarkdownParser", () => {
  it("renders markdown bold as <strong>", () => {
    const wrapper = mount(MarkdownParser, { props: { description: "**bold**" } });
    expect(wrapper.find("strong").text()).toBe("bold");
  });

  it("converts [[wiki]] links to schema.org URLs", () => {
    const wrapper = mount(MarkdownParser, { props: { description: "[[Thing]]" } });
    expect(wrapper.find("a").attributes("href")).toContain("schema.org/Thing");
  });

  it("opens links in a new tab", () => {
    const wrapper = mount(MarkdownParser, { props: { description: "[x](https://a.com)" } });
    expect(wrapper.find("a").attributes("target")).toBe("_blank");
  });

  it("shows fallback text when description is omitted", () => {
    const wrapper = mount(MarkdownParser);
    expect(wrapper.text()).toContain("No description available");
  });
});

// ── ToolCard ──────────────────────────────────────────────────────────────────

describe("ToolCard", () => {
  const props = {
    title: "My Tool",
    text: "A description",
    link: "/tool",
    link_text: "Go",
    image: "/img.png",
    image_alt: "alt text",
    cls: "extra-class",
  };

  it("renders title and text", () => {
    const wrapper = mount(ToolCard, { props, global: { stubs } });
    expect(wrapper.find("h2").text()).toBe("My Tool");
    expect(wrapper.text()).toContain("A description");
  });

  it("applies cls to the card element", () => {
    const wrapper = mount(ToolCard, { props, global: { stubs } });
    expect(wrapper.find(".tool-card").classes()).toContain("extra-class");
  });

  it("renders image with correct alt attribute", () => {
    const wrapper = mount(ToolCard, { props, global: { stubs } });
    expect(wrapper.find("img").attributes("alt")).toBe("alt text");
  });
});

// ── ObjectBox ─────────────────────────────────────────────────────────────────

describe("ObjectBox", () => {
  it("renders a PropertyBox stub for each property", () => {
    const properties = { name: { type: "string" }, age: { type: "number" } };
    const wrapper = mount(ObjectBox, {
      props: { properties, required: ["name"] },
      global: { stubs },
    });
    expect(wrapper.findAll("property-box-stub")).toHaveLength(2);
  });

  it("renders nothing when properties is empty", () => {
    const wrapper = mount(ObjectBox, {
      props: { properties: {}, required: [] },
      global: { stubs },
    });
    expect(wrapper.findAll("property-box-stub")).toHaveLength(0);
  });
});

// ── MoreButton ────────────────────────────────────────────────────────────────

describe("MoreButton", () => {
  it("renders all six shape paths and the plus polygon", () => {
    const wrapper = mount(MoreButton);
    const ids = ["yellow", "purple", "red", "pink", "green", "blue", "plus"];
    ids.forEach((id) => expect(wrapper.find(`#${id}`).exists()).toBe(true));
  });
});
