import { test, expect } from "@playwright/test";

test.describe("Data Portals page", () => {
  test("loads with heading", async ({ page }) => {
    await page.goto("/portal");
    await expect(page.getByRole("heading", { name: "Data Portals", exact: true })).toBeVisible();
  });

  test("portal cards load from API", async ({ page }) => {
    await page.goto("/portal");
    await expect(page.locator("#portals .card").first()).toBeVisible({ timeout: 10000 });
  });

  test("each portal card links to its detail page", async ({ page }) => {
    await page.goto("/portal");
    const firstCard = page.locator("#portals .card").first();
    await expect(firstCard).toBeVisible({ timeout: 10000 });
    const link = firstCard.getByRole("link").first();
    const href = await link.getAttribute("href");
    expect(href).toMatch(/^\/portal\/.+/);
  });

  test("clicking a portal card navigates to its detail page", async ({ page }) => {
    await page.goto("/portal");
    const firstCard = page.locator("#portals .card").first();
    await expect(firstCard).toBeVisible({ timeout: 10000 });
    await firstCard.getByRole("link").first().click();
    await expect(page).toHaveURL(/\/portal\/.+/);
    await expect(page.locator("h1, h2, h3").first()).toBeVisible();
  });
});
