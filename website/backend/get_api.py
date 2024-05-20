from dotenv import load_dotenv
import os
import requests
import json
from website.backend import check

load_dotenv()

URL = 'https://api.hypixel.net/v2/skyblock/profile'
headers = {'API-Key': os.getenv('HYPIXEL-API-KEY')}


def get_profiles(username):
    uuid = check.username(username)

    if uuid[:6] == "ERROR:":
        return uuid
    else:

        stranded_profiles = check.stranded(uuid)

        if stranded_profiles[:6] == "ERROR:":
            return stranded_profiles

        # Update the data here

        # set updates to the items updated
        updates = [stranded_profiles]

        return 'updated'
