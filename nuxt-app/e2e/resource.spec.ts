import { test, expect } from "@playwright/test";

test.describe("Resource Registry page", () => {
  test("loads with heading and search box", async ({ page }) => {
    await page.goto("/resource");
    await expect(page.getByRole("heading", { name: "Resource Registry" })).toBeVisible();
    await expect(page.locator("#search_query")).toBeVisible();
  });

  test("results load from API on page load", async ({ page }) => {
    await page.goto("/resource");
    await expect(page.locator("#regTippyParent li").nth(1)).toBeVisible({ timeout: 10000 });
  });

  test("searching shows a result count", async ({ page }) => {
    await page.goto("/resource");
    await page.locator("#search_query").fill("dataset");
    await page.keyboard.press("Enter");
    await expect(page.locator(".bg-secondary.text-light.text-center")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".bg-secondary.text-light.text-center")).toContainText("Results");
  });

  test("search returns matching results", async ({ page }) => {
    await page.goto("/resource");
    await page.locator("#search_query").fill("dataset");
    await page.keyboard.press("Enter");
    await expect(page.locator("#regTippyParent li").nth(1)).toBeVisible({ timeout: 10000 });
  });

  test("clicking an item navigates to its detail page", async ({ page }) => {
    await page.goto("/resource");
    const firstLink = page.locator("#regTippyParent a").first();
    await expect(firstLink).toBeVisible({ timeout: 10000 });
    await firstLink.click();
    await expect(page).toHaveURL(/\/resource\/.+/);
    await expect(page.locator("h1").first()).toBeVisible({ timeout: 10000 });
  });
});
