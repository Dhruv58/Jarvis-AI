from datetime import datetime
import multiprocessing
from random import choice
from typing import Self
import numpy as np
import sounddevice as sd
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Rotate, Rectangle, Color
from kivy.uix.image import Image
# import speech_recognition as sr
import speech_recognition as sr
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.textinput import TextInput
import threading
import keyboard
import pyttsx3
import pyautogui
import webbrowser
import os
import subprocess as sp
import pywhatkit
import wolframalpha
import imdb
import pprint
import requests
from conv import random_text
from multiprocessing.pool import ThreadPool
from deco_rator import *
# from main import wish_me,take_user_input

from online import find_my_ip, youtube,search_on_google,search_on_wikipedia,send_email,get_news,weather_forecast

# Set the width and height of the screen
width, height = 1920, 1080

# Print the width and height for verification
print(width, height)

# Configure the graphics settings
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'fullscreen', 'True')

# Get the configured screen width and height
SCREEN_WIDTH = Config.getint('graphics', 'width')
SCREEN_HEIGHT = Config.getint('graphics', 'height')

# Print the screen width and height for verification
print(SCREEN_WIDTH, SCREEN_HEIGHT)

engine = pyttsx3.init('sapi5')

engine.setProperty('volume', 1.5)
engine.setProperty('rate', 220)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()
  
@threaded      
def take_command():
    # try:    
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         print("Listening...")
    #         r.pause_threshold = 1
    #         audio = r.listen(source)

    #     print("Recognizing....")
    #     query = r.recognize_google(audio, language='en-in')
    #     print(query)
    #     return query.lower()

    # except Exception as e:
    #     print(e)
    #     speak("Sorry I couldn't understand. Can you please repeat that?")
    #     return 'None'
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir,take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri
    
    





# Custom button class that rotates
class RotatingButton(Button):

    def __init__(self, **kwargs):
        super(RotatingButton, self).__init__(**kwargs)
        self.angle = 2  # By regulating angle, you can indirectly control the speed of rotation
        self.background_angle = 0  # Angle for rotating only the background

    def rotate_button(self, *args):
        """
        Rotate the button by updating the canvas rotation angle.
        """
        self.background_angle += self.angle
        self.canvas.before.clear()
        with self.canvas.before:
            Rotate(angle=self.background_angle, origin=self.center)



# Custom widget representing the circle
class CircleWidget(Widget):

    def __init__(self, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0,0,0,0,0,0,0]

        # By increasing the size of volume_history_size, you can make the transition of size more smooth.
        self.volume_history_size = 140

        # Define relative minimal and maximal sizes for your circle
        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH
        
        # Create a rotating button representing the circle
        self.add_widget(Image(source='border.eps.png', size=(1920, 1080)))
        self.circle = RotatingButton(size=(284.0, 284.0), background_normal='circle.png')
        self.circle.bind(on_press=self.start_recording)
        # self.add_widget(Image(source='jarvis.gif', size=(self.min_size, self.min_size)))
        self.add_widget(Image(source='jarvis.gif', size=(self.min_size, self.min_size), pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)))

        # Create a label for displaying the spoken text
        
        time_layout = BoxLayout(orientation='vertical', pos=(150,900))
        self.time_label = Label(text='', font_size=24, markup=True, font_name='mw.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)
        # Schedule the update function for the time label
        Clock.schedule_interval(self.update_time, 1)
        
        self.title = Label(text='[b][color=3333ff]ERROR BY NIGHT[/color][/b]', font_size=42, markup=True, font_name='dusri.ttf', pos=(920, 900))
        self.add_widget(self.title)

        self.subtitles_input = TextInput(
            text='Hey Dhruv! I am Jarvis, your personal assistant.',
            font_size=24,
            readonly=True,
            background_color=(0, 0, 0, 0),  # Set background color to be transparent
            foreground_color=(1, 1, 1, 1),  # Set text color to be white
            size_hint_y=None,
            height=80,  # Set the height of the TextInput
            pos=(720, 100),
            width=1200,
            font_name='teesri.otf',
        )
        self.add_widget(self.subtitles_input)
        self.vrh =  Label(text='', font_size=30, markup=True, font_name='mw.ttf', pos=(1500, 500))
        self.add_widget(self.vrh)
        
        self.vlh =  Label(text='', font_size=30, markup=True, font_name='mw.ttf', pos=(400, 500))
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        keyboard.on_press_key('`', self.on_keyboard_down)


    def on_keyboard_down(self, event):
        # Check if the pressed key is '`'
        print(event.name)
        if event.name == '`':
            # Call the start_recording function
            self.start_recording()
  

    def start_recording(self, *args):
        # Move the speech recognition logic to a separate thread
        threading.Thread(target=self.run_speech_recognition).start()
        # multiprocessing.Process(target=self.run_speech_recognition).start()

    def run_speech_recognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold=1
            audio = r.listen(source)

        query = r.recognize_google(audio,language="en-in")
        # query = take_command()
        # Update the GUI from the main thread using Clock.schedule_once
    
        Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', query))
        CircleWidget.handle_jarvis_commands(query.lower())
        return query.lower()

    
    
    def update_time(self, dt):
        current_time = time.strftime('TIME\n\t%H:%M:%S')
        self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'

    
    

    def update_circle(self, dt):
        try:
            self.size_value = int(np.mean(self.volume_history))
        except Exception as E:
            self.size_value = self.min_size
            
        
        
        # Ensure the size remains within the defined limits
        if self.size_value <= self.min_size:
            self.size_value = self.min_size
        elif self.size_value >= self.max_size:
            self.size_value = self.max_size

        # Update the size and position of the circle button
        self.circle.size = (self.size_value, self.size_value)
        self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)


    def update_volume(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 100
        self.volume = volume_norm
        self.volume_history.append(volume_norm)
        self.vrh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
        self.vlh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
        self.vlh.text = f'''[b][color=3344ff]
            {round(self.volume_history[0], 7)}\n
            {round(self.volume_history[1], 7)}\n
            {round(self.volume_history[2], 7)}\n
            {round(self.volume_history[3], 7)}\n
            {round(self.volume_history[4], 7)}\n
            {round(self.volume_history[5], 7)}\n
            {round(self.volume_history[6], 7)}\n
            [/color][/b]'''
        
        self.vrh.text = f'''[b][color=3344ff]
            {round(self.volume_history[0], 7)}\n
            {round(self.volume_history[1], 7)}\n
            {round(self.volume_history[2], 7)}\n
            {round(self.volume_history[3], 7)}\n
            {round(self.volume_history[4], 7)}\n
            {round(self.volume_history[5], 7)}\n
            {round(self.volume_history[6], 7)}\n
            [/color][/b]'''
        # Keep the volume history within the defined size limit
        if len(self.volume_history) > self.volume_history_size:
            self.volume_history.pop(0)


    def start_listening(self):
        self.stream = sd.InputStream(callback=self.update_volume)
        self.stream.start()
       
    def handle_jarvis_commands(query):
        try:
            if "how are you" in query:
                speak("I am fine how are you.")
        
            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad for you sir")
                notepad_path = "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
                os.startfile(notepad_path)

            elif "open discord" in query:
                speak("Opening Discord for you sir")
                discord_path = "C:\\Users\\ASUS\\AppData\\Local\\Discord\\app-1.0.9028\\Discord.exe"
                os.startfile(discord_path)

            elif "open gta" in query:
                speak("Opening Gta for you sir")
                gta_path = "D:\\Tanishq\\GTA\\Launcher.exe"
                os.startfile(gta_path)
        

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

        # elif 'calculate' in query:
        #             app_id = ""
        #             client = wolframalpha.Client(app_id)
        #             ind = query.lower().split().index("calculate")
        #             text = query.split()[ind + 1:]
        #             res = client.query(" ".join(text))
        #             try:
        #                 ans = next(res.results).text
        #                 speak("The answer is " + ans)
        #                 print("the answer is " + ans)
        #             except StopIteration:
        #                 speak("I couldn't calculate that. Please try again.")

        # elif 'what is' in query or 'who is' in query or 'which is' in query or 'where did ' in query:
        #             app_id = ""  # Replace with your actual Wolfram Alpha App ID
        #             client = wolframalpha.Client(app_id)
        #             try:

        #                 ind = query.lower().index('what is') if 'what is' in query.lower() else \
        #                     query.lower().index('who is') if 'who is' in query.lower() else \
        #                         query.lower().index('which is') if 'which is' in query.lower() else None

        #                 if ind is not None:
        #                     text = query.split()[ind + 2:]
        #                     res = client.query(" ".join(text))
        #                     ans = next(res.results).text
        #                     speak("The answer is " + ans)
        #                     print("The answer is " + ans)
        #                 else:
        #                     speak("I couldn't find that. Please try again.")
        #             except StopIteration:
        #                 speak("I couldn't find that. Please try again.")

        # elif 'ip address' in query:
        #             ip_address = find_my_ip()
        #             speak(
        #                 f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
        #             print(f'Your IP Address is {ip_address}')

            elif 'search on wikipedia' in query:
                        speak('What do you want to search on Wikipedia, sir?')        
                        return_val = take_command().result_queue.get()
                        results = search_on_wikipedia(return_val)
                        speak(f"According to Wikipedia, {results}")
                        # speak("For your convenience, I am printing it on the screen sir.")
                        # print(results)

            elif 'youtube' in query:
                        speak('What do you want to play on Youtube, sir?')
                        video = take_command().result_queue.get()
                        youtube(video)

            elif 'search on google' in query:
                        speak('What do you want to search on Google, sir?')
                        query = take_command().result_queue.get()
                        search_on_google(query)

            elif "send an email" in query:
                        speak("On what email address do I send sir? Please enter in the console: ")
                        receiver_address = input("Enter email address: ")
                        speak("What should be the subject sir?")
                        subject = take_command().result_queue.get()
                        speak("What is the message sir?")
                        message = take_command().result_queue.get()
                        if send_email(receiver_address, subject, message):
                            speak("I've sent the email sir.")
                            print("I've sent the email sir.")
                        else:
                            speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        # elif 'tell me any joke' in query:
        #             speak(f"Hope you like this one sir")
        #             joke = get_random_joke()
        #             speak(joke)
        #             speak("For your convenience, I am printing it on the screen sir.")
        #             pprint(joke)

            elif 'movie' in query:
                        movies_db = imdb.IMDb()
                        speak("please tell me the movie name :")
                        text = take_command().result_queue.get()
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
                        
                        speak(f"I'm reading out the latest news hea`dlines, sir")
                        speak(get_news())
                        

            elif 'weather' in query:
                        ip_address = find_my_ip()
                        city = 'indore'
                        speak(f"Getting weather report for your city {city}")
                        weather, temperature, feels_like = weather_forecast(city)
                        speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                        speak(f"Also, the weather report talks about {weather}")
                        speak("For your convenience, I am printing it on the screen sir.")
                        print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
           
        except Exception as e:
            print(e)
        

        
# Custom Kivy App class
class MyKivyApp(App):

    def build(self):
        # speak('Hey Dhruv I am Jarvis your personal assistant')
        
        circle_widget = CircleWidget()

        # Start listening to the audio stream
        circle_widget.start_listening()

        # Schedule the update events for the circle widget
        self.update_event = Clock.schedule_interval(circle_widget.update_circle, 1 / 60)
        self.btn_rotation_event = Clock.schedule_interval(circle_widget.circle.rotate_button, 1 / 60)

        return circle_widget
        


# Run the Kivy application
if __name__ == '__main__':
    MyKivyApp().run()
    