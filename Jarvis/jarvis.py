import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import subprocess

# ── Voice ────────────────────────────────────────────────────────────
def speak(audio) -> None:
    """Speaks the given text out loud using a fresh engine each time."""
    print(f"Jarvis: {audio}")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 = David (male)
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    engine.say(audio)
    engine.runAndWait()
    engine.stop()


# ── Time & Date ──────────────────────────────────────────────────────
def time() -> None:
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def date() -> None:
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%B')} {now.day}, {now.year}")


# ── Greeting ─────────────────────────────────────────────────────────
def wishme() -> None:
    speak("Welcome back, Manav!")
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
    else:
        speak("Good night, see you tomorrow.")
    assistant_name = load_name()
    speak(f"{assistant_name} at your service. How may I assist you?")


# ── Screenshot ───────────────────────────────────────────────────────
def screenshot() -> None:
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak("Screenshot saved to your Pictures folder.")


# ── Name management ──────────────────────────────────────────────────
def set_name() -> None:
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Manav's Jarvis"


# ── Wikipedia ────────────────────────────────────────────────────────
def search_wikipedia(query) -> None:
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")


# ── Music ────────────────────────────────────────────────────────────
def play_music(song_name=None) -> None:
    song_dir = os.path.expanduser("~\\Music")
    try:
        songs = os.listdir(song_dir)
        songs = [s for s in songs if s.endswith(('.mp3', '.wav', '.m4a'))]
    except Exception:
        songs = []

    if song_name:
        matches = [s for s in songs if song_name.lower() in s.lower()]
    else:
        matches = songs

    if matches:
        song = random.choice(matches)
        speak(f"Playing {song}.")
        os.startfile(os.path.join(song_dir, song))
    else:
        speak("No song found in your Music folder. Try playing on Spotify instead.")


# ── Spotify ──────────────────────────────────────────────────────────
def open_spotify() -> None:
    spotify_paths = [
        os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
        r"C:\Program Files\Spotify\Spotify.exe",
        r"C:\Program Files (x86)\Spotify\Spotify.exe",
    ]
    for path in spotify_paths:
        if os.path.exists(path):
            speak("Opening Spotify.")
            subprocess.Popen([path])
            return
    speak("Opening Spotify in your browser.")
    wb.open("https://open.spotify.com")

def play_on_spotify(song_name) -> None:
    if not song_name:
        speak("Please tell me the song name.")
        return
    speak(f"Playing {song_name} on Spotify.")
    query = song_name.replace(" ", "%20")
    # Open Spotify app with the song search using URI
    os.system(f'start spotify:search:{query}')
    import time
    time.sleep(4)  # Wait for Spotify to open
    # Press Tab to focus first result, then Enter to play
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')


# ── Voice Input ──────────────────────────────────────────────────────
def takecommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            return ""
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


# ── Main Loop ────────────────────────────────────────────────────────
if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in query:
            song = query.replace("play music", "").strip()
            play_music(song if song else None)

        elif "open spotify" in query:
            open_spotify()

        elif "play" in query and "spotify" in query:
            song = query.replace("play", "").replace("spotify", "").replace("on", "").strip()
            play_on_spotify(song)

        elif query.startswith("play ") and "music" not in query:
            song = query.replace("play", "").strip()
            play_on_spotify(song)

        elif "open youtube" in query:
            speak("Opening YouTube.")
            wb.open("youtube.com")

        elif "open google" in query:
            speak("Opening Google.")
            wb.open("google.com")

        elif "open instagram" in query:
            speak("Opening Instagram.")
            wb.open("instagram.com")

        elif "open whatsapp" in query:
            speak("Opening WhatsApp.")
            wb.open("web.whatsapp.com")

        elif "open github" in query:
            speak("Opening GitHub.")
            wb.open("github.com")

        elif "screenshot" in query:
            screenshot()

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "change your name" in query:
            set_name()

        elif "shutdown" in query:
            speak("Shutting down the system. Goodbye, Manav!")
            os.system("shutdown /s /f /t 1")
            break

        elif "restart" in query:
            speak("Restarting the system. Please wait.")
            os.system("shutdown /r /f /t 1")
            break

        elif "offline" in query or "exit" in query or "bye-bye" in query:
            speak("Going offline. Have a great day, Manav!")
            break