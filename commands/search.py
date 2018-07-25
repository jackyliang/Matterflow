from urllib import parse
from flask import jsonify
from helpers import COUNT, get_answer_emoji

# Generates the rows of the table containing the questions from given search terms
def generate_search_results(result):
    score = result['score']
    is_answered = get_answer_emoji(result['is_answered'])
    link = result['link']
    title = '[' + result['title'] + '](' + link + ')'
    ans_count = result['answer_count']
    question_id = result['question_id']
    return '| {} | {} | {} | {} | {} |'.format(score, is_answered, title, ans_count, question_id)

# Generates the Google search link if there are no results returned by Stack Overflow's search
def get_google_search(query):
    google_url = 'https://www.google.com/search?q=' + urllib.parse.quote(query) + '&as_sitesearch=stackoverflow.com'
    return 'No results! But I created a [Google](' + google_url + ') search for you instead!'

# Gets all the questions of given search terms and generates a Markdown table
def search(so, query):
    if not query:
        return jsonify({'text': 'Please make sure your input is valid and not empty!'})

    result = so.fetch('search', intitle=query, sort='relevance', order='desc')['items']

    formatted_result = ['### Stack Overflow Questions For: ' + query]

    if len(result) < 1:
        formatted_result.append(get_google_search(query))
    else:
        formatted_result.append('| Score | Answered | Title | # of Answers | Question ID | \n'
                                '|:-----:|:--------:|:------|:------------:|:-----------:|')
        formatted_result.extend(map(generate_search_results, result[:COUNT]))

    return jsonify({'text': '\n'.join(formatted_result)})