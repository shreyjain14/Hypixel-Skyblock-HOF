from dotenv import load_dotenv
import os
import psycopg2
from website.backend import check
from website.backend.stranded_api import stranded

load_dotenv()

db_url = os.getenv('DATABASE_URL')


def update_leaderboard(connection, cursor, stranded_data, username, table_name="hof"):

    changes = []

    for category, values in stranded_data.items():
        for title, xp in values.items():

            cursor.execute(f"SELECT COUNT(*) FROM hof WHERE title = '{title}';")
            title_check = cursor.fetchone()[0]

            if title_check == 0:

                title_name = ' '.join(title.upper().split('_'))

                cursor.execute(
                    f"INSERT INTO hof(title, category, title_name, value_one, value_two, value_three) "
                    f"VALUES ('{title}', '{category}', '{title_name}', 0, 0, 0);"
                )
                connection.commit()

            cursor.execute(
                f"SELECT player_one, value_one, player_two, value_two, player_three, value_three FROM {table_name} "
                f"WHERE title = %s",
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

                    changes.append(f"Updated 🥇 in {title} in {category}")

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

                        changes.append(f"Placed 🥇 in {title} in {category}")

                    else:
                        # Update the second place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_two = %s
                            WHERE title = %s
                        """, (xp, title))

                        changes.append(f"Updated 🥈 in {title} in {category}")

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

                        changes.append(f"Placed 🥇 in {title} in {category}")

                    elif value_one >= xp > value_two:
                        # Move the third place to the second place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s,
                                value_two = %s, player_two = %s
                            WHERE title = %s
                        """, (value_two, player_two, xp, username, title))

                        changes.append(f"Placed 🥈 in {title} in {category}")

                    else:
                        # Update the third place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s
                            WHERE title = %s
                        """, (xp, username, title))

                        changes.append(f"Updated 🥉 in {title} in {category}")

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

                        changes.append(f"Placed 🥇 in {title} in {category}")

                    elif value_one >= xp > value_two:
                        # Move existing positions and update the second place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s,
                                value_two = %s, player_two = %s
                            WHERE title = %s
                        """, (value_two, player_two, xp, username, title))

                        changes.append(f"Placed 🥈 in {title} in {category}")

                    elif value_two >= xp > value_three:
                        # Update the third place
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET value_three = %s, player_three = %s
                            WHERE title = %s
                        """, (xp, username, title))

                        changes.append(f"Placed 🥉 in {title} in {category}")

    connection.commit()

    if len(changes) == 0:
        changes.append("you are still not placed in any category!")

    return changes


def get_profiles(username):
    uuid = check.username(username)

    if uuid[:6] == "ERROR:":
        return uuid
    else:

        stranded_data = stranded(uuid)

        if type(stranded_data) == str:
            if stranded_data[:6] == "ERROR:":
                return [stranded_data]

        connection = psycopg2.connect(db_url)

        with connection:
            with connection.cursor() as cursor:

                try:
                    updates = update_leaderboard(connection, cursor, stranded_data, username)

                except AttributeError:
                    return ['ERROR: Contact DarkDash (@pestopastasauce on discord)']

        return updates


if __name__ == "__main__":
    pass
