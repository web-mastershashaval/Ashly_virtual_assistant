import pyttsx3
import speech_recognition as sr
import pandas as pd
from GoogleNews import GoogleNews
import datetime
import time
import threading
import requests

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Choose the desired voice here

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def generate_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_date

def news():
    google_news = GoogleNews(period='id')
    google_news.search('kenya')
    result = google_news.result()
    
    # Convert result to DataFrame for further processing
    data = pd.DataFrame.from_dict(result)
    data = data.drop(columns=['img'])  # Drop the 'img' column if not needed

    # Print news headlines and use TTS to speak them
    for item in result:
        title = item.get("title")
        if title:
            speak(title)

def set_alarm():
    alarm_time = input("Tell me the alarm time (HH:MM): ").strip()

    def alarm():
        speak(f"Alarm is set for {alarm_time}")
        while True:
            now = datetime.datetime.now().strftime("%H:%M")
            if now == alarm_time:
                speak("Alarm! Time to wake up!")
                break
            time.sleep(20)  # Check every 20 seconds

    # Create a new thread for the alarm function
    alarm_thread = threading.Thread(target=alarm)
    alarm_thread.start()

def get_weather(city):
    api_key = 'your_openweathermap_api_key'  # Replace with your OpenWeatherMap API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"  # Metric units for temperature in Celsius

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather_description = data["weather"][0]["description"]
            temperature = main["temp"]
            humidity = main["humidity"]

            weather_report = (f"Weather in {city}: {weather_description}. "
                              f"Temperature: {temperature}°C. Humidity: {humidity}%.")
            speak(weather_report)
        else:
            speak("City not found. Please check the city name.")
    except Exception as e:
        speak(f"An error occurred while fetching weather data: {e}")


# Call the news function

# Set an alarm for a specific time
# Format for alarm_time should be "HH:MM" (24-hour format)


# Get weather updates
city = input("Enter the city for weather update: ").strip()
get_weather(city)
