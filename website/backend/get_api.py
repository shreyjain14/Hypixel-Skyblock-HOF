from dotenv import load_dotenv
import os
import requests
import json
import psycopg2
from website.backend import check

load_dotenv()

db_url = os.getenv('DATABASE_URL')


def update_leaderboard(connection, cursor, stranded_data, username, table_name="hof"):
    for category, values in stranded_data.items():
        for title, xp in values.items():
            cursor.execute(
                f"SELECT player_one, value_one, player_two, value_two, player_three, value_three FROM {table_name} WHERE title = %s",
                (title,))
            result = cursor.fetchone()

            if result:
                player_one, value_one, player_two, value_two, player_three, value_three = result

                if player_one == username:
                    # Update the first place
                    cursor.execute(f"""
                        UPDATE {table_name}
                        SET value_one = %s
                        WHERE title = %s
                    """, (xp, title))

                elif player_two == username:
                    # Check if the new value beats the first place
                    if xp > value_one:
                        # Swap the first and second places
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_one = %s, player_one = %s,
                                value_two = %s, player_two = %s
                            WHERE title = %s
                        """, (xp, username, value_one, player_one, title))
                    else:
                        # Update the second place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_two = %s
                            WHERE title = %s
                        """, (xp, title))

                elif player_three == username:
                    # Check if the new value beats the second and first places
                    if xp > value_one:
                        # Move the existing values down and update the first place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s,
                                value_two = %s, player_two = %s,
                                value_one = %s, player_one = %s
                            WHERE title = %s
                        """, (value_two, player_two, value_one, player_one, xp, username, title))
                    elif value_one > xp > value_two:
                        # Move the third place to the second place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s,
                                value_two = %s, player_two = %s
                            WHERE title = %s
                        """, (value_two, player_two, xp, username, title))
                    else:
                        # Update the third place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s
                            WHERE title = %s
                        """, (xp, username, title))

                else:
                    # If the username is not in the leaderboard
                    if xp > value_one:
                        # Move existing positions and update the first place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s,
                                value_two = %s, player_two = %s,
                                value_one = %s, player_one = %s
                            WHERE title = %s
                        """, (value_two, player_two, value_one, player_one, xp, username, title))

                    elif value_one > xp > value_two:
                        # Move existing positions and update the second place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s,
                                value_two = %s, player_two = %s
                            WHERE title = %s
                        """, (value_two, player_two, xp, username, title))

                    elif value_two > xp > value_three:
                        # Update the third place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s
                            WHERE title = %s
                        """, (xp, username, title))

    connection.commit()


def get_profiles(username):
    uuid = check.username(username)

    if uuid[:6] == "ERROR:":
        return uuid
    else:

        stranded_data = check.stranded(uuid)

        if type(stranded_data) == list:
            if stranded_data[:6] == "ERROR:":
                return stranded_data

        connection = psycopg2.connect(db_url)

        with connection:
            with connection.cursor() as cursor:

                update_leaderboard(connection, cursor, stranded_data, username)

        return 'updated'


if __name__ == "__main__":
    pass
