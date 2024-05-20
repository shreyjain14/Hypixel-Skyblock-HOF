from flask import Blueprint, request, make_response, jsonify
from .backend import check

form_data = Blueprint('form_data', __name__)


@form_data.route('/load')
def load():
    if request.args:

        username = request.args.get('u')

        uuid = check.username(username)

        if uuid[:6] == "ERROR:":
            return make_response(jsonify([uuid]), 400)
        else:

            stranded_profiles = check.stranded(uuid)

            if stranded_profiles[:6] == "ERROR:":
                return make_response(jsonify([stranded_profiles]), 400)

            # Update the data here

            # set updates to the items updated
            updates = [stranded_profiles]

            return make_response(jsonify(updates), 200)
