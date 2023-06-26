# SWDV 630 - Object-Oriented Software Architecture

from datetime import datetime, timedelta
from base import Base

from factory import PersonFactory
from prototype import PrototypeFactory
from room import Room
from stay import Stay
from schedule import Shift, Schedule
from printer import Printer

from utils import get_session, future_date

def main():
    #session = get_session()

    room_1 = Room(1, 'queen', 100)
    room_2 = Room(2, 'king', 125)
    room_3 = Room(3, '2 queens', 150)

    manager = PersonFactory.create('manager', 30, 'Jenny', 'manager@email.com')
    emp_a = PersonFactory.create('employee', 20, 'Julian', 'emp_a@email.com')
    emp_b = PersonFactory.create('employee', 20, 'Jennifer', 'emp_b@email.com')
    manager.add_employee(emp_a)
    manager.add_employee(emp_b)

    guest_a = PersonFactory.create('guest', 'Mike', 'guest_a@email.com')
    guest_b = PersonFactory.create('guest', 'Marcy', 'guest_b@email.com')
    ga_account = guest_a.get_account()
    gb_account = guest_b.get_account()

    printer = Printer(100)

    # Check availability / room rate
    print(room_1.available_on(future_date(2)))   # -> True
    print(room_1.get_rate())                     # -> 100

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

    print(gb_account)
    guest_b.cancel_stay()
    print(guest_b.get_stay())    # -> None
    print(f'{gb_account}\n')     # -> Zero balance and credits

    # Alter stay
    stay_c = Stay(room_3, future_date(10), future_date(14))
    guest_b.book_stay(stay_c)
    print(stay_c)
    guest_b.alter_stay(end=future_date(12))
    print(stay_c)
    print(f'{gb_account}\n')     # -> Balance due of $200

    

    #session.close()

if __name__ == '__main__': main()