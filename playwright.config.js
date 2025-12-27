// Playwright configuration for testing DRF API
// Playwright is like a robot that tests your website automatically

module.exports = {
  testDir: './tests',
  timeout: 30000,
  use: {
    baseURL: 'http://127.0.0.1:8000',
    headless: false, // Set to true to run without opening browser
  },
  projects: [
    {
      name: 'chromium',
      use: { ...require('@playwright/test').devices['Desktop Chrome'] },
    },
  ],
};

