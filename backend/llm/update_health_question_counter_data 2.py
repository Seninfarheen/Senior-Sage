import json
import os
from datetime import datetime

# Global file path for health questions
health_questions_file = 'health_questions.json'

# Ensure the user-specific log folder exists
USER_HEALTH_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_health_question_counter_logs')
os.makedirs(USER_HEALTH_LOG_DIR, exist_ok=True)

# Load the health_questions.json file (containing questions and their frequencies)
def load_health_questions():
    try:
        with open(health_questions_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

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
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    for q_idx, data in questions.items():
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
            if counter_data[q_idx]["asked_date"] != None:
                diff = (datetime.fromisoformat(curr_date) - datetime.fromisoformat(counter_data[q_idx]["asked_date"])).days
                if diff == counter_data[q_idx]["freq"]:
                    counter_data[q_idx]["counter"]=False
                    counter_data[q_idx]["asked_date"]=None
                    counter_data[q_idx]["diff"]=0
                else:
                    counter_data[q_idx]["diff"] = diff

    
    save_user_health_question_counter(username, counter_data)
    # Create the 'questions_to_ask_stack.json' after update
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
    # the 'questions_to_ask_stack.json' after update
    create_questions_to_ask_stack(questions, counter_data, username)

# Create a JSON file with questions that have counter = False
def create_questions_to_ask_stack(questions, counter_data, username):
    # List of questions with counter = 0
    questions_to_ask = {}
    
    for q_idx, data in counter_data.items():
        if data["counter"] == False:
            if q_idx in questions:
                questions_to_ask[q_idx] = questions[q_idx]
    
    # Save the questions to ask in a new JSON file for a specific user.
    user_questions_to_ask_file = os.path.join(USER_HEALTH_LOG_DIR, f"{username}_questions_to_ask_stack.json")
    try:
        with open(user_questions_to_ask_file, 'w') as f:
            json.dump(questions_to_ask, f, indent=4)
        print(f"Questions to ask stack updated successfully: {len(questions_to_ask)} questions")
    except IOError as e:
        print(f"Error saving questions to ask stack: {e}")
