from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import speech_recognition as sr

app = Flask(__name__)
socketio = SocketIO(app)
recognizer = sr.Recognizer()

@socketio.on('start_recording')
def start_recording():
    with sr.Microphone() as source:
        while True:
            try:
                socketio.emit("status_recording", {'status': "Enregistrement en cours ..."})
                recognizer.adjust_for_ambient_noise(source=source)
                text = recognizer.recognize_google(recognizer.listen(source, timeout=3, phrase_time_limit=5), language="fr-FR")
                socketio.emit('recognized_text', {'text': text})
                socketio.emit("status_recording", {'status': "Enregistrement transcrit avec succés."})
                break
            except sr.WaitTimeoutError:
                socketio.emit("error_recording", {'status': "Aucune voix détecté, vueillez réessayer."})
                break
            except sr.UnknownValueError:
                socketio.emit("error_recording", {'status': "Impossible, je ne comprend pas ce que vous dites."})
                break
            except sr.RequestError as error:
                socketio.emit ("error_recording", {'status': f"Impossible de contacter Google pour l'instant, vueillez réessayer plus tard : {error}"})
                break

@socketio.on('stop_recording')
def start_recording():
    socketio.emit("status_recording", {'status': "Enregistrement stoppé avec succés"})
    return False

@app.route('/')
def index():
    return render_template('speech_to_text_test.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)