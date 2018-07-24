import os, sys, stackexchange, urllib

from stackexchange import Site, StackOverflow, Sort
from flask import Flask, request, Response, redirect, jsonify

try:
    import config
    se_key = config.SE_KEY
except:
    se_key = os.environ.get('SE_KEY')

if not se_key:
    print('Please make sure you have a config.py file!')
    sys.exit(0)

so = Site(StackOverflow, se_key)
app = Flask(__name__)

def get_result(result):
    result_json = result.json
    return ':arrow_up_small: {} | {} | {}'.format(result_json['score'], result.url, result.title)

@app.route('/matterflow-search', methods=['post'])
def search():
    query = request.values.get('text')
    try:
        result = so.search(intitle=query, sort='relevance', order='desc')
    except SyntaxError:
        response = jsonify({'text': 'Please make sure your input is valid and not empty!'})
        return response

    print(len(result))

    if len(result) < 1:
        google_url = 'https://www.google.com/search?q=' + urllib.quote_plus(query) + '&as_sitesearch=stackoverflow.com'
        return jsonify({'text': 'No results!\nTry searching [Google](' + google_url + ') instead!'})

    formatted_result = ['### Stack Overflow Answers For: ' + query]
    formatted_result.append('| Score | URL | Title |\n'
                            '|:------|:----|:------|')
    formatted_result.extend(map(get_result, result[:5]))
    response = jsonify({'text': '\n'.join(formatted_result)})
    return response

@app.route('/')
def hello():
    return Response('Hello!')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
