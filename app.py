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

so = SITE = StackAPI('stackoverflow')
app = Flask(__name__)

# Takes the JSON response and outputs the corresponding rows of the table
def get_result(result):
    return '| {} | {} | {} | {} | {} |'.format(result['score'], result['is_answered'],  result['title'], result['answer_count'], result['link'])

# Queries the Stack Overflow Search API and returns a Markdown table of results
@app.route('/search', methods=['post'])
def search():
    query = request.values.get('text')
    try:
        result = so.fetch('search', intitle=query, sort='relevance', order='desc')['items']
    except SyntaxError:
        response = jsonify({'text': 'Please make sure your input is valid and not empty!'})
        return response

    if len(result) < 1:
        google_url = 'https://www.google.com/search?q=' + urllib.parse.quote(query) + '&as_sitesearch=stackoverflow.com'
        return jsonify({'text': 'No results!\nHere\'s a custom [Google](' + google_url + ') search!'})

    formatted_result = ['### Stack Overflow Answers For: ' + query]
    formatted_result.append('| Score | Answered | Title | # of Answers | URL |\n'
                            '|:------|:---------|:------|:-------------|:----|')
    formatted_result.extend(map(get_result, result[:5]))
    response = jsonify({'text': '\n'.join(formatted_result)})
    return response

@app.route('/')
def hello():
    return Response('Hello!')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
