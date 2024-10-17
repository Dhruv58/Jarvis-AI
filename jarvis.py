import time
import threading
import keyboard
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import os
import pyautogui
import subprocess as sp
import webbrowser
import imdb
from kivy.uix import widget, image, label, boxlayout, textinput
from kivy import clock
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, RANDOM_TEXT,GEMINI_API
from utils import speak, youtube,search_on_google,search_on_wikipedia,send_email,get_news,weather_forecast,find_my_ip
from jarvis_button import JarvisButton
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='AIzaSyAN88my5PXgphFsuFVJusu-hJQY1WYa4_4')
model = genai.GenerativeModel('gemini-1')

class Jarvis(widget.Widget):
    def __init__(self, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0,0,0,0,0,0,0]

        self.volume_history_size = 140

        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH
        
        self.add_widget(image.Image(source='static/border.eps.png', size=(1920, 1080)))
        self.circle = JarvisButton(size=(284.0, 284.0), background_normal='static/circle.png')
        self.circle.bind(on_press=self.start_recording)
        self.start_recording()
        self.add_widget(image.Image(source='static/jarvis.gif', size=(self.min_size, self.min_size), pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)))

        
        time_layout = boxlayout.BoxLayout(orientation='vertical', pos=(150,900))
        self.time_label = label.Label(text='', font_size=24, markup=True, font_name='static/mw.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)

        clock.Clock.schedule_interval(self.update_time, 1)
        
        self.title = label.Label(text='[b][color=3333ff]ERROR BY NIGHT[/color][/b]', font_size=42, markup=True, font_name='static/dusri.ttf', pos=(920, 900))
        self.add_widget(self.title)

        self.subtitles_input = textinput.TextInput(
            text='Hey Dhruv! I am Jarvis, your personal assistant.',
            font_size=24,
            readonly=True,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=80,
            pos=(720, 100),
            width=1200,
            font_name='static/teesri.otf',
        )
        self.add_widget(self.subtitles_input)
        self.vrh =  label.Label(text='', font_size=30, markup=True, font_name='static/mw.ttf', pos=(1500, 500))
        self.add_widget(self.vrh)
        
        self.vlh =  label.Label(text='', font_size=30, markup=True, font_name='static/mw.ttf', pos=(400, 500))
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        # keyboard.on_press_key('`', self.on_keyboard_down)
        keyboard.add_hotkey('`', self.start_recording)

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language='en-in')
            return query.lower()
        
        except Exception:
            speak("Sorry I couldn't understand. Can you please repeat that?")
            query = 'None'
        

    def start_recording(self, *args):
        print('Recording started')
        threading.Thread(target=self.run_speech_recognition).start()
        print('Recording ended')

    def run_speech_recognition(self):
        print('before speech rec obj')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            print('audio recorded')

        print('after speech rec obj')
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"Recognized: {query}")
        # Update the GUI from the main thread using Clock.schedule_once
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', query))
            self.handle_jarvis_commands(query.lower())
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return query.lower() 

    def get_gemini_response(self, query):
        try:
            response = model.generate_content(query)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return "I'm sorry, I couldn't process that request."
    
    def update_time(self, dt):
        current_time = time.strftime('TIME\n\t%H:%M:%S')
        self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'


    def update_circle(self, dt):
        # print('UPDATING CIRLC ESIEZ ')
        try:
            self.size_value = int(np.mean(self.volume_history))
            # print('SIZE VALUE: ', self.size_value)
        except Exception as e:
            self.size_value = self.min_size
            print('WARNING: ', e)

        if self.size_value <= self.min_size:
            self.size_value = self.min_size
        elif self.size_value >= self.max_size:
            self.size_value = self.max_size
        self.circle.size = (self.size_value, self.size_value)
        self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)


    def update_volume(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 200
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
       
    def handle_jarvis_commands(self, query):
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


            elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(
                        f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')

            elif 'search on wikipedia' in query:
                        speak('What do you want to search on Wikipedia, sir?')        
                        return_val = self.take_command()
                        results = search_on_wikipedia(return_val)
                        speak(f"According to Wikipedia, {results}")
                        # speak("For your convenience, I am printing it on the screen sir.")
                        # print(results)

            elif 'youtube' in query:
                        speak('What do you want to play on Youtube, sir?')
                        video = self.take_command()
                        youtube(video)

            elif 'search on google' in query:
                        speak('What do you want to search on Google, sir?')
                        query = self.take_command()
                        search_on_google(query)

            elif "send an email" in query:
                        speak("On what email address do I send sir? Please enter in the console: ")
                        receiver_address = input("Enter email address: ")
                        speak("What should be the subject sir?")
                        subject = self.take_command()
                        speak("What is the message sir?")
                        message = self.take_command()
                        if send_email(receiver_address, subject, message):
                            speak("I've sent the email sir.")
                            print("I've sent the email sir.")
                        else:
                            speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

            elif 'movie' in query:
                        movies_db = imdb.IMDb()
                        speak("please tell me the movie name :")
                        text = self.take_command()
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
                        
                        speak("I'm reading out the latest news headlines, sir")
                        speak(get_news())
                        

            elif 'weather' in query.lower():
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")
            
            else:
                gemini_response = self.get_gemini_response(query)
                gemini_response = gemini_response.replace("*","")
                if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                    speak(gemini_response)
                    print(gemini_response)
                
            
        except Exception as e:
            print(e)
