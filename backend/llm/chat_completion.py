from voice_interactions import tts_whisper
import openai
import json
from dotenv import load_dotenv
from function_calling import reminders, responses, preferences, rewards
from rag import get_context
import os
from update_health_question_counter_data import create_questions_to_ask_stack  

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_HEALTH_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'health_question_counter')
USER_HEALTH_QUESTIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions_to_ask')
TASKS_FILE = os.path.join(BASE_DIR, 'tasks.json')

os.makedirs(USER_HEALTH_LOG_DIR, exist_ok=True)

def load_health_questions_to_ask(username):
    questions_file = os.path.join(USER_HEALTH_QUESTIONS_DIR, f"{username}_questions_to_ask_stack.json")
    try:
        with open(questions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading health questions: {e}")
        return {}
    
def load_tasks(username):
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        tasks_config = json.load(f)
    ret = []

    k = list(tasks_config.keys())
    for i in range(len(k)):
        desc = tasks_config[k[i]]['description']
        ret.append((k[i], desc))

    return ret

def openai_complete(username, user_ip, context, vector_db, voice):
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
        },
        {
            "type": "function",
            "function": {
                "name": "rewards",
                "description": "Track and calculate user rewards for completing specific tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "The user's name"
                        },
                        "task_completed": {
                            "type": "string",
                            "description": "The specific task that was completed (must match a task in tasks.json)"
                        }
                    },
                    "required": ["username", "task_completed"]
                }
            }
        }
        
    ]

    # Load health questions
    health_questions = load_health_questions_to_ask(username)
    related_chunks = get_context(vector_db, user_ip)
    tasks = load_tasks(username)
    
    system_prompt = f'''
    You are a helpful assistant for the elderly, try and have conversations with {username}. Your primary goal is to get answers to these questions provided in the QUESTIONAIRE while being natural at it and not posing questions one after another.
    Make sure to have sense of what questions you have discussed with the user in the day and try to continue your conversation from there instead of starting from the beginning. Ex: A user mentions their hobby or plans for the day once, try to refer the chat history and documentation to understand the user preference and how you can continue the conversations from there.
    You can make use of the "QUESTIONAIRE" which includes some day to day questions that you should ask the user in a POLITE WAY, making sure it looks NATURAL and not like they are giving a medical form. When the user answers these question, call the ``responses`` function to store the answers to the questions and update your question bank.
    Keep short and consize answers not to bother them too much. Do not output long answers as it may be too long for them to read. Keep it short and simple and human-like.
    Utilize the "CHAT HISTORY" given below to keep track of user queries and your answers. Try to bring up events from past conversations using CHAT HISTORY to make it a more personalised experience for the user.
    Also try and keep a track of the users preferences, anything that makes them unique. Store results in one of the following: ["food", "hobby", "daily routine", "family", "health", "entertainment", "social", "other"] by calling the ``preferences`` function.
    Some relevant context related to user queries is provided in "CONTEXT" along with the source of that information. Whenever a user asks you a health related question, make use of the CONTEXT to drive your answers and ALWAYS TELL THEM THE SOURCE OF YOUR ANSWER, as mentioned in CONTEXT (example, According to Healthy Meal Planning_ Tips for Older Adults _ National Institute on Aging.pdf, mention Source as National Institute on Aging).
    If you don't understand a request, ask for clarification rather than making assumptions. Always prioritize user safety by never providing medical diagnosis, treatment recommendations, or interpreting medical results. When in doubt, encourage consulting a healthcare professional.
    The conversation should be done in English (it can include numbers), if the user responds or asks you a question in any other language, return "Pardon, I didn't quite get that,could you try again in English"
    If the user asks you to log a reward, mentioned in REWARDS_TASKS, please extract the relevant information and use the ``rewards`` function. 
    If the user asks you to set a reminder, please extract the relevant information and use the ``reminders`` function. If the user hasn't provided information regarding time and frequency, ask them gently.
    When the user tries to end the conversation using "exit","bye" or "see you soon" or anything simlilar, return 'Alright then, have a great day ahead!'
    Please note your answers must never be in a list format,if you get CONTEXT that is too big, try and summarize it for the user before giving your final output and DONT MAKE YOUR ANSWER BIGGER THAN 80 WORDS.

    CHAT HISTORY: {context}
    QUESTIONAIRE: {health_questions}
    REWARDS_TASKS : {tasks}
    CONTEXT: {related_chunks} '''

    

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

        print(f"\n\n{response}\n\n")
        
        # Check if the model wants to call a function
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_call = response.tool_calls[0]
            
            if tool_call.function.name == "reminders":
                # Handle reminder function call
                function_args = json.loads(tool_call.function.arguments)
                reminders(
                    username=function_args["username"],
                    remind=function_args["remind"]
                )
                confirmation = f"I've set a reminder for {function_args['remind']['reminder_for']} at {function_args['remind']['details']['time']}, {function_args['remind']['details']['frequency']}."
                print(f"Chatbot: {confirmation}")
                tts_whisper(confirmation, voice)
                return confirmation
                
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
                    print(f"Error processing health response: {str(e)}")
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
                    print(f"Error storing user preference: {str(e)}")
                    raise
            elif tool_call.function.name == "rewards":
                try:
                    function_args = json.loads(tool_call.function.arguments)
                    reward_result = rewards(
                        username=function_args["username"],
                        task_completed=function_args["task_completed"]
                    )
                    print(reward_result)
                    try:
                        rem = reward_result['remaining_time']
                        confirmation = f"You have already completed this task, please try again after {rem} days!"
                        print(f"Chatbot: {confirmation}")
                    except:
                        confirmation = f"You have earned {reward_result['points_earned']} points for completing '{reward_result['task']}'! \n Congratulations, you now have earned {reward_result['total_points']} points!"
                        print(f"Chatbot: {confirmation}")
                except Exception as e:
                    print(f"Error storing user rewards: {str(e)}")
                    raise
        
        # Handle regular response
        regular_response = response.content
        if regular_response is None:
            follow_up_completion = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_ip},
                    {"role": "assistant", "content": "I've noted your response. Let me follow up on that."},
                    {"role": "user", "content": "Please acknowledge my previous response and continue our conversation naturally."}
                ]
            )
            regular_response = follow_up_completion.choices[0].message.content
            
        print(f"Chatbot: {regular_response}")
        tts_whisper(regular_response, voice)
        return regular_response

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        tts_whisper("I'm sorry, I encountered an error while processing your request.", voice)
        return error_msg