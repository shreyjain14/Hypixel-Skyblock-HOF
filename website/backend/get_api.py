from dotenv import load_dotenv
import os
import requests
import json
import psycopg2
from website.backend import check

load_dotenv()

db_url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(db_url)


def get_profiles(username):
    uuid = check.username(username)

    if uuid[:6] == "ERROR:":
        return uuid
    else:

        stranded_data = check.stranded(uuid)

        if type(stranded_data) == list:
            if stranded_data[:6] == "ERROR:":
                return stranded_data

        with connection:
            with connection.cursor() as cursor:
                for skill, xp in stranded_data['skills'].items():
                    cursor.execute(
                        "SELECT player_one, value_one, player_two, value_two, player_three, value_three FROM hof WHERE title = %s",
                        (skill,))
                    result = cursor.fetchone()

                    if result:
                        player_one, value_one, player_two, value_two, player_three, value_three = result

                        if xp > value_one:
                            cursor.execute("""
                                UPDATE hof
                                SET value_three = %s, player_three = %s,
                                    value_two = %s, player_two = %s,
                                    value_one = %s, player_one = %s
                                WHERE title = %s
                            """, (value_two, player_two, value_one, player_one, xp, username, skill))

                        elif value_one > xp > value_two:
                            cursor.execute("""
                                UPDATE hof
                                SET value_three = %s, player_three = %s,
                                    value_two = %s, player_two = %s
                                WHERE title = %s
                            """, (value_two, player_two, xp, username, skill))

                        elif value_two > xp > value_three:
                            cursor.execute("""
                                UPDATE hof
                                SET value_three = %s, player_three = %s
                                WHERE title = %s
                            """, (xp, username, skill))

                for slayer, xp in stranded_data['slayer'].items():
                    cursor.execute(
                        "SELECT player_one, value_one, player_two, value_two, player_three, value_three FROM hof WHERE title = %s",
                        (slayer,))
                    result = cursor.fetchone()

                    if result:
                        player_one, value_one, player_two, value_two, player_three, value_three = result

                        if xp > value_one:
                            cursor.execute("""
                                UPDATE hof
                                SET value_three = %s, player_three = %s,
                                    value_two = %s, player_two = %s,
                                    value_one = %s, player_one = %s
                                WHERE title = %s
                            """, (value_two, player_two, value_one, player_one, xp, username, slayer))

                        elif value_one > xp > value_two:
                            cursor.execute("""
                                UPDATE hof
                                SET value_three = %s, player_three = %s,
                                    value_two = %s, player_two = %s
                                WHERE title = %s
                            """, (value_two, player_two, xp, username, slayer))

                        elif value_two > xp > value_three:
                            cursor.execute("""
                                UPDATE hof
                                SET value_three = %s, player_three = %s
                                WHERE title = %s
                            """, (xp, username, slayer))

            connection.commit()

        return 'updated'


if __name__ == "__main__":
    get_profiles('Z109')
