from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import speech_recognition as sr

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the Recognizer instance
recognizer = sr.Recognizer()

@socketio.on('start_recording')
def start_recording():
    with sr.Microphone() as source:
        socketio.emit("status_recording", {'status': "Enregistrement traduit avec succés"})
        while True:
            try:
                recognizer.adjust_for_ambient_noise(source=source)
                text = recognizer.recognize_google(recognizer.listen(source), language="fr-FR")
                socketio.emit('recognized_text', {'text': text})
                print(text)
                if text:
                    socketio.emit("status_recording", {'status': "Enregistrement traduit avec succés"})
            except sr.WaitTimeoutError:
                break
            except sr.UnknownValueError:
                socketio.emit({"status_recording": "Impossible, je ne comprend pas ce que vous dites"})

@socketio.on('stop_recording')
def start_recording():
    socketio.emit("status_recording", {'status': "Enregistrement stoppé avec succés"})

@app.route('/')
def index():
    return render_template('test.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)