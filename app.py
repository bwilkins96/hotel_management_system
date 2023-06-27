# SWDV 630 - Object-Oriented Software Architecture
# Application file showing main functionality of hotel management system

from datetime import datetime
from base import Base

from factory import PersonFactory
from room import Room, RoomFactory
from stay import Stay
from schedule import Shift, Schedule
from account import Account
from printer import Printer

from utils import get_session, future_date

def main():
    session = get_session()

    room_1 = Room(1, 'queen', 100)
    room_2 = Room(2, 'king', 125)
    room_3 = Room(3, '2 queens', 150)

    manager = PersonFactory.create('manager', Schedule(), 30, 'Jenny', 'manager@email.com')
    emp_a = PersonFactory.create('employee', Schedule(), 20, 'Julian', 'emp_a@email.com')
    emp_b = PersonFactory.create('employee', Schedule(), 20, 'Jennifer', 'emp_b@email.com')
    manager.add_employee(emp_a)
    manager.add_employee(emp_b)

    guest_a = PersonFactory.create('guest', Account(), 'Mike', 'guest_a@email.com')
    guest_b = PersonFactory.create('guest', Account(), 'Marcy', 'guest_b@email.com')
    ga_account = guest_a.get_account()
    gb_account = guest_b.get_account()

    # Save data to database
    data = [room_1, room_2, room_3, manager, emp_a, emp_b, guest_a, guest_b]
    Base.save_all(data, session)

    printer = Printer(100)

    room_factory = RoomFactory()
    for room in [room_1, room_2, room_3]:
        room_factory.register(room.get_type(), room)

    # ---------------------- #
    # Use case functionality #
    # ---------------------- #

    # Check availability / room rate
    available_rooms = Room.get_all_available(session, datetime.now(), future_date(5))
    print(room_1.available_on(future_date(2)))    # -> True
    print(available_rooms)                        # -> List of all rooms
    print(room_1.get_rate())                      # -> 100

    # Book stay
    stay_a = Stay(room_1, datetime.now(), future_date(5))
    guest_a.book_stay(stay_a)
    print(f'\n{guest_a.get_stay()}\n')  

    # Check pay and pay bill
    print(ga_account.get_total_due())            # -> 500         
    ga_account.pay(ga_account.get_total_due())   
    print(f'{ga_account.get_total_due()}\n')     # -> 0

    # Check-in, check-out, get/replace room key
    stay_a.check_in()
    print(guest_a.is_checked_in())         # -> True
    stay_a.get_keycard(printer)            # Should print mock message
    stay_a.get_keycard(printer)            # Should print mock message

    stay_a.get_keycard(printer)            # Should NOT print mock message
    stay_a.replace_keycard(printer)        # Should print mock message
    stay_a.check_out()
    print(f'{guest_a.is_checked_in()}\n')  # -> False

    # Cancel stay
    stay_b = Stay(room_2, future_date(2), future_date(7))
    guest_b.book_stay(stay_b)

    print(gb_account)            # -> Balance due of $625
    guest_b.cancel_stay()
    print(guest_b.get_stay())    # -> None
    print(f'{gb_account}\n')     # -> Zero balance and credits

    # Alter stay
    stay_c = Stay(room_3, future_date(10), future_date(14))
    guest_b.book_stay(stay_c)   
    print(stay_c)                         
    guest_b.alter_stay(end=future_date(12))
    print(stay_c)
    print(f'{gb_account}\n')      # -> Balance due of $300

    # Check employee pay
    emp_a.add_hours(40, 5)
    print(f'{emp_a.get_total_pay()}\n')  # -> 950

    # Set / check work schedule
    ea_schedule = emp_a.get_schedule()
    shift_a = Shift(datetime.now(), future_date(hours=8))
    ea_schedule.add_shift(shift_a)
    print(f'{ea_schedule.get_shifts()}\n')

    # clock-in / clock-out of shift
    ea_schedule.get_current_shift().clock_in()
    print(emp_a.is_clocked_in())                   # -> True
    ea_schedule.get_current_shift().clock_out()
    print(f'{emp_a.is_clocked_in()}\n')            # -> False

    # Set room / room type rates
    room_2.set_rate(130)
    print(room_2.get_rate())    # -> 130

    for i in range(4, 16):
        new_room = room_factory.get('queen')
        new_room.set_room_number(i)
        data.append(new_room)

    Base.save_all(data, session)
    Room.set_type_rate('queen', 90, session)

    print(room_1.get_rate())    # -> 90
    room_factory.register('queen', room_1)

    Base.save_all(data, session)
    session.close()

if __name__ == '__main__': main()