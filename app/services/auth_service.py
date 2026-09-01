"""Authentication business logic placeholder."""


class AuthService:
    def __init__(self):
        self.user_count = 0

    def authenticate(self, email: str, password: str) -> bool:
        return bool(email and password)
