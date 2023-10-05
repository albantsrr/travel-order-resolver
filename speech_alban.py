import speech_recognition as sr

# Initialiser le recognizer
recognizer = sr.Recognizer()

# Fonction pour effectuer la reconnaissance vocale
def recognize_speech():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Dites quelque chose...")
            audio = recognizer.listen(source)
            print("Enregistrement terminé. Analyse en cours...")

            # Reconnaissance vocale en utilisant Google Web Speech API
            text = recognizer.recognize_google(audio, language='fr-FR')
            return text

    except sr.RequestError as e:
        print("Erreur lors de la demande à l'API Google; {0}".format(e))
    except sr.UnknownValueError:
        print("Google Web Speech API n'a pas pu comprendre l'audio.")

# Appel de la fonction pour effectuer la reconnaissance vocale
result = recognize_speech()

# Affichage du texte reconnu
print("Texte reconnu : " + result)
