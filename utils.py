# SWDV 630 - Object-Oriented Software Architecture

from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from base import Base

def get_session(echo=False):
    #engine = create_engine("sqlite+pysqlite:///test.db", echo=echo)
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=echo)
    Base.metadata.create_all(engine)
    return Session(engine)

def future_date(days):
    return datetime.now() + timedelta(days=days)