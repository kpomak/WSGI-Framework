class IntegrityError(Exception):
    def __init__(self, message):
        super().__init__(f"Database Intgrity Error: {message}")
