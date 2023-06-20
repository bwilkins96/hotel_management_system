# SWDV 630 - Object-Oriented Software Architecture
# Room class

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import PickleType
from base import Base
from prototype import Prototype

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

    def available_on(self, date):
        for start in self._unavailable_dates:
            end = self._unavailable_dates[start]

            if date >= start and date < end:
                return False
            
        return True

    def calculate_total(self, num_days):
        return self._rate * num_days
    
    def __repr__(self):
        return f'<Room {self._room_number}: ${self._rate:.2f}>'
    
def test():
    from datetime import date

    room = Room(101, 'king', 175)
    room.add_unavailable(date(2023, 8, 1), date(2023, 8, 5))
    
    print(room.available_on(date(2023, 8, 3)))    # -> False
    print(room.available_on(date(2023, 7, 3)))    # -> True

if __name__ == '__main__': test()
