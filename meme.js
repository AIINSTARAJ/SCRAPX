

import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import randomUseragent from 'random-useragent';
import chalk from 'chalk';
import figlet from 'figlet';
import { createInterface } from 'readline';
import { URL, URLSearchParams } from 'url';


puppeteer.use(StealthPlugin());

const url = "https://api-gw-tg.memefi.club/graphql";
const commonHeaders = {
  "accept": "*/*",
  "accept-language": "en-US,en;q=0.9",
  "content-type": "application/json",
  "priority": "u=1, i",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "Referer": "https://tg-app.memefi.club/",
  "Referrer-Policy": "strict-origin-when-cross-origin",
};

let tapCount = Math.floor(Math.random() * (439000000 - 438000000 + 1)) + 438000000;

const payloads = [
  // Payload 1 (Booster)
  {
    operationName: "telegramGameActivateBooster",
    variables: { boosterType: "Turbo" },
    query: `mutation telegramGameActivateBooster($boosterType: BoosterType!) {
      telegramGameActivateBooster(boosterType: $boosterType) {
        ...FragmentBossFightConfig
        __typename
      }
    }
    fragment FragmentBossFightConfig on TelegramGameConfigOutput {
      _id coinsAmount currentEnergy maxEnergy weaponLevel zonesCount tapsReward
      energyLimitLevel energyRechargeLevel tapBotLevel
      currentBoss { _id level currentHealth maxHealth __typename }
      freeBoosts {
        _id currentTurboAmount maxTurboAmount turboLastActivatedAt turboAmountLastRechargeDate
        currentRefillEnergyAmount maxRefillEnergyAmount refillEnergyLastActivatedAt refillEnergyAmountLastRechargeDate
        __typename
      }
      bonusLeaderDamageEndAt bonusLeaderDamageStartAt bonusLeaderDamageMultiplier nonce __typename
    }`
  },
  // Payload 2 (Process Taps)
  {
    operationName: "MutationGameProcessTapsBatch",
    variables: {
      payload: {
        nonce: "c22632481d17814aeb8126b41f1ca9b09e450a9ae81960db30b797227b77187e",
        tapsCount: tapCount,
        vector: "2,3,4,3,3",
      },
    },
    query: `mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {
      telegramGameProcessTapsBatch(payload: $payload) {
        ...FragmentBossFightConfig
        __typename
      }
    }
    fragment FragmentBossFightConfig on TelegramGameConfigOutput {
      _id coinsAmount currentEnergy maxEnergy weaponLevel zonesCount tapsReward
      energyLimitLevel energyRechargeLevel tapBotLevel
      currentBoss { _id level currentHealth maxHealth __typename }
      freeBoosts {
        _id currentTurboAmount maxTurboAmount turboLastActivatedAt turboAmountLastRechargeDate
        currentRefillEnergyAmount maxRefillEnergyAmount refillEnergyLastActivatedAt refillEnergyAmountLastRechargeDate
        __typename
      }
      bonusLeaderDamageEndAt bonusLeaderDamageStartAt bonusLeaderDamageMultiplier nonce __typename
    }`
  },
  // Payload 3 (Set Next Boss)
  {
    operationName: "telegramGameSetNextBoss",
    variables: {},
    query: `mutation telegramGameSetNextBoss {
      telegramGameSetNextBoss {
        ...FragmentBossFightConfig
        __typename
      }
    }
    fragment FragmentBossFightConfig on TelegramGameConfigOutput {
      _id coinsAmount currentEnergy maxEnergy weaponLevel zonesCount tapsReward
      energyLimitLevel energyRechargeLevel tapBotLevel
      currentBoss { _id level currentHealth maxHealth __typename }
      freeBoosts {
        _id currentTurboAmount maxTurboAmount turboLastActivatedAt turboAmountLastRechargeDate
        currentRefillEnergyAmount maxRefillEnergyAmount refillEnergyLastActivatedAt refillEnergyAmountLastRechargeDate
        __typename
      }
      bonusLeaderDamageEndAt bonusLeaderDamageStartAt bonusLeaderDamageMultiplier nonce __typename
    }`
  },
];

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const getUserInput = async (question) => {
  const readline = createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    readline.question(chalk.cyan(question), (answer) => {
      readline.close();
      resolve(answer.trim());
    });
  });
};

const parseWebAppData = (link) => {
  const url = new URL(link);
  const params = new URLSearchParams(url.hash.slice(1));
 
  const tgWebAppData = params.get('tgWebAppData');
  const tgWebAppDataParams = new URLSearchParams(tgWebAppData);

  const webAppData = {
    query_id: tgWebAppDataParams.get('query_id'),
    user: JSON.parse(decodeURIComponent(tgWebAppDataParams.get('user'))),
    auth_date: parseInt(tgWebAppDataParams.get('auth_date')),
    hash: tgWebAppDataParams.get('hash'),
    version: params.get('tgWebAppVersion'),
    platform: params.get('tgWebAppPlatform'),
    theme_params: JSON.parse(decodeURIComponent(params.get('tgWebAppThemeParams')))
  };

  if (!webAppData.user.username) {
    webAppData.user.username = webAppData.user.first_name || 'User';
  }

  return webAppData;
};

const getAccessToken = async (page, webAppData) => {
  console.log(chalk.yellow('Attempting to get access token...'));
 
  const loginPayload = [{
    operationName: "MutationTelegramUserLogin",
    variables: {
      webAppData: {
        auth_date: parseInt(webAppData.auth_date),
        hash: webAppData.hash,
        query_id: webAppData.query_id,
        checkDataString: `auth_date=${webAppData.auth_date}\nquery_id=${webAppData.query_id}\nuser=${JSON.stringify(webAppData.user)}`,
        user: webAppData.user
      }
    },
    query: "mutation MutationTelegramUserLogin($webAppData: TelegramWebAppDataInput!, $referralCode: String) { telegramUserLogin(webAppData: $webAppData, referralCode: $referralCode) { access_token __typename } }"
  }];

  try {
    const response = await page.evaluate(async (url, payload) => {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      return await res.json();
    }, url, loginPayload);

    console.log('Response:', JSON.stringify(response, null, 2));

    if (response[0] && response[0].data && response[0].data.telegramUserLogin) {
      const accessToken = response[0].data.telegramUserLogin.access_token;
      console.log(chalk.green('Access token obtained successfully'));
      return accessToken;
    } else {
      if (response[0] && response[0].errors) {
        console.error(chalk.red(`Server returned errors: ${JSON.stringify(response[0].errors)}`));
      }
      throw new Error('Unexpected response structure');
    }
  } catch (error) {
    console.error(chalk.red(`Failed to obtain access token: ${error.message}`));
    throw error;
  }
};

const sendRequest = async (page, payload, index) => {
  try {
    const response = await page.evaluate(async (url, commonHeaders, payload) => {
      const response = await fetch(url, {
        method: 'POST',
        headers: commonHeaders,
        body: JSON.stringify([payload])
      });
      return { status: response.status, body: await response.json() };
    }, url, commonHeaders, payload);

    if (response.status === 200) {
      const data = response.body[0].data;
      if (index === 0) {
        const boosterUsed = data.telegramGameActivateBooster.freeBoosts.currentTurboAmount < data.telegramGameActivateBooster.freeBoosts.maxTurboAmount;
        console.log(chalk.blue(`Booster ${boosterUsed ? 'activated' : 'not activated'}`));
      } else if (index === 1) {
        const { coinsAmount, currentBoss } = data.telegramGameProcessTapsBatch;
        console.log(chalk.green(`Coins: ${coinsAmount} | Boss Level: ${currentBoss.level} | Boss Health: ${currentBoss.currentHealth}`));
      } else if (index === 2) {
        const { coinsAmount, currentBoss } = data.telegramGameSetNextBoss;
        console.log(chalk.magenta(`New Boss Level: ${currentBoss.level} | Total Coins: ${coinsAmount}`));
      }
      return true;
    } else {
      console.error(chalk.red(`Request ${index + 1} failed with status code: ${response.status}`));
      return false;
    }
  } catch (error) {
    console.error(chalk.red(`Error in request ${index + 1}: ${error.message}`));
    return false;
  }
};

const sendAllRequests = async (page, targetPoints) => {
  let cycleCount = 0;
  let totalPoints = 0;
  const pointsPerCycle = 50000000;

  while (totalPoints < targetPoints) {
    cycleCount++;
    console.log(chalk.yellow(`Starting cycle ${cycleCount}`));
    const startTime = Date.now();

    let cycleFailed = false;
    for (let i = 0; i < payloads.length; i++) {
      const success = await sendRequest(page, payloads[i], i);
      if (!success) {
        console.warn(chalk.yellow(`Cycle ${cycleCount} failed at request ${i + 1}, restarting cycle.`));
        cycleFailed = true;
        break;
      }
      await delay(5000); // Distribute requests evenly within 10 seconds
    }

    if (!cycleFailed) {
      totalPoints += pointsPerCycle;
      console.log(chalk.cyan(`Total points: ${totalPoints.toLocaleString()} / ${targetPoints.toLocaleString()}`));
    }

    const elapsedTime = Date.now() - startTime;
    if (elapsedTime < 10000) {
      const waitTime = 10000 - elapsedTime;
      console.log(chalk.cyan(`Waiting ${waitTime / 1000} seconds before the next cycle...`));
      await delay(waitTime);
    }

    // Additional wait time between cycles (5-10 seconds)
    const additionalWaitTime = Math.floor(Math.random() * 5000) + 5000;
    console.log(chalk.cyan(`Additional wait time: ${additionalWaitTime / 1000} seconds`));
    await delay(additionalWaitTime);
  }

  console.log(chalk.green(`Target of ${targetPoints.toLocaleString()} points reached successfully!`));
};

(async () => {
  console.log(chalk.bold.green(figlet.textSync('MEMEFI AUTOMATION', { horizontalLayout: 'full' })));
  console.log(chalk.italic('Built with love by A.I Instaraj\n'));

  const userLink = await getUserInput('Please enter your Memefi Telegram Web App link: ');
  const webAppData = parseWebAppData(userLink);
  console.log(chalk.green('Web app data parsed successfully'));
  console.log('Parsed Web App Data:', JSON.stringify(webAppData, null, 2));

  const targetPointsInput = await getUserInput('Enter the number of points you want to add: ');
  const targetPoints = parseInt(targetPointsInput);

  if (isNaN(targetPoints) || targetPoints <= 0) {
    console.error(chalk.red('Invalid input. Please enter a positive number.'));
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setUserAgent(randomUseragent.getRandom());

  try {
    const accessToken = await getAccessToken(page, webAppData);
    commonHeaders.authorization = `Bearer ${accessToken}`;

    await sendAllRequests(page, targetPoints);
  } catch (error) {
    console.error(chalk.red(`An error occurred: ${error.message}`));
  } finally {
    console.log(chalk.green("All requests completed. Closing browser."));
    await browser.close();
  }
})();