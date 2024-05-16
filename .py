import speech_recognition as sr  # Importing the SpeechRecognition library for voice recognition
import pyttsx3  # Importing pyttsx3 for text-to-speech conversion
import pywhatkit  # Importing pywhatkit for various functionalities like playing songs, searching on YouTube, etc.
import datetime  # Importing datetime for working with dates and times
import wikipedia  # Importing Wikipedia API for fetching information from Wikipedia
import pyjokes  # Importing pyjokes for generating jokes
import requests  # Importing requests for making HTTP requests
import webbrowser  # Importing webbrowser for opening websites
import random  # Importing random for generating random values
import os  # Importing os for interacting with the operating system
from selenium import webdriver  # Importing Selenium for web automation
from selenium.webdriver.common.keys import Keys  # Importing Keys for keyboard actions in Selenium
import time  # Importing time for time-related functions
import csv  # Importing csv for reading CSV files
import pyautogui  # Importing pyautogui for GUI automation

# Initializing the recognizer and engine objects
listener = sr.Recognizer()
engine = pyttsx3.init()

# Setting the voice for the engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Global variable for the Selenium web driver
driver = None

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Function to open the online Python compiler using Selenium
def open_compiler():
    global driver
    url = "https://www.programiz.com/python-programming/online-compiler/"
    driver = webdriver.Chrome()  # Initialize the Chrome web driver
    driver.get(url)
    speak("Opening the online Python compiler.")
    time.sleep(5)  # Wait for the compiler to fully load

    if driver is not None:
        try:
            speak("The online Python compiler is now open.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred while opening the compiler.")
            driver.quit()  # Close the browser window
            driver = None

# Function to write 'Hello, world!' in the code editor of the online compiler
def write_hello_world(code_editor):
    try:
        speak("Writing 'Hello, world!' in the code editor.")
        code_editor.send_keys("print(\"Hello, world!\")")
        time.sleep(1)  # Wait for a moment
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while writing the code.")

# Function to run the program in the online compiler
def run_program(code_editor):
    try:
        speak("Running the program.")
        code_editor.send_keys(Keys.CONTROL, Keys.RETURN) 
        speak("Code printed: print(\"Hello, world!\")")
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while running the code.")

# Function to perform actions in the online Python compiler
def perform_compiler_actions():
    global driver
    open_compiler()
    if driver is not None:
        try:
            # Find the code editor element and write the code
            code_editor = driver.find_element("class name", "ace_text-input")
            write_hello_world(code_editor)
            run_program(code_editor)
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred while executing the code.")
        finally:
            driver.quit()  # Close the browser window
            driver = None
    else:
        speak("The online Python compiler is not open.")

# Function to load contacts from a CSV file
def load_contacts(csv_path):
    contacts = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contacts[row['Name'].lower()] = row['Phone']
    return contacts

# Function to execute various commands based on voice input
def run_leo():
    # Load contacts from CSV file
    contacts = load_contacts(r'C:\Users\SAI PAVAN\Desktop\contacts.csv')
    command = listen()
    print(command)
    
    # Command handling logic
    if 'play' in command:
        song = command.replace('play', '')
        speak('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is ' + time_now)
        print('Current time is ' + time_now)
    elif 'tell me about' in command:
        person = command.replace('tell me about', '')
        info = wikipedia.summary(person, 2)
        print(info)
        speak(info)
    elif 'joke' in command:
        speak(pyjokes.get_joke())
        print(pyjokes.get_joke())
    elif 'weather' in command:
        city = command.replace('weather in', '')
        weather_info = get_weather(city)
        print(weather_info)
        speak(weather_info)
    # Other command cases...
    else:
        speak('Please say the command again')

# Function to get weather information for a city
def get_weather(city):
    base_url = f'https://api.open-meteo.com/weather?forecast=hourly&daily=7&timezone=Europe%2FBerlin&current_weather=yes&longitude=&latitude=&hourly=temperature_2m'

    try:
        params = {'city': city}
        weather_data = requests.get(base_url, params=params).json()
        current_temperature = weather_data['current_weather']['temperature_2m']
        return f'The current temperature in {city} is {current_temperature}°C.'
    except KeyError:
        return 'Sorry, I couldn\'t retrieve the weather information.'

# Function to generate a random compliment
def generate_compliment():
    compliments = [
        "You're doing great!",
        "You have a wonderful smile!",
        "You're incredibly smart!",
        "Your positive attitude is contagious!",
        "You're one of a kind!"
    ]
    return random.choice(compliments)

# Function to get top news headlines
def get_news():
    news_api_key = '5945632ecd7c4e928633891c85dc18e1'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}'
    response = requests.get(url)
    news_data = response.json()
    headlines = [article['title'] for article in news_data['articles']]
    return headlines

def trivia_game():
    speak("Welcome to the Trivia Game! I will ask you three trivia questions. Let's see how many you can answer correctly.")
    print("Welcome to the Trivia Game! I will ask you three trivia questions. Let's see how many you can answer correctly.")
    questions = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
        {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
    ]

    score = 0

    for question_data in questions:
        speak(question_data["question"])
        user_answer = listen().lower()

        if user_answer == question_data["answer"].lower():
            speak("Correct! Well done.")
            print("Correct! Well done.")
            score += 1
        else:
            speak(f"Wrong! The correct answer is {question_data['answer']}.")
            print(f"Wrong! The correct answer is {question_data['answer']}.")

    speak(f"Game over. Your final score is {score} out of {len(questions)}.")
    print(f"Game over. Your final score is {score} out of {len(questions)}.")

def get_quote_of_the_day():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
    ]
    return random.choice(quotes)

def main():
    speak("Hello! How can I assist you today?")

    while True:
        run_leo()

if __name__ == "__main__":
    main()

