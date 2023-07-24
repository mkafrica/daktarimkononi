import re
import long_responses as long
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses ------------------------------------------------------------------------
    response("hello too!", ["hi", "sup", "hey"], single_response=True)
    response("I\"m doing fine, and you", ["how", "are", "you"], required_words=["how"])
    response("AIDS is a diseases that is transmitted via a virus called AIDS ", ["AIDS", "HIV", "DEADLY"], required_words=["aids"])
    response("AIDS is a Disease caused by HIV. do you how how it is transmitted and how to prevent yourself from being infected", ["deadly", "hiv", "death"], required_words=["death"])
    response(long.R_EATING, ["explain", "you"], required_words=["you,", "explain"])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    response = get_response(user_input)
    return jsonify({'bot_response': response})

def get_response(user_input):
    split_message = re.split(r"\s+|[,;?.-]\s*", user_input.lower())
    response = check_all_messages(split_message)
    return response

if __name__ == '__main__':
    app.run(debug=True)
