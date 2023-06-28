# SWDV 630 - Object-Oriented Software Architecture
# Stay class

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from room import Room

class Stay(Base):
    def __init__(self, room, start, end, keycards=2): 
        self._room = None
        self._checked_in = False
        self._start = start
        self._end = end
        self._remaining_keycards = keycards
        self._replacement_keycards = 0

        self._setup_room(room)

    __tablename__ = 'stay'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _room_number: Mapped[int] = mapped_column(ForeignKey('room._room_number'))
    _room: Mapped[Room] = relationship()
    _start: Mapped[datetime]
    _end: Mapped[datetime]
    _checked_in: Mapped[bool]
    _remaining_keycards: Mapped[int]
    _replacement_keycards: Mapped[int]
    _guest_id: Mapped[int] = mapped_column(ForeignKey('person._id'), nullable=True)

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
        self.reset_room()
        self._room = None
        self._setup_room(room)

    def set_start(self, start):
        self.reset_room()
        self._start = start
        self._setup_room(self.get_room())

    def set_end(self, end):
        self.reset_room()
        self._end = end
        self._setup_room(self.get_room())

    def set_remaining_keycards(self, keycards):
        self._remaining_keycards = keycards

    def reset_room(self):
        room = self.get_room()
        room.remove_unavailable(self.get_start())

    def _setup_room(self, room):
        start = self.get_start()
        end = self.get_end()

        if not room.available_on(start, end):
            raise Exception('Room instance is not available on specified dates')

        self._room = room
        room.add_unavailable(start, end)

    def num_nights(self):
        return (self.get_end() - self.get_start()).days

    def check_in(self):
        if self.is_checked_in(): return False
        
        self._checked_in = True
        self.reset_room()
        self._start = datetime.now()
        self._setup_room(self.get_room())
        return True

    def check_out(self):
        if not self.is_checked_in(): return False
        
        self._checked_in = False
        self._end = datetime.now()
        return True
    
    def is_checked_in(self):
        return self._checked_in
    
    def get_keycard(self, printer):
        if self.get_remaining_keycards() > 0:
            printer.print_keycard(self.get_room())
            self._remaining_keycards -= 1
            return True
        
        return False
    
    def replace_keycard(self, printer):
        printer.print_keycard(self.get_room())
        self._replacement_keycards += 1

    def get_total_charge(self):
        room = self.get_room()
        return room.calculate_total(self.num_nights())
    
    def __repr__(self):
        room_number = self.get_room().get_room_number()
        start_date = self.get_start().date()
        end_date = self.get_end().date()
        return f'<Stay: Room {room_number}, {start_date} to {end_date}>'
    
def test():
    from utils import future_datetime

    room = Room(101, 'queen', 150)
    stay = Stay(room, datetime.now(), datetime.now())
    future = future_datetime(4)
    future_2 = future_datetime(5)

    print(stay.get_room().available_on(future))    # -> True
    stay.set_end(future_2)
    print(stay.get_room().available_on(future))    # -> False

    stay.check_in()
    print(f'\n{stay.is_checked_in()}')             # -> True
    stay.check_out()
    print(stay.is_checked_in())                    # -> False

    # Test room available validation
    try:
        stay_2 = Stay(room, datetime.now(), future_2)
    except:
        print('\ncorrectly raised exception')

    stay_3 = Stay(room, future_datetime(10), future_datetime(14))
    print("correctly didn't raise exception")

if __name__ == '__main__': test()
