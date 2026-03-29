from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    email: str
    full_name: str
    password_hash: str
    photo_filename: Optional[str] = None