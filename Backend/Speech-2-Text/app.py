from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
import speech_recognition as sr
from flask_cors import CORS
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = Flask(__name__)
CORS(app, origins="http://localhost:4200", methods=["GET", "POST"])
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")
recognizer = sr.Recognizer()

# Charger le modèle BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("./models")

@socketio.on('start_recording')
def start_recording():
    with sr.Microphone() as source:
        while True:
            try:
                socketio.emit("status_recording", {'status': "Enregistrement en cours ..."})
                recognizer.adjust_for_ambient_noise(source=source)
                text = recognizer.recognize_google(recognizer.listen(source, timeout=3, phrase_time_limit=5), language="fr-FR")
                socketio.emit('recognized_text', {'text': text})
                socketio.emit("status_recording_approve", {'status': "Enregistrement transcrit avec succés."})
                break
            except sr.WaitTimeoutError:
                socketio.emit("status_recording_error", {'status': "Aucune voix détecté, vueillez réessayer."})
                break
            except sr.UnknownValueError:
                socketio.emit("status_recording_error", {'status': "Impossible, je ne comprend pas ce que vous dites."})
                break
            except sr.RequestError as error:
                socketio.emit ("status_recording_error", {'status': f"Impossible de contacter Google pour l'instant, vueillez réessayer plus tard : {error}"})
                break

@socketio.on('stop_recording')
def start_recording():
    socketio.emit("status_recording", {'status': "Enregistrement stoppé avec succés"})
    return False



@app.route('/detect_city', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        sentence = data['sentence']

        # Encodage de la phrase
        encoded_input = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt", max_length=128)

        # Prédiction avec le modèle
        with torch.no_grad():
            output = model(**encoded_input)

        # Récupération de la prédiction (classe 1 pour "Villes" et classe 0 pour "Pas de villes")
        prediction = torch.argmax(output.logits, dim=1).item()

        if prediction == 1:
            result = "Il y a une ville dans la phrase."
        else:
            result = "Il n'y a pas de ville dans la phrase."

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/')
def index():
    return render_template('speech_to_text_test.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)