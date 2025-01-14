import socketio
import sounddevice as sd
from pynput import keyboard
import wave
import time
from pydub.playback import play
import pydub
from pydub import AudioSegment
import io

sio = socketio.Client(logger=True, engineio_logger=True)

@sio.on('connect', namespace='/llm')
def connect():
    print('connected to server')
    sio.emit('auth', namespace='/llm')

@sio.on('connected', namespace='/llm')
def connected(data):
    print('done')
    print(data)
    record_audio()
    sio.emit('voice_input', open("user_response.wav", 'rb').read(), namespace='/llm')

@sio.on('voice_response', namespace='/llm')
def handle_voice_response(data):
    print(data['disconnect'])
    # handle_voice_response(data)
    aud_seg = AudioSegment.from_file(io.BytesIO(data['data']), format="mp3")
    play(aud_seg)
    if not data['disconnect']:
        record_audio()
        sio.emit('voice_input', open("user_response.wav", 'rb').read(), namespace='/llm')
    

@sio.on('connection_denied', namespace='/llm')
def connection_denied(data):
    print('auth failed', data)

# def handle_voice_response(data):
#     # Decode audio data (if necessary)
#     decoded_audio = data['data']

#     # Create pydub.AudioSegment object (if not already an AudioSegment)
#     audio_segment = pydub.AudioSegment.from_mp3(decoded_audio)  # Adjust format if needed

#     try:
#         # Attempt playback with ffplay (fallback if missing)
#         audio_segment.export(f.name, "wav")
#     except (OSError, AttributeError):  # OSError for missing ffplay
#         print("Failed to play audio using ffplay. Falling back to alternative method...")
#         # Implement alternative playback logic (e.g., pyaudio)
#     return audio_segment

def record_audio(duration=None):
    CHUNK = 1024
    FORMAT = 'int16'
    CHANNELS = 1
    RATE = 10000
    WAVE_OUTPUT_FILENAME = "user_response.wav"

    frames = []
    stream = None
    is_recording = False
    recording_stopped = False
    close = False

    def record_audio():
        nonlocal frames, stream
        frames = []

        stream = sd.InputStream(
            samplerate=RATE,
            channels=CHANNELS,
            dtype=FORMAT,
            blocksize=CHUNK,
            callback=callback
        )

        stream.start()

    def callback(indata, frame_count, time, status):
        nonlocal stream
        if is_recording:
            frames.append(indata.copy())

    def stop_recording():
        nonlocal frames, stream, recording_stopped

        stream.stop()
        stream.close()


        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        recording_stopped = True

    def on_key(key):
        nonlocal is_recording, close

        if key == keyboard.Key.up:
            if not is_recording:
                record_audio()
                is_recording = True
            else:
                stop_recording()
                is_recording = False
        elif key == keyboard.Key.down:
            close = True

    listener = keyboard.Listener(on_press=on_key)
    listener.start()

    start_time = time.time()
    while listener.running:
        if recording_stopped:
            listener.stop()
        elif duration and (time.time() - start_time) > duration:
            listener.stop()
        elif close:
            listener.stop()
            break
        time.sleep(0.01)

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:51323/', headers={
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzYWdlLXNlcnZlciIsImV4cCI6MTc2OTAxNzQzMSwibmJmIjoxNzMzMDIxMDMxLCJpYXQiOjE3MzMwMjEwMzEsInVzZXJfaWQiOiI0MzZmMmZjOWE3ZmNlNjYwZDhkZjhjZGVhZjQ5ZDg0YyJ9.yfqmb6qyr_INSDdUb9I_SD1QSmeMSY5hWZVVmkmkQ3I'
    }, namespaces='/llm')
    sio.wait()
    # record_audio()

