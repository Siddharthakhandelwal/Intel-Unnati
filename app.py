from flask import Flask, request, jsonify, send_from_directory, session
from flask import redirect
from chatbot import get_chatbot_response
from chat_logger import log_chat_to_txt   # Import the logger
import os
import random

# Import math_solver and quiz features
from math_solver import solve_math_from_image
from quiz import generate_quiz_from_json

app = Flask(__name__, static_folder='webapp', static_url_path='')
app.secret_key = 'demo_secret_key'  # For session management (demo only)

# In-memory user store for demo
USERS = {}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if username in USERS:
        return jsonify({'error': 'Username already exists'}), 400
    USERS[username] = {'password': password, 'name': data.get('name', username)}
    session['username'] = username
    return jsonify({'message': 'Signup successful', 'username': username, 'name': USERS[username]['name']})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid username or password'}), 401
    session['username'] = username
    return jsonify({'message': 'Login successful', 'username': username, 'name': user['name']})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session.get('username')
    if not username or username not in USERS:
        return jsonify({'error': 'Not logged in'}), 401
    user = USERS[username]
    return jsonify({'username': username, 'name': user['name']})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    user_query = data['query']
    print(f"[User]: {user_query}")

    try:
        response = get_chatbot_response(user_query)
        print(f"[Bot]: {response}")

        # Log chat to txt file
        log_chat_to_txt(user_query, response)

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Math solver endpoint (expects an image file upload)
@app.route('/solve-math', methods=['POST'])
def solve_math():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    image = request.files['image']
    image_path = os.path.join('temp_upload', image.filename)
    os.makedirs('temp_upload', exist_ok=True)
    image.save(image_path)
    result = solve_math_from_image(image_path)
    os.remove(image_path)
    return jsonify({'result': result})

# Quiz generator endpoint
@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing input data'}), 400
    result = generate_quiz_from_json(data)
    return jsonify(result)

# Assignment generator endpoint
@app.route('/generate-assignment', methods=['POST'])
def generate_assignment():
    data = request.get_json()
    subject = data.get('subject', 'General')
    topic = data.get('topic', 'General Topic')
    difficulty = data.get('difficulty', 'Intermediate')
    number_of_questions = int(data.get('number_of_questions', 5))
    assignment_type = data.get('assignment_type', 'mixed')
    
    # Simple demo question templates
    templates = {
        'mcq': lambda i: f"Q{i+1}. [MCQ] What is a key concept in {topic} ({subject})?",
        'short-answer': lambda i: f"Q{i+1}. [Short Answer] Explain a principle of {topic} in {subject}.",
        'essay': lambda i: f"Q{i+1}. [Essay] Discuss the importance of {topic} in {subject}.",
        'problem-solving': lambda i: f"Q{i+1}. [Problem] Solve a problem related to {topic} in {subject}.",
        'mixed': lambda i: random.choice([
            f"Q{i+1}. [MCQ] What is a key concept in {topic} ({subject})?",
            f"Q{i+1}. [Short Answer] Explain a principle of {topic} in {subject}.",
            f"Q{i+1}. [Essay] Discuss the importance of {topic} in {subject}.",
            f"Q{i+1}. [Problem] Solve a problem related to {topic} in {subject}."
        ])
    }
    gen = templates.get(assignment_type, templates['mixed'])
    questions = [gen(i) for i in range(number_of_questions)]
    return jsonify({
        'subject': subject,
        'topic': topic,
        'difficulty': difficulty,
        'number_of_questions': number_of_questions,
        'assignment_type': assignment_type,
        'questions': questions
    })

@app.route('/check-quiz-answers', methods=['POST'])
def check_quiz_answers():
    data = request.get_json()
    quiz = data.get('quiz', [])
    user_answers = data.get('answers', [])
    results = []
    correct_count = 0
    for i, q in enumerate(quiz):
        correct = (user_answers[i] == q.get('answer'))
        results.append({
            'question': q.get('question'),
            'your_answer': user_answers[i],
            'correct_answer': q.get('answer'),
            'is_correct': correct
        })
        if correct:
            correct_count += 1
    score = int((correct_count / len(quiz)) * 100) if quiz else 0
    return jsonify({'score': score, 'results': results, 'total': len(quiz), 'correct': correct_count})

# Serve static files (frontend)
@app.route('/')
def serve_index():
    username = session.get('username')
    if not username or username not in USERS:
        return redirect('/login.html')
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)