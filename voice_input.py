import speech_recognition as sr
r = sr.Recognizer()


def transcribe_audio(audio):
    try:
        transcribed_text = r.recognize_google(audio)
        # print("You said: " + transcribed_text)
    except sr.UnknownValueError:
        # print("Could not understand audio.")
        return 'Could not understand audio.'
    except sr.RequestError as e:
        # print("Could not request results from Speech Recognition service; {0}".format(e))
        return 'Could not understand audio.'
    return transcribed_text


def listen_for_speech():
    with sr.Microphone() as source:
        print("\033[32mListening...\033[0m")
        audio = r.listen(source)
    return transcribe_audio(audio)


