# SWDV 630 - Object-Oriented Software Architecture

from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from base import Base

from factory import PersonFactory
from prototype import PrototypeFactory
from room import Room
from stay import Stay
from schedule import Shift, Schedule
from printer import Printer

def get_session(echo=False):
    #engine = create_engine("sqlite+pysqlite:///test.db", echo=echo)
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=echo)
    Base.metadata.create_all(engine)
    return Session(engine)

def future_date(days):
    return datetime.now() + timedelta(days=days)

def book_stay(guest, stay, session=None):
    guest.set_stay(stay)
    account = guest.get_account()
    room = stay.get_room()
    
    total_charge = room.calculate_total(stay.num_nights())
    account.charge(total_charge)

    if session:
        guest.save(session)
        stay.save(session)

def main():
    session = get_session()

    room_1 = Room(1, 'queen', 100)
    room_2 = Room(2, 'king', 125)
    room_3 = Room(3, '2 queens', 150)

    manager = PersonFactory.create('manager', 30, 'Jenny', 'manager@email.com')
    emp_a = PersonFactory.create('employee', 20, 'Julian', 'emp_a@email.com')
    emp_b = PersonFactory.create('employee', 20, 'Jennifer', 'emp_b@email.com')
    manager.add_employee(emp_a)
    manager.add_employee(emp_b)

    printer = Printer(100)

    # Check availability / room rate
    print(room_1.available_on(future_date(2)))
    print(room_1.get_rate())

    # Create guest and book stay
    guest_a = PersonFactory.create('guest', None, 'Mike', 'guest_a@email.com')
    stay_a = Stay(room_1, future_date(2), future_date(7))
    book_stay(guest_a, stay_a)
    print(f'\n{guest_a.get_stay()}')
    print(guest_a.get_account().get_total_due())


    session.close()

if __name__ == '__main__': main()