import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
from datetime import datetime


class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI")

        # Text area to display responses
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

        # Entry for user input
        self.user_input_entry = tk.Entry(root, width=30)
        self.user_input_entry.grid(column=0, row=1, padx=10, pady=10)

        # Button to submit user input
        self.submit_button = tk.Button(root, text="Submit", command=self.process_user_input)
        self.submit_button.grid(column=1, row=1, padx=10, pady=10)

        # Button to enable speech recognition
        self.listen_button = tk.Button(root, text="Listen", command=self.listen_to_user)
        self.listen_button.grid(column=2, row=1, padx=10, pady=10)

        # Initialize Text-to-Speech engine
        self.engine = pyttsx3.init()

    def process_user_input(self):
        user_input = self.user_input_entry.get()
        self.display_response(f"User: {user_input}")

        # Call your Jarvis AI logic here
        # You can replace the following line with your own Jarvis AI processing
        response = f"Jarvis: You said '{user_input}'. Implement your AI logic here."
        self.display_response(response)

    def listen_to_user(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio)
            self.user_input_entry.delete(0, tk.END)
            self.user_input_entry.insert(0, user_input)
        except sr.UnknownValueError:
            messagebox.showinfo("Error", "Sorry, I could not understand your speech.")
        except sr.RequestError:
            messagebox.showinfo("Error", "There was an error connecting to Google Speech Recognition service.")

    def display_response(self, response):
        self.text_area.insert(tk.END, f"{response}\n")
        self.engine.say(response)
        self.engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    gui = JarvisGUI(root)
    root.mainloop()
