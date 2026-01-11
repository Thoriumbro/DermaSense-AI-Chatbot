import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import pygame
import os
import time
import translator  

pygame.mixer.init()

def initialize_engine():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        return engine
    except Exception as e:
        print(f"Error initializing speech engine: {e}")
        return None

def speak(engine, text, target_lang="English"):
    if not engine or not text:
        return
        
    try:
        if target_lang.lower() != "english":
            translated_text = translator.translate(text, target_lang)
            if translated_text:
                text = translated_text

        if target_lang.lower() != "english":
            lang_code = translator.languages.get(target_lang, "en")
            tts = gTTS(text=text, lang=lang_code)
            
            temp_file = f"temp_speech_{int(time.time())}.mp3"
            tts.save(temp_file)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            pygame.mixer.music.unload()
            if os.path.exists(temp_file):
                os.remove(temp_file)
        else:
            engine.say(text)
            engine.runAndWait()
            
    except Exception as e:
        print(f"Error in speech synthesis: {e}")
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            print("Failed to speak the message")

def listen(target_lang="English"):
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)
            
            try:
                text = recognizer.recognize_google(audio)
                
                if target_lang.lower() != "english":
                    translated_text = translator.translate(text, "English", target_lang)
                    if translated_text:
                        text = translated_text
                
                return text.lower()
                
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Please try again.")
                return ""
                
    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"Error in voice recognition: {e}")
        return ""