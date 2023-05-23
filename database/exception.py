class IntegrityError(Exception):
    def __init__(self, message):
        super().__init__(f"Database Intgrity Error: {message}")


class IdentityMapError(Exception):
    def __init__(self, message):
        super().__init__(f"Identity Map Error: {message}")
