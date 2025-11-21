from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/say', methods=['POST'])
def say():
    data = request.json
    text = data.get('text', '')
    return jsonify({'response': f'You said: {text}'})


if __name__ == '__main__':
    app.run(debug=True)
