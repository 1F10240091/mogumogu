import { expect, test } from '@playwright/test';

test.describe('Home Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load successfully', async ({ page }) => {
    await expect(page).toHaveTitle(/Mogumogu/);
  });

  test('should have main heading', async ({ page }) => {
    await expect(page.locator('h1')).toBeVisible();
  });
});

test.describe('Navigation', () => {
  test('should navigate to recipes page', async ({ page }) => {
    await page.goto('/');
    await page.click('text=レシピ');
    await expect(page).toHaveURL(/.*recipes/);
  });
});
