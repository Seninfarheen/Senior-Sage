import json
import os
from helper import *
from datetime import timedelta, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_FILE = os.path.join(BASE_DIR, 'curr_response.json')
HEALTH_QUESTIONS_FILE = os.path.join(BASE_DIR, 'health_questions.json')
TASKS_FILE = os.path.join(BASE_DIR, 'tasks.json')
USER_REWARDS_DIR = os.path.join(BASE_DIR, 'user_rewards')

def reminders(username:str, remind:dict) -> None:
    add_reminder(username, remind)
    return

def preferences(username: str, preference_type: str, preference_detail: str, sentiment: str):
    """
    Store user preferences in a JSON file. Each user has their own preferences file that maintains
    a history of their stated preferences with timestamps.
    
    Args:
        username (str): The user's name
        preference_type (str): Category of the preference (food, hobby, etc.)
        preference_detail (str): Detailed description of the preference
        sentiment (str): Whether it's a like, dislike, or neutral preference
    """
    # Create preferences directory if it doesn't exist
    preferences_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_preferences')
    os.makedirs(preferences_dir, exist_ok=True)
    
    # Path to user's preferences file
    preferences_file = os.path.join(preferences_dir, f"{username.lower()}_preferences.json")
    
    try:
        # Load existing preferences if file exists
        if os.path.exists(preferences_file):
            with open(preferences_file, 'r', encoding='utf-8') as f:
                preferences = json.load(f)
        else:
            preferences = {
                "user": username,
                "last_updated": None,
                "preferences": []
            }
        
        # Create new preference entry
        new_preference = {
            "type": preference_type,
            "detail": preference_detail,
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Add new preference to the list
        preferences["preferences"].append(new_preference)
        preferences["last_updated"] = datetime.now().isoformat()
        
        # Write updated preferences back to file
        with open(preferences_file, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully stored preference for {username}: {preference_detail}")
        return True
        
    except Exception as e:
        print(f"Error storing preference for {username}: {str(e)}")
        raise

def get_user_preferences(username: str) -> dict:
    """
    Retrieve all stored preferences for a given user.
    
    Args:
        username (str): The user's name
        
    Returns:
        dict: Dictionary containing all user preferences
    """
    preferences_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_preferences')
    preferences_file = os.path.join(preferences_dir, f"{username.lower()}_preferences.json")
    
    try:
        if os.path.exists(preferences_file):
            with open(preferences_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error retrieving preferences for {username}: {str(e)}")
        return None

def get_preferences_by_type(username: str, preference_type: str) -> list:
    """
    Retrieve all preferences of a specific type for a given user.
    
    Args:
        username (str): The user's name
        preference_type (str): Type of preferences to retrieve (e.g., 'food', 'hobby')
        
    Returns:
        list: List of preferences of the specified type
    """
    preferences = get_user_preferences(username)
    if preferences and 'preferences' in preferences:
        return [
            pref for pref in preferences['preferences']
            if pref['type'] == preference_type
        ]
    return []

def responses(q_idx: int, username: str, user_answer: str) -> None:
    """
    Save user responses to health-related questions.
    
    Args:
        q_idx (int): Index of the question being answered
        user (str): Name of the user
        user_answer (str): User's response to the question
    """
    print("Processing health response...")
    
    try:
        try:
            with open(RESPONSES_FILE, 'r', encoding='utf-8') as file:
                curr_response = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            curr_response = {
                "user": "",
                "q_idx": 0,
                "Questions": "",
                "Answer": "",
                "Date": ""
            }
        try:
            with open(HEALTH_QUESTIONS_FILE, 'r', encoding='utf-8') as file:
                health_questions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading health questions: {e}")
            return 

        # Convert q_idx to string for dictionary lookup
        q_idx_str = str(q_idx)
        
        # Verify the question index exists
        if q_idx_str not in health_questions:
            print(f"Question index {q_idx} not found in health questions")
            return 

        # Update the response dictionary
        curr_response.update({
            "user": username,
            "q_idx": q_idx,
            "Questions": health_questions[q_idx_str],
            "Answer": user_answer,
            "Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        # Save the updated responses
        with open(RESPONSES_FILE, 'w', encoding='utf-8') as file:
            json.dump(curr_response, file, indent=4, ensure_ascii=False)
            
        counter_data = load_user_health_question_counter(username)
        update_health_question_counter(username, q_idx_str, counter_data)
        save_user_health_question_counter(username, counter_data)

        print(f"Successfully saved response for question {q_idx}")

    except Exception as e:
        print(f"Error in responses function: {e}")
        raise

    return 

def rewards(username, task_completed):
    """
    Calculate and track rewards for users based on completed tasks with advanced time tracking.
    
    Args:
        username (str): The username of the user
        task_completed (str): The specific task that was completed
    
    Returns:
        dict: A dictionary containing reward details
    """
    # Paths for relevant files
    USER_REWARDS_FILE = os.path.join(USER_REWARDS_DIR, f"{username}_rewards_log.json")
    # Create user rewards directory if it doesn't exist
    os.makedirs(USER_REWARDS_DIR, exist_ok=True)

    # Load tasks configuration
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks_config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading tasks configuration: {e}")
        return {"error": "Could not load tasks configuration"}

    # Load or initialize user rewards log
    try:
        with open(USER_REWARDS_FILE, 'r', encoding='utf-8') as f:
            user_rewards_log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        user_rewards_log = {
            "total_points": 0,
            "task_history": {}
        }

    # Current timestamp
    current_time = datetime.now()

    # Check if the task exists in configuration
    if task_completed not in tasks_config:
        return {"error": "Task not found in configuration"}

    task_info = tasks_config[task_completed]
    points = task_info.get('points', 0)
    
    # New time-based parameters
    when_should_be_reasked = task_info.get('when_should_be_reasked', timedelta(days=1))
    
    # Ensure task history exists
    if task_completed not in user_rewards_log['task_history']:
        user_rewards_log['task_history'][task_completed] = {
            "last_rewarded": None,
            "total_times_rewarded": 0
        }

    task_history = user_rewards_log['task_history'][task_completed]
    last_rewarded = task_history.get('last_rewarded')

    # Calculate time difference
    can_reward = False
    if last_rewarded is None:
        # Never rewarded before
        can_reward = True
    else:
        # Convert last_rewarded to datetime
        last_rewarded_dt = datetime.fromisoformat(last_rewarded)
        
        # Calculate time difference
        diff = current_time - last_rewarded_dt
        
        # Check if enough time has passed
        if diff.days >= when_should_be_reasked:
            can_reward = True

    # Process reward if task can be rewarded
    if can_reward:
        # Update task history
        task_history['last_rewarded'] = current_time.isoformat()
        task_history['total_times_rewarded'] += 1

        # Update total points
        user_rewards_log['total_points'] += points

        # Save updated rewards log
        with open(USER_REWARDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_rewards_log, f, indent=4)

        return {
            "task": tasks_config[task_completed]['description'],
            "points_earned": points,
            "total_points": user_rewards_log['total_points'],
            "last_rewarded": current_time.isoformat(),
            "times_rewarded": task_history['total_times_rewarded'],
            "message": f"Congratulations! You earned {points} points for {task_completed}."
        }
    else:
        # Calculate remaining time until next reward
        remaining_time = when_should_be_reasked - (current_time - datetime.fromisoformat(last_rewarded)).days
        
        return {
            "task": tasks_config[task_completed]['description'],
            "points_earned": 0,
            "total_points": user_rewards_log['total_points'],
            "last_rewarded": last_rewarded,
            "times_rewarded": task_history.get('total_times_rewarded', 0),
            "message": f"You can earn points for this task again in {remaining_time} days.",
            "remaining_time": str(remaining_time)
        }