import gtts 
import playsound 
import os
import requests 
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from constants import (
    EMAIL,
    PASSWORD,
    IP_ADDR_API_URL,
    NEWS_FETCH_API_URL,
    WEATHER_FORECAST_API_URL,
    SMTP_URL,
    SMTP_PORT,
    NEWS_FETCH_API_KEY,
    WEATHER_FORECAST_API_KEY,
)
from pydub import AudioSegment

def speak(text):
    tts = gtts.gTTS(text, lang="en")
    tts.save("output.mp3")
    audio = AudioSegment.from_file("output.mp3")
    os.remove("output.mp3")
    audio = audio.speedup(playback_speed=1.5)
    audio.export('output.mp3', format='mp3')
    playsound.playsound("output.mp3")
    os.remove("output.mp3")

def find_my_ip():
    ip_address = requests.get(IP_ADDR_API_URL, params={"format": "json"}).json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email["To"] = receiver_add
        email["Subject"] = subject
        email["From"] = EMAIL 
        email.set_content(message)
        s = smtplib.SMTP(SMTP_URL, SMTP_PORT)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True 
    except Exception as e:
        print(e)
        return False

def get_news():
    news_headline = []
    result = requests.get(
        NEWS_FETCH_API_URL,
        params={
            "country": "in",
            "category": "general",
            "apiKey": NEWS_FETCH_API_KEY,
        },
    ).json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]

def weather_forecast(city):
    res = requests.get(
        WEATHER_FORECAST_API_URL,
        params={
            "q": city,
            "appid": WEATHER_FORECAST_API_KEY,
            "units": "metric"
        },
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"