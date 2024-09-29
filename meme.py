import asyncio
import json
import time
from fake_useragent import UserAgent
import cloudscraper

Auth = input("Enter Auth Token: ")

url = "https://api-gw-tg.memefi.club/graphql"
common_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY2Zjc0ZWY0ZjI3ZGE2NzU0ZTFjZGIwNSIsInVzZXJuYW1lIjoiU2FuZ29fb3RhIn0sInNlc3Npb25JZCI6IjY2Zjc1MTZmNTRmMWU2MTZjNmE5MjhjNiIsInN1YiI6IjY2Zjc0ZWY0ZjI3ZGE2NzU0ZTFjZGIwNSIsImlhdCI6MTcyNzQ4NDI3MSwiZXhwIjoxNzM1MjYwMjcxfQ.8Kig7REsHS2Sof55HZeMj_Bbeffk86y2vOG6E9F-dYk",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://tg-app.memefi.club/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}
tap_count = 1500000000

payloads = [
    # Payload 1 (Booster)
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
            _id
            coinsAmount
            currentEnergy
            maxEnergy
            weaponLevel
            zonesCount
            tapsReward
            energyLimitLevel
            energyRechargeLevel
            tapBotLevel
            currentBoss {
                _id
                level
                currentHealth
                maxHealth
                __typename
            }
            freeBoosts {
                _id
                currentTurboAmount
                maxTurboAmount
                turboLastActivatedAt
                turboAmountLastRechargeDate
                currentRefillEnergyAmount
                maxRefillEnergyAmount
                refillEnergyLastActivatedAt
                refillEnergyAmountLastRechargeDate
                __typename
            }
            bonusLeaderDamageEndAt
            bonusLeaderDamageStartAt
            bonusLeaderDamageMultiplier
            nonce
            __typename
        }"""
    },
    # Payload 2 (Process Taps)
    {
        "operationName": "MutationGameProcessTapsBatch",
        "variables": {
            "payload": {
                "nonce": "c22632481d17814aeb8126b41f1ca9b09e450a9ae81960db30b797227b77187e",
                "tapsCount": tap_count,
                "vector": "2,3,4,3,3,4,3,2",
            }
        },
        "query": """mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {
            telegramGameProcessTapsBatch(payload: $payload) {
                ...FragmentBossFightConfig
                __typename
            }
        }
        fragment FragmentBossFightConfig on TelegramGameConfigOutput {
            _id
            coinsAmount
            currentEnergy
            maxEnergy
            weaponLevel
            zonesCount
            tapsReward
            energyLimitLevel
            energyRechargeLevel
            tapBotLevel
            currentBoss {
                _id
                level
                currentHealth
                maxHealth
                __typename
            }
            freeBoosts {
                _id
                currentTurboAmount
                maxTurboAmount
                turboLastActivatedAt
                turboAmountLastRechargeDate
                currentRefillEnergyAmount
                maxRefillEnergyAmount
                refillEnergyLastActivatedAt
                refillEnergyAmountLastRechargeDate
                __typename
            }
            bonusLeaderDamageEndAt
            bonusLeaderDamageStartAt
            bonusLeaderDamageMultiplier
            nonce
            __typename
        }"""
    },
    # Payload 3 (Set Next Boss)
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
            _id
            coinsAmount
            currentEnergy
            maxEnergy
            weaponLevel
            zonesCount
            tapsReward
            energyLimitLevel
            energyRechargeLevel
            tapBotLevel
            currentBoss {
                _id
                level
                currentHealth
                maxHealth
                __typename
            }
            freeBoosts {
                _id
                currentTurboAmount
                maxTurboAmount
                turboLastActivatedAt
                turboAmountLastRechargeDate
                currentRefillEnergyAmount
                maxRefillEnergyAmount
                refillEnergyLastActivatedAt
                refillEnergyAmountLastRechargeDate
                __typename
            }
            bonusLeaderDamageEndAt
            bonusLeaderDamageStartAt
            bonusLeaderDamageMultiplier
            nonce
            __typename
        }"""
    },
]

def send_request(scraper, payload, index):
    try:
        response = scraper.post(url, json=payload)
        print(f"Request {index + 1} status:", response.status_code)
        print('Response body:', response.text)
        return response.status_code == 200
    except Exception as e:
        print(f"Error in request {index + 1}: {str(e)}")
        return False

def send_all_requests():
    ua = UserAgent()
    user_agent = ua.random

    common_headers['User-Agent'] = user_agent

    scraper = cloudscraper.create_scraper()
    scraper.headers.update(common_headers)

    while True:
        start_time = time.time()

        # Send the first payload and verify
        success = send_request(scraper, payloads[0], 0)
        if not success:
            print("First payload failed, restarting cycle.")
            continue

        # Send and verify the second payload
        success = send_request(scraper, payloads[1], 1)
        if not success:
            print("Second payload failed, restarting cycle.")
            continue

        # Send and verify the third payload
        success = send_request(scraper, payloads[2], 2)
        if not success:
            print("Third payload failed, restarting cycle.")
            continue

        # Continue sending the second and third payloads until 10 seconds pass
        while time.time() - start_time < 10:
            success = send_request(scraper, payloads[1], 1)
            if not success:
                break

            success = send_request(scraper, payloads[2], 2)
            if not success:
                break

        # Wait for 5 seconds before restarting the cycle
        print("Waiting 30 seconds before starting the next cycle...")
        time.sleep(2)

if __name__ == "__main__":
    send_all_requests()

