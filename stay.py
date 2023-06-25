# SWDV 630 - Object-Oriented Software Architecture
# Stay class

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from room import Room

class Stay(Base):
    def __init__(self, room, start, end, keycards=2): 
        self._room = room
        self._checked_in = False
        self._start = start
        self._end = end
        self._remaining_keycards = keycards
        self._replacement_keycards = 0

        self._setup_room()

    __tablename__ = 'stay'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _room_number: Mapped[int] = mapped_column(ForeignKey('room._room_number'))
    _room: Mapped[Room] = relationship()
    _start: Mapped[datetime]
    _end: Mapped[datetime]
    _checked_in: Mapped[bool]
    _remaining_keycards: Mapped[int]
    _replacement_keycards: Mapped[int]

    def get_room(self):
        return self._room
    
    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    
    def get_remaining_keycards(self):
        return self._remaining_keycards
    
    def get_replacement_keycards(self):
        return self._replacement_keycards
    
    def set_room(self, room):
        self._reset_room()
        self._room = room
        self._setup_room()

    def set_start(self, start):
        self._reset_room()
        self._start = start
        self._setup_room()

    def set_end(self, end):
        self._reset_room()
        self._end = end
        self._setup_room()

    def set_remaining_keycards(self, keycards):
        self._remaining_keycards = keycards

    def _setup_room(self):
        room = self.get_room()
        room.add_unavailable(self.get_start(), self.get_end())

    def _reset_room(self):
        room = self.get_room()
        room.remove_unavailable(self.get_start())

    def check_in(self):
        if self.checked_in(): return False
        
        self._checked_in = True
        self._start = datetime.now()
        return True

    def check_out(self):
        if not self.checked_in(): return False
        
        self._checked_in = False
        self._end = datetime.now()
        return True
    
    def is_checked_in(self):
        return self._checked_in
    
    def get_keycard(self, printer):
        if self.get_remaining_keycards() > 0:
            printer.print_keycard()
            self._remaining_keycards -= 1
            return True
        
        return False
    
    def replace_keycard(self, printer):
        printer.print_keycard()
        self._replacement_keycards += 1
    
    def __repr__(self):
        room_number = self.get_room().get_room_number()
        start_date = self.get_start().date()
        end_date = self.get_end().date()
        return f'<Stay: Room {room_number}, {start_date} to {end_date}>'
    
def test():
    from datetime import timedelta

    room = Room(101, 'queen', 150)
    stay = Stay(room, datetime.now(), datetime.now())
    print(stay.get_room()._unavailable_dates)
    
    print()
    stay.set_end(datetime.now() + timedelta(days=5))
    print(stay.get_room()._unavailable_dates)

if __name__ == '__main__': test()
