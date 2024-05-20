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
                        profiles.append(profile_info['profile_id'])
    elif response['cause'] == "Invalid API key":
        return "ERROR: Hypixel API Not Responding"
    elif response['cause'] == "Malformed UUID":
        return "ERROR: Username doesn't exist with Hypixel"
    elif response['cause'] == "Key throttle":
        return "ERROR: Key Throttled! Try again later"

    if len(profiles) == 0:
        return "ERROR: You do not have any Stranded Profiles"

    return profiles


if __name__ == "__main__":
    print(stranded(username('MumboJumbo')))
