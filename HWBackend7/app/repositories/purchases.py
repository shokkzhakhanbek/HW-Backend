from typing import List
from app.models.purchase import Purchase

class PurchasesRepository:
    def __init__(self):
        self._purchases: List[Purchase] = []

    def add(self, user_id: int, flower_id: int) -> Purchase:
        purchase = Purchase(user_id=user_id, flower_id=flower_id)
        self._purchases.append(purchase)
        return purchase

    def list_by_user(self, user_id: int) -> List[Purchase]:
        return [p for p in self._purchases if p.user_id == user_id]