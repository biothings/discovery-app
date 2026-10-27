import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import APIIcon from "../app/components/APIIcon.vue";
import CoverageIcon from "../app/components/CoverageIcon.vue";
import FAQIcon from "../app/components/FAQIcon.vue";
import MetadataIcon from "../app/components/MetadataIcon.vue";
import SchemaIcon from "../app/components/SchemaIcon.vue";
import WebsiteIcon from "../app/components/WebsiteIcon.vue";

const COLOR = "#1a2b3c";

describe("CoverageIcon", () => {
  it("applies the color prop as stroke on the polygon", () => {
    const wrapper = mount(CoverageIcon, { props: { color: COLOR } });
    const polygon = wrapper.find("polygon");
    expect(polygon.exists()).toBe(true);
    expect(polygon.attributes("style")).toContain(`stroke: ${COLOR}`);
  });
});

describe("APIIcon", () => {
  it("applies the color prop as stroke on all paths", () => {
    const wrapper = mount(APIIcon, { props: { color: COLOR } });
    const paths = wrapper.findAll("path");
    expect(paths.length).toBeGreaterThan(0);
    paths.forEach((p) => expect(p.attributes("style")).toContain(`stroke: ${COLOR}`));
  });
});

describe("FAQIcon", () => {
  it("applies the color prop as stroke on all paths", () => {
    const wrapper = mount(FAQIcon, { props: { color: COLOR } });
    const paths = wrapper.findAll("path");
    expect(paths.length).toBeGreaterThan(0);
    paths.forEach((p) => expect(p.attributes("style")).toContain(`stroke: ${COLOR}`));
  });
});

describe("MetadataIcon", () => {
  it("applies the color prop as stroke on paths and rects", () => {
    const wrapper = mount(MetadataIcon, { props: { color: COLOR } });
    const elements = [...wrapper.findAll("path"), ...wrapper.findAll("rect")];
    expect(elements.length).toBeGreaterThan(0);
    elements.forEach((el) => expect(el.attributes("style")).toContain(`stroke: ${COLOR}`));
  });
});

describe("SchemaIcon", () => {
  it("applies the color prop as stroke on all rects", () => {
    const wrapper = mount(SchemaIcon, { props: { color: COLOR } });
    const rects = wrapper.findAll("rect");
    expect(rects.length).toBeGreaterThan(0);
    rects.forEach((r) => expect(r.attributes("style")).toContain(`stroke: ${COLOR}`));
  });
});

describe("WebsiteIcon", () => {
  it("applies the color prop as stroke on all polylines", () => {
    const wrapper = mount(WebsiteIcon, { props: { color: COLOR } });
    const polylines = wrapper.findAll("polyline");
    expect(polylines.length).toBeGreaterThan(0);
    polylines.forEach((pl) => expect(pl.attributes("style")).toContain(`stroke: ${COLOR}`));
  });
});
