import psycopg2
import json
from collections import defaultdict

import requests
from dotenv import load_dotenv
import os
from website.backend import stranded_api

load_dotenv()


def get_user_data():
    # Database connection parameters - replace with your actual database configuration
    db_config = os.getenv("DATABASE_URL")

    usernames = ['its23lives', 'straindead']

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(db_config)
    cursor = conn.cursor()

    # Query to fetch data for specific usernames
    cursor.execute("""
        SELECT username, timestramp, chocolate, increase, rabbit_dupes, rabbit_dupes_inc
        FROM cf_tracker
        WHERE username IN %s
        ORDER BY username, timestramp;
    """, (tuple(usernames),))

    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Process the results
    user_data = defaultdict(list)
    last_chocolates = {username: None for username in usernames}

    for row in rows:
        username, timestramp, chocolate, increase, dupes, dupes_inc = row

        user_data[username].append({
            'time': timestramp,
            'chocolate': chocolate,
            'increase': increase,
            'dupes': dupes,
            'dupes_inc': dupes_inc
        })

        last_chocolates[username] = chocolate

    return user_data


def add_data():
    db_config = os.getenv("DATABASE_URL")

    usernames = ['its23lives', 'straindead']

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(db_config)
    cursor = conn.cursor()

    for username in usernames:

        cursor.execute(f"SELECT chocolate, rabbit_dupes FROM cf_tracker WHERE username = '{username}' ORDER BY id DESC LIMIT 1")

        # Fetch the result
        last_row = cursor.fetchone()

        reply = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()

        if 'id' in reply:
            headers = {'API-Key': os.getenv('HYPIXEL-API-KEY')}
            params = {'uuid': reply['id']}

            url = 'https://api.hypixel.net/v2/skyblock/profiles'

            response = requests.get(url, headers=headers, params=params).json()

            profiles = []

            if response['success']:
                if response['profiles']:
                    for profile_info in response['profiles']:
                        if 'game_mode' in profile_info:
                            if profile_info['game_mode'] == 'island':
                                profiles.append(profile_info['members'][reply['id']])

            chocolate = 0
            rabbits_dupes = 0

            for profile in profiles:

                if 'events' in profile:
                    if 'easter' in profile['events']:
                        if 'total_chocolate' in profile['events']['easter']:
                            if profile['events']['easter']['total_chocolate'] > chocolate:
                                chocolate = profile['events']['easter']['total_chocolate']

                        if 'rabbits' in profile['events']['easter']:
                            dupes = 0

                            for i in profile['events']['easter']['rabbits'].values():
                                if type(i) != dict:
                                    dupes += i - 1

                            if dupes > rabbits_dupes:
                                rabbits_dupes = dupes

        # Query to fetch data for specific usernames
        cursor.execute(f"""
            INSERT INTO cf_tracker (username, chocolate, increase, timestramp, rabbit_dupes, rabbit_dupes_inc)
            VALUES ('{username}', {chocolate}, {chocolate - last_row[0]}, CURRENT_TIMESTAMP, {rabbits_dupes}, {rabbits_dupes - last_row[1]});
        """)

    conn.commit()

    cursor.close()
    conn.close()


# Usage

if __name__ == '__main__':
    import time

    while True:
        add_data()
        time.sleep(300)
