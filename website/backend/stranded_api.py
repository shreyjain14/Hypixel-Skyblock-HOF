import json
import requests
from dotenv import load_dotenv
import os


def stranded(uuid):
    load_dotenv()

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

    with open('website/backend/json_files/leaderboards.json') as f:
        stranded_tops = json.load(f)

    for profile in profiles:

        # SKYBLOCK LEVEL
        if 'leveling' in profile:
            if profile['leveling']['experience'] > stranded_tops['skyblock']['skyblock_xp']:
                stranded_tops['skyblock']['skyblock_xp'] = profile['leveling']['experience']

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

            # FISHING
            if 'sea_creature_kills' in profile['player_stats']:
                if profile['player_stats']['sea_creature_kills'] > stranded_tops['fishing']['sea_creature_kills']:
                    stranded_tops['fishing']['sea_creature_kills'] = profile['player_stats']['sea_creature_kills']

            if 'items_fished' in profile['player_stats']:
                total_fished_sum = 0

                if 'treasure' in profile['player_stats']['items_fished']:
                    total_fished_sum += profile['player_stats']['items_fished']['treasure']

                if 'large_treasure' in profile['player_stats']['items_fished']:
                    total_fished_sum += profile['player_stats']['items_fished']['large_treasure']

                if total_fished_sum > stranded_tops['fishing']['treasure_fished']:
                    stranded_tops['fishing']['treasure_fished'] = total_fished_sum

                if 'trophy_fish' in profile['player_stats']['items_fished']:
                    if profile['player_stats']['items_fished']['trophy_fish'] > stranded_tops['fishing']['trophy_fished']:
                        stranded_tops['fishing']['trophy_fished'] = profile['player_stats']['items_fished']['trophy_fish']

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


if __name__ == '__main__':
    print(stranded('1e95370ee22d4d2281a603d1594b6d61'))
