from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allows requests from any origin

order_state = {
    'drinkType': '',
    'size': '',
    'milk': '',
    'extras': [],
    'name': ''
}

questions = [
    ('drinkType', "Hi! I'm your Brewtastic barista! What drink would you like?"),
    ('size', "What size would you prefer (small/medium/large)?"),
    ('milk', "What kind of milk would you like (regular/oat/soy)?"),
    ('extras', "Any extras you'd like (whipped cream, caramel, syrup, etc.)?"),
    ('name', "Can I have your name to put on the cup?")
]

def find_next_question():
    for key, question in questions:
        if key == 'extras' and (not order_state[key] or len(order_state[key]) == 0):
            return key, question
        elif not order_state[key]:
            return key, question
    return None, "All details collected!"

@app.route('/order', methods=['POST'])
def handle_order():
    data = request.json
    answer = data.get('answer', '').strip()
    key_to_update = data.get('update_key', '')

    # If new order is started (no key and no answer), reset the order state
    if not key_to_update and not answer:
        for k in order_state:
            order_state[k] = '' if isinstance(order_state[k], str) else []

    # Step 1: Update the last field answered
    if key_to_update:
        if key_to_update == 'extras':
            order_state['extras'] = [x.strip() for x in answer.split(",") if x.strip()]
        else:
            order_state[key_to_update] = answer

    next_key, next_question = find_next_question()

    # Step 3: If all fields are filled, save to JSON and return summary
    if not next_key:
        with open("order.json", "w") as f:
            json.dump(order_state, f, indent=2)
        return jsonify({
            'question': "Thank you! Here’s your order summary:",
            'order_state': order_state,
            'done': True
        })
    else:
        return jsonify({
            'question': next_question,
            'order_state': order_state,
            'update_key': next_key,
            'done': False
        })

@app.route('/')
def index():
    return '<h2>Brewtastic Barista Agent API is running.</h2>'

if __name__ == "__main__":
    app.run(debug=True)
