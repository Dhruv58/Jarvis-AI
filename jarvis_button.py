from kivy.uix.button import Button
from kivy.graphics import Rotate

class JarvisButton(Button):
    def __init__(self, **kwargs):
        super(JarvisButton, self).__init__(**kwargs)
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
