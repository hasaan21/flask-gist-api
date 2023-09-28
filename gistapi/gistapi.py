# coding=utf-8
"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests
from flask import Flask, jsonify, request
import re


# *The* app object
app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = 'https://api.github.com/users/{username}/gists'.format(
            username=username)

    # BONUS: What failures could happen?
    # Failures like username not found or API limit reached can happen
    # These are handled by following if block.
    # BONUS: Paging? How does this work for users with tons of gists?
    # If a user has tons of gists. The trucated flag will be set to true.

    response = requests.get(gists_url)
    if response.status_code != 200:
        return None

    return response.json()


def valid_arguments(arguments):
    if set(['username', 'pattern']) == set(arguments) and isinstance(arguments['username'], str) and \
       isinstance(arguments['pattern'], str):
        return True
    return False


@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """

    post_data = request.json
    result = {}
    status = True
    warnings = []
    gists = None

    # BONUS: Validate the arguments?
    if not valid_arguments(post_data):
        status = False

    if status:
        username = post_data['username']
        pattern = post_data['pattern']

        result['matches'] = []
        gists = gists_for_user(username)
        # BONUS: Handle invalid users?
        if gists is not None:
            for gist in gists:
                # REQUIRED: Fetch each gist and check for the pattern
                # Completed
                # BONUS: What about huge gists?
                # If gists are greater than 300, added warning
                # BONUS: Can we cache results in a datastore/db?
                # Skipped

                response = requests.get(gist['url'])

                if gist['truncated']:
                    warnings.append(f"Gist({gist['id']}): More than 300 files")

                # Search if not truncated
                if re.search(pattern, response.content.decode('utf-8')):
                    result['matches'].append(f"https://gist.github.com/{username}/{gist['id']}")
                    continue

                if(response.status_code != 200):
                    # Skipping if API limit reached
                    break

                gist_json = response.json()
                files = gist_json['files']

                # Search if truncated
                for key in files:
                    if files[key]['truncated']:
                        file_response = requests.get(files[key]["raw_url"])
                        if(file_response.status_code != 200):
                            # Skipping if API limit reached
                            break
                        if re.search(pattern, file_response.content.decode("utf-8")):
                            result['matches'].append(f"https://gist.github.com/{username}/{gist['id']}")
            result['status'] = 'success'
        else:
            result['status'] = 'failure'

    if status:
        result['username'] = username
        result['pattern'] = pattern
        if len(warnings) > 0:
            result['warnings'] = warnings
    else:
        result['status'] = 'arguments not valid'

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9876)
