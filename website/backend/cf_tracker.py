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
        SELECT username, timestramp, chocolate, increase
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
        username, timestramp, chocolate, increase = row

        user_data[username].append({
            'time': timestramp,
            'chocolate': chocolate,
            'increase': increase
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

        cursor.execute(f"SELECT chocolate FROM cf_tracker WHERE username = '{username}' ORDER BY id DESC LIMIT 1")

        # Fetch the result
        last_row = cursor.fetchone()[0]

        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()

        if 'id' in response:
            chocolate = stranded_api.stranded(response['id'])['misc']['chocolate']

        # Query to fetch data for specific usernames
        cursor.execute(f"""
            INSERT INTO cf_tracker (username, chocolate, increase, timestramp)
            VALUES ('{username}', {chocolate}, {chocolate - last_row}, CURRENT_TIMESTAMP);
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
