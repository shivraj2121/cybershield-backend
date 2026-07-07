# CyberShield Backend — Flask REST API

Python Flask backend for CyberShield AI cybersecurity web application.

## Features
- 🤖 AI Chat API using Groq (LLaMA 3.3)
- 🔐 Password Strength Analyzer
- 👤 User Authentication (Register/Login)
- 🗄️ MySQL Database Integration

## Tech Stack
- Python 3.14
- Flask
- Groq AI API
- MySQL / PyMySQL
- Flask-CORS
- Python-dotenv

## Setup & Run
1. Clone the repository
   git clone https://github.com/shivraj2121/cybershield-backend.git
2. Create virtual environment
   python -m venv venv
   source venv/Scripts/activate
3. Install dependencies
   pip install flask flask-cors groq pymysql python-dotenv
4. Create .env file
   GROQ_API_KEY=your_key_here
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DB=cybershield
5. Run the server
   python app.py
6. Server runs on http://127.0.0.1:5000

## Frontend
https://github.com/shivraj2121/cybershield-frontend