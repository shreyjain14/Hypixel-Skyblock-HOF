import requests
from flask import Blueprint, request, make_response, jsonify
from .backend.get_api import get_profiles
from dotenv import load_dotenv
import psycopg2
import os
from .backend import check, cf_tracker


load_dotenv()

db_url = os.getenv('DATABASE_URL')

form_data = Blueprint('form_data', __name__)


load_dotenv()


@form_data.route('/load')
def load():
    connection = psycopg2.connect(db_url)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('update_form', CURRENT_TIMESTAMP);")

            connection.commit()

    if request.args:

        username = request.args.get('u').lower()

        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()

        if 'id' in uuid:
            username = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid['id']}").json()['name']

            updates = get_profiles(username)

            return make_response(jsonify(updates), 200)

        else:
            return make_response(jsonify(['ERROR: Username not Found!']), 400)


@form_data.route('/blacklist-user')
def blacklist():
    connection = psycopg2.connect(db_url)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO analytics (page, visit_time) VALUES ('blacklist_form', CURRENT_TIMESTAMP);")

            connection.commit()

    if request.args:

        username = request.args.get('u')
        password = request.args.get('p')

        connection = psycopg2.connect(db_url)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT value_name FROM keys WHERE key_name='password';")
                result = cursor.fetchone()[0]

        if password == result:

            uuid = check.username(username)

            if uuid[:6] == 'ERROR:':
                if uuid == 'ERROR: Username Not Found!':
                    return make_response(jsonify([uuid]), 400)
                else:
                    return make_response(jsonify(["ERROR: User is already in blacklist"]), 400)

            else:

                connection = psycopg2.connect(db_url)

                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(f"INSERT INTO blacklist (uuid, username) VALUES ('{uuid}', '{username}');")
                        connection.commit()

                return make_response(jsonify([f"{username} Blacklisted"]), 200)

        else:
            return make_response(jsonify(["ERROR: Incorrect Password"]), 400)


@form_data.route('/tracker-data')
def tracker_data():
    res = cf_tracker.get_user_data()
    return make_response(jsonify(res), 200)


@form_data.route('/tracker-load')
def tracker_load():
    cf_tracker.add_data()
    return make_response(jsonify(['done']), 200)
