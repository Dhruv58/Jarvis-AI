import pyttsx3
import requests
import keyboard
# import tkinter
# from tkinter import *
# from tkinter import _tkinter
import webbrowser
# from PIL import ImageTk,Image
import pyautogui  # pip install pyautogui
import random
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text
from pprint import pprint
import wolframalpha  # pip install wolkframalpha
import imdb  # pip install imdbpy
import time

from osp import open_camera, open_notepad, open_cmd, open_gta
from online import search_on_wikipedia, play_on_youtube, search_on_google, send_email, get_random_joke, get_latest_news, \
    find_my_ip, get_weather_report

EMAIL = ""

USER = config('USER')
HOSTNAME = config('BOT')

engine = pyttsx3.init('sapi5')

engine.setProperty('volume', 1.5)
engine.setProperty('rate', 220)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


#
# window = Tk()
#
# window.configure(bg = “”)
#
# SET_WIDTH = 800
#
# SET_HEIGHT = 700
def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish_me():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you?{USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print("Started listening.")


def pause_listening():
    global listening
    listening = False
    print("Stopped listening.")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing....')
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry,I could not understand. Could you please say that again?')
        queri = 'None'
    return queri


if __name__ == '__main__':

    wish_me()

    while True:
        if listening:
            try:
                query = take_user_input().lower()

                if "how are you" in query:
                    speak("I am absolutely Fine Sir!!!")

                elif 'open camera' in query:
                    open_camera()
                elif 'open notepad' in query:
                    open_notepad()
                elif 'open command prompt' in query:
                    open_cmd()
                elif 'open gta 5' in query:
                    open_gta()

                    # elif "can you calculate" in query:
                    #

                elif 'subscribe' in query:
                    speak(
                        "Everyone who are watching this video, Please subscribe for more amazing content from error by "
                        "night. I will show you how to do this")
                    speak("Firstly Go to youtube")
                    webbrowser.open("https://www.youtube.com/")
                    speak("click on the search bar")
                    pyautogui.moveTo(806, 125, 1)
                    pyautogui.click(x=806, y=125, clicks=1, interval=0, button='left')
                    speak("Error by night")
                    pyautogui.typewrite("Error by night", 0.1)
                    time.sleep(1)
                    speak("press enter")
                    pyautogui.press('enter')
                    pyautogui.moveTo(971, 314, 1)
                    speak("Here you will see our channel")
                    pyautogui.moveTo(1688, 314, 1)
                    speak("click here to subscribe our channel")
                    pyautogui.click(x=1688, y=314, clicks=1, interval=0, button='left')
                    speak("And also Don't forget to press the bell icon")
                    pyautogui.moveTo(1750, 314, 1)
                    pyautogui.click(x=1750, y=314, clicks=1, interval=0, button='left')
                    speak("turn on all notifications")
                    pyautogui.click(x=1750, y=320, clicks=1, interval=0, button='left')

                elif 'calculate' in query:
                    app_id = "6QA5RJ-LHVGXJXLJ7"
                    client = wolframalpha.Client(app_id)
                    ind = query.lower().split().index("calculate")
                    text = query.split()[ind + 1:]
                    res = client.query(" ".join(text))
                    try:
                        ans = next(res.results).text
                        speak("The answer is " + ans)
                        print("the answer is " + ans)
                    except StopIteration:
                        speak("I couldn't calculate that. Please try again.")

                elif 'what is' in query or 'who is' in query or 'which is' in query or 'where did ' in query:
                    app_id = "6QA5RJ-LHVGXJXLJ7"  # Replace with your actual Wolfram Alpha App ID
                    client = wolframalpha.Client(app_id)
                    try:

                        ind = query.lower().index('what is') if 'what is' in query.lower() else \
                            query.lower().index('who is') if 'who is' in query.lower() else \
                                query.lower().index('which is') if 'which is' in query.lower() else None

                        if ind is not None:
                            text = query.split()[ind + 2:]
                            res = client.query(" ".join(text))
                            ans = next(res.results).text
                            speak("The answer is " + ans)
                            print("The answer is " + ans)
                        else:
                            speak("I couldn't find that. Please try again.")
                    except StopIteration:
                        speak("I couldn't find that. Please try again.")

                elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(
                        f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')

                elif 'search on wikipedia' in query:
                    speak('What do you want to search on Wikipedia, sir?')
                    search_query = take_user_input().lower()
                    results = search_on_wikipedia(search_query)
                    speak(f"According to Wikipedia, {results}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(results)

                elif 'youtube' in query:
                    speak('What do you want to play on Youtube, sir?')
                    video = take_user_input().lower()
                    play_on_youtube(video)

                elif 'where is' in query:
                    ind = query.lower().split().index("is")
                    location = query.split()[ind + 1:]
                    url = "https://www.google.com/maps/place/" + "".join(location)
                    speak("This is where " + str(location) + " is.")
                    webbrowser.open(url)

                elif 'search on google' in query:
                    speak('What do you want to search on Google, sir?')
                    query = take_user_input().lower()
                    search_on_google(query)

                elif "send an email" in query:
                    speak("On what email address do I send sir? Please enter in the console: ")
                    receiver_address = input("Enter email address: ")
                    speak("What should be the subject sir?")
                    subject = take_user_input().capitalize()
                    speak("What is the message sir?")
                    message = take_user_input().capitalize()
                    if send_email(receiver_address, subject, message):
                        speak("I've sent the email sir.")
                        print("I've sent the email sir.")
                    else:
                        speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

                elif 'tell me any joke' in query:
                    speak(f"Hope you like this one sir")
                    joke = get_random_joke()
                    speak(joke)
                    speak("For your convenience, I am printing it on the screen sir.")
                    pprint(joke)

                elif 'movie' in query:
                    movies_db = imdb.IMDb()
                    speak("please tell me the movie name :")
                    text = take_user_input()
                    movies = movies_db.search_movie(text)
                    speak("Searching for" + text)
                    speak("I Found these: ")
                    for movie in movies:
                        title = movie["title"]
                        year = movie["year"]
                        speak(f"{title}-{year}")
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info["rating"]
                        cast = movie_info["cast"]
                        actor = cast[0:5]
                        plot = movie_info.get('plot outline', 'Plot summary not available')
                        speak(
                            f'{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor} . The plot summary'
                            f'of movie is {plot}')
                        print(
                            f'{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor} The plot summary '
                            f'of movie is {plot}')

                elif 'give me news' in query:
                    speak(f"I'm reading out the latest news headlines, sir")
                    speak(get_latest_news())
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(*get_latest_news(), sep='\n')

                elif 'weather' in query:
                    ip_address = find_my_ip()
                    city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                    speak(f"Getting weather report for your city {city}")
                    weather, temperature, feels_like = get_weather_report(city)
                    speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

            except KeyboardInterrupt:
                print("Listening stopped. Press 'enter' to start listening again.")
                input()
                start_listening()
