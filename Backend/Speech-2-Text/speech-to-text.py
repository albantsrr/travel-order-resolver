import speech_recognition as sr  

# get audio from the microphone                                                                       
recognizer = sr.Recognizer()                                                                                   
with sr.Microphone() as source:
    while True:
        try:
            recognizer.adjust_for_ambient_noise(source=source)
            audio_data = recognizer.listen(source, timeout=5)
            print(audio_data)
            text = recognizer.recognize_google(audio_data, language="fr-FR")
            print(text)
        except sr.WaitTimeoutError:
            print("je passe dans le timeout")
            break
        except sr.UnknownValueError:
            print("La valeur est inconnue")
            break
    