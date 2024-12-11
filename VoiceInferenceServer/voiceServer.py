# this is the inference server fot TTS and STT
# receive the audio from client and return the result to client

from flask import Flask, request, jsonify, send_file
import os
import sys
import json
import requests
import wave
import whisperEngine as we
import soundBoard


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SOUNDBOARD = soundBoard.SoundBoard()
MODLE_SIZE = "base"
WHISPER_RECOGNIZER = we.WhisperRecognizer(model_size=MODLE_SIZE)

@app.route('/tts', methods=['POST'])
def tts():
    if request.method == 'POST':
        text = request.form['text']
        if SOUNDBOARD.speak(text):
            # respond with generated auido
            return send_file('tts_generated/temp.wav', mimetype='audio/wav')
        else:
            return jsonify({"result": "fail"})
    else:
        return jsonify({"error": "Invalid request method"})



@app.route('/stt', methods=['POST'])
def stt():
    if request.method == 'POST':
        audio_data = request.files['audio']
        # check file format to be wav
        if audio_data.filename.split('.')[-1] != 'wav':
            return jsonify({"error": "file format must be wav"})

        audio_data.save(os.path.join(UPLOAD_FOLDER, audio_data.filename))
        with wave.open(os.path.join(UPLOAD_FOLDER, audio_data.filename), 'rb') as f:
            audio_data = f.readframes(f.getnframes())

        text = WHISPER_RECOGNIZER.recognize(audio_data)
        return jsonify({"text": text})
    else:
        return jsonify({"error": "Invalid request method"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

