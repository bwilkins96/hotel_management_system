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

    printer = Printer(100)

    # Check availability / room rate
    print(room_1.available_on(future_date(2)))   # -> True
    print(room_1.get_rate())                     # -> 100

    # Create guest and book stay
    guest_a = PersonFactory.create('guest', 'Mike', 'guest_a@email.com')
    stay_a = Stay(room_1, datetime.now(), future_date(5))
    guest_a.book_stay(stay_a)
    print(f'\n{guest_a.get_stay()}\n')  

    # Check pay and pay bill
    ga_account = guest_a.get_account()
    print(ga_account)           
    ga_account.pay(ga_account.get_total_due())
    print(f'{ga_account}\n')    

    # Check-in, check-out, get/replace room key
    stay_a.check_in()
    print(guest_a.is_checked_in())       # -> True
    stay_a.get_keycard(printer)          # Should print mock message
    stay_a.get_keycard(printer)          # Should print mock message

    print()
    stay_a.get_keycard(printer)          # Should NOT print mock message
    stay_a.replace_keycard(printer)      # Should print mock message
    stay_a.check_out()
    print(f'{guest_a.is_checked_in()}\n')  # -> False

    # Cancel stay
    guest_b = PersonFactory.create('guest', 'Marcy', 'guest_b@email.com')
    guest_b.book_stay(Stay(room_2, future_date(2), future_date(7)))

    gb_account = guest_b.get_account()
    print(gb_account)
    guest_b.cancel_stay()
    
    print(guest_b.get_stay())    # -> None
    print(gb_account)            # -> Equal balance and credits
    gb_account.apply_credits()
    print(gb_account)            # -> Zero balance and credits

    # Alter stay

    #session.close()

if __name__ == '__main__': main()