from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from functools import wraps
from flask import request
from flask_socketio import disconnect, emit
import requests
from other import llm_authenticate, pull_user_data, del_user_data, get_response_data_from_llm, set_logger
import time
from flask import Flask
import logging
import traceback

import yaml

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG) # Set the desired log level
set_logger(app.logger)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong', 200



with open('/app/config/conf.yaml', 'r') as file:
    cfg = yaml.safe_load(file)
# cfg = {'llmUsername': 'llmuser', 'llmPassword': 'llmpassword', 'openaiApiKey': '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', 'storageService': {'host': 'storage-service-svc.senior-sage', 'port': 8080}, 'authzService': {'host': 'authz-svc.senior-sage', 'port': 8080}}
print(cfg)
ok = llm_authenticate(cfg)
if not ok:
    print("Error authenticating with LLM")
    time.sleep(5)
    exit(1)

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
        
#         global cfg
#         print('authenticating')
#         token = None
#         if "Authorization" in request.headers:
#             token = request.headers["Authorization"]
#         print(token)
#         if not token:
#             emit('connection_denied', {
#                 "message": "Authentication Token is missing!",
#                 "data": None,
#                 "error": "Unauthorized"
#             })
#             return
#         try:
#             authzHost = cfg['authzService']['host']
#             authzPort = cfg['authzService']['port']
#             response = requests.get(f"http://{authzHost}:{authzPort}/auth/verify", json={"jwt_token": token})
#             response.raise_for_status()
#             current_user = response.json()
#             if current_user['valid'] == False:
#                 emit('connection_denied', {
#                     "message": "Invalid Token",
#                     "data": None,
#                     "error": "Unauthorized"
#                 })
#                 return
#             current_user = current_user['user_id']
#         except Exception as e:
#             emit('connection_denied',{
#                 "message": "Something went wrong",
#                 "data": None,
#                 "error": str(e)
#             })
#             return

#         return f(current_user, *args, **kwargs)

#     return decorated

state_data = {}


@socketio.on('auth', namespace='/llm')
def handle_auth():
    global app, state_data, cfg
    app.logger.info('authenticating')
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
    app.logger.info(token)
    if not token:
        emit('connection_denied', {
            "message": "Authentication Token is missing!",
            "data": None,
            "error": "Unauthorized"
        })
        return
    try:
        authzHost = cfg['authzService']['host']
        authzPort = cfg['authzService']['port']
        response = requests.get(f"http://{authzHost}:{authzPort}/auth/verify", json={"jwt_token": token})
        response.raise_for_status()
        current_user = response.json()
        if current_user['valid'] == False:
            emit('connection_denied', {
                "message": "Invalid Token",
                "data": None,
                "error": "Unauthorized"
            })
            return
        current_user = current_user['user_id']
    except Exception as e:
        emit('connection_denied',{
            "message": "Something went wrong",
            "data": None,
            "error": str(e)
        })
        return
    state_data[request.sid] = current_user
    pull_user_data(cfg, current_user)
    app.logger.info(current_user)
    print('Client connected')
    emit('connected', {'data': 'Connected', 'sid': request.sid})

@socketio.on('disconnect', namespace='/llm')
def handle_disconnect():
    global app, state_data
    app.logger.info('disconnect')
    del_user_data(state_data[request.sid])
    del state_data[request.sid]
    print('Client disconnected')

# @socketio.on('connect', namespace='/llm')
# def handle_connect():
#     [request.sid]
#     del state_data[request.sid]
#     print('Client disconnected')

@socketio.on('voice_input', namespace='/llm')
def handle_voice_capture(raw_voice_data):
    global app, state_data
    try:
        app.logger.info(f'voice_input: user_id: {state_data[request.sid]}, request.sid: {request.sid}')
        user_id = state_data[request.sid]
        voice_response, disconnect = get_response_data_from_llm(user_id, raw_voice_data)
        emit('voice_response', {'data': voice_response, 'disconnect': disconnect})
    except Exception as e:
        # import traceback, sys
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # error_message = traceback.format_exception(exc_type, exc_value, exc_traceback)
        # app.logger.error('Error:', error_message)
        app.logger.info(f"Exception type: {type(e)}")
        app.logger.error(f"Exception message: {str(e)}")
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        app.logger.error(traceback_str)
        # app.logger.error(e)

if __name__ == '__main__':
    print('Starting server...')
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0')