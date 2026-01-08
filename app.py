from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
# from model.model import generate_mental_health_response
from model.rag import retrieve_response 
# from sentence_transformers import SentenceTransformer


load_dotenv()

# print("Loading model...")
# model = SentenceTransformer('all-MiniLM-L6-v2')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/emergency')
def emergency():
    return render_template('phone.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Thik se daal BKL'}), 400

    try:
        response_text, category = retrieve_response(user_message)
        return jsonify({'response': response_text, 'category': category})
    except Exception as e:
        print(f"Error : {e}")
        return jsonify({'error': 'Failed to generate response'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
