import { test, expect } from "@playwright/test";

test.describe("Metadata Validator page", () => {
  test("loads with heading and schema input", async ({ page }) => {
    await page.goto("/validator");
    await expect(page.getByRole("heading", { name: "Metadata Validator" })).toBeVisible();
    await expect(page.locator('input[placeholder="Start here"]')).toBeVisible();
  });

  test("Load button appears after typing a schema name", async ({ page }) => {
    await page.goto("/validator");
    await page.locator('input[placeholder="Start here"]').fill("Dataset");
    await expect(page.getByRole("button", { name: "Load", exact: true })).toBeVisible();
  });

  test("submitting a schema class updates the URL", async ({ page }) => {
    await page.goto("/validator");
    await page.locator('input[placeholder="Start here"]').fill("schema:Dataset");
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/schema_class=schema:Dataset/);
  });
});
