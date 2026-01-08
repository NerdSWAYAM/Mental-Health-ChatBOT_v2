from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
# from model.model import generate_mental_health_response
from model.rag import retrieve_response
from model.db import init_db, add_user, authenticate_user 
# from sentence_transformers import SentenceTransformer


load_dotenv()

# print("Loading model...")
# model = SentenceTransformer('all-MiniLM-L6-v2')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/health')
def health_check():
    return "OK", 200

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

@app.route('/api/signup', methods=['POST'])
def signup_api():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if not all([first_name, last_name, email, password]):
        return jsonify({'error': 'All fields are required'}), 400

    success, message = add_user(first_name, last_name, email, password)
    if success:
        return jsonify({'message': message}), 201
    else:
        # If user exists, we return 409 Conflict, but frontend can handle it
        if "exists" in message:
            return jsonify({'error': message}), 409
        return jsonify({'error': message}), 500

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    success, message = authenticate_user(email, password)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 401

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
    init_db()
    app.run(host="0.0.0.0", debug="True")
