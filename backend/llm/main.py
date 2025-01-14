import re
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from voice_interactions import stt_whisper, tts_whisper, record_audio
from chat_completion import openai_complete
from update_health_question_counter_data import update_health_question_counter, save_user_health_question_counter, load_health_questions
from helper import *
from rag import load_vector_db, create_vector_db
# from emotion_detection import analyze_emotion

def main_func():
    user_info = load_user_info()
    questions = load_health_questions()
    

    print("Login:\n")
    login_message = "Please enter your name to login and continue your conversation:"
    tts_whisper(login_message)
    name = input("Enter your name to continue your conversation:\t").strip()
    
    if not name:
        name_empty_message = "Name cannot be empty. Exiting."
        tts_whisper(name_empty_message)
        return
    
    if name not in user_info:
        welcome_message = f"Welcome to the VA, {name}!"
        tts_whisper(welcome_message)
        voice = select_voice()
        user_info[name] = voice
        save_user_info(user_info)
    else:
        voice = user_info[name]
        welcome_back_message = f"Welcome back, {name}! Your selected voice is: {voice}"
        tts_whisper(welcome_back_message)

    
    past_logs = load_user_logs(name)
    context = []
    for session in past_logs:
        for entry in session.get('messages', []):
            context.append((entry['timestamp'], entry['user_message'], entry['bot_response']))

    counter_data = load_user_health_question_counter(name)
    initialize_health_question_counter(questions, counter_data, name)

    SAVE_DIR = os.path.join(BASE_DIR, "vector_db")
    if os.path.exists(SAVE_DIR):
        embeddings = OpenAIEmbeddings()
        vector_db = load_vector_db(SAVE_DIR, embeddings)
    else:
        vector_db = create_vector_db(SAVE_DIR)
    
    counter_data = load_user_health_question_counter(name)
    # Initialize the health questions counter for all the new questions in the health quessionaire; 
    # and update the current date and diff everytime a user logs in
    initialize_health_question_counter(questions, counter_data, name)

    print("\nYou can start your conversation. Say 'exit' to end.")
    
    cur_time = datetime.now().isoformat()
    current_conversation = {
        'timestamp': cur_time,
        'messages': []
    } 
    
    while True:
        record_audio()
        audio_file = open("user_response.wav", "rb")
        user_message = stt_whisper(audio_file).strip()
        # user_message = input()
        
        if user_message.lower() == 'exit':
            print("Ending conversation session.")
            break
        
        print(f"You: {user_message}")
        bot_response = openai_complete(name, user_message, context, vector_db, voice)
        cur_time = datetime.now().isoformat()
        context.append((cur_time, user_message, bot_response))

        if "alright then" in re.sub(r'[^\w\s]', '', bot_response).lower() or "have a great day ahead" in re.sub(r'[^\w\s]', '', bot_response).lower():
            current_conversation['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response
            })
            break
        
        current_conversation['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response
        })


    
    append_conversation(name, current_conversation)
    print(f"Conversation session saved for user '{name}'.")

    # # Emotion detection for the current session
    # analyze_emotion(current_conversation)

if __name__ == "__main__":
    main_func()

