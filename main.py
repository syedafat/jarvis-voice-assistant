import sys
import webbrowser
from urllib.parse import quote_plus

import pyttsx3
import speech_recognition as sr
from flask import Flask, jsonify, render_template, request


recognizer = sr.Recognizer()
engine = pyttsx3.init()
app = Flask(__name__)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(command):
    """Return a feedback message and URL for a website command or search."""
    command = command.strip()
    command_lower = command.lower()

    websites = {
        "open google": ("Google", "https://google.com"),
        "open facebook": ("Facebook", "https://facebook.com"),
        "open youtube": ("YouTube", "https://youtube.com"),
        "open linkedin": ("LinkedIn", "https://linkedin.com"),
    }

    for phrase, (name, url) in websites.items():
        if phrase in command_lower:
            return {"message": f"Opening {name}.", "url": url}

    # Treat other text as a product or web search.
    search_text = command
    if command_lower.startswith("search for "):
        search_text = command[10:].strip()
    elif command_lower.startswith("search "):
        search_text = command[7:].strip()

    if not search_text:
        return {"message": "Please enter a command or search term.", "url": None}

    search_url = "https://www.google.com/search?q=" + quote_plus(search_text)
    return {"message": f'Searching for "{search_text}".', "url": search_url}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    # The page sends its input as JSON, and this route returns feedback and a link.
    data = request.get_json(silent=True) or {}
    command = data.get("command", "")

    if not isinstance(command, str) or not command.strip():
        return jsonify({"message": "Please enter a command or search term.", "url": None}), 400

    return jsonify(processCommand(command))


def runVoiceAssistant():
    speak("Initializing Jarvis")

    try:
        # Calibrate the microphone once before listening.
        with sr.Microphone() as source:
            print("Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            while True:
                try:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    phrase = recognizer.recognize_google(audio)
                    print("You said:", phrase)

                    if "jarvis" in phrase.lower():
                        speak("Yes")
                        print("Jarvis Active...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        print("Command:", command)
                        result = processCommand(command)
                        speak(result["message"])
                        if result["url"]:
                            webbrowser.open(result["url"])

                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.WaitTimeoutError:
                    print("Listening timed out.")
                except sr.RequestError as error:
                    print("Speech Recognition service error:", error)
    except KeyboardInterrupt:
        print("Exiting Jarvis...")


if __name__ == "__main__":
    if "--voice" in sys.argv:
        runVoiceAssistant()
    else:
        print("Jarvis web assistant is running at http://127.0.0.1:5000")
        app.run(debug=False)
