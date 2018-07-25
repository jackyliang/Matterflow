from flask import jsonify

# Prints a helpful message that describes all the features of Matterflow
def show():
    help_text = ('### Matterflow\n'
    'Welcome to Matterflow, a Stack Overflow plugin for Mattermost!\n'
    'This integration offers functionality such as:\n'
    '- [/search](http://api.stackexchange.com/docs/answers-on-questions) `<search query>` - Get all the results for a certain search query\n'
    '- [/question](http://api.stackexchange.com/docs/answers-by-ids) `<question ID>` - Get all the answers for a specific question ID (which can be retrieved by `/search`)\n'
    '- [/ask](https://stackoverflow.com/questions/ask) - Gets a link for you to ask a question on Stack Overflow\n'
    '- and more to come!\n'
    'Created by Jacky Liang at https://github.com/jackyliang/Matterflow\n')

    return jsonify({'text': help_text})