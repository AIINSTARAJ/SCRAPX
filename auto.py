import pyfiglet
from colorama import Fore, Style
from fake_useragent import UserAgent
import asyncio
from playwright.async_api import async_playwright
import httpx
import json
import random
from urllib.parse import urlparse, parse_qs, unquote

# Set up global variables
url = "https://api-gw-tg.memefi.club/graphql"
common_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://tg-app.memefi.club/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

tap_count = random.randint(438000000, 439000000)

payloads = [
    {
        "operationName": "telegramGameActivateBooster",
        "variables": {"boosterType": "Turbo"},
        "query": """mutation telegramGameActivateBooster($boosterType: BoosterType!) {
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
        }"""
    },
    {
        "operationName": "MutationGameProcessTapsBatch",
        "variables": {
            "payload": {
                "nonce": "c22632481d17814aeb8126b41f1ca9b09e450a9ae81960db30b797227b77187e",
                "tapsCount": tap_count,
                "vector": "2,3,4,3,3",
            }
        },
        "query": """mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {
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
        }"""
    },
    {
        "operationName": "telegramGameSetNextBoss",
        "variables": {},
        "query": """mutation telegramGameSetNextBoss {
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
        }"""
    }
]

# Helper functions
async def delay(ms):
    await asyncio.sleep(ms / 1000)

def parse_web_app_data(link):
    parsed_url = urlparse(link)
    params = parse_qs(parsed_url.fragment)

    tg_web_app_data = unquote(params['tgWebAppData'][0])
    tg_web_app_data_params = parse_qs(tg_web_app_data)

    web_app_data = {
        "query_id": tg_web_app_data_params['query_id'][0],
        "user": json.loads(unquote(tg_web_app_data_params['user'][0])),
        "auth_date": int(tg_web_app_data_params['auth_date'][0]),
        "hash": tg_web_app_data_params['hash'][0],
        "version": params['tgWebAppVersion'][0],
        "platform": params['tgWebAppPlatform'][0],
        "theme_params": json.loads(unquote(params['tgWebAppThemeParams'][0]))
    }

    if 'username' not in web_app_data['user']:
        web_app_data['user']['username'] = web_app_data['user'].get('first_name', 'User')

    return web_app_data

async def get_access_token(page, web_app_data):
    print(Fore.YELLOW + 'Attempting to get access token...' + Style.RESET_ALL)
    
    login_payload = [{
        "operationName": "MutationTelegramUserLogin",
        "variables": {
            "webAppData": {
                "auth_date": web_app_data['auth_date'],
                "hash": web_app_data['hash'],
                "query_id": web_app_data['query_id'],
                "checkDataString": f"auth_date={web_app_data['auth_date']}\nquery_id={web_app_data['query_id']}\nuser={json.dumps(web_app_data['user'])}",
                "user": web_app_data['user']
            }
        },
        "query": """mutation MutationTelegramUserLogin($webAppData: TelegramWebAppDataInput!, $referralCode: String) {
          telegramUserLogin(webAppData: $webAppData, referralCode: $referralCode) {
            access_token __typename
          }
        }"""
    }]
    
    try:
        response = await page.evaluate('''async (url, payload) => {
            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            return await res.json();
        }''', url, login_payload)
        
        print('Response:', json.dumps(response, indent=2))

        if response[0] and response[0]['data'] and response[0]['data']['telegramUserLogin']:
            access_token = response[0]['data']['telegramUserLogin']['access_token']
            print(Fore.GREEN + 'Access token obtained successfully' + Style.RESET_ALL)
            return access_token
        else:
            if response[0] and response[0]['errors']:
                print(Fore.RED + f"Server returned errors: {json.dumps(response[0]['errors'])}" + Style.RESET_ALL)
            raise Exception('Unexpected response structure')
    except Exception as e:
        print(Fore.RED + f'Failed to obtain access token: {e}' + Style.RESET_ALL)
        raise e

async def send_request(page, payload, index):
    try:
        response = await page.evaluate('''async (url, headers, payload) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify([payload])
            });
            return { status: response.status, body: await response.json() };
        }''', url, common_headers, payload)

        if response['status'] == 200:
            data = response['body'][0]['data']
            if index == 0:
                booster_used = data['telegramGameActivateBooster']['freeBoosts']['currentTurboAmount'] < data['telegramGameActivateBooster']['freeBoosts']['maxTurboAmount']
                print(Fore.BLUE + f"Booster {'activated' if booster_used else 'not activated'}" + Style.RESET_ALL)
            elif index == 1:
                coins_amount = data['telegramGameProcessTapsBatch']['coinsAmount']
                boss_level = data['telegramGameProcessTapsBatch']['currentBoss']['level']
                boss_health = data['telegramGameProcessTapsBatch']['currentBoss']['currentHealth']
                print(Fore.YELLOW + f"Coins: {coins_amount} | Boss Lv. {boss_level} HP: {boss_health}" + Style.RESET_ALL)
            elif index == 2:
                print(Fore.YELLOW + "Next boss set!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: Status code {response['status']}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Failed to send request: {e}" + Style.RESET_ALL)

async def run_bot(web_app_url):
    user_agent = UserAgent()
    ascii_banner = pyfiglet.figlet_format("memefi_bot")
    print(Fore.GREEN + ascii_banner + Style.RESET_ALL)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=user_agent.random)
        page = await context.new_page()
        await page.goto(web_app_url)
        await delay(5000)
        
        # Extract the web app data from the URL
        web_app_data = parse_web_app_data(web_app_url)
        
        # Retrieve the access token
        access_token = await get_access_token(page, web_app_data)
        
        # Set the authorization header
        common_headers['authorization'] = f'Bearer {access_token}'
        
        # Send requests with delays
        for idx, payload in enumerate(payloads):
            await send_request(page, payload, idx)
            await delay(3000)  # Delay between requests
        
        await browser.close()

# Entry point
if __name__ == '__main__':
    web_app_url = input(Fore.CYAN + "Enter the Telegram WebApp link: " + Style.RESET_ALL)
    asyncio.run(run_bot(web_app_url))
