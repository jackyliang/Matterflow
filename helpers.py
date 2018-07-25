import sys, urllib

from flask import Flask, request, redirect, jsonify
from stackapi import StackAPI

COUNT = 5 # max number of results

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

so = StackAPI('stackoverflow', key=se_key)

# Converts answered/accepted to a nice little emoji :)
def get_answer_emoji(is_answered):
    if is_answered == True:
        return ':white_check_mark:'
    else:
        return ':x:'

# Generates the rows of the table containing the questions from given search terms
def generate_search_results(result):
    score = result['score']
    is_answered = get_answer_emoji(result['is_answered'])
    link = result['link']
    title = '[' + result['title'] + '](' + link + ')'
    ans_count = result['answer_count']
    question_id = result['question_id']
    return '| {} | {} | {} | {} | {} |'.format(score, is_answered, title, ans_count, question_id)

# Generates the rows of the table containing the answers to a given question
def generate_answers(answers):
    score = answers['score']
    is_answered = get_answer_emoji(answers['is_accepted'])
    link = answers['link']
    return '| {} | {} | {} |'.format(score, is_answered, link)

# Generates the Google search link if there are no results returned by Stack Overflow's search
def get_google_search(query):
    google_url = 'https://www.google.com/search?q=' + urllib.parse.quote(query) + '&as_sitesearch=stackoverflow.com'
    return 'No results! But I created a [Google](' + google_url + ') search for you instead!'

# Gets all the questions of given search terms and generates a Markdown table
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

# Gets all the answers given a question ID and generates a Markdown table
def question(query):
    try:
        answers = so.fetch('questions/{ids}/answers', ids=[query], sort='votes', order='desc', filter='!9Z(-wyPr8')['items']
        title = so.fetch('questions/{ids}', ids=[query], sort='votes', order='desc')['items'][0]['title']
    except SyntaxError:
        response = jsonify({'text': 'Please make sure your input is valid and not empty!'})
        return response

    formatted_result = ['### All Answers for ' + title]
    formatted_result.append('| Score | Accepted | Link |\n'
                            '|:-----:|:--------:|:-----|')
    formatted_result.extend(map(generate_answers, answers[:COUNT]))
    return jsonify({'text': '\n'.join(formatted_result)})

# Prints a helpful message that describes all the features of Matterflow
def matterflow_help():
    help_text = ('### Matterflow\n'
    'Welcome to Matterflow, a Stack Overflow plugin for Mattermost!\n'
    'This integration offers functionality such as:\n'
    '- [/search](http://api.stackexchange.com/docs/answers-on-questions) `<search query>` - Get all the results for a certain search query\n'
    '- [/question](http://api.stackexchange.com/docs/answers-by-ids) `<question ID>` - Get all the answers for a specific question ID (which can be retrieved by `/search`)\n'
    '- [/ask](https://stackoverflow.com/questions/ask) - Gets a link for you to ask a question on Stack Overflow\n'
    '- and more to come!\n'
    'Created by Jacky Liang at https://github.com/jackyliang/Matterflow\n')

    return jsonify({'text': help_text})

# Generates a link to ask a question on Stack Overflow
def ask():
    ask_so_question = 'Can\'t find what you are looking for? Click [me](https://stackoverflow.com/questions/ask) to ask a question on Stack Overflow!'
    return jsonify({'text': ask_so_question})

# Makes sure users know what to do when a wrong command is entered
def invalid_command():
    return jsonify({'text': 'Sorry, I do not recognize your command! Use `/so help` for a list of all available commands.'})