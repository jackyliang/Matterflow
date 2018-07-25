from flask import jsonify

# Generates a link to ask a question on Stack Overflow
def link():
    ask_so_question = 'Can\'t find what you are looking for? Click [me](https://stackoverflow.com/questions/ask) to ask a question on Stack Overflow!'
    return jsonify({'text': ask_so_question})