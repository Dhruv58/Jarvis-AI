from kivy.uix.button import Button
from kivy.graphics import Rotate

class JarvisButton(Button):
    def __init__(self, **kwargs):
        super(JarvisButton,self).__init__(**kwargs)
        self.angle = 2
        self.background_angle = 0
        
    def rotate_button(self, *args):
        self.background_angle += self.angle
        self.canvas.before.clear()
        with self.canvas.before:
            Rotate(angle=self.background_angle,origin=self.center)    