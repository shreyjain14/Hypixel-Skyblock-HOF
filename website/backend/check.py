from dotenv import load_dotenv
import requests
from dotenv import load_dotenv
import os
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


if __name__ == "__main__":
    pass
