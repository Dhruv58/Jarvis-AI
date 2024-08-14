import os
from kivy.config import Config 
from dotenv import load_dotenv
load_dotenv("env/.env")

width, height = 1920, 1080

Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'fullscreen', 'True')

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

IP_ADDR_API_URL = os.environ.get("IP_ADDR_API_URL")
NEWS_FETCH_API_URL = os.environ.get("NEWS_FETCH_API_URL")
NEWS_FETCH_API_KEY = os.environ.get("NEWS_FETCH_API_KEY")
WEATHER_FORECAST_API_URL = os.environ.get("WEATHER_FORECAST_API_URL")
WEATHER_FORECAST_API_KEY = os.environ.get("WEATHER_FORECAST_API_KEY")

SCREEN_WIDTH = Config.getint('graphics', 'width')
SCREEN_HEIGHT = Config.getint('graphics', 'height')

SMTP_URL = os.environ.get("SMTP_URL")
SMTP_PORT = os.environ.get("SMTP_PORT")

RANDOM_TEXT = [
    "Cool, I'm on it sir.",
    "Okay sir, I'm working on it.",
    "Just a second sir.",
]