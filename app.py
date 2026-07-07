from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import pymysql
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB'),
        ssl={'ssl': {'ca': True}},
        cursorclass=pymysql.cursors.DictCursor
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = hash_password(data.get('password'))
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', 
                      (username, email, password))
        db.commit()
        db.close()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = hash_password(data.get('password'))
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', 
                      (email, password))
        user = cursor.fetchone()
        db.close()
        if user:
            return jsonify({'message': 'Login successful!', 'username': user['username']}), 200
        else:
            return jsonify({'error': 'Invalid email or password!'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are CyberShield AI, a smart assistant specialized in cybersecurity, networking, coding, and general knowledge. Be helpful, smart and concise."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1024
        )
        return jsonify({'response': completion.choices[0].message.content}), 200
    except Exception as e:
        print("CHAT ERROR:", str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/api/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get('password')
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append('Use at least 8 characters')

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append('Add uppercase letters')

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append('Add lowercase letters')

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append('Add numbers')

    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        score += 1
    else:
        feedback.append('Add special characters (!@#$%^&*)')

    if score <= 2:
        strength = 'Weak'
    elif score <= 3:
        strength = 'Medium'
    elif score == 4:
        strength = 'Strong'
    else:
        strength = 'Very Strong'

    return jsonify({'strength': strength, 'score': score, 'feedback': feedback}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)