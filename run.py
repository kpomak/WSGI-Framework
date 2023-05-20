from wsgiref.simple_server import make_server

from config.app import create_app
from config.settings import SERVER_IP_ADDRESS, SERVER_PORT

app = create_app()


if __name__ == "__main__":
    server = make_server(SERVER_IP_ADDRESS, SERVER_PORT, app)
    print(f'Server started on {SERVER_IP_ADDRESS or "0.0.0.0"}:{SERVER_PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down")
