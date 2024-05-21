from dotenv import load_dotenv
import requests
import dotenv
import os
import json
import psycopg2


load_dotenv()

db_url = os.getenv('DATABASE_URL')


def username(uname):

    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uname}").json()
    if 'id' in response:

        connection = psycopg2.connect(db_url)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM blacklist WHERE uuid = '{response['id']}';")
                result = cursor.fetchone()

                if result[0] > 0:
                    return "ERROR: You have been blacklisted from this leaderboard"
                else:
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
            'runecrafting_xp': 0,
            'social_xp': 0
        },
        'slayer': {
            'zombie_xp': 0,
            'spider_xp': 0,
            'wolf_xp': 0,
            'enderman_xp': 0,
            'blaze_xp': 0
        },
        'misc': {
            'unique_minions': 0,
            'highest_damage': 0,
            'highest_crit_damage': 0,
            'chocolate': 0,
            'deaths': 0,
            'collections': 0,
            'spooky_score': 0,
            'highest_pet_score': 0
        }
    }

    for profile in profiles:

        # SKYBLOCK LEVEL
        if 'leveling' in profile:
            if profile['leveling']['experience'] > stranded_tops['skills']['skyblock_xp']:
                stranded_tops['skills']['skyblock_xp'] = profile['leveling']['experience']

            # MISC
            if 'highest_pet_score' in profile['leveling']:
                if profile['leveling']['highest_pet_score'] > stranded_tops['misc']['highest_pet_score']:
                    stranded_tops['misc']['highest_pet_score'] = profile['leveling']['highest_pet_score']

        # SKILLS
        if 'experience' in profile['player_data']:

            if 'SKILL_FARMING' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_FARMING'] > stranded_tops['skills']['farming_xp']:
                    stranded_tops['skills']['farming_xp'] = profile['player_data']['experience']['SKILL_FARMING']

            if 'SKILL_SOCIAL' in profile['player_data']['experience']:
                if profile['player_data']['experience']['SKILL_SOCIAL'] > stranded_tops['skills']['social_xp']:
                    stranded_tops['skills']['social_xp'] = profile['player_data']['experience']['SKILL_SOCIAL']

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

        # SLAYERS
        if 'slayer' in profile:
            if 'xp' in profile['slayer']['slayer_bosses']['zombie']:
                if profile['slayer']['slayer_bosses']['zombie']['xp'] > stranded_tops['slayer']['zombie_xp']:
                    stranded_tops['slayer']['zombie_xp'] = profile['slayer']['slayer_bosses']['zombie']['xp']

            if 'xp' in profile['slayer']['slayer_bosses']['spider']:
                if profile['slayer']['slayer_bosses']['spider']['xp'] > stranded_tops['slayer']['spider_xp']:
                    stranded_tops['slayer']['spider_xp'] = profile['slayer']['slayer_bosses']['spider']['xp']

            if 'xp' in profile['slayer']['slayer_bosses']['wolf']:
                if profile['slayer']['slayer_bosses']['wolf']['xp'] > stranded_tops['slayer']['wolf_xp']:
                    stranded_tops['slayer']['wolf_xp'] = profile['slayer']['slayer_bosses']['wolf']['xp']

            if 'enderman' in profile['slayer']['slayer_bosses']:
                if 'xp' in profile['slayer']['slayer_bosses']['enderman']:
                    if profile['slayer']['slayer_bosses']['enderman']['xp'] > stranded_tops['slayer']['enderman_xp']:
                        stranded_tops['slayer']['enderman_xp'] = profile['slayer']['slayer_bosses']['enderman']['xp']

            if 'blaze' in profile['slayer']['slayer_bosses']:
                if 'xp' in profile['slayer']['slayer_bosses']['blaze']:
                    if profile['slayer']['slayer_bosses']['blaze']['xp'] > stranded_tops['slayer']['blaze_xp']:
                        stranded_tops['slayer']['blaze_xp'] = profile['slayer']['slayer_bosses']['blaze']['xp']

        # MISCELLANEOUS
        if 'player_data' in profile:
            if 'crafted_generators' in profile['player_data']:
                if len(profile['player_data']['crafted_generators']) > stranded_tops['misc']['unique_minions']:
                    stranded_tops['misc']['unique_minions'] = len(profile['player_data']['crafted_generators'])

        if 'player_stats' in profile:
            if 'highest_damage' in profile['player_stats']:
                if profile['player_stats']['highest_damage'] > stranded_tops['misc']['highest_damage']:
                    stranded_tops['misc']['highest_damage'] = profile['player_stats']['highest_damage']

            if 'highest_critical_damage' in profile['player_stats']:
                if profile['player_stats']['highest_critical_damage'] > stranded_tops['misc']['highest_crit_damage']:
                    stranded_tops['misc']['highest_crit_damage'] = profile['player_stats']['highest_critical_damage']

        if 'events' in profile:
            if 'easter' in profile['events']:
                if 'total_chocolate' in profile['events']['easter']:
                    if profile['events']['easter']['total_chocolate'] > stranded_tops['misc']['chocolate']:
                        stranded_tops['misc']['chocolate'] = profile['events']['easter']['total_chocolate']

        if 'death_count' in profile['player_data']:
            if profile['player_data']['death_count'] > stranded_tops['misc']['deaths']:
                stranded_tops['misc']['deaths'] = profile['player_data']['death_count']

        if 'unlocked_coll_tiers' in profile['player_data']:
            if len(profile['player_data']['unlocked_coll_tiers']) > stranded_tops['misc']['collections']:
                stranded_tops['misc']['collections'] = len(profile['player_data']['unlocked_coll_tiers'])

        if 'player_stats' in profile:
            if 'candy_collected' in profile['player_stats']:
                for i in profile['player_stats']['candy_collected'].values():

                    if type(i) == dict:
                        score = 0

                        if 'green_candy' in i:
                            score += int(i['green_candy'])

                        if 'purple_candy' in i:
                            score += int(i['purple_candy']) * 5

                        if score > stranded_tops['misc']['spooky_score']:
                            stranded_tops['misc']['spooky_score'] = score

    return stranded_tops


if __name__ == "__main__":
    print(stranded(username('DarkDash')))
