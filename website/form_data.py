from flask import Blueprint, request, make_response, jsonify
from .backend.get_api import get_profiles

form_data = Blueprint('form_data', __name__)


@form_data.route('/load')
def load():
    if request.args:

        username = request.args.get('u')

        updates = [get_profiles(username)]

        return make_response(jsonify(updates), 200)
