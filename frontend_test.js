const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(`file://${process.cwd()}/examples/web-baseline.html`);
  await page.screenshot({ path: 'web-baseline-screenshot.png' });

  console.log("Screenshot saved as web-baseline-screenshot.png");
  await browser.close();
})();
