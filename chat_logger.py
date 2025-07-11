from datetime import datetime

def log_chat_to_txt(user_query, bot_response, file_path='chat_logs.txt'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] User: {user_query}\n")
        f.write(f"[{timestamp}] Bot: {bot_response}\n")
        f.write("-------------------------------------------------------\n")
