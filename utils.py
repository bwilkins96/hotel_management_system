# SWDV 630 - Object-Oriented Software Architecture
# Utility functions

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from base import Base

def get_session(echo=False):
    #engine = create_engine("sqlite+pysqlite:///test.db", echo=echo)
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=echo)
    Base.metadata.create_all(engine)
    return Session(engine)

def future_datetime(days=0, hours=0):
    return datetime.now() + timedelta(days=days, hours=hours)

def calculate_hours(time1, time2):
    if time2 > time1:
        diff = time2 - time1
    else:
        diff = time1 - time2

    hours = diff.seconds / 60 / 60
    return hours