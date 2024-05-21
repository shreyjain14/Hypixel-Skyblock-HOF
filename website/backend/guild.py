from dotenv import load_dotenv
import os
import requests

from website.backend.get_api import get_profiles

load_dotenv()


def load():

    headers = {'API-Key': os.getenv('HYPIXEL-API-KEY')}
    params = {'id': '61cdf8b48ea8c981ac653ff1'}

    url = 'https://api.hypixel.net/v2/guild'

    response = requests.get(url, headers=headers, params=params).json()['guild']['members']

    for idx, member in enumerate(response):

        if idx < 98:
            continue

        try:
            username = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{member['uuid']}").json()['name']
            print(idx, username)
            get_profiles(username)

        except AttributeError:
            pass


if __name__ == "__main__":
    load()
