# SWDV 630 - Object-Oriented Software Architecture
# Room class

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import PickleType
from sqlalchemy.orm.session import make_transient
from base import Base
from prototype import Prototype, PrototypeFactory

class Room(Base, Prototype):
    def __init__(self, room_num, type, rate):
        self._room_number = int(room_num)
        self._type = type
        self._rate = float(rate)
        self._unavailable_dates = {}

    __tablename__ = 'room'

    _room_number: Mapped[int] = mapped_column(primary_key=True)
    _type: Mapped[str]
    _rate: Mapped[float]
    _unavailable_dates = mapped_column(PickleType)

    def get_room_number(self):
        return self._room_number
    
    def set_room_number(self, room_num):
        self._room_number = int(room_num)

    def get_type(self):
        return self._type
    
    def get_rate(self):
        return self._rate
    
    def set_rate(self, rate):
        self._rate = float(rate)

    def add_unavailable(self, start, end):
        self._unavailable_dates[start] = end

    def remove_unavailable(self, start):
        del self._unavailable_dates[start]

    def available_on(self, start_date, end_date=None):
        for start in self._unavailable_dates:
            end = self._unavailable_dates[start]

            if start_date >= start and start_date < end:
                return False
            
            if end_date and (end_date >= start and end_date < end):
                return False
            
        return True

    def calculate_total(self, num_days):
        return self._rate * num_days
    
    @classmethod
    def get_all_available(cls, session, start_date, end_date=None):
        rooms = cls.get_all(session)
        return [room for room in rooms if room.available_on(start_date, end_date)]
    
    def __repr__(self):
        return f'<Room {self._room_number}: ${self._rate:.2f}>'
    
class RoomFactory(PrototypeFactory):
    def register(self, key, room):
        if type(room) == Room:
            room_clone = room.clone()
            make_transient(room_clone)
            return super().register(key, room_clone)
        
        return False
    
def test():
    from datetime import datetime

    room = Room(101, 'king', 175)
    room.add_unavailable(datetime(2023, 8, 1), datetime(2023, 8, 5))
    
    print(room.available_on(datetime(2023, 8, 3)))    # -> False
    print(room.available_on(datetime(2023, 7, 3)))    # -> True
    print(room.available_on(datetime(2023, 8, 4), datetime(2023, 8, 8)))    # -> False
    print(room.available_on(datetime(2023, 8, 5), datetime(2023, 8, 8)))    # -> True

if __name__ == '__main__': test()
