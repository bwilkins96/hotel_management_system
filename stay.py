# SWDV 630 - Object-Oriented Software Architecture
# Stay class

from datetime import datetime
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
    _start: Mapped[datetime]
    _end: Mapped[datetime]
    _checked_in: Mapped[bool]

    def get_room(self):
        return self._room
    
    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    
    def set_room(self, room):
        self._room = room

    def set_start(self, start):
        self._start = start

    def set_end(self, end):
        self._end = end

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
    
    def __repr__(self):
        room_number = self.get_room().get_room_number()
        start_date = self.get_start().date()
        end_date = self.get_end().date()
        return f'<Stay: Room {room_number}, {start_date} to {end_date}>'