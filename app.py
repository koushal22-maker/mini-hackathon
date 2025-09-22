import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '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')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

@app.route('/api/symptoms', methods=['POST'])
def get_solution():
    data = request.get_json()
    symptoms = data.get('symptoms', '')
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'moonshotai/kimi-k2-instruct-0905',
        'messages': [
            {'role': 'system', 'content': 'You are an expert healthcare assistant. When answering, provide the solution in only the most important main points or bullet points. Be concise.'},
            {'role': 'user', 'content': f'My symptoms are: {symptoms}'}
        ]
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
        if response.status_code != 200:
            print('Groq API error:', response.status_code, response.text)
            return jsonify({'error': f'Groq API error {response.status_code}: {response.text}'}), response.status_code
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return jsonify({'solution': answer})
    except Exception as e:
        print('Exception during Groq API call:', str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
