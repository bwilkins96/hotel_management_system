# SWDV 630 - Object-Oriented Software Architecture
# base class for mapping classes with the SQLAlchemy ORM

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """SQLAlchemy base class"""
    
    def save(self, session):
        """Saves the instance to database connected to session"""
        session.add(self)
        session.commit()

    @staticmethod
    def save_all(lst, session):
        """Saves all instances in lst to database connected to session"""
        for obj in lst:
            session.add(obj)
        session.commit()

    @classmethod
    def get_all(cls, session):
        """Returns all instances of class from database connected to session"""
        stmt = select(cls)
        return session.scalars(stmt).all()

    
