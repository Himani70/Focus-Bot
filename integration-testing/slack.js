const puppeteer = require('puppeteer')
const cheerio = require('cheerio');
const config = require('./configs.json');

const slackUrl = config.slack_url;

async function login(browser, url, loginEmail, loginPassword, channel, page=null) {

  if(!page)
  {
  page = await browser.newPage();
  }

  await page.goto(url, {waitUntil: 'networkidle0'});

  // Login
  await page.type('input[id=email]', loginEmail);
  await page.type('input[id=password]', loginPassword);
  await page.click('button[id=signin_btn]');

  // Wait for redirect
  await page.waitForNavigation();
  await page.goto(channel, {waitUntil: 'networkidle0'});
  return page;
}

async function postMessage(page, msg)
{
  // Waiting for page to load
  //await page.waitForSelector('#undefined');

  // Focus on post textbox and press enter.
  await page.focus('#undefined')
  await page.keyboard.type( msg );
  await page.keyboard.press('Enter');
  return page
}

async function logout(page)
{
   await page.click('button[class="c-button-unstyled p-classic_nav__team_header__team__icon_button"]');
   //await page.waitForNavigation();
   const html = await page.content();
   const $ = cheerio.load(html);
   buttons = $('.c-menu_item__li').map((i, card) => {
  return {
      data: $(card).find('button').attr('data-qa'),
      id: $(card).find('button').attr('id')
  }
  }).get()
  var id =0
  for(var i=0;i<buttons.length;i++){
    if(buttons[i].data=="sign-out"){
      id = buttons[i].id;
    }
  }

   await page.click(`button[id=${id}]`);
   await page.waitForNavigation();
   return page
}

(async () => {

  const browser = await puppeteer.launch({headless: false, args: ["--no-sandbox", "--disable-web-security"]});
  
  const sleep = m => new Promise(r => setTimeout(r, m))

  let page = await login( browser, `${slackUrl}`, config.login_email_positive, config.login_password_positive, config.dm_channel_positive );
  await postMessage(page, "@FocusBot describe commands");
  await sleep(20000);
  await postMessage(page, "@FocusBot List tasks");
  await sleep(20000);
  await postMessage(page, "@FocusBot Start task issue-2 10 5 8 5");
  await sleep(35000);
  await postMessage(page, "@FocusBot Start task issue-2");
  await sleep(10000);
  await postMessage(page, "@FocusBot Create task Focus-1 milestone1 milestone1Description 5");
  await sleep(20000);
  await postMessage(page, "@FocusBot Create task Focus-1 milestone1 milestone1Description -3");
  await sleep(10000);
  await postMessage(page, "@FocusBot Show progress");
  await sleep(20000);
  await logout(page);
  page = await login( browser, `${slackUrl}` , config.login_email_negative, config.login_password_negative, config.dm_channel_negative, page);
  await postMessage(page, "@FocusBot List tasks");
  await sleep(20000);
  await postMessage(page, "@FocusBot Show progress");
  await sleep(30000)
  browser.close();
})()

