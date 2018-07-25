import os

from flask import Flask, request, redirect
from helpers import *

app = Flask(__name__)

# Main route that processes all incoming commands and queries to Matterflow
# All helper methods are stored in helpers.py for organization sake
@app.route('/so', methods=['post'])
def stackoverflow():
    values = request.values.get('text').split(' ', 1)
    command = values[0] # Matterflow command
    if command == 'search':
        return search(values[1])
    elif command == 'question':
        return question(values[1])
    elif command == 'help':
        return matterflow_help()
    elif command == 'ask':
        return ask()
    else:
        return invalid_command()

@app.route('/')
def woops():
    return redirect('https://github.com/jackyliang/Matterflow')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
