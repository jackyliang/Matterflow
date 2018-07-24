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
    return 'No results!\nHere\'s a custom [Google](' + google_url + ') search!'

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

def generate_answers(answers):
    score = answers['score']
    is_answered = get_answer_emoji(answers['is_accepted'])
    link = answers['link']
    return '| {} | {} | {} |'.format(score, is_answered, link)

def question(query):
    try:
        answers = so.fetch('questions/{ids}/answers', ids=[query], sort='activity', order='desc', filter='!9Z(-wyPr8')['items']
        title = so.fetch('questions/{ids}', ids=[query], sort='votes', order='desc')['items'][0]['title']
    except SyntaxError:
        response = jsonify({'text': 'Please make sure your input is valid and not empty!'})
        return response

    formatted_result = ['### ' + title]
    formatted_result.append('| Score | Answered | Link |\n'
                            '|:-----:|:--------:|:-----|')
    formatted_result.extend(map(generate_answers, answers[:COUNT]))
    return jsonify({'text': '\n'.join(formatted_result)})

# Queries the Stack Overflow Search API and returns a Markdown table of results
@app.route('/so', methods=['post'])
def stackoverflow():
    values = request.values.get('text').split(' ', 1)
    command = values[0]
    query = values[1]
    if command == 'search':
        return search(query)
    elif command == 'question':
        return question(query)

@app.route('/')
def hello():
    return Response('Hello!')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
