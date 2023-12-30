import numpy as np
import sounddevice as sd
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Rotate, Rectangle, Color
from kivy.uix.image import Image

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.textinput import TextInput

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
        self.volume_history = []

        # By increasing the size of volume_history_size, you can make the transition of size more smooth.
        self.volume_history_size = 50

        # Define relative minimal and maximal sizes for your circle
        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH
        print(self.min_size)
        # Create a rotating button representing the circle
        self.add_widget(Image(source='border.eps.png', size=(1920, 1080)))
        self.circle = RotatingButton(size=(284.0, 284.0), background_normal='circle.png')
        # self.add_widget(Image(source='jarvis.gif', size=(self.min_size, self.min_size)))
        self.add_widget(Image(source='jarvis.gif', size=(self.min_size, self.min_size), pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)))

        # Create a label for displaying the spoken text
        # self.add_widget(Label(text='Hey, I am Jarvis!', font_size=20, markup=True, pos=(0, 0)))
        
        time_layout = BoxLayout(orientation='vertical', pos=(150,900))
        self.time_label = Label(text='', font_size=24, markup=True, font_name='mw.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)
        # Schedule the update function for the time label
        Clock.schedule_interval(self.update_time, 1)
        
        self.title = Label(text='[b][color=3333ff]ERROR BY NIGHT[/color][/b]', font_size=42, markup=True, font_name='mw.ttf', pos=(800, 900))
        self.add_widget(self.title)

        self.subtitles_input = TextInput(
            text='Hey Dhruv! I am Jarvis, your personal assistant.',
            font_size=20,
            readonly=True,
            background_color=(0, 0, 0, 0),  # Set background color to be transparent
            foreground_color=(1, 1, 1, 1),  # Set text color to be white
            size_hint_y=None,
            height=80,  # Set the height of the TextInput
            pos=(750, 100),
            width=1200,
        )
        self.add_widget(self.subtitles_input)

        self.add_widget(self.circle)



    def update_time(self, dt):
        current_time = time.strftime('TIME\n\t%H:%M:%S')
        self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'


    def update_circle(self, dt):
        try:
            self.size_value = int(np.mean(self.volume_history))
        except:
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
        
        # Keep the volume history within the defined size limit
        if len(self.volume_history) > self.volume_history_size:
            self.volume_history.pop(0)

    def start_listening(self):
        self.stream = sd.InputStream(callback=self.update_volume)
        self.stream.start()

# Custom Kivy App class
class MyKivyApp(App):

    def build(self):
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
