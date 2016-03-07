# gistapi

Gistapi is a simple HTTP API server for searching Github Gists.

## Contents

This project contains a [tox](https://testrun.org/tox/latest/) definition for testing against both Python 2.7 and Python 3.4.
There is a `requirements.txt` file for installing the required Python modules via pip.  There is a `Dockerfile` and `docker-compose.yml` file 
if you'd like to run the project as a docker container.  The `tests/` directory contains two very simple tests to get started.  The `gistapi/`
directory contains the code you'll want to modify to implement the desired features.

## Challenge

The existing code is a skeleton -- the main functionality is left for you to implement.  The main task is to use the list of gist metadata 
fetched from the Github Gist API to fetch the contents of each Gist (also via the API) and to run the given regular expression over those 
matches returning the matched Gists once complete.  Throughout the `gistapi.py` file, there are comments of the form `# REQUIRED`.  These 
comments mark places in the code where the above functionality must be implemented.

There are also a number of places in the code marked `# BONUS` where additional code would yield a more robust or performant service.  If you 
finish the above quickly, feel free to investigate these added features or anything else you think might make for an interesting demo.  Please 
don't work on the additional optional features before the main task is complete.

## Development

The code will be checked while running in a [Docker](https://www.docker.com/) container but there is no requirement to develop/test inside 
docker.  The simplest way is to use a virtualenv for development:

```bash
    ~/Projects/coding_challenge% virtualenv ./env
    New python executable in /home/dion/Projects/coding_challenge/env/bin/python
    Installing setuptools, pip, wheel...done.
    ~/Projects/coding_challenge% source env/bin/activate
    (env) ~/Projects/coding_challenge% pip install -r requirements.txt
    Collecting Flask==0.10.1 (from -r requirements.txt (line 7))
    ...
    Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.4 gunicorn-19.4.5 itsdangerous-0.24 requests-2.9.1 six-1.10.0
    (env) ~/Projects/coding_challenge% python -m gistapi.gistapi
     * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger pin code: 111-111-111

    # In another terminal:
    ~/Projects/coding_challenge% curl -H "Content-Type: application/json" \
           -X POST \
           -d '{"username": "justdionysus", "pattern": "LOL[ab]*"}' \
           http://127.0.0.1:8000/api/v1/search
    {
      "matches": [],
      "pattern": "LOL[ab]*",
      "status": "success",
      "username": "justdionysus"
    }

    # When done, Ctrl-C in the server window
    # When done working on the code, deactivate the virtualenv:
    (env) ~/Projects/coding_challenge% deactivate
    ~/Projects/coding_challenge%
```

