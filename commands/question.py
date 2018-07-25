from helpers import COUNT, get_answer_emoji
from flask import jsonify

# Generates the rows of the table containing the answers to a given question
def generate_answers(answers):
    score = answers['score']
    is_answered = get_answer_emoji(answers['is_accepted'])
    link = answers['link']
    return '| {} | {} | {} |'.format(score, is_answered, link)

# Gets all the answers given a question ID and generates a Markdown table
# Uses the following Stack Exchange APIs:
# - https://api.stackexchange.com/docs/answers-on-questions
# - https://api.stackexchange.com/docs/answers-by-ids
def search_by_id(so, query):
    if not query:
        return jsonify({'text': 'Please make sure your input is valid and not empty!'})

    answers = so.fetch('questions/{ids}/answers', ids=[query], sort='votes', order='desc', filter='!9Z(-wyPr8')['items']
    question_details = so.fetch('questions/{ids}', ids=[query], sort='votes', order='desc')['items']

    if len(question_details) < 1:
        return jsonify({'text': 'No questions found for ID: ' + query + '. Please make sure you have entered the right ID!'})
    else:
        title = question_details[0]['title']

    formatted_result = ['### All Answers for ' + title]
    formatted_result.append('| Score | Accepted | Link |\n'
                            '|:-----:|:--------:|:-----|')
    formatted_result.extend(map(generate_answers, answers[:COUNT]))
    return jsonify({'text': '\n'.join(formatted_result)})