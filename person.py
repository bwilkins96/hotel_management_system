# SWDV 630 - Object-Oriented Software Architecture
# Person superclass and 3 subclasses for a hotel management system

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from stay import Stay
from account import Account
from schedule import Schedule

class Person(Base):
    """Person base class for a hotel management system"""
    
    def __init__(self, name, email, joined=datetime.now()):
        """
        Sets up a Person instance with name, start date, and end date parameters.
        Parameters start and end should be date objects.
        """
        self._name = name.title() 
        self._email = email
        self._joined = joined

    __tablename__ = 'person'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _name: Mapped[str]
    _email: Mapped[str] = mapped_column(unique=True)
    _joined: Mapped[datetime]
    _type: Mapped[str]

    # Used to set up a table that keeps track of all instances of the base and subclasses 
    __mapper_args__ = {
        "polymorphic_on": "_type",
        "polymorphic_identity": "person",
    }

    def get_name(self):
        return self._name
    
    def get_email(self):
        return self._email
    
    def get_joined(self):
        return self._joined

    def set_name(self, name):
        self._name = name.title() 

    def set_email(self, email):
        self._email = email

    def days_since_join(self):
        joined = self.get_joined()
        diff = datetime.now() - joined
        return joined.days

    def __repr__(self):
        return f'<Person: {self.get_name()}, {self._type.title()}>'

class Guest(Person):
    """Guest subclass for a hotel management system"""

    def __init__(self, account, *args, **kwargs):
        """Sets up a Guest instance with a stay parameter"""
        self._stay = None
        self._account = account
        super().__init__(*args, **kwargs)

    _stay_id: Mapped[int] = mapped_column(ForeignKey('stay._id'), nullable=True)
    _account_id: Mapped[int] = mapped_column(ForeignKey('account._id'), nullable=True)
    _stay: Mapped[Stay] = relationship()
    _account: Mapped[Account] = relationship(cascade='all, delete')

    __mapper_args__ = {
        "polymorphic_identity": "guest",
    }

    def get_stay(self):
        return self._stay
    
    def get_account(self):
        return self._account
    
    def book_stay(self, stay):
        self._stay = stay
        account = self.get_account()
        account.charge(stay.get_total_charge())

    def cancel_stay(self):
        stay = self.get_stay()
        if stay:
            account = self.get_account()
            account.credit(stay.get_total_charge())
            account.apply_credits()
            
            stay.reset_room()
            self._stay = None

    def alter_stay(self, start=None, end=None):
        stay = self.get_stay()
        if stay:
            account = self.get_account()
            account.credit(stay.get_total_charge())

            if start: stay.set_start(start)
            if end: stay.set_end(end)

            account.charge(stay.get_total_charge())
            account.apply_credits()

    def is_checked_in(self):
        stay = self.get_stay()
        if stay:
            return stay.is_checked_in()
       
        return False

class Employee(Person):
    """Employee subclass for a hotel management system"""

    def __init__(self, schedule, pay_rate,  *args, **kwargs):
        """Sets up an Employee instance with a pay_rate parameter"""
        self._pay_rate = float(pay_rate)
        self._unpaid_hours = 0.0
        self._unpaid_overtime = 0.0
        self._schedule = schedule

        super().__init__(*args, **kwargs)

    _pay_rate: Mapped[float] = mapped_column(nullable=True)
    _unpaid_hours: Mapped[float] = mapped_column(nullable=True)
    _unpaid_overtime: Mapped[float] = mapped_column(nullable=True)
    _manager_id: Mapped[int] = mapped_column(ForeignKey('person._id'), nullable=True)
    _schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule._id'), nullable=True)
    _schedule: Mapped[Schedule] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }

    def get_schedule(self):
        return self._schedule

    def get_pay_rate(self):
        return self._pay_rate
    
    def set_pay_rate(self, pay_rate):
        self._pay_rate = float(pay_rate)

    def add_hours(self, hours, overtime=0):
        """
        Adds hours to unpaid_hours and the optional overtime parameter to unpaid_overtime.
        The overtime parameter defaults to 0.
        """
        self._unpaid_hours += hours
        self._unpaid_overtime += overtime

    def reset_hours(self):
        """Sets unpaid_hours and unpaid_overtime to 0"""
        self._unpaid_hours = 0.0
        self._unpaid_overtime = 0.0

    def get_total_pay(self):
        """Returns the total pay owed to the Employee instance"""
        rate = self.get_pay_rate()
        total = (self._unpaid_hours * rate) + (self._unpaid_overtime * rate * 1.5)
        return total
    
    def is_clocked_in(self):
        return self.get_schedule().is_clocked_in()
    
    def apply_schedule_hours(self):
        schedule = self.get_schedule()
        hours = schedule.hours_worked()
        overtime = 0

        if hours > 40:
            overtime = hours - 40
            hours = 40.0

        self.add_hours(hours, overtime)
        schedule.reset()
    
class Manager(Employee):
    """Manager subclass for a hotel management system"""

    def __init__(self, *args, **kwargs):
        """Sets up a Manager instance with an office parameter"""
        self._employees = []
        super().__init__(*args, **kwargs)

    _employees: Mapped[list[Employee]] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    def get_employees(self):
        return self._employees[:]
    
    def add_employee(self, emp):
        """Adds Employee emp to employees list"""
        if type(emp) == Employee:
            self._employees.append(emp)

    def remove_employee(self, emp):
        """Removes Employee emp from employees list"""
        emp_idx = self._employees.index(emp)
        return self._employees.pop(emp_idx)

# Test functions
def test_guest():
    from stay import Stay
    from room import Room

    room = Room(101, 'queen', 150)
    stay = Stay(room, datetime.now(), datetime.now())
    guest = Guest(Account(), 'Joe', 'test@email.com', datetime(2023, 5, 20))
    guest.book_stay(stay)
    print(guest.is_checked_in(), guest.get_joined())     # False, 2023-05-20

    guest.get_stay().check_in()
    print(guest.is_checked_in())        # True

    guest.get_stay().check_out()
    print(guest.is_checked_in())        # False

def test_employee():
    emp = Employee(Schedule(), 20, 'Jeff', 'test2@email.com')
    emp.add_hours(40)
    print(emp.get_total_pay())          # 800.0

    emp.add_hours(40, 5)
    print(emp.get_total_pay())          # 1750.0

    emp.reset_hours()
    print(emp.get_total_pay())          # 0.0

def test_manager():
    man = Manager(Schedule(), 30, 'Jenny', 'test3@email.com')
    print(man.get_employees())          # []

    emp_a = Employee(Schedule(), 20, 'Julian', 'test4@email.com')
    emp_b = Employee(Schedule(), 20, 'Jennifer', 'test5@email.com')
    man.add_employee(emp_a)
    man.add_employee(emp_b)
    print(man.get_employees())          # [(Person: Julian), (Person: Jennifer)]

    man.remove_employee(emp_a)
    print(man.get_employees())          # [(Person: Jennifer)]

def test():
    test_guest()
    print()
    test_employee()
    print()
    test_manager()

if __name__ == '__main__': test()