from config.middlware import Logger


SERVER_IP_ADDRESS = ""
SERVER_PORT = 5000

RAINBOW_TYPE = "app"  # app | log | fake

DATABASE_URI = "db.sqlite3"

logger = Logger("server")
