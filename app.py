import os, sys, urllib

from stackapi import StackAPI
from flask import Flask, request, Response, redirect, jsonify

try:
    import config
    se_key = config.SE_KEY
except:
    se_key = os.environ.get('SE_KEY')

if not se_key:
    print('Please make sure you have a config.py file!')
    sys.exit(0)

so = StackAPI('stackoverflow', key=se_key)
app = Flask(__name__)
COUNT = 5

def get_answer_emoji(is_answered):
    if is_answered == True:
        return ':white_check_mark:'
    else:
        return ':x:'

# Takes the JSON response and outputs the corresponding rows of the table
def generate_search_results(result):
    score = result['score']
    is_answered = get_answer_emoji(result['is_answered'])
    link = result['link']
    title = '[' + result['title'] + '](' + link + ')'
    ans_count = result['answer_count']
    question_id = result['question_id']
    return '| {} | {} | {} | {} | {} |'.format(score, is_answered, title, ans_count, question_id)

def get_google_search(query):
    google_url = 'https://www.google.com/search?q=' + urllib.parse.quote(query) + '&as_sitesearch=stackoverflow.com'
    return 'No results! But I created a [Google](' + google_url + ') search for you instead!'

def generate_answers(answers):
    score = answers['score']
    is_answered = get_answer_emoji(answers['is_accepted'])
    link = answers['link']
    return '| {} | {} | {} |'.format(score, is_answered, link)

def search(query):
    try:
        result = so.fetch('search', intitle=query, sort='relevance', order='desc')['items']
    except SyntaxError:
        return jsonify({'text': 'Please make sure your input is valid and not empty!'})

    formatted_result = ['### Stack Overflow Answers For: ' + query]

    if len(result) < 1:
        formatted_result.append(get_google_search(query))
    else:
        formatted_result.append('| Score | Answered | Title | # of Answers | Question ID | \n'
                                '|:-----:|:--------:|:------|:------------:|:-----------:|')
        formatted_result.extend(map(generate_search_results, result[:COUNT]))

    return jsonify({'text': '\n'.join(formatted_result)})

def question(query):
    try:
        answers = so.fetch('questions/{ids}/answers', ids=[query], sort='votes', order='desc', filter='!9Z(-wyPr8')['items']
        title = so.fetch('questions/{ids}', ids=[query], sort='votes', order='desc')['items'][0]['title']
    except SyntaxError:
        response = jsonify({'text': 'Please make sure your input is valid and not empty!'})
        return response

    formatted_result = ['### ' + title]
    formatted_result.append('| Score | Answered | Link |\n'
                            '|:-----:|:--------:|:-----|')
    formatted_result.extend(map(generate_answers, answers[:COUNT]))
    return jsonify({'text': '\n'.join(formatted_result)})

def matterflow_help():
    help_text = ('### Matterflow\n'
    'Welcome to Matterflow, a Stack Overflow plugin for Mattermost!\n'
    'This integration offers functionality such as:\n'
    '- [/search](http://api.stackexchange.com/docs/answers-on-questions) `<search query>` - Get all the results for a certain search query\n'
    '- [/question](http://api.stackexchange.com/docs/answers-by-ids) `<question ID>` - Get all the answers for a specific question ID (which can be retrieved by `/search`)\n'
    '- and more to come!\n'
    'Created by Jacky Liang at https://github.com/jackyliang/Matterflow\n')

    return jsonify({'text': help_text})

def ask():
    ask_so_question = 'Can\'t find what you are looking for? Click [me](https://stackoverflow.com/questions/ask) to ask a question on Stack Overflow!'
    return jsonify({'text': ask_so_question})

def invalid_command():
    return jsonify({'text': 'Sorry, I do not recognize your command! Use `/so help` for a list of all available commands.'})

# TODO
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
def hello():
    return Response('Looks like you shouldn\'t be here! Check out the repo instead: https://github.com/jackyliang/Matterflow')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
