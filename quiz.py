import json
import random
import re

def generate_quiz_from_json(input_data: dict) -> dict:
    topic = input_data.get("topic", "General Topic").strip()
    num_questions = int(input_data.get("num_questions", 5))
    if not topic:
        return {"error": "Missing 'topic' in input JSON."}
    quiz = []
    for i in range(num_questions):
        qtype = random.choice(['mcq', 'true_false', 'fill_blank'])
        if qtype == 'mcq':
            quiz.append({
                'question': f"Q{i+1}: What is a key concept in {topic}?",
                'options': [f"Option {chr(65+j)}" for j in range(4)],
                'answer': "Option A",
                'type': 'mcq'
            })
        elif qtype == 'true_false':
            quiz.append({
                'question': f"Q{i+1}: Is this statement about {topic} true or false?",
                'options': ["True", "False"],
                'answer': "True",
                'type': 'true_false'
            })
        else:
            quiz.append({
                'question': f"Q{i+1}: Fill in the blank for {topic}.",
                'options': [f"Blank {j+1}" for j in range(3)],
                'answer': "Blank 1",
                'type': 'fill_blank'
            })
    return {"quiz": quiz}
