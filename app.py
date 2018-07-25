import os

from stackapi import StackAPI
from flask import Flask, request, redirect
from commands import search, question, help, ask

# Attempts to grab the StackExchange API key from either Heroku's env variables or the local config.py
# The SE_KEY can be generated at: https://stackapps.com/apps/oauth/register
#              or retrieved from: https://stackapps.com/apps/oauth
try:
    import config
    se_key = config.SE_KEY
except:
    se_key = os.environ.get('SE_KEY')

if not se_key:
    print('Please make sure you have a config.py file!')
    sys.exit(0)

app = Flask(__name__)
so = StackAPI('stackoverflow', key=se_key)

# Main route that processes all incoming commands and queries to Matterflow
# All helper methods are stored in helpers.py for organization sake
@app.route('/so', methods=['post'])
def stackoverflow():
    values = request.values.get('text').split(' ', 1)
    command = values[0] # Matterflow command

    try:
        query = values[1]
    except IndexError:
        query = ''

    if command == 'search':
        return search.search(so, query)
    elif command == 'question':
        return question.search_by_id(so, query)
    elif command == 'help':
        return help.show()
    elif command == 'ask':
        return ask.link()
    else:
        return helpers.invalid_command()

@app.route('/')
def woops():
    return redirect('https://github.com/jackyliang/Matterflow')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
