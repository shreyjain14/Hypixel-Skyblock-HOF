from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

URL = 'https://api.hypixel.net/v2/skyblock/profile'
headers = {'API-Key': os.getenv('HYPIXEL-API-KEY')}


def get_profiles(username):
    pass
