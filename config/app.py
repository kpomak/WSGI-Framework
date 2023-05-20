from whitenoise import WhiteNoise

from config.core import RainbowFucktory
from config.settings import RAINBOW_TYPE, DATABASE_URI
from config.urls import url_patterns, context_gen
from database.storage import init_db
from mainapp import views


def create_app():
    app = RainbowFucktory.create(RAINBOW_TYPE, url_patterns, context_gen)
    app = WhiteNoise(app)
    app.add_files("./static", "static/")

    init_db(DATABASE_URI)

    return app
