from typing import List, Optional
from app.models.flower import Flower


class FlowersRepository:
    def __init__(self):
        self._flowers: List[Flower] = []
        self._next_id = 1

    def create(self, title: str, amount: int, price: float) -> Flower:
        flower = Flower(id=self._next_id, title=title, amount=amount, price=price)
        self._next_id += 1
        self._flowers.append(flower)
        return flower

    def list_all(self) -> List[Flower]:
        return list(self._flowers)

    def get_by_id(self, flower_id: int) -> Optional[Flower]:
        return next((f for f in self._flowers if f.id == flower_id), None)