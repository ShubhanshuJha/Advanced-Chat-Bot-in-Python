import pyttsx3

def say(text: str):
    engine = pyttsx3.init()
    engine.setProperty('speech.speed', 0.2) # this will slower speech rate
    engine.say(text)
    engine.runAndWait()

