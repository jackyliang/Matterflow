from flask import jsonify

COUNT = 5 # max number of results

# Converts answered/accepted to a nice little emoji :)
def get_answer_emoji(is_answered):
    if is_answered == True:
        return ':white_check_mark:'
    else:
        return ':x:'

# Makes sure users know what to do when a wrong command is entered
def invalid_command():
    return jsonify({'text': 'Sorry, I do not recognize your command! Use `/so help` for a list of all available commands.'})