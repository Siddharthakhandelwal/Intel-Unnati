# AI Classroom Assistant

## Overview
A modern, full-stack web application for students and teachers to:
- Chat with an AI assistant
- Generate assignments and quizzes
- Solve math problems from images
- Track learning progress (demo)
- Register, log in, and manage user accounts

## Features
- **User Authentication:** Signup, login, logout, and dashboard (demo, in-memory)
- **Chatbot:** Ask questions and get instant AI answers
- **Assignment Generator:** Create custom assignments by subject, topic, and type
- **Quiz Generator:** Generate and take quizzes, auto-check answers, and get instant feedback
- **Math Image Solver:** Upload a math problem image and get a solution
- **Clean, modern UI:** Responsive, easy to use, and mobile-friendly

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **AI/ML:** Demo logic for quizzes and assignments, Groq API for chatbot (configurable), math solver with transformers/torch

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```
3. **Activate the environment:**
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```sh
     source venv/bin/activate
     ```
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Set up environment variables:**
   - Create a `.env` file in the root directory:
     ```
     GROQ_API_KEY=your_groq_api_key
     GROQ_MODEL=your_groq_model
     ```
   - (Optional) Configure other API keys as needed.
6. **Run the app:**
   ```sh
   python app.py
   ```
7. **Open your browser:**
   - Go to [http://localhost:5000/](http://localhost:5000/)

## Usage Guide
- **Signup/Login:** Required to access the app. Your session is stored in memory (demo only).
- **Dashboard:** Shows your name and email. (No persistent data yet.)
- **Assignment Generator:** Fill the form, click Generate, and get dynamic questions.
- **Quiz Section:** Generate a quiz, answer questions, and submit to see your score and feedback.
- **Ask Query:**
  - Text Query: Ask any question.
  - Math Image Query: Upload a math problem image and get a solution.

## Troubleshooting
- **Math Solver errors:**
  - Requires `torch`, `transformers`, and `Pillow`. Install Visual C++ Redistributable on Windows if you see DLL errors.
- **Quiz generator errors:**
  - Now uses demo logic, no external dependencies required.
- **Session/auth issues:**
  - User data is in-memory only. Restarting the server will clear all users.
- **API keys:**
  - Make sure to set your Groq API key in `.env` for chatbot functionality.

## Customization & Contribution
- Add persistent storage (database) for real user data.
- Integrate more advanced AI models for quizzes/assignments.
- Fork and PRs welcome!

## License
MIT (or specify your license) 