# import json
# from datetime import datetime
# from transformers import pipeline
# import os

# # Initialize the emotion detection pipeline
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# USER_EMOTION_FILE = os.path.join(BASE_DIR, 'emotion_analysis.json')
# emotion_detector = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# # Perform emotion detection on a session
# def analyze_emotion(session):
#     """
#     Analyze the emotions in a conversation session and store the results in a JSON file.
#     :param session: The current conversation session as a dictionary.
#     """
#     try:
#         emotion_results = []
#         user_message  = []

#         for message in session.get("messages", []):
#             user_message.append(message["user_message"])



#         # Perform emotion detection for the user message
#         emotion_analysis = emotion_detector(user_message)
#         detected_emotion = emotion_analysis[0][0]["label"]  # Get the top emotion
#         emotion_score = emotion_analysis[0][0]["score"]

#         # Append results
#         emotion_results.append({
#             "emotion": detected_emotion,
#             "confidence": emotion_score
#         })

#         # Save results to JSON
#         save_emotions_to_json(session["timestamp"], emotion_results)

#     except Exception as e:
#         print(f"Error during emotion detection: {e}")

# # Save emotions to JSON
# def save_emotions_to_json(session_id, emotions):
#     """
#     Save emotion analysis results to a JSON file.
#     :param session_id: The timestamp of the session as an identifier.
#     :param emotions: List of emotions analyzed for the session.
#     """
#     try:
#         # Load existing data or create a new structure
#         try:
#             with open(USER_EMOTION_FILE, "r") as file:
#                 data = json.load(file)
#         except FileNotFoundError:
#             data = {}

#         # Save session data
#         data[session_id] = emotions

#         with open(USER_EMOTION_FILE, "w") as file:
#             json.dump(data, file, indent=4)

#         print(f"Emotion analysis for session '{session_id}' saved successfully.")

#     except Exception as e:
#         print(f"Error saving emotions to JSON: {e}")