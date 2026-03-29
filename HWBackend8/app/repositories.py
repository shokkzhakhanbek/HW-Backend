from sqlalchemy.orm import Session

from models import User, Flower, Purchase

class UsersRepository:

    def create_user(self, db: Session, email: str, full_name: str, password: str) -> User:
        new_user = User(
            email=email,
            full_name=full_name,
            password=password 
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()


class FlowersRepository:

    def get_all_flowers(self, db: Session) -> list[Flower]:
        return db.query(Flower).all()

    def create_flower(self, db: Session, name: str, count: int, cost: float) -> Flower:
        new_flower = Flower(name=name, count=count, cost=cost)
        db.add(new_flower)
        db.commit()
        db.refresh(new_flower)
        return new_flower

    def get_flower_by_id(self, db: Session, flower_id: int) -> Flower | None:
        return db.query(Flower).filter(Flower.id == flower_id).first()

    def update_flower(self, db: Session, flower_id: int, name: str = None, count: int = None, cost: float = None) -> Flower | None:
        flower = self.get_flower_by_id(db, flower_id)
        if flower is None:
            return None

        if name is not None:
            flower.name = name
        if count is not None:
            flower.count = count
        if cost is not None:
            flower.cost = cost

        db.commit()
        db.refresh(flower)
        return flower

    def delete_flower(self, db: Session, flower_id: int) -> bool:
        flower = self.get_flower_by_id(db, flower_id)
        if flower is None:
            return False

        db.delete(flower)
        db.commit()
        return True


class PurchasesRepository:

    def create_purchase(self, db: Session, user_id: int, flower_id: int) -> Purchase:
        new_purchase = Purchase(user_id=user_id, flower_id=flower_id)
        db.add(new_purchase)
        db.commit()
        db.refresh(new_purchase)
        return new_purchase

    def get_purchases_by_user(self, db: Session, user_id: int) -> list[Purchase]:
        return db.query(Purchase).filter(Purchase.user_id == user_id).all()