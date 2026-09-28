import { test, expect } from "@playwright/test";

test.describe("Schema Viewer page", () => {
  test("loads with title and subtitle", async ({ page }) => {
    await page.goto("/ns");
    await expect(page.getByRole("heading", { name: "Schema Viewer" })).toBeVisible();
    await expect(page.getByText("Visualize and Register Your Own Schema")).toBeVisible();
  });

  test("shows Get started section", async ({ page }) => {
    await page.goto("/ns");
    await expect(page.getByRole("heading", { name: "Get started:" })).toBeVisible();
  });
});
