# SWDV 630 - Object-Oriented Software Architecture
# base class for mapping classes with the SQLAlchemy ORM

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    def save(self, session):
        session.add(self)
        session.commit()

    @staticmethod
    def save_all(lst, session):
        for obj in lst:
            session.add(obj)
        session.commit()
    
