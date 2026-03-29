from typing import Optional, List
from app.models.user import User


class UsersRepository:
    def __init__(self):
        self._users: List[User] = []
        self._next_id = 1

    def create(self, email: str, full_name: str, password_hash: str, photo_filename: str | None = None) -> User:
        user = User(
            id=self._next_id,
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            photo_filename=photo_filename
        )
        self._next_id += 1
        self._users.append(user)
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._users if u.email == email), None)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self._users if u.id == user_id), None)