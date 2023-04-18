from wsgiref.simple_server import make_server
from whitenoise import WhiteNoise

from config.core import Rainbow
from config.settings import SERVER_IP_ADDRESS, SERVER_PORT
from config.urls import url_patterns, context_gen


app = Rainbow(url_patterns, context_gen)
app = WhiteNoise(app)
app.add_files('./static', 'static/')

server = make_server(SERVER_IP_ADDRESS, SERVER_PORT, app)
print(f'Server started on {SERVER_IP_ADDRESS or "0.0.0.0"}:{SERVER_PORT}')
try:
  server.serve_forever()
except KeyboardInterrupt:
  print('\nServer is shutting down')
