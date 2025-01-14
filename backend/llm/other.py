import requests
from datetime import datetime
# from voice_interactions import stt_whisper, fetch_audio
# from server import cfg
import openai
import json
import re
import logging

llm_token = ""
cfg = {}

logger: logging.Logger = logging.Logger('test')

def set_logger(l):
    global logger
    logger = l

def llm_authenticate(cfg1):
    global cfg
    global llm_token
    cfg = cfg1
    username = cfg['llmUsername']
    password = cfg['llmPassword']
    try:
        host = cfg['authzService']['host']
        port = cfg['authzService']['port']
        response = requests.post(f"http://{host}:{port}/auth/signup", json={"email": username, "password": password, "name": "LLM Server", "voice_selection": "nova"})
        response = requests.post(f"http://{host}:{port}/auth/login", json={"email": username, "password": password})
        response.raise_for_status()
        token = response.json()['token']
    except Exception as e:
        logger.debug(f"Error authenticating with LLM: {e}")
        return False
    llm_token = token
    return True

all_user_data = {}

def pull_user_data(cfg, user_id):
    global llm_token, all_user_data, logger
    try:
        host = cfg['storageService']['host']
        port = cfg['storageService']['port']
        response = requests.get(f"http://{host}:{port}/data", json={"requester_token": llm_token, "user_id": user_id})
        response.raise_for_status()
        user_data = response.json()
        logger.info(f'user data: {user_data}')
        past_logs = user_data.get('chat_history', [])
        context = []
        for session in past_logs:
            for entry in session.get('messages', []):
                context.append((entry['timestamp'], entry['user_message'], entry['bot_response']))

        curr_time = datetime.now().isoformat()
        all_user_data[user_id] = {
            'user_data': user_data,
            'current_session': {
                'timestamp': curr_time,
                'messages': []
            },
            'context': context
        }
    except Exception as e:
        logger.error(f"Error pulling user data: {e}")
        raise e

def del_user_data(user_id):
    global all_user_data
    try:
        if user_id in all_user_data:
            # make a http request to update the user chat history
            host = cfg['storageService']['host']
            port = cfg['storageService']['port']
            response = requests.put(f"http://{host}:{port}/chat-history", json={
                "requester_token": llm_token,
                "user_id": user_id,
                "chat_history": all_user_data[user_id]['current_session']
            })
            response.raise_for_status()
            del all_user_data[user_id]
    except Exception as e:
        logger.error(f"Error updating user data: {e}")

questions = {
    0: {
        "question": "Have you had any alcohol or smoked recently?",
        "freq": 1
    },
    1: {
        "question": "Have you taken all your medications as prescribed today?",
        "freq": 1
    },
    2: {
        "question": "Are you experiencing any pain or discomfort today?",
        "freq": 1
    },
    3: {
        "question": "Did you spend time with family or friends today?",
        "freq": 7
    },
    4: {
        "question": "Did you sleep well last night?",
        "freq": 1
    },
    5: {
        "question": "How would you rate your overall physical health today?",
        "freq": 1
    },
    6: {
        "question": "Are you drinking enough water today?",
        "freq": 1
    },
    7: {
        "question": "On a scale of 1-10, how would you rate your mood today?",
        "freq": 1
    },
    8: {
        "question": "Do you feel irritable or frustrated more than usual?",
        "freq": 7
    },
    9: {
        "question": "Have you felt sad, down, or depressed in the past week?",
        "freq": 7
    }
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "reminders",
            "description": "Save a reminder for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The user's name",
                    },
                    "remind": {
                        "type": "object",
                        "properties": {
                            "reminder_for": {
                                "type": "string",
                                "description": "Description of what the reminder is for",
                            },
                            "details": {
                                "type": "object",
                                "properties": {
                                    "time": {
                                        "type": "string",
                                        "description": "Time for the reminder (e.g., '8:30 am', '9:30 pm')",
                                    },
                                    "frequency": {
                                        "type": "string",
                                        "description": "Frequency of the reminder (e.g., 'one-time','daily','weekly','monthly', etc.)",
                                    },
                                    "start_date": {
                                        "type": "string",
                                        "description": "A string containing todays date" 
                                    },
                                    "cron_job": {
                                        "type": "string",
                                        "description": "A cron job is a scheduled task that runs automatically at specified times and dates, defined using a format of ``minute hour day-of-month month day-of-week``"
                                    }
                                },
                                "required": ["time", "frequency", "start_date", "cron_job"]
                            }
                        },
                        "required": ["reminder_for", "details"]
                    }
                },
                "required": ["username", "remind"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "responses",
            "description": "Save user responses to health-related questions asked by the assistant, and update the question bank per user",
            "parameters": {
                "type": "object",
                "properties": {
                    "q_idx": {
                        "type": "integer",
                        "description": "Index of the question from health_questions.json"
                    },
                    "username": {
                        "type": "string",
                        "description": "The user's name"
                    },
                    "user_answer": {
                        "type": "string",
                        "description": "User's response to the health question"
                    }
                },
                "required": ["q_idx", "username", "user_answer"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "preferences",
            "description": "Store user's preferences, likes, dislikes, or any personal information they share during conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "The user's name"
                    },
                    "preference_type": {
                        "type": "string",
                        "description": "Category of the preference (e.g., 'food', 'hobby', 'daily routine', 'family', etc.)",
                        "enum": ["food", "hobby", "daily routine", "family", "health", "entertainment", "social", "other"]
                    },
                    "preference_detail": {
                        "type": "string",
                        "description": "Detailed description of the preference or information shared by the user"
                    },
                    "sentiment": {
                        "type": "string",
                        "description": "Whether this is something the user likes, dislikes, or is neutral about",
                        "enum": ["like", "dislike", "neutral"]
                    }
                },
                "required": ["username", "preference_type", "preference_detail", "sentiment"]
            }
        }
    }
    
]


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
    questions_to_ask = create_questions_to_ask_stack(questions, counter_data, username)

    return counter_data, questions_to_ask

def save_user_health_question_counter(username, counter_data):
    pass

def create_questions_to_ask_stack(questions, counter_data, username):
    # List of questions with counter = 0
    questions_to_ask = {}
    
    for q_idx, data in counter_data.items():
        if data["counter"] == False:
            if q_idx in questions:
                questions_to_ask[q_idx] = questions[q_idx]
    
    return questions_to_ask

def get_response_data_from_llm(user_id, voice_data):
    global questions, all_user_data
    if user_id not in all_user_data.keys():
        logger.info(f'userid {user_id} not in all_user_data')
        all_user_data[user_id] = {}
        # pull_user_data(cfg, user_id)
    current_user_data: dict = all_user_data.get(user_id, {})
    counter_data, questions_to_ask = initialize_health_question_counter(questions, current_user_data.get('question_counts', {}), user_id)
    current_user_data['question_counts'] = counter_data

    text_data = stt_whisper(voice_data)
    logger.info(current_user_data)
    text_response, audio_response = openai_complete(user_id, text_data, questions_to_ask, current_user_data.get('preferences', []), current_user_data.get('context', []), current_user_data.get('user_data', {}).get('voice', 'nova'), current_user_data.get('user_data', {}).get('name', 'unknown'))
    
    cur_time = datetime.now().isoformat()
    context = current_user_data.get('context', [])
    context.append((cur_time, text_data, text_response))

    if 'current_session' not in current_user_data.keys():
        current_user_data['current_session'] = {'messages': []}
    if "Alright then have a great" in re.sub(r'[^\w\s]', '', text_response):
        logger.info(f'ending conversation for {user_id}')
        logger.info(f'current_user_data: {current_user_data}')
        current_user_data['current_session']['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': text_data,
            'bot_response': text_response
        })
        # disconnect from the user
        return audio_response, True

    
    current_user_data['current_session']['messages'].append({
        'timestamp': datetime.now().isoformat(),
        'user_message': text_data,
        'bot_response': text_response
    })

    return audio_response, False



def openai_complete(username, user_ip, questions_to_ask, user_preferences, context, voice, name):
    # global client

    # Load health questions
    health_questions = questions_to_ask
    
    system_prompt = f'''
    You are a helpful assistant for the elderly, try and have conversations with {username}. Your primary goal is to get answers to these questions provided in the QUESTIONAIRE while being natural at it and not posing questions one after another.
    Make sure to have sense of what questions and contexts you have discussed with the user in the day and try to continue your conversation from there instead of starting from the beginning. Ex: A user mentions their hobby or plans for the day once, try to refer the chat history and documentation to understand the user preference and how you can continue the conversations from there.
    You can make use of the "QUESTIONAIRE" which includes some day to day questions that you should ask the user in a POLITE WAY, making sure it looks NATURAL and not like they are giving a medical form. When the user answers these question, call the ``responses`` function to store the answers to the questions and update your question bank.
    Keep short and consize answers not to bother them too much. Do not output long answers as it may be too long for them to read. Keep it short and simple and human-like. 
    Utilize the context given below to keep track of user queries and your answers. Try to bring up events from past conversations using CHAT HISTORY to make it a more personalised experience for the user.
    Also try and keep a track of the users preferences, anything that makes them unique. Store results in one of the following: ["food", "hobby", "daily routine", "family", "health", "entertainment", "social", "other"] by calling the ``preferences`` function.
    If you don't understand a request, ask for clarification rather than making assumptions. Always prioritize user safety by never providing medical diagnosis, treatment recommendations, 
    or interpreting medical results. When in doubt, encourage consulting a healthcare professional.
    The conversation should be done in English (it can include numbers), if the user responds or asks you a question in any other language, return 
    "Pardon, I didn't quite get that,could you try again in English"
    If the user asks you to set a reminder, please extract the relevant information and use the ``reminders`` function. If the user hasn't provided information regarding time and frequency, ask them gently.
    When the user tries to end the conversation using "exit","bye" or "see you soon" or anything simlilar, return 'Alright then, have a great day ahead!'

    CHAT HISTORY: {context}
    QUESTIONAIRE: {health_questions}
    USER PREFERENCES: {user_preferences}
    USER REMINDERS: {all_user_data[username]['user_data']['reminder_details']}
    USER NAME: {name}'''

    # api_key = 
    client = openai.OpenAI(api_key=cfg.get('openaiApiKey'))
    logger.info(f'init client in openai complete')

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_ip}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        response = completion.choices[0].message

        logger.debug(f"\n\n{response}\n\n")
        
        # Check if the model wants to call a function
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_call = response.tool_calls[0]
            
            if tool_call.function.name == "reminders":
                # Handle reminder function call
                function_args = json.loads(tool_call.function.arguments)
                logger.info(f"reminders function args: {function_args}")
                reminders(
                    username=username,
                    remind=function_args["remind"]
                )
                confirmation = f"I've set a reminder for {function_args['remind']['reminder_for']} at {function_args['remind']['details']['time']}, {function_args['remind']['details']['frequency']}."
                logger.debug(f"Chatbot: {confirmation}")
                audio_response = fetch_audio(confirmation, voice)
                return confirmation, audio_response
                
            elif tool_call.function.name == "responses":
                # Handle health responses function call
                try:
                    function_args = json.loads(tool_call.function.arguments)
                    responses(
                        q_idx=function_args["q_idx"],
                        username=function_args["username"],
                        user_answer=function_args["user_answer"]
                    )
                except Exception as e:
                    logger.debug(f"Error processing health response: {str(e)}")
                    raise

            elif tool_call.function.name == "preferences":
                # Handle storing user preferences
                try:
                    function_args = json.loads(tool_call.function.arguments)
                    preferences(
                        username=function_args["username"],
                        preference_type=function_args["preference_type"],
                        preference_detail=function_args["preference_detail"],
                        sentiment=function_args["sentiment"]
                    )
                except Exception as e:
                    logger.debug(f"Error storing user preference: {str(e)}")
                    raise
        
        # Handle regular response
        regular_response = response.content
        if regular_response is None:
            follow_up_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_ip},
                    {"role": "assistant", "content": "I've noted your response. Let me follow up on that."},
                    {"role": "user", "content": "Please acknowledge my previous response and continue our conversation naturally."}
                ]
            )
            regular_response = follow_up_completion.choices[0].message.content
            
        logger.debug(f"Chatbot: {regular_response}")
        audio_response = fetch_audio(regular_response, voice)
        return regular_response, audio_response

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logger.debug(error_msg)
        audio_response = fetch_audio("I'm sorry, I encountered an error while processing your request.", voice)
        return error_msg, audio_response


def preferences(username, preference_type, preference_detail, sentiment):
    global all_user_data, cfg
    current_user_data = all_user_data.get(username, {})
    current_user_data['user_data']['preferences'].append(preference_detail)
    # make a http request to store the preference
    host = cfg['storageService']['host']
    port = cfg['storageService']['port']
    response = requests.put(f"http://{host}:{port}/preferences", json={
        "requester_token": llm_token,
        "user_id": username,
        "preferences": current_user_data['user_data']['preferences']
    })
    response.raise_for_status()


def reminders(username, remind):
    global all_user_data, cfg
    all_user_data[username]['user_data']['reminder_details'].append({'reminder_for': remind['reminder_for'], 'time': remind['details']['time'], 'frequency': remind['details']['frequency'], 'start_date': remind['details']['start_date'], 'cron_job': remind['details']['cron_job']})
    # make a http request to store the reminder
    host = cfg['storageService']['host']
    port = cfg['storageService']['port']
    logger.info(f'making request to store reminders: {all_user_data[username]["user_data"]["reminder_details"]}')
    response = requests.put(f"http://{host}:{port}/reminders", json={
        "requester_token": llm_token,
        "user_id": username,
        "reminders": all_user_data[username]['user_data']['reminder_details']
    })
    response.raise_for_status()
    logger.debug(f'reminder api response: {response.json()}')


def responses(q_idx, username, user_answer):
    global all_user_data
    current_user_data = all_user_data.get(username, {})
    current_user_data['user_data']['question_responses'].append(
        {
            "q_id": q_idx,
            "question": questions[q_idx],
            "answer": user_answer,
            "date": datetime.now().isoformat()
        }
    )
    # make a http request to store the response
    host = cfg['storageService']['host']
    port = cfg['storageService']['port']
    response = requests.put(f"http://{host}:{port}/reponses", json={
        "requester_token": llm_token,
        "user_id": username,
        "responses": all_user_data[username]['question_responses']
    })
    response.raise_for_status()


    update_health_question_counter(username, q_idx, current_user_data['question_counts'])
    response = requests.put(f"http://{host}:{port}/question-counter", json={
        "requester_token": llm_token,
        "user_id": username,
        "question_counts": all_user_data[username]['question_counts']
    })
    response.raise_for_status()
    # current_user_data['question_counts'] = counter_data
    # current_user_data[''] = create_questions_to_ask_stack(questions, current_user_data['question_counts'], username)
    

def update_health_question_counter(username, q_idx, counter_data):
    counter_data[q_idx]['counter'] = True
    counter_data[q_idx]['asked_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

import io
def stt_whisper(audio_file):
    client = openai.OpenAI(api_key=cfg.get('openaiApiKey'))
    buffer = io.BytesIO(audio_file)
    buffer.name = 'file.mp3'
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        # file=io.BufferedReader(io.BytesIO(audio_file))
        file=io.BufferedReader(buffer)
        # content=audio_file
    )
    logger.info(f'transcript text: {transcript.text}')
    return transcript.text

def fetch_audio(sentence, voice="nova"):
    api_key = cfg.get('openaiApiKey')
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice.lower(),
        input=sentence
    )
    return response.content