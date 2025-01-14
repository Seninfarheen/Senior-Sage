import json
import os
import re
from datetime import datetime, timedelta
from voice_interactions import stt_whisper, tts_whisper
from update_health_question_counter_data import update_health_question_counter, save_user_health_question_counter, load_health_questions

from datetime import datetime
from voice_interactions import tts_whisper

# Base directory is the folder containing this script file (assuming it's in "llm" folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths using os.path.join() for OS independence
USER_INFO_FILE = os.path.join(BASE_DIR, 'user_info.json')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
REMINDER_DIR = os.path.join(BASE_DIR, 'reminder')
health_questions_file = os.path.join(BASE_DIR,'health_questions.json')
USER_HEALTH_LOG_DIR = os.path.join(BASE_DIR, 'health_question_counter')
USER_HEALTH_QUESTIONS_DIR = os.path.join(BASE_DIR, 'questions_to_ask')

os.makedirs(USER_HEALTH_LOG_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(REMINDER_DIR, exist_ok=True)

def load_health_questions():
    try:
        with open(health_questions_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
questions = load_health_questions()

# **Updated function to load user-specific health question counters**
def load_user_health_question_counter(username):
    """Load health question counter for a specific user."""
    user_health_counter_file = os.path.join(USER_HEALTH_LOG_DIR, f"{username}_health_question_counter.json")
    if os.path.exists(user_health_counter_file):
        try:
            with open(user_health_counter_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {user_health_counter_file} is corrupted. Starting with empty counter.")
    return {} 

# **Function to update the health question counter**
def initialize_health_question_counter(questions, counter_data, username):
    for q_idx, data in questions.items():
        curr_date = datetime.now().isoformat()
        if q_idx not in counter_data:
            # If question is not in the counter, add it
            counter_data[q_idx] = {
                "counter": False,
                "freq": data["freq"],
                "asked_date": None,
                "curr_date": curr_date,
                "diff": 0  # No difference yet, as it's just added
            }
        else:
            counter_data[q_idx]["curr_date"] = curr_date
            curr_date = counter_data[q_idx]["curr_date"][:10]  # Extract only the date part (YYYY-MM-DD)
            asked_date = counter_data[q_idx]["asked_date"][:10] if counter_data[q_idx]["asked_date"] else None

            if asked_date:
                diff = (datetime.fromisoformat(curr_date) - datetime.fromisoformat(asked_date)).days
                if diff >= counter_data[q_idx]["freq"]:
                    counter_data[q_idx]["counter"] = False
                    counter_data[q_idx]["asked_date"] = None
                    counter_data[q_idx]["diff"] = 0
                else:
                    counter_data[q_idx]["diff"] = diff

    save_user_health_question_counter(username, counter_data)
    create_questions_to_ask_stack(questions, counter_data, username)

    return counter_data

# Save the updated health_question_counter for a specific user
def save_user_health_question_counter(username, counter_data):
    user_counter_file = os.path.join(USER_HEALTH_LOG_DIR, f"{username}_health_question_counter.json")
    try:
        with open(user_counter_file, 'w') as f:
            json.dump(counter_data, f, indent=4)
    except IOError as e:
        print(f"Error saving health question counter for {username}: {e}")

def update_health_question_counter(username, q_idx, counter_data):
    counter_data[q_idx]['counter'] = True
    counter_data[q_idx]['asked_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_questions_to_ask_stack(questions, counter_data, username)


def create_questions_to_ask_stack(questions, counter_data, username):
    # List of questions with counter = 0
    questions_to_ask = {}
    
    for q_idx, data in counter_data.items():
        if data["counter"] == False:
            if q_idx in questions:
                questions_to_ask[q_idx] = questions[q_idx]
    
    # Save the questions to ask in a new JSON file for a specific user.
    user_questions_to_ask_file = os.path.join(USER_HEALTH_QUESTIONS_DIR, f"{username}_questions_to_ask_stack.json")
    try:
        with open(user_questions_to_ask_file, 'w') as f:
            json.dump(questions_to_ask, f, indent=4)
        print(f"Questions to ask stack updated successfully: {len(questions_to_ask)} questions")
    except IOError as e:
        print(f"Error saving questions to ask stack: {e}")

def select_voice():
    """Prompt the user to select a voice and return the selected voice."""
    voice_select_message = "Please select the voice of your choice"
    tts_whisper(voice_select_message)
    print("Please choose a voice to converse with:")
    print("1. Alloy\n2. Echo\n3. Fable\n4. Onyx\n5. Nova\n6. Shimmer")
    dic = {"1": "Alloy", "2": "Echo", "3": "Fable", "4": "Onyx", "5": "Nova", "6": "Shimmer"}
    while True:
        ip = input("Select an option (1-6):\t").strip()
        if ip in dic:
            return dic[ip]
        else:
            print("Invalid selection. Please choose a number between 1 and 6.")

def load_json_data(file_path, default_value):
    """General function to load JSON data with error handling."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {file_path} is corrupted. Returning default value.")
    return default_value

def load_user_info():
    """Load user information from a JSON file."""
    return load_json_data(USER_INFO_FILE, {})

def load_user_logs(username):
    """Load conversation logs for a specific user."""
    log_file = os.path.join(LOGS_DIR, f"{username}.json")
    return load_json_data(log_file, [])

def load_user_reminders(username):
    """Load reminders for a specific user."""
    reminder_file = os.path.join(REMINDER_DIR, f"{username}_reminders.json")
    return load_json_data(reminder_file, [])

def save_data(file_path, value, username = "all"):
    try:
        with open(file_path, 'w') as f:
            json.dump(value, f, indent=4)
    except IOError as e:
        print(f"Error saving file at location: {file_path} for {username}")

def save_user_info(user_info):
    """Save user information to a JSON file."""
    save_data(USER_INFO_FILE, user_info)

def save_user_logs(username, logs):
    """Save conversation logs for a specific user."""
    log_file = os.path.join(LOGS_DIR, f"{username}.json")
    save_data(log_file, logs, username)

def save_user_reminders(username, reminders):
    """Save reminders for a specific user."""
    reminder_file = os.path.join(REMINDER_DIR, f"{username}_reminders.json")
    save_data(reminder_file, reminders, username)

def add_reminder(username, reminder_details):
    """Add a new reminder to the user's reminders list."""
    reminders = load_user_reminders(username)
    reminders.append(reminder_details)
    save_user_reminders(username, reminders)

def add_preferences(username, reminder_details):
    """Add a new preference to the user's preferences list."""
    reminders = load_user_reminders(username)
    reminders.append(reminder_details)
    save_user_reminders(username, reminders)

def append_conversation(username, conversation):
    """Append a completed conversation session to the user's log."""
    logs = load_user_logs(username)
    logs.append(conversation)
    save_user_logs(username, logs)
