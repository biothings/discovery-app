import { test, expect } from "@playwright/test";

test.describe("Schema Registry page", () => {
  test("loads with correct title and tabs", async ({ page }) => {
    await page.goto("/registry");
    await expect(page.getByRole("heading", { name: "Schema Registry" })).toBeVisible();
    await expect(page.getByRole("link", { name: "Search By Class Name" })).toBeVisible();
    await expect(page.getByRole("link", { name: "Browse By Namespace" })).toBeVisible();
    await expect(page.getByRole("link", { name: "Compare Classes" })).toBeVisible();
  });

  test("class search tab shows search input", async ({ page }) => {
    await page.goto("/registry?search=classes");
    await expect(page.locator("#search_query")).toBeVisible();
    await expect(page.getByRole("heading", { name: "Classes" })).toBeVisible();
  });

  test("search returns results", async ({ page }) => {
    await page.goto("/registry?search=classes");
    await page.locator("#search_query").fill("Dataset");
    await page.keyboard.press("Enter");
    await expect(page.locator("#regTippyParent li").first()).toBeVisible({ timeout: 10000 });
  });

  test("namespace tab loads namespace list", async ({ page }) => {
    await page.goto("/registry?search=namespaces");
    await expect(page.getByRole("heading", { name: "Namespaces" })).toBeVisible();
    await expect(page.locator("ul.list-group a").first()).toBeVisible({ timeout: 10000 });
  });

  test("namespace links point to /ns routes", async ({ page }) => {
    await page.goto("/registry?search=namespaces");
    const firstLink = page.locator("ul.list-group a").first();
    await expect(firstLink).toBeVisible({ timeout: 10000 });
    const href = await firstLink.getAttribute("href");
    expect(href).toMatch(/^\/ns\/.+/);
  });
});
