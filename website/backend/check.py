import requests
import dotenv
import os
import json


def username(uname):
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uname}").json()
    if 'id' in response:
        return response['id']
    else:
        return "ERROR: Username Not Found!"


def stranded(uuid):
    dotenv.load_dotenv()

    headers = {'API-Key': os.getenv('HYPIXEL-API-KEY')}
    params = {'uuid': uuid}

    url = 'https://api.hypixel.net/v2/skyblock/profiles'

    response = requests.get(url, headers=headers, params=params).json()

    profiles = []

    if response['success']:
        if response['profiles']:
            for profile_info in response['profiles']:
                if 'game_mode' in profile_info:
                    if profile_info['game_mode'] == 'island':
                        profiles.append(profile_info['members'][uuid])
    elif response['cause'] == "Invalid API key":
        return "ERROR: Hypixel API Not Responding"
    elif response['cause'] == "Malformed UUID":
        return "ERROR: Username doesn't exist with Hypixel"
    elif response['cause'] == "Key throttle":
        return "ERROR: Key Throttled! Try again later"

    if len(profiles) == 0:
        return "ERROR: You do not have any Stranded Profiles"

    stranded_tops = {
        'skills': {
            'skyblock_xp': 0,
            'farming_xp': 0,
            'mining_xp': 0,
            'combat_xp': 0,
            'foraging_xp': 0,
            'fishing_xp': 0,
            'enchanting_xp': 0,
            'alchemy_xp': 0,
            'carpentry_xp': 0,
            'taming_xp': 0,
            'runecrafting_xp': 0
        }
    }

    for profile in profiles:
        if profile['leveling']['experience'] > stranded_tops['skills']['skyblock_xp']:
            stranded_tops['skills']['skyblock_xp'] = profile['leveling']['experience']

        if 'experience' in profile['player_data']:

            if 'SKILL_FARMING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_FARMING'] > stranded_tops['skills']['farming_xp']:
                    stranded_tops['skills']['farming_xp'] = profile['player_data']['experience']['SKILL_FARMING']

            if 'SKILL_MINING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_MINING'] > stranded_tops['skills']['mining_xp']:
                    stranded_tops['skills']['mining_xp'] = profile['player_data']['experience']['SKILL_MINING']

            if 'SKILL_COMBAT' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_COMBAT'] > stranded_tops['skills']['combat_xp']:
                    stranded_tops['skills']['combat_xp'] = profile['player_data']['experience']['SKILL_COMBAT']

            if 'SKILL_FORAGING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_FORAGING'] > stranded_tops['skills']['foraging_xp']:
                    stranded_tops['skills']['foraging_xp'] = profile['player_data']['experience']['SKILL_FORAGING']

            if 'SKILL_FISHING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_FISHING'] > stranded_tops['skills']['fishing_xp']:
                    stranded_tops['skills']['fishing_xp'] = profile['player_data']['experience']['SKILL_FISHING']

            if 'SKILL_ENCHANTING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_ENCHANTING'] > stranded_tops['skills']['enchanting_xp']:
                    stranded_tops['skills']['enchanting_xp'] = profile['player_data']['experience']['SKILL_ENCHANTING']

            if 'SKILL_ALCHEMY' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_ALCHEMY'] > stranded_tops['skills']['alchemy_xp']:
                    stranded_tops['skills']['alchemy_xp'] = profile['player_data']['experience']['SKILL_ALCHEMY']

            if 'SKILL_CARPENTRY' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_CARPENTRY'] > stranded_tops['skills']['carpentry_xp']:
                    stranded_tops['skills']['carpentry_xp'] = profile['player_data']['experience']['SKILL_CARPENTRY']

            if 'SKILL_TAMING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_TAMING'] > stranded_tops['skills']['taming_xp']:
                    stranded_tops['skills']['taming_xp'] = profile['player_data']['experience']['SKILL_TAMING']

            if 'SKILL_RUNECRAFTING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_RUNECRAFTING'] > stranded_tops['skills']['runecrafting_xp']:
                    stranded_tops['skills']['runecrafting_xp'] = profile['player_data']['experience']['SKILL_RUNECRAFTING']

    return stranded_tops


if __name__ == "__main__":
    print(stranded(username('DarkDash')))
