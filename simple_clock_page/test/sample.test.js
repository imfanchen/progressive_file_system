import { expect } from 'chai';

describe('Sample test', function () {
  let page;

  before(async function () {
    this.timeout(0);
    page = await global.browser.newPage();
    await page.setDefaultNavigationTimeout(0);
    await page.goto('http://localhost:3000', { waitUntil: 'load', timeout: 10000 });
    await page.waitForNetworkIdle({ idleTime: 2000, timeout: 5000 });
  });

  after(async function () {
    await page.close();
  });

  it('sample test', async () => {
    // sample test
  });
});
