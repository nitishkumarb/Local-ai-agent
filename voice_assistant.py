import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import webbrowser
import os

# --- Record audio ---
def record_audio(filename="input.wav", duration=7, fs=16000):
    print("🎤 Speak now... (Recording for", duration, "seconds)")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, recording)
    print("✅ Recording saved to", filename)

# --- Transcribe audio ---
def transcribe_audio(filename="input.wav"):
    print("🔄 Processing your speech...")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            if not text:
                return "No speech detected"
            return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio")
        return None
    except sr.RequestError as e:
        print("❌ Error during transcription:", str(e))
        return None
    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return None

# --- Simple command handler ---
def handle_command(command):
    command = command.lower().strip()
    print("🔍 Processing command:", command)  # Debug line

    # YouTube commands
    if any(phrase in command for phrase in ["youtube", "you tube"]):
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return

    # Music commands
    if any(phrase in command for phrase in ["music", "spotify", "play"]):
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com")
        return

    # Google search
    if any(phrase in command for phrase in ["search", "google", "look up"]):
        search_query = command.replace("search", "").replace("google", "").replace("look up", "").strip()
        speak(f"Searching for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        return

    # Weather command
    if "weather" in command:
        speak("Opening weather forecast")
        webbrowser.open("https://weather.com")
        return

    speak("Sorry, I didn't understand that. You can try commands like 'open youtube', 'play music', 'search for something', or 'check weather'")

# --- TTS using pyttsx3 (free & offline) ---
def speak(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- Main ---
if __name__ == "__main__":
    print("🤖 Voice Assistant is ready! You can try commands like:")
    print("  - 'open youtube'")
    print("  - 'play music'")
    print("  - 'search for cats'")
    print("  - 'check weather'")
    
    try:
        record_audio(duration=7)
        print("\n🎯 Processing...")
        command = transcribe_audio()
        print("\n👉 You said:", command)
        if command and command != "No speech detected":
            handle_command(command)
    except Exception as e:
        print("❌ Error:", str(e))





