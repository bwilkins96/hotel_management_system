# SWDV 630 - Object-Oriented Software Architecture
# Stay class

from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from room import Room

class Stay(Base):
    def __init__(self, room, start, end): 
        self._room = room
        self._checked_in = False
        self._start = start
        self._end = end

    __tablename__ = 'stay'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _room_number: Mapped[int] = mapped_column(ForeignKey('room._room_number'))
    _room: Mapped[Room] = relationship()
    _start: Mapped[date]
    _end: Mapped[date]
    _checked_in: Mapped[bool]

    def checked_in(self):
        return self._checked_in

    def check_in(self):
        if self.checked_in(): return False
        
        self._checked_in = True
        self._start = date.today()
        return True

    def check_out(self):
        if not self.checked_in(): return False
        
        self._checked_in = False
        self._end = date.today()
        return True
    
    def is_checked_in(self):
        return self._checked_in
    
    def __repr__(self):
        return f'<Stay: Room {self._room.get_room_number()}, {self._start} to {self._end}>'