import { expect } from 'chai';

describe('Level 2 - Clock updater', () => {
  let page;

  let hoursUpButton, hoursDownButton;
  let minutesUpButton, minutesDownButton;

  const getClockValue = async () => {
    return await page.$eval('#clock', (node) => node.innerHTML);
  };

  const getButtonElements = async () => {
    hoursUpButton = await page.$('#hours-up-button');
    hoursDownButton = await page.$('#hours-down-button');
    minutesUpButton = await page.$('#minutes-up-button');
    minutesDownButton = await page.$('#minutes-down-button');
  }

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

  it('successfully increases the hour', async () => {
    // wait for loading the page
    await page.waitForSelector('#clock', { timeout: 1500 });
    await getButtonElements();

    expect(await getClockValue()).to.equal('00:00');
    await hoursUpButton.click();
    expect(await getClockValue()).to.equal('01:00');
  }).timeout(2000);

  it('successfully decreases the hour', async () => {
    expect(await getClockValue()).to.equal('01:00');
    await hoursDownButton.click();
    expect(await getClockValue()).to.equal('00:00');
  }).timeout(2000);

  it('successfully increases the minute', async () => {
    expect(await getClockValue()).to.equal('00:00');
    await minutesUpButton.click();
    expect(await getClockValue()).to.equal('00:01');
  }).timeout(2000);

  it('successfully decreases the minute', async () => {
    expect(await getClockValue()).to.equal('00:01');
    await minutesDownButton.click();
    expect(await getClockValue()).to.equal('00:00');
  }).timeout(2000);

  it('makes the minutes `59` when decreased from `00`', async () => {
    expect(await getClockValue()).to.equal('00:00');
    await minutesDownButton.click();
    expect(await getClockValue()).to.equal('00:59');
  }).timeout(2000);

  it('makes the minutes `59` when increased from `59`', async () => {
    expect(await getClockValue()).to.equal('00:59');
    await minutesUpButton.click();
    expect(await getClockValue()).to.equal('00:00');
  }).timeout(2000);

  it('makes the hours `23` when decreased from `00`', async () => {
    expect(await getClockValue()).to.equal('00:00');
    await hoursDownButton.click();
    expect(await getClockValue()).to.equal('23:00');
  }).timeout(2000);

  it('makes the hours `00` when increased from `23`', async () => {
    expect(await getClockValue()).to.equal('23:00');
    await hoursUpButton.click();
    expect(await getClockValue()).to.equal('00:00');
  }).timeout(2000);

  it('stays the same after increasing the hours 24 time and decreasing the minutes 60 time', async () => {
    expect(await getClockValue()).to.equal('00:00');
    await hoursUpButton.click();
    await minutesUpButton.click();
    expect(await getClockValue()).to.equal('01:01');
    for (let i = 0; i < 24; i++) {
      await hoursUpButton.click();
    }
    expect(await getClockValue()).to.equal('01:01');
    for (let i = 0; i < 60; i++) {
      await minutesDownButton.click();
    }
    expect(await getClockValue()).to.equal('01:01');
  }).timeout(5000);

  it('successfully makes the time `16:08`', async () => {
    expect(await getClockValue()).to.equal('01:01');

    for (let i = 0; i < 9; i++) {
      await hoursDownButton.click();
    }
    expect(await getClockValue()).to.equal('16:01');
    for (let i = 0; i < 7; i++) {
      await minutesUpButton.click();
    }
    expect(await getClockValue()).to.equal('16:08');
  }).timeout(5000);
});
