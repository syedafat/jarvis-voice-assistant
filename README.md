# Jarvis Assistant

Jarvis has a small web page for typed commands and searches, plus an optional voice mode. The web page can open Google, Facebook, YouTube, and LinkedIn, or search Google for a product or topic.

## Setup

1. Install Python.
2. Open a terminal in this project folder.
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Run the web assistant

Run:

```bash
python main.py
```

Then open <http://127.0.0.1:5000> in Chrome or Edge. Click **Speak to Jarvis** and say a command such as `open YouTube`; Jarvis opens the result in a new tab. You can also enter a command or search term in the text field and select its result link. Allow microphone access and pop-ups when your browser asks.

## Run the voice assistant

Run:

```bash
python main.py --voice
```

Say "Jarvis," then give a command. Voice recognition uses Google's online service and requires an internet connection and a microphone. Press `Ctrl+C` to stop either mode.
