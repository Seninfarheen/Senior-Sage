import openai
from dotenv import load_dotenv
import os
import time
import re
import sounddevice as sd
from pynput import keyboard
import wave
import io
from pydub import AudioSegment
from pydub.playback import play
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def stt_whisper(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

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
        nonlocal is_recording

        if key == keyboard.Key.up:
            if not is_recording:
                record_audio()
                is_recording = True
            else:
                stop_recording()
                is_recording = False

    listener = keyboard.Listener(on_press=on_key)
    listener.start()

    start_time = time.time()
    while listener.running:
        if recording_stopped:
            listener.stop()
        elif duration and (time.time() - start_time) > duration:
            listener.stop()
        time.sleep(0.01)


def fetch_audio(sentence, voice="nova"):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice.lower(),
        input=sentence
    )
    return response.content  # Returns raw audio bytes

# Main TTS function with preloading
def tts_whisper(input_text, voice="nova"):
    sentences = re.split(r'(?<=[.:])\s+', input_text)
    executor = ThreadPoolExecutor(max_workers=2)  # One thread for current, one for preloading
    next_audio = None

    for i, sentence in enumerate(sentences):
        # Submit the next sentence for preloading if it exists
        if i < len(sentences) - 1:
            future = executor.submit(fetch_audio, sentences[i + 1], voice)
        
        # Play current sentence audio (preloaded if available)
        if next_audio is None:
            # Load initial sentence and convert to AudioSegment
            current_audio_bytes = fetch_audio(sentence, voice)
            current_audio = AudioSegment.from_file(BytesIO(current_audio_bytes), format="mp3")
        else:
            current_audio = AudioSegment.from_file(BytesIO(next_audio), format="mp3")  # Use preloaded audio

        play(current_audio)

        # Update next_audio with the preloaded future result
        next_audio = future.result() if i < len(sentences) - 1 else None