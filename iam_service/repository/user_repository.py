from sqlmodel import Session, select
from models.user import User


class UserRepository:

    # Create
    def create(self, db: Session, user: User):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e

    # Get by Email
    def get_by_email(self, db: Session, email: str):
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    # Get by ID
    def get_by_id(self, db: Session, user_id):
        statement = select(User).where(User.id == user_id)
        return db.exec(statement).first()

    # Get All Users
    def get_all(self, db: Session):
        statement = select(User)
        return db.exec(statement).all()

    # Update User
    def update(self, db: Session, user: User):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e

    #Delete User
    def delete(self, db: Session, user_id):
        try:
            user = self.get_by_id(db, user_id)
            if not user:
                return False

            db.delete(user)
            db.commit()
            return True

        except Exception as e:
            db.rollback()
            raise e