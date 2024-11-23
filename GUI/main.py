from dotenv import load_dotenv
load_dotenv()
from kivy import app, clock
from jarvis import Jarvis

class MykivyApp(app.App):
    def build(self):
        jarvis = Jarvis()
        jarvis.start_listening()
        
        self.update_event = clock.Clock.schedule_interval(jarvis.update_circle,1/60)
        self.btn_rotation_event = clock.Clock.schedule_interval(jarvis.circle.rotate_button,1/60)
        
        return jarvis
    
    
if __name__ == '__main__':
    MykivyApp = MykivyApp()
    MykivyApp.run()    