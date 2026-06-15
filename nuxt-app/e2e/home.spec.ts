import { test, expect } from "@playwright/test";

test.describe("Home page", () => {
  test("loads and shows main heading", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/Data Discovery Engine/i);
    await expect(page.locator("h1#home")).toContainText("DATA DISCOVERY ENGINE");
  });

  test("shows all four section headings", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "Schema Playground" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Metadata ToolKit" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Data Portals", exact: true }).first()).toBeVisible();
    await expect(page.getByRole("heading", { name: "Registries" })).toBeVisible();
  });

  test("nav links point to correct routes", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("link", { name: /Browse our schemas/i })).toHaveAttribute("href", "/registry");
    await expect(page.getByRole("link", { name: /Visualize your schema/i })).toHaveAttribute("href", "/ns");
    await expect(page.getByRole("link", { name: /Create metadata/i })).toHaveAttribute("href", "/markup-generator");
    await expect(page.getByRole("link", { name: /Validate metadata/i })).toHaveAttribute("href", "/validator");
  });
});
