import { expect } from 'chai';

describe('Level 1 - Clock updater', () => {
  let page;

  let hoursUpButton, hoursDownButton;
  let minutesUpButton, minutesDownButton;

  const getClockValue = async () => {
    return await page.$eval('#clock', (node) => node.innerHTML);
  };

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

  it('has all four buttons', async () => {
    // wait for loading the page
    await page.waitForSelector('#clock', { timeout: 1500 });

    hoursUpButton = await page.$('#hours-up-button');
    hoursDownButton = await page.$('#hours-down-button');
    minutesUpButton = await page.$('#minutes-up-button');
    minutesDownButton = await page.$('#minutes-down-button');
    expect(hoursUpButton).not.equal(null);
    expect(hoursDownButton).not.equal(null);
    expect(minutesUpButton).not.equal(null);
    expect(minutesDownButton).not.equal(null);
  }).timeout(5000);

  it('has the default state', async () => {
    expect(await getClockValue()).to.equal('00:00');
  }).timeout(5000);

});
