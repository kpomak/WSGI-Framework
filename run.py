from wsgiref.simple_server import make_server
from whitenoise import WhiteNoise

from config.core import RainbowFucktory
from config.settings import SERVER_IP_ADDRESS, SERVER_PORT, RAINBOW_TYPE
from config.urls import url_patterns, context_gen


app = RainbowFucktory.create(RAINBOW_TYPE, url_patterns, context_gen)
app = WhiteNoise(app)
app.add_files("./static", "static/")

if __name__ == "__main__":
    server = make_server(SERVER_IP_ADDRESS, SERVER_PORT, app)
    print(f'Server started on {SERVER_IP_ADDRESS or "0.0.0.0"}:{SERVER_PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down")
